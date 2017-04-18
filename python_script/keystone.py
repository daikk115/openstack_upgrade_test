import json

from config import *
from utils import *
from get_auth import TOKEN

# We must have an user that we will update name testing
# Do NOT confuse with user which we have configured in config.py
USER_ID = "1f794d2fc66b439a899043cac71db9d9"

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
set_users = {user.get('id') for user in result if 'test' in user.get('name')}

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
    try:
        while True:
            time.sleep(0.3)
            # Get token and quit
            future = send_request(get_token_url, 'POST',
                                  headers=get_token_headers,
                                  data=json.JSONEncoder().encode(get_token_data))
            # To get token: future.result().headers.get("X-Subject-Token")

            # Create user
            create_user_data = {
                "user": {
                    "name": "create_{}".format(i),
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
            try:
                user_id = set_users.pop()
                delete_user_url = AUTH_URL + "/users/{}".format(user_id)
                send_request(update_user_url, 'DELETE',
                             headers=token_headers)
            except KeyError:
                continue
            # Increase counter variable
            i += 1
    except KeyboardInterrupt:
        time.sleep(3)
        footer()
