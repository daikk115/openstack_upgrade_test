#!/bin/bash

dir_path=$(dirname $0)
bash $dir_path/../haproxy/disable_server.sh glance-api controller2
bash $dir_path/../haproxy/disable_server.sh glance-registry controller2
sleep 10

service glance-api stop
service glance-registry stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade glance
service glance-api start
service glance-registry start
sleep 5

bash $dir_path/../haproxy/enable_server.sh glance-api controller2
bash $dir_path/../haproxy/enable_server.sh glance-registry controller2
sleep 10