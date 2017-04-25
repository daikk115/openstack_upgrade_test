#!/bin/bash

service glance-api stop
service glance-registry stop
apt-get -o Dpkg::Options::="--force-confold" -y install --only-upgrade glance
service glance-api start
service glance-registry start
		
