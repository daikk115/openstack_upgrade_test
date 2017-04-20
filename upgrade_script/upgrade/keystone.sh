# Start upgrade kestone
echo "Start to upgrade Keystone"
ssh controller1 << EOF
	bash /root/test/keystone/1_upgrade_source.sh
	bash /root/test/keystone/2_upgrade_database.sh
EOF
ssh controller2 << EOF
	bash /root/test/keystone/1_upgrade.sh
EOF
ssh controller3 << EOF
	bash /root/test/keystone/1_upgrade.sh
EOF
