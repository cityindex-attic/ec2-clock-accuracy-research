#
# Cookbook Name:: base
# Recipe:: default
#
# Copyright 2012, City Index Ltd
#
# Apache v2
#


node['users'] = ['mrdavidlaing', 'sopel']

include_recipe "user::data_bag"

sudo "group_admin_NOPASSWD" do
  group "admin"
  commands ["ALL"] # array of commands, will be .join(",")
  host "ALL"
  nopasswd true # true prepends the runas_spec with NOPASSWD
  not_if { node['platform'].include? "windows" }
end