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