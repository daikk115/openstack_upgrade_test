#!/bin/bash

service apache2 stop
apt-get install --only-upgrade keystone
service apache2 start
keystone-manage db_sync --contract
