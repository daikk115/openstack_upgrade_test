#!/bin/bash
for id in {1..100}
do
	openstack user create --project $1 $2_$id
done

# To use: $ . this_script.sh <project> <prefix>
# For instance: . this_script.sh admin testing to create list of users with "testing" prefix
