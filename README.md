# OpenStack Upgrade Test

- Prepare:
    + Reconfigure config.py file
    + The parameter of server nodes:
        - 03 controller nodes:
            + CPU: 4 cores
            + RAM: 8G
            + Disk: 80G
        - 02 network nodes:
            + CPU: 4 cores
            + RAM: 4G
            + Disk: 80G
        - 03 compute nodes:
            + CPU: 8 cores
            + RAM: 8G
            + Disk: 80G
        - 01 database node:
            + CPU: 6 cores
            + RAM: 10G
            + Disk: 40G

- Topology:
![topology](/images/Testbed_topology.png)