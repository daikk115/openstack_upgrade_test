# Start upgrade kestone
echo "Start to upgrade Glance on controller1"
sleep 2
ssh controller1 "bash /root/test/glance/1_upgrade_source_and_database.sh"
ssh controller1 "bash /root/test/glance/2_migrate_data.sh"
ssh controller1 "bash /root/test/glance/3_start_services.sh"
echo "Start to upgrade Glance on controller2"
sleep 2
ssh controller2 "bash /root/test/glance/1_upgrade.sh"
echo "Start to upgrade Glance on controller3"
sleep 2
ssh controller3 "bash /root/test/glance/1_upgrade_and_contract.sh"