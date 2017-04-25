#!/bin/bash

service glance-api stop
service glance-registry stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade glance
glance-manage db expand
