echo "Start to upgrade Cinder"
sleep 3
echo "Upgrade cinder database"
sleep 3
sshpass -p 1 ssh daidv@10.164.178.148 "cinder-manage db sync"
sleep 3
ssh controller1 "bash /root/test/cinder/1_cinder_api_upgrade"
ssh controller2 "bash /root/test/cinder/1_cinder_api_upgrade"
ssh controller3 "bash /root/test/cinder/1_cinder_api_upgrade"

ssh controller1 "bash /root/test/cinder/2_cinder_scheduler_upgrade"
ssh controller2 "bash /root/test/cinder/2_cinder_scheduler_upgrade"
ssh controller3 "bash /root/test/cinder/2_cinder_scheduler_upgrade"

ssh controller2 "bash /root/test/cinder/4_cinder_volume_upgrade"
ssh controller3 "bash /root/test/cinder/4_cinder_volume_upgrade"

ssh controller1 "service cinder-volume stop"
ssh controller3 "service cinder-volume start"

ssh controller1 "bash /root/test/cinder/4_cinder_volume_upgrade"