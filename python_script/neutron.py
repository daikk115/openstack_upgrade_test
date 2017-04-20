import json
from requests import ConnectionError

from config import *
from utils import *
from get_auth import TOKEN

# Create network
create_network_url = "http://{}:9696/v2.0/networks".format(IP)
token_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

# Create router
create_router_url = "http://{}:9696/v2.0/routers".format(IP)

# Get network for DELETE
get_network_list_url = create_network_url
future = send_request(get_network_list_url, 'GET', headers=token_headers)
result = future.result().content
result = json.loads(result)
list_networks = result.get("networks")
list_networks = [network for network in list_networks if "testing" in network.get('name')]

# Get routers for DELETE
get_router_list_url = create_router_url
future = send_request(get_router_list_url, 'GET', headers=token_headers)
result = future.result().content
result = json.loads(result)
list_routers = result.get("routers")
list_routers = [router for router in list_routers if "testing" in router.get('name')]

# Update network
# We should have separate network for updating --> ensure have network for update, that is.
NETWORK_ID = "f6e3556e-29ab-4ee7-ba64-7fab0c423e26"

# Update router
# We should have separate router for updating --> ensure have router for update, that is.
ROUTER_ID = "b0e19990-d9ba-4981-9da7-5aeec2957c77"

if __name__ == '__main__':
    i = 1
    while continue_test:
        time.sleep(0.3)
        try:
            # Create network
            create_network_data = {
                "network": {
                    "name": "new_network_{}".format(i)
                }
            }
            i += 1
            future = send_request(create_network_url, 'POST',
                                  headers=token_headers,
                                  data=json.JSONEncoder().encode(create_network_data))
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

            # Update network name
            update_network_data = {
                "network": {
                    "name": "new_name_{}".format(i)
                }
            }
            update_network_url = "http://{}:9696/v2.0/networks/{}".format(IP, NETWORK_ID)
            send_request(update_network_url, 'PUT',
                         headers=token_headers,
                         data=json.JSONEncoder().encode(update_network_data))

            # Create router
            create_router_data = {
                "router": {
                    "name": "new_router_{}".format(i)
                }
            }
            future = send_request(create_router_url, 'POST',
                                  headers=token_headers,
                                  data=json.JSONEncoder().encode(create_router_data))

            # Get and delete network
            if not (len(list_routers) == 0):
                delete_router = list_routers.pop()
                delete_router_id = delete_router.get("id")
                get_router_url = "http://{}:9696/v2.0/routers/{}".format(IP, delete_router_id)
                send_request(get_router_url, 'GET', headers=token_headers)
                send_request(get_router_url, 'DELETE', headers=token_headers)

            # Update router name
            update_router_data = {
                "router": {
                    "name": "new_name_{}".format(i)
                }
            }
            update_router_url = "http://{}:9696/v2.0/routers/{}".format(IP, ROUTER_ID)
            send_request(update_router_url, 'PUT',
                         headers=token_headers,
                         data=json.JSONEncoder().encode(update_router_data))
        except ConnectionError or ValueError:
            pass
