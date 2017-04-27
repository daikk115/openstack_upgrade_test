echo "Start to upgrade Nova"
sleep 2
echo "Upgrade Nova database"
sleep 2
ssh mariadb << EOF
mysql -uroot -pnam123 -e "CREATE DATABASE nova_cell0;"
mysql -uroot -pnam123 -e "GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'nam123';"
mysql -uroot -pnam123 -e "GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'nam123';"
EOF
sshpass -p nam123 ssh daidv@10.164.178.148 "nova-manage db sync"
sshpass -p nam123 ssh daidv@10.164.178.148 "nova-manage api_db sync"

ssh controller1 "bash /root/test/nova/1_nova_api_stop" &
ssh controller2 "bash /root/test/nova/1_nova_api_stop" &
ssh controller3 "bash /root/test/nova/1_nova_api_stop" &
wait
ssh controller1 "bash /root/test/nova/2_nova_service_stop" & 
ssh controller2 "bash /root/test/nova/2_nova_service_stop" &
ssh controller3 "bash /root/test/nova/2_nova_service_stop" &
wait
ssh controller1 "bash /root/test/nova/3_nova_upgrade_code" &
ssh controller2 "bash /root/test/nova/3_nova_upgrade_code" &
ssh controller3 "bash /root/test/nova/3_nova_upgrade_code" &
wait
ssh controller1 "bash /root/test/nova/5_nova_conductor_start" &
ssh controller2 "bash /root/test/nova/5_nova_conductor_start" &
ssh controller3 "bash /root/test/nova/5_nova_conductor_start" &
wait
ssh controller1 "bash /root/test/nova/6_nova_services_start" &
ssh controller2 "bash /root/test/nova/6_nova_services_start" &
ssh controller3 "bash /root/test/nova/6_nova_services_start" &
wait
ssh controller1 "bash /root/test/nova/7_nova_api_start" &
ssh controller2 "bash /root/test/nova/7_nova_api_start" &
ssh controller3 "bash /root/test/nova/7_nova_api_start" &
wait
sleep 3 
#echo "Starting upgrade on Compute node" &
#ssh compute1 "bash /root/test/nova/nova_compute_restart" &
#ssh compute2 "bash /root/test/nova/nova_compute_restart" &
#ssh compute3 "bash /root/test/nova/nova_compute_restart" &
#wait
#ssh controller1 "bash /root/test/nova/1_nova_api_stop" &
#ssh controller2 "bash /root/test/nova/1_nova_api_stop" &
#ssh controller3 "bash /root/test/nova/1_nova_api_stop" &
#wait
#ssh controller1 "bash /root/test/nova/2_nova_service_stop" &
#ssh controller2 "bash /root/test/nova/2_nova_service_stop" &
#ssh controller3 "bash /root/test/nova/2_nova_service_stop" &
#wait
#
#ssh controller1 "bash /root/test/nova/5_nova_conductor_start" &
#ssh controller2 "bash /root/test/nova/5_nova_conductor_start" &
#ssh controller3 "bash /root/test/nova/5_nova_conductor_start" &
#wait
#ssh controller1 "bash /root/test/nova/6_nova_services_start" &
#ssh controller2 "bash /root/test/nova/6_nova_services_start" &
#ssh controller3 "bash /root/test/nova/6_nova_services_start" &
#wait
#ssh controller1 "bash /root/test/nova/7_nova_api_start" &
#ssh controller2 "bash /root/test/nova/7_nova_api_start" &
#ssh controller3 "bash /root/test/nova/7_nova_api_start" &
