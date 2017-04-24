#!/bin/bash

dir_path=$(dirname $0)

keystone-manage db_sync --expand
keystone-manage db_sync --migrate
service apache2 start

dir_path=$(dirname $0)
bash $dir_path/../haproxy/enable_server.sh keystone_admin controller1
bash $dir_path/../haproxy/enable_server.sh keystone_api controller1
sleep 10
