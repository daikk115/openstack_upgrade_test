import json

from config import *
from utils import *
from get_auth import TOKEN, PROJECT_ID

# Create network
create_volume_url = "http://{}:8776/v2/{}/volumes".format(IP, PROJECT_ID)
token_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

# Get network for DELETE
get_list_url = create_volume_url
future = send_request(get_list_url, 'GET', headers=token_headers)
result = future.result().content
result = json.loads(result)
list_volumes = result.get("volumes")
list_volumes = [v for v in list_volumes if "testing" in v.get('name')]

# Update volume
# We should have separate volume for updating --> ensure have volume for update, that is.
VOLUME_ID = "49d81132-6bcb-4c08-8547-62d829a02e3d"

if __name__ == '__main__':
    i = 1
    while continue_test:
        time.sleep(0.3)
        # Create volume 1 GB
        create_data = {
            "volume": {
                "size": 1,
                "name": "new_volume_{}".format(i)
            }
        }
        i += 1
        send_request(create_volume_url, 'POST',
                     headers=token_headers,
                     data=json.JSONEncoder().encode(create_data))
        # Get and delete an VM
        if not (len(list_volumes) == 0):
            volume = list_volumes.pop()
            volume_url = "http://{}:8776/v2/{}/volumes/{}".format(IP, PROJECT_ID, volume.get('id'))
            send_request(volume_url, 'GET', headers=token_headers)
            # Delete VM
            send_request(volume_url, 'DELETE', headers=token_headers)

        # Update VM name
        update_data = {
            "volume": {
                "name": "new_name_{}".format(i)
            }
        }
        update_url = "http://{}:8776/v2/{}/volumes/{}".format(IP, PROJECT_ID, VOLUME_ID)
        send_request(update_url, 'PUT',
                     headers=token_headers,
                     data=json.JSONEncoder().encode(update_data))
