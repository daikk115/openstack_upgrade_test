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
list_networks = [network for network in list_networks if "testing" in network.get('name')]

# Update network
# We should have separate network for updating --> ensure have network for update, that is.
NETWORK_ID = "f75ff26b-6334-446b-b0b3-50318832c716"

if __name__ == '__main__':
    i = 1
    while continue_test:
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
        if not (len(list_networks) == 0):
            delete_network = list_networks.pop()
            delete_network_id = delete_network.get("id")
            get_network_url = "http://{}:9696/v2.0/networks/{}".format(IP, delete_network_id)
            send_request(get_network_url, 'GET', headers=token_headers)
            send_request(get_network_url, 'DELETE', headers=token_headers)

        # Update VM name
        update_data = {
            "network": {
                "name": "new_name_{}".format(i)
            }
        }
        update_url = "http://{}:9696/v2.0/networks/{}".format(IP, NETWORK_ID)
        send_request(update_url, 'PUT',
                     headers=token_headers,
                     data=json.JSONEncoder().encode(update_data))
