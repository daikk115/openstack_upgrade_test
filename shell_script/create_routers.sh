#!/bin/bash
for id in {1..2000}
do
	openstack router create --project $1 $2_$id
done

# To use: $ . this_script.sh <project> <prefix>
# For instance: . this_script.sh admin testing to create list of routers with "testing" prefix
