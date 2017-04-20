echo "Starting upgrade Neutron"
sleep 3

ssh controller1 "bash /root/test/neutron/1_neutron_server_stop" &
ssh controller2 "bash /root/test/neutron/1_neutron_server_stop" &
ssh controller3 "bash /root/test/neutron/1_neutron_server_stop" &
wait
ssh controller1 "bash /root/test/neutron/2_neutron_server_upgrade_code && bash /root/test/neutron/3_neutron_upgrade_db" &
wait

ssh controller2 "bash /root/test/neutron/2_neutron_server_upgrade_code" &
ssh controller3 "bash /root/test/neutron/2_neutron_server_upgrade_code" &
wait
ssh controller1 "bash /root/test/neutron/4_neutron_server_start" &
ssh controller2 "bash /root/test/neutron/4_neutron_server_start" &
ssh controller3 "bash /root/test/neutron/4_neutron_server_start" &
wait
ssh network1 "bash /root/test/neutron/5_neutron_l2_upgrade" &
ssh network2 "bash /root/test/neutron/5_neutron_l2_upgrade" &
ssh compute1 "bash /root/test/neutron/5_neutron_l2_upgrade" &
ssh compute2 "bash /root/test/neutron/5_neutron_l2_upgrade" &
ssh compute3 "bash /root/test/neutron/5_neutron_l2_upgrade" &
wait
ssh network1 "bash /root/test/neutron/6_neutron_l3_upgrade" &
ssh network2 "bash /root/test/neutron/6_neutron_l3_upgrade" &
wait
ssh network1 "bash /root/test/neutron/7_neutron_dhcp_restart" &
ssh network2 "bash /root/test/neutron/7_neutron_dhcp_restart" &
wait
ssh network1 "bash /root/test/neutron/8_neutron_metadata_restart" &
ssh network2 "bash /root/test/neutron/8_neutron_metadata_restart" &
