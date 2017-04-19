import json

from config import *
from utils import *
from get_auth import TOKEN

# We must have an user that we will update name testing
# Do NOT confuse with user which we have configured in config.py
USER_ID = "4d61238c6d5a4e2bb270cdf594c7e73c"

# Url
get_token_url = AUTH_URL + "/auth/tokens"
create_user_url = AUTH_URL + "/users"
update_user_url = AUTH_URL + "/users/{}".format(USER_ID)

# Headers
get_token_headers = {
    'Content-Type': 'application/json'
}

token_headers = {
    'Content-Type': 'application/json',
    'X-Auth-Token': TOKEN
}

# List users for DELETE with name that contain "test" mark
future = send_request(create_user_url, 'GET',
                      headers=token_headers)

result = future.result().content
result = json.loads(result)
result = result.get("users")
list_users = [user.get('id') for user in result if 'testing' in user.get('name')]

# Data payload
get_token_data = {
    "auth": {
        "identity": {
            "methods": ["password"],
            "password": {
                "user": {
                    "name": USERNAME,
                    "domain": {"id": "default"},
                    "password": PASSWORD
                }
            }
        },
        "scope": {
            "project": {
                "name": "admin",
                "domain": {"id": "default"}

            }
        }
    }
}

if __name__ == '__main__':
    i = 1
    while continue_test:
        time.sleep(0.3)
        # Get token
        future = send_request(get_token_url, 'POST',
                              headers=get_token_headers,
                              data=json.JSONEncoder().encode(get_token_data))
        # To get token: future.result().headers.get("X-Subject-Token")

        # Create user
        create_user_data = {
            "user": {
                "name": "create2_{}".format(i),
                "password": "default"
            }
        }
        send_request(create_user_url, 'POST',
                     headers=token_headers,
                     data=json.JSONEncoder().encode(create_user_data))

        # Update user
        update_user_data = {
            "user": {
                "name": "update_{}".format(i)
            }
        }
        send_request(update_user_url, 'PATCH',
                     headers=token_headers,
                     data=json.JSONEncoder().encode(update_user_data))
        # Delete user
        if not (len(list_users) == 0):
            user_id = list_users.pop()
            delete_user_url = AUTH_URL + "/users/{}".format(user_id)
            send_request(delete_user_url, 'DELETE',
                         headers=token_headers)
        # Increase counter variable
        i += 1
