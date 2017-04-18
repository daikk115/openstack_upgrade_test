#!/bin/bash
for id in {1..100}
do
	openstack image create "testing" --file ../python_script/cirros-0.3.5-x86_64-disk.img --disk-format qcow2 --container-format bare --public
done
