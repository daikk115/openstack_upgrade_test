echo "Start to upgrade Cinder"
sleep 3
ssh controller1 "bash /root/test/cinder/1_cinder_api_upgrade"
ssh controller2 "bash /root/test/cinder/1_cinder_api_upgrade"
ssh controller3 "bash /root/test/cinder/1_cinder_api_upgrade"

ssh controller1 "bash /root/test/cinder/2_cinder_scheduler_upgrade"
ssh controller2 "bash /root/test/cinder/2_cinder_scheduler_upgrade"
ssh controller3 "bash /root/test/cinder/2_cinder_scheduler_upgrade"

ssh controller1 << EOF
	bash /root/test/cinder/3_cinder_move_cinder_volume_to_controller3
	sleep 2
	bash /root/test/cinder/4_cinder_volume_upgrade
EOF

ssh controller2 "bash /root/test/cinder/4_cinder_volume_upgrade"
ssh controller3 << EOF
	bash /root/test/cinder/5_cinder_move_cinder_volume_to_controller1
	bash /root/test/cinder/4_cinder_volume_upgrade
EOF
	
echo "Restart"

ssh controller1 "service cinder-api restart"
ssh controller2 "service cinder-api restart"
ssh controller3 "service cinder-api restart"

ssh controller1 "service cinder-scheduler restart"
ssh controller2 "service cinder-scheduler restart"
ssh controller3 "service cinder-scheduler restart"
