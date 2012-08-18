log_level        :info
log_location     STDOUT

chef_server_url  "http://chef.labs.cityindex.com"
validation_client_name "chef-validator" 
client_key        "/etc/chef/client.pem"
validation_key    "/etc/chef/validation.pem"

file_cache_path   "/etc/chef/cache"
file_backup_path  "/etc/chef/backup"
cache_options     ({:path => "/etc/chef/cache/checksums", :skip_expires => true})
