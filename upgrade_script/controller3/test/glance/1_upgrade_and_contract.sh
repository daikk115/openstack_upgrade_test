#!/bin/bash

dir_path=$(dirname $0)
bash $dir_path/../haproxy/disable_server.sh glance-api controller3
bash $dir_path/../haproxy/disable_server.sh glance-registry controller3

sleep 5

service glance-api stop
service glance-registry stop
apt-get -o Dpkg::Options::="--force-confold" -y  install --only-upgrade glance
service glance-api start
service glance-registry start
sleep 3

bash $dir_path/../haproxy/enable_server.sh glance-api controller3
bash $dir_path/../haproxy/enable_server.sh glance-registry controller3

glance-manage db contract
		
