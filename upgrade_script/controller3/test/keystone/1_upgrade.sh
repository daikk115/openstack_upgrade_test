#!/bin/bash

dir_path=$(dirname $0)
bash $dir_path/../haproxy/disable_server.sh keystone_admin node1
bash $dir_path/../haproxy/disable_server.sh keystone_api node1

service apache2 stop
apt-get -y -o Dpkg::Options::="--force-confold" install --only-upgrade keystone
service apache2 start
keystone-manage db_sync --contract

bash $dir_path/../haproxy/enable_server.sh keystone_admin node1
bash $dir_path/../haproxy/enable_server.sh keystone_api node1
