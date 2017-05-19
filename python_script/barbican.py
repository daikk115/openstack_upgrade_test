import json

from config import *
from utils import *
from get_auth import TOKEN


headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

secrets_url = 'http://{}:9311/v1/secrets'.format(IP)


def main():
    for i in range(500):
        # Get secret
        send_request(url=secrets_url, method='GET', headers=headers)
        data_secret = {
            'name': 'secret_{}'.format(str(i)),
            'algorithm': 'aes',
            'bit_length': 256,
            'mode': 'cbc',
            'payload': 'data_secret_{}'.format(str(i)),
        }
        # Create secret
        send_request(secrets_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(data_secret))

if __name__ == '__main__':
    main()
