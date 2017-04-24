#!/bin/bash
dir_path=$(dirname $0)

service glance-api start
service glance-registry start
sleep 5

dir_path=$(dirname $0)
bash $dir_path/../haproxy/enable_server.sh glance_api controller1
bash $dir_path/../haproxy/enable_server.sh glance_res controller1
sleep 10
