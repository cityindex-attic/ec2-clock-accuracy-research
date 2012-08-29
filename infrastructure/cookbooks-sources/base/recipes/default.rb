#
# Cookbook Name:: base
# Recipe:: default
#
# Copyright 2012, City Index Ltd
#
# Apache v2
#


node['users'] = ['mrdavidlaing', 'sopel']

recipe "user::data_bag"