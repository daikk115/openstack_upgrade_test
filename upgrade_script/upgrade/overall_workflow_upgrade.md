========== WORKFLOW UPGRADE KEYSTONE ==================

Step 1: 
+ Using drain mode in haproxy to detach keystone1 from cluster
+ Action on Controller1:
	- Stop keystone: 
	- Install new Keystone code: 
	- Run expand phase
	- Running migration phase
	- Start service service apache2 start
+ Joint keystone1 to cluster
	
Step 2: 
+ Using drain mode in haproxy to detach keystone2 from cluster
+ Action on Controller2:
	- Stop keystone: service apache2 stop
	- Install new Keystone code:
	- Start service
+ Joint keystone2 to cluster

Step 3: 
+ Using drain mode in haproxy to detach keystone3 from cluster
+ Action on Controller3:
	- Stop keystone: 
	- Install new Keystone code:
	- Start service
	- After all keystone nodes at new release (Ocata) then run contract phase
+ Joint keystone3 to cluster


========== WORKFLOW UPGRADE GLANCE ==================

Step 1: 
+ Using drain mode in haproxy to detach glance1 from cluster
+ Action on Controller1:
	- Stop glance-api and glance-registry services:
	- Upgrade glance code:
	- Running expand phase in glance database:		
	- Running migration phase in glance database:
		
	- Start glance-api and glance-registry services:
+ Joint glance1 to cluster

Step 2: 
+ Using drain mode in haproxy to detach glance2 from cluster
+ Action on Controller2:
	- Stop glance-api and glance-registry services:
	- Upgrade code:
	- Start glance-api and glance-registry services:
+ Joint glance2 to cluster

Step 3: 
+ Using drain mode in haproxy to detach glance2 from cluster
+ Action on Controller3:

	- Stop glance-api and glance-registry services:
	- Upgrade code:
	- Start glance-api and glance-registry services:
+ Joint glance3 to cluster

	- After all glance services at new release then running contract phase


========== WORKFLOW UPGRADE NOVA ==================

Append this configure: [upgrade_levels]compute=auto to all nodes

Step 1: Shutdown nova-api on 3 server:

Step 2 Shutdown nova-condutor, nova-scheduler, nova-

Step 3: Upgrade new code:
	
Step 4: Upgrade DB on Controller1
Note: For Nova, there are two commands to upgrade nova database
	nova-manage db sync
	nova-manage api_db sync
	
Step 5: Start Nova services:

	+ Start all nova-conductor on 3 servers
	+ Start nova-scheduler on 3 servers
	+ Start nova-api	


========== WORKFLOW UPGRADE NEUTRON ==================

Step 1: 
+ Using drain mode in haproxy to detach neutron-api1 from cluster
+ Action on controller1
	- Stop neutron-server
	- Upgrade code
	- Upgrade neutron database by running expand phase
	- Start neutron-server
+ Joint neutron-api1 to cluster

Step 2: 
+ Using drain mode in haproxy to detach neutron-api2 from cluster
+ Action on controller2
	- Stop neutron-server
	- Upgrade code
	- Start neutron-server
+ Joint neutron-api2 to cluster

Step 3: 
+ Using drain mode in haproxy to detach neutron-api3 from cluster
+ Action on controller3
	- Stop neutron-server
	- Upgrade code
	- Start neutron-server
+ Joint neutron-api3 to cluster

Step 4: Stop and upgrade L2-agent on two network node, 03 controller node

Step 5: Stop and Upgrade L3-agent on two network nodes:

Step 6 Stop and upgrade DHCP-agent on two network nodes
	
Step 7 Stop and upgrade Metadata-agent on two network nodes



========== WORKFLOW UPGRADE CINDER ==================

Step 1: Upgrade cinder database
	cinder-manage db sync

Step 2: 
+ Using drain mode in haproxy to detach cinder-api1 from cluster
+ Action on controller1
	- Stop cinder-api
	- Upgrade code
	- Start cinder-api
+ Joint cinder-api1 to cluster


Step 3: 
+ Using drain mode in haproxy to detach cinder-api2 from cluster
+ Action on controller2
	- Stop cinder-api
	- Upgrade code
	- Start cinder-api
+ Joint cinder-api2 to cluster

Step 4: 
+ Action on controller3
	- Stop cinder-api
	- Upgrade code
	- Start cinder-api

Step 5: 
+ Action on controller1
	- Stop cinder-scheduler
	- Upgrade code
	- Start cinder-scheduler

Step 6: 
+ Action on controller2
	- Stop cinder-scheduler
	- Upgrade code
	- Start cinder-scheduler

Step 7: 
+ Action on controller3
	- Stop cinder-scheduler
	- Upgrade code
	- Start cinder-scheduler

Step 8: Upgrade cinder-volume code on controller2 and controller3
Note: At this time, we are using cinder-volume active/passive and cinder-volume is running controller1.
So we just stop cinder-volume on controller 1 and start it on controller2 or 3
Then upgrade source code for cinder-volume on controller1.

Step 9: Restart cinder-api and cinder-scheduler gradually to two services can understand cinder-volume was upgraded.
