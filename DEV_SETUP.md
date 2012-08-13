### Dev machine setup

Ubuntu 12.04:

1.  Clone this repo
1.  Ensure Ruby 1.9.3+ is installed, eg:  ```sudo apt-get install ruby1.9.3```
1.  Might also need to uninstall ruby 1.8?
1.  ```sudo gem install chef rake knife-ec2 knife-windows librarian --no-ri --no-rdoc```
1.  Run ```librarian-chef install``` 
	eg: ``` ~/Projects/ec2-clock-accuracy-research/infrastructure$ librarian-chef install```
    This will create a cookbooks & tmp folder, and download all the cookbooks referenced in the Cheffile
1.  Rename infrastructure/.chef/knife.rb.sample to infrastructure/.chef/knife.rb & update with your chef-server credentials (you might need to copy some pem files into this foler, or reference existing pem files already in your account)
1.  Test knife is working by running  ```knife cookbook metadata --all``` 
    eg: ```~/Projects/ec2-clock-accuracy-research/infrastructure$ knife cookbook metadata --all```
1.  Run the integration tests (causes test EC2 instances to be fired up) 
    ```mrdavidlaing@commander:~/Projects/ec2-clock-accuracy-research/infrastructure$ rake integration_test```

    
#### Note on Windows nodes

1.  WinRM must be enabled for knife-windows commands to work. Add the following to the EC2 instance userdata when launching (must use Amazon Windows AMI > April 2012)

            <script>
			net user bootstrapper BootMeBaby123 /add
			net localgroup administrators bootstrapper /add
			winrm quickconfig -q
			winrm set winrm/config/winrs @{MaxMemoryPerShellMB="300"}
			winrm set winrm/config @{MaxTimeoutms="1800000"}
			winrm set winrm/config/service @{AllowUnencrypted="true"}
			winrm set winrm/config/service/auth @{Basic="true"}
			</script>


1.  Then chef can be bootstrapped using:

       knife bootstrap windows winrm {ec2-46-51-149-124.eu-west-1.compute.amazonaws.com} -x bootstrapper -P 'BootMeBaby123'