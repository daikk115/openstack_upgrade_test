#!/bin/bash

service glance-api stop
service glance-registry stop
apt-get -y install --only-upgrade glance
service glance-api start
service glance-registry start
		
