#!/bin/bash

haproxy_node = crm_mon -1 | grep haproxy | awk '{print $4}'
echo "enable server $1/$2" | socat stdio /etc/haproxy/haproxy.sock
