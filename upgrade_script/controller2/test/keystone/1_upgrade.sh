#!/bin/bash

service apache2 stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade keystone
service apache2 start
