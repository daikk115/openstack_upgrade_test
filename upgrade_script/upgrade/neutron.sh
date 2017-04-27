echo "Starting upgrade Neutron"
sleep 3

ssh controller1 "bash /root/test/neutron/1_neutron_server_restart"
sleep 2
ssh controller2 "bash /root/test/neutron/1_neutron_server_restart"
sleep 2
ssh controller3 "bash /root/test/neutron/1_neutron_server_restart"
sleep 3

echo "Restart on compute1, compute2 and compute3"
ssh compute1 "bash /root/test/neutron/5_neutron_l2_upgrade"
ssh compute2 "bash /root/test/neutron/5_neutron_l2_upgrade"
ssh compute3 "bash /root/test/neutron/5_neutron_l2_upgrade"
sleep 3

echo "Restart network1"
ssh network1 "bash /root/test/neutron/5_neutron_l2_upgrade"
ssh network1 "bash /root/test/neutron/6_neutron_l3_upgrade"
ssh network1 "bash /root/test/neutron/7_neutron_dhcp_restart"
ssh network1 "bash /root/test/neutron/8_neutron_metadata_restart"
sleep 3

echo "Restart network2"
ssh network2 "bash /root/test/neutron/5_neutron_l2_upgrade"
ssh network2 "bash /root/test/neutron/6_neutron_l3_upgrade"
ssh network2 "bash /root/test/neutron/7_neutron_dhcp_restart"
ssh network2 "bash /root/test/neutron/8_neutron_metadata_restart"

