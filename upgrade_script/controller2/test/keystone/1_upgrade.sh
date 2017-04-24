#!/bin/bash

dir_path=$(dirname $0)
bash $dir_path/../haproxy/disable_server.sh keystone_admin controller2
bash $dir_path/../haproxy/disable_server.sh keystone_api controller2

service apache2 stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade keystone
service apache2 start

bash $dir_path/../haproxy/enable_server.sh keystone_admin controller2
bash $dir_path/../haproxy/enable_server.sh keystone_api controller2
sleep 5