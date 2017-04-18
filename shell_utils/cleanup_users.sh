#!/bin/bash
for id in $(openstack user list | grep $1 | awk {'print $2'})
do
	openstack user delete $id
done

# To use: $ . this_script.sh mark_word
# For instance: . this_script.sh create to delete all user contain "create" in name
