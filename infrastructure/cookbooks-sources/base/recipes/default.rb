#
# Cookbook Name:: base
# Recipe:: default
#
# Copyright 2012, City Index Ltd
#
# Apache v2
#



def setup_ssh_keys(u)
	# Set home to location in data bag,
    # or a reasonable default (/home/$user).
    if u['home']
      home_dir = u['home']
    else
      home_dir = "/home/#{u['id']}"
    end

	if home_dir != "/dev/null"
      directory "#{home_dir}/.ssh" do
        owner u['id']
        group u['gid'] || u['id']
        mode "0700"
      end

      if u['ssh_keys']
        template "#{home_dir}/.ssh/authorized_keys" do
          source "authorized_keys.erb"
          owner u['id']
          group u['gid'] || u['id']
          mode "0600"
          variables :ssh_keys => u['ssh_keys']
        end
      end
    end
end

###############################

group_bag = node['group']['data_bag_name']
user_bag = node['user']['data_bag_name']
super_admins = data_bag_item(group_bag, node['group']['super_admins_group_name'])['users']

super_admins.each do |super_admin_name|
	u = data_bag_item(user_bag, super_admin_name)
	username = u['username'] || u['id']

	user username do
		comment 	u['comment'] 	if u['comment']
		password 	u['password'] 	if (u['action'] and 	platform? 'windows')
		uid 		u['uid'] 		if (u['uid'] 	and not platform? 'windows')
		gid 		u['gid'] 		if (u['gid'] 	and not platform? 'windows')
		home 		u['home'] 		if (u['home'] 	and not platform? 'windows')
		home 		u['shell'] 		if (u['shell'] 	and not platform? 'windows')
		
		action u['action'].to_sym if u['action']
	end

	setup_ssh_keys(u) unless platform? 'windows'

	# Make user local administrator
	local_admin_group = "admin"
	local_admin_group = "Administrators" if platform? 'windows'

	group local_admin_group do
		action :modify
	    members username
	    append true
	end
end

sudo "group_admin_NOPASSWD" do
  group "admin"
  commands ["ALL"] # array of commands, will be .join(",")
  host "ALL"
  nopasswd true # true prepends the runas_spec with NOPASSWD
  not_if { node['platform'].include? "windows" }
end

