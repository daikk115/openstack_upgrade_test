#!/bin/bash

dir_path=$(dirname $0)
bash $dir_path/../haproxy/disable_server.sh keystone_admin controller1
bash $dir_path/../haproxy/disable_server.sh keystone_api controller1

sleep 10

service apache2 stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade keystone
keystone-manage doctor
