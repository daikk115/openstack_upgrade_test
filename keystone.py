from config import *
from graceful_exit import *

get_token = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": USERNAME,
                    "domain": {
                        "name": "Default"
                    },
                    "password": PASSWORD
                }
            }
        }
    }
}
if __name__ == '__main__':
    while True:
        try:
            future = send_request(AUTH_URL, 'GET',
                                  headers=get_token)
            content = future.result().content
            print(content)
        except:
            continue
