### Dev machine setup

Ubuntu 12.04:

1.  Clone this repo
1.  ```sudo gem install chef```
1.  ```sudo gem install librarian```
1.  Run ```librarian-chef install``` 
	eg: ``` ~/Projects/ec2-clock-accuracy-research/infrastructure$ librarian-chef install```
    This will create a cookbooks & tmp folder, and download all the cookbooks referenced in the Cheffile
1.  Rename infrastructure/.chef/knife.rb.sample to infrastructure/.chef/knife.rb & update with your chef-server credentials (you might need to copy some pem files into this foler, or reference existing pem files already in your account)
1.  Test knife is working by running  ```knife cookbook metadata --all``` 
    eg: ```~/Projects/ec2-clock-accuracy-research/infrastructure$ knife cookbook metadata --all```


    