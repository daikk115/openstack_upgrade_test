# Start upgrade kestone
echo "Start to upgrade Glance"
ssh controller1 << EOF
	bash /root/test/glance/1_upgrade_source_and_database.sh
	bash /root/test/glance/2_migrate_data.sh
	bash /root/test/glance/3_start_services.sh
EOF
ssh controller2 << EOF
	bash /root/test/glance/1_upgrade.sh
EOF
ssh controller3 << EOF
	bash /root/test/glance/1_upgrade_and_contract.sh
EOF
