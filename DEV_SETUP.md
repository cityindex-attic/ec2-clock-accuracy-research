### Dev machine setup

Ubuntu 12.04:

1.  Clone this repo
1.  ```sudo gem install chef rake knife-ec2 librarian --no-ri --no-rdoc```
1.  Run ```librarian-chef install``` 
	eg: ``` ~/Projects/ec2-clock-accuracy-research/infrastructure$ librarian-chef install```
    This will create a cookbooks & tmp folder, and download all the cookbooks referenced in the Cheffile
1.  Rename infrastructure/.chef/knife.rb.sample to infrastructure/.chef/knife.rb & update with your chef-server credentials (you might need to copy some pem files into this foler, or reference existing pem files already in your account)
1.  Test knife is working by running  ```knife cookbook metadata --all``` 
    eg: ```~/Projects/ec2-clock-accuracy-research/infrastructure$ knife cookbook metadata --all```
1.  Run the integration tests (causes test EC2 instances to be fired up) 
    ```mrdavidlaing@commander:~/Projects/ec2-clock-accuracy-research/infrastructure$ rake integration_test```

    
#### Note on Windows nodes

1.  WinRM must be enabled for knife-windows commands to work.  From an Admin command prompt

           winrm quickconfig -q
           winrm set winrm/config/winrs @{MaxMemoryPerShellMB="300"}
           winrm set winrm/config @{MaxTimeoutms="1800000"}
           winrm set winrm/config/service @{AllowUnencrypted="true"}
           winrm set winrm/config/service/auth @{Basic="true"}

 1.  TODO - how can we secure winrm traffic?