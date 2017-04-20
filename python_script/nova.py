import json

from config import *
from utils import *
from get_auth import TOKEN, PROJECT_ID

FLAVOR_ID = "ee4d9c29-cffd-4a1a-8e80-8f3c9875a2e4"
IMAGE_ID = "e082313d-e423-4355-8799-e0010bb0212b"

# Create instance
create_url = "http://{}:8774/v2.1/{}/servers".format(IP, PROJECT_ID)

create_data = {
    "server": {
        "min_count": 1,
        "flavorRef": FLAVOR_ID,
        "name": "Testing",  # Create the same VM name, it's OK
        "imageRef": IMAGE_ID,
        "max_count": 1,
        "networks": [
            {
                "uuid": "66883877-e7c3-4963-95ea-28d3fd6be62b"
            }
        ]
    }
}

create_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

# Delete instances
# We should have enough instances for delete job
get_url = "http://{}:8774/v2.1/{}/servers?name={}".format(IP, PROJECT_ID, "VM")
get_headers = create_headers
future = send_request(get_url, 'GET', headers=get_headers)
result = future.result().content
result = json.loads(result)
list_servers = result.get("servers")

# Update VM
# We should have separate VM for updating --> ensure have VM for update, that is.
VM_ID = "857f9828-692b-4bda-99dd-b810b437f80a"

if __name__ == '__main__':
    i = 1
    while continue_test:
        time.sleep(0.3)
        # Create VM
        send_request(create_url, 'POST',
                     headers=create_headers,
                     data=json.JSONEncoder().encode(create_data))
        # Get and delete an VM
        if not (len(list_servers) == 0):
            server = list_servers.pop()
            vm_url = "http://{}:8774/v2.1/{}/servers/{}".format(IP, PROJECT_ID, server.get('id'))
            send_request(vm_url, 'GET', headers=get_headers)
            # Delete VM
            send_request(vm_url, 'DELETE', headers=get_headers)

        # Update VM name
        i += 1
        update_data = {
            "server": {
                "name": "new_name_{}".format(i)
            }
        }
        update_url = "http://{}:8774/v2.1/{}/servers/{}".format(IP, PROJECT_ID, VM_ID)
        send_request(update_url, 'PUT',
                     headers=get_headers, data=json.JSONEncoder().encode(update_data))
