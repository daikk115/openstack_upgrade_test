#!/bin/bash

dir_path=$(dirname $0)
bash $dir_path/../haproxy/disable_server.sh glance-api controller1
bash $dir_path/../haproxy/disable_server.sh glance-registry controller1

sleep 10

service glance-api stop
service glance-registry stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade glance
glance-manage db expand
