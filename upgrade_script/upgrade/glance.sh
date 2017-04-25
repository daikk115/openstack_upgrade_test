# Start upgrade kestone
echo "Start to upgrade Glance on controller1"
ssh controller1 << EOF
	bash /root/test/glance/1_upgrade_source_and_database.sh
	bash /root/test/glance/2_migrate_data.sh
	bash /root/test/glance/3_start_services.sh
EOF
echo "Start to upgrade Glance on controller2"
ssh controller2 << EOF
	bash /root/test/glance/1_upgrade.sh
EOF
echo "Start to upgrade Glance on controller3"
ssh controller3 << EOF
	bash /root/test/glance/1_upgrade_and_contract.sh
EOF
