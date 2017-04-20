#!/bin/bash

service apache2 stop
apt-get -y install --only-upgrade keystone
keystone-manage doctor
