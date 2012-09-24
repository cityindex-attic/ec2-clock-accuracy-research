from datetime import datetime
import logging
from operator import attrgetter
ec2_log = logging.getLogger('boto_cli.ec2')

DEFAULT_BACKUP_SET = "default"
CREATED_BY_BOTO_EBS_SNAPSHOT_SCRIPT_SIGNATURE = "Created by Boto EBS Snapshot Script from ";
CREATED_BY_BOTO_EC2_IMAGE_SCRIPT_SIGNATURE = "Created by Boto EC2 Image Script from ";
TAG_NAME = "Name"
TAG_BACKUP_POLICY = "Backup Policy"

def derive_name(ec2, resource_id, iso_datetime=None, id_only=False):
    if not iso_datetime:
        iso_datetime = datetime.utcnow()

    name = resource_id;
    if not id_only:
        filters = { "resource-id": resource_id}
        tags = ec2.get_all_tags(filters=filters)
        for tag in tags:
            if tag.name == TAG_NAME and tag.value:
                name = tag.value

    name += "." + iso_datetime.strftime("%Y%m%dT%H%M%SZ");
    return name;

def create_snapshots(ec2, volumes, backup_set, description):
    log = ec2_log
    for volume in volumes:
        signature = description if description else CREATED_BY_BOTO_EBS_SNAPSHOT_SCRIPT_SIGNATURE + volume.id
        log.debug("Description: " + signature)
        response = ec2.create_snapshot(volume.id, description=signature)

        name = derive_name(ec2, volume.id)
        log.debug(TAG_NAME + ": " + name)
        tags = {TAG_NAME: name, TAG_BACKUP_POLICY: backup_set}
        ec2.create_tags([response.id], tags)

def delete_snapshots(ec2, volumes, backup_set, backup_retention, no_origin_safeguard=False):
    log = ec2_log
    for volume in volumes:
        snapshot_filters = {"volume-id": volume.id, "tag:" + TAG_BACKUP_POLICY: backup_set}
        if not no_origin_safeguard:
            snapshot_filters['description'] = CREATED_BY_BOTO_EBS_SNAPSHOT_SCRIPT_SIGNATURE + volume.id
        log.debug(snapshot_filters)
        snapshots = ec2.get_all_snapshots(owner='self', filters=snapshot_filters)
        log.info("Deleting snapshots of " + volume.id + " (set '" + backup_set + "', " + str(len(snapshots)) + " available, retaining " + str(backup_retention) + "):")
        # While snapshots are apparently returned in oldest to youngest order, this isn't documented;
        # therefore an explicit sort is performed to ensure this regardless.
        num_snapshots = len(snapshots);
        for snapshot in sorted(snapshots, key=attrgetter('start_time')):
            log.debug(snapshot.start_time)
            if num_snapshots <= backup_retention:
                log.info("... retaining last " + str(backup_retention) + " snapshots.")
                break
            num_snapshots -= 1
            log.info("... deleting snapshot '" + snapshot.id + "' ...")
            response = ec2.delete_snapshot(snapshot.id)

def create_images(ec2, reservations, backup_set, description, no_reboot=False):
    log = ec2_log
    for reservation in reservations:
        for instance in reservation.instances:
            signature = description if description else CREATED_BY_BOTO_EC2_IMAGE_SCRIPT_SIGNATURE + instance.id
            log.debug("Description: " + signature)
            iso_datetime = datetime.utcnow()
            ami_name = derive_name(ec2, instance.id, iso_datetime, True)
            log.debug("AMI name: " + ami_name)
            image_id = ec2.create_image(instance.id, name=ami_name, description=signature, no_reboot=no_reboot)

            name = derive_name(ec2, instance.id, iso_datetime)
            log.debug(TAG_NAME + ": " + name)
            tags = {TAG_NAME: name, TAG_BACKUP_POLICY: backup_set}
            ec2.create_tags([image_id], tags)

def delete_images(ec2, reservations, backup_set, backup_retention, no_origin_safeguard=False):
    log = ec2_log
    for reservation in reservations:
        for instance in reservation.instances:
            image_filters = {"name": instance.id + "*", "tag:" + TAG_BACKUP_POLICY: backup_set}
            if not no_origin_safeguard:
                image_filters['description'] = CREATED_BY_BOTO_EC2_IMAGE_SCRIPT_SIGNATURE + instance.id
            log.debug(image_filters)
            images = ec2.get_all_images(owners=['self'], filters=image_filters)
            log.info("Deregistering images of " + instance.id + " (set '" + backup_set + "', " + str(len(images)) + " available, retaining " + str(backup_retention) + "):")
            # While images are apparently returned in oldest to youngest order, this isn't documented;
            # therefore an explicit sort is performed to ensure this regardless.
            num_images = len(images);
            for image in sorted(images, key=attrgetter('name')):
                log.debug(image.name)
                if num_images <= backup_retention:
                    log.info("... retaining last " + str(backup_retention) + " images.")
                    break
                num_images -= 1
                log.info("... deregistering image '" + image.id + "' ...")
                response = ec2.deregister_image(image.id, delete_snapshot=True)
