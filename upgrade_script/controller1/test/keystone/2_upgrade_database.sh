#!/bin/bash

keystone-manage db_sync --expand
keystone-manage db_sync --migrate
service apache2 start

sleep 5

dir_path=$(dirname $0)
bash $dir_path/../haproxy/enable_server.sh keystone_admin controller1
bash $dir_path/../haproxy/enable_server.sh keystone_api controller1

sleep 20
