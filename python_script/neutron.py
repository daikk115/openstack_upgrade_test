import json

from config import *
from utils import *
from get_auth import TOKEN

# Create network
create_network_url = "http://{}:9696/v2.0/networks".format(IP)
token_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

# Get network for DELETE
get_list_url = create_network_url
future = send_request(get_list_url, 'GET', headers=token_headers)
result = future.result().content
result = json.loads(result)
list_networks = result.get("networks")
list_networks = {network for network in list_networks if "testing" in network.get('name')}

if __name__ == '__main__':
    i = 1
    while True:
        # Create network
        create_data = {
            "network": {
                "name": "sample_network_x_{}".format(i)
            }
        }
        i += 1
        future = send_request(create_network_url, 'POST',
                              headers=token_headers,
                              data=json.JSONEncoder().encode(create_data))
        result = future.result().content
        result = json.loads(result)
        network = result.get('network')
        if type(network) is dict:
            network_id = result['network']['id']
            create_subnet_data = {
                "subnet": {
                    "network_id": network_id,
                    "ip_version": 4,
                    "cidr": "192.168.199.0/24"
                }
            }
            create_subnet_url = "http://{}:9696/v2.0/subnets".format(IP)
            send_request(create_subnet_url, 'POST',
                         headers=token_headers,
                         data=json.JSONEncoder().encode(create_subnet_data))

        # Get and delete network
        delete_network = list_networks.pop()
        if not delete_network:
            continue
        delete_network_id = delete_network.get("id")
        get_network_url = "http://{}:9696/v2.0/network/{}".format(IP, delete_network_id)
        send_request(get_network_url, 'GET', headers=token_headers)
        send_request(get_network_url, 'DELETE', headers=token_headers)
