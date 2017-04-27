#!/bin/bash

haproxy_node=$(crm_mon -1 | grep "lsb:haproxy" | awk '{print $4}')
ssh $haproxy_node "echo 'disable server $1/$2' | socat stdio /var/lib/haproxy/stats"
sleep 5
