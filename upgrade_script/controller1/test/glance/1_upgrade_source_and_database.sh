#!/bin/bash

service glance-api stop
service glance-registry stop
apt-get -y install --only-upgrade glance
glance-manage db expand
