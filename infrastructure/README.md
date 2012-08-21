# Infrastructure setup instructions

The clock accuracy data for this experiment is collected by running a cluster of Amazon EC2 machines of differing sizes and OS.
The collection of Python, Ruby and Chef scripts contained in this folder automate the creation of this cluster and the data collection.

## Requirements

1. An Amazon AWS account with full permissions
1. An Opscode Chef server
1. About $500 for a 2 week data collection run.

## Workstation setup instructions

#### Ubuntu 12.04:

1.  Clone this repo
1.  Ensure Ruby 1.9.3+ is installed - ```ruby --version``` ([Instructions on how to switch from ruby 1.8 to 1.9.3p0?](http://lenni.info/blog/2012/05/installing-ruby-1-9-3-on-ubuntu-12-04-precise-pengolin/))
1.  Install Ruby gems: ```sudo gem install chef rake knife-ec2 knife-windows librarian nokogiri --no-ri --no-rdoc```
1.  Ensure Python 2.7.3 is installed ```sudo apt-get install python python-pip```
1.  Install Python packages ```sudo pip install boto argparse```
1.  Configure your AWS credentials:
    1. Add the following to your ```~/.bashrc```
       ```
       export AWS_ACCESS_KEY_ID="AKIAI....."
	   export AWS_SECRET_ACCESS_KEY="oF8S8UQ....."
	   ```
	1. Refresh your environment - ```source ~/.bashrc```
1.  Configure Chef knife
	1. Rename ```infrastructure/.chef/knife.rb.sample``` to ```infrastructure/.chef/knife.rb```
	1. Update with your chef-server credentials (you will need to reference some pem files already in your account)
1.  All commands can be kicked off using rake.  Test rake is working (and see the available commands) by running ```rake -T```
    from within the from inside this ```infrastructure``` folder 
1.  Init Chef repo - ```rake update_chef_repo```
    This will create a cookbooks & tmp folder, and download all the cookbooks referenced in the Cheffile
1.  Test knife is working by running  ```knife cookbook metadata --all``` 

1.  Run an integration test (causes test EC2 instances to be fired up, takes about 30 min, should terminate all instances created if finishes successfully) 
    ```rake integration_test_ubuntu```

#### Windows 2008:

1.  Clone this repo
1.  Ensure Ruby 1.9.3+ (including DevKit) is installed - ```ruby --version``` (Or install from http://rubyinstaller.org/downloads/ )
1.  Install Ruby gems: ```gem install ffi ruby-wmi win32-service chef rake knife-ec2 knife-windows librarian nokogiri --no-ri --no-rdoc```
1.  Ensure Python 2.7.3 is installed ( http://www.python.org/getit/releases/2.7.3/ )
1.	Put ```c:\Python27``` and ```c:\Python27\Scripts``` in the path.  Test by opening a command prompt and running ```python```
1.  Ensure Python PIP is installed ( http://pypi.python.org/pypi/setuptools#windows )
	1.  Download and install setuptools
	1.  Then run: ```easy_install.exe pip```
1.  Install Python packages ```pip install boto boto argparse```
1.  Configure your AWS credentials:
    1. Add the following to your environment
       ```
       export AWS_ACCESS_KEY_ID="AKIAI....."
	   export AWS_SECRET_ACCESS_KEY="oF8S8UQ....."
	   ```
	1. Close and reopen your command line terminal
1.  Configure Chef knife
	1. Rename ```infrastructure/.chef/knife.rb.sample``` to ```infrastructure/.chef/knife.rb```
	1. Update with your chef-server credentials (you will need to reference some pem files already in your account)
1.  All commands can be kicked off using rake.  Test rake is working (and see the available commands) by running ```rake -T```
    from within the from inside this ```infrastructure``` folder 
1.  Init Chef repo - ```rake update_chef_repo```
    This will create a cookbooks & tmp folder, and download all the cookbooks referenced in the Cheffile
1.  Test knife is working by running  ```knife cookbook metadata --all``` 

1.  Run an integration test (causes test EC2 instances to be fired up, takes about 30 min, should terminate all instances created if finishes successfully) 
    ```rake integration_test_ubuntu```
