#
# Cookbook Name:: base
# Recipe:: default
#
# Copyright 2012, City Index Ltd
#
# Apache v2
#

group_bag = node['group']['data_bag_name']
user_bag = node['user']['data_bag_name']
super_admins = data_bag_item(group_bag, node['group']['super_admins_group_name'])['users']

super_admins.each do |super_admin_name|
	u = data_bag_item(user_bag, super_admin_name.gsub(/[.]/, '-'))
	username = u['username'] || u['id']

	user_account username do
		%w{comment uid gid home shell password system_user manage_home create_group
		    ssh_keys ssh_keygen}.each do |attr|
		  send(attr, u[attr]) if u[attr]
		end
		action u['action'].to_sym if u['action']
	end

	if platform?(%w{debian ubuntu})
		group "admin" do
		    members username
		    append true
		end
	end

	if platform? 'windows'
		group "Administrators" do
		    members username
		    append true
		end
	end
end

sudo "group_admin_NOPASSWD" do
  group "admin"
  commands ["ALL"] # array of commands, will be .join(",")
  host "ALL"
  nopasswd true # true prepends the runas_spec with NOPASSWD
  not_if { node['platform'].include? "windows" }
end