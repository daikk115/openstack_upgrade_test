#!/bin/bash
for id in {2001..3700}
do
	sleep 5
	openstack volume create --size 1 $1_$id
done

# To use: $ . this_script.sh <prefix>
# For instance: . this_script.sh testing to create list of volumes with "testing" prefix
