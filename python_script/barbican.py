import json

from config import *
from utils import *
from get_auth import TOKEN

headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

update_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'text/plain',
    'Content-Encoding': 'base64'
}

secrets_url = 'http://{}:9311/v1/secrets'.format(IP)
orders_url = 'http://{}:9311/v1/orders'.format(IP)
containers_url = 'http://{}:9311/v1/containers'.format(IP)


def prepare_test_env():
    for i in range(1500):
        secret_no_payload = {
            "secret_type": "opaque",
            "bit_length": 256,
            "name": 'no_payload_secret_{}'.format(str(i)),
            "algorithm": "aes",
            "mode": "cbc"
        }

        secret_data = {
            "secret_type": "opaque",
            "name": 'delete_secret_{}'.format(str(i)),
            "algorithm": "aes",
            "payload_content_type": "text/plain",
            "mode": "cbc",
            "bit_length": 256,
            "payload": 'data_secret_{}'.format(str(i))
        }

        # Store secret
        send_request(secrets_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(secret_no_payload))
        send_request(secrets_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(secret_data))

        order_data = {
            "type": "key",
            "meta":
                {
                    "name": 'delete_order_{}'.format(str(i)),
                    "algorithm": "AES",
                    "bit_length": 256,
                    "mode": "cbc",
                    "payload_content_type": "application/octet-stream"
                }
        }

        # Create order
        send_request(orders_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(order_data))

        container_data = {
            "type": "generic",
            "name": 'delete_container_{}'.format(str(i)),
            "secret_refs": [
            ]
        }

        # Create order
        send_request(containers_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(container_data))


def test():
    i = 3008
    """ GET LIST STUFFS """
    # List secret
    unlimit_secrets_url = secrets_url + "?limit=100000"
    secrets = send_request(url=unlimit_secrets_url, method='GET',
                           headers=headers)
    secrets = secrets.result().content
    secrets = json.loads(secrets)
    list_secrets = secrets.get("secrets")
    list_delete_secrets = [secret for secret in list_secrets if
                           "delete_secret" in secret['name']]
    list_update_secrets = [secret for secret in list_secrets if
                           "no_payload_secret" in secret['name']]

    unlimit_orders_url = orders_url + "?limit=100000"
    orders = send_request(url=unlimit_orders_url, method='GET', headers=headers)
    orders = orders.result().content
    orders = json.loads(orders)
    list_orders = orders.get("orders")
    list_delete_orders = [order for order in list_orders if
                          "delete_order" in order['meta']['name']]

    unlimit_containers_url = containers_url + "?limit=100000"
    containers = send_request(url=unlimit_containers_url,
                              method='GET', headers=headers)
    containers = containers.result().content
    containers = json.loads(containers)
    list_containers = containers.get("containers")
    list_delete_containers = [container for container in list_containers if
                              "delete_container" in container['name']]

    number_delete_secrets = len(list_delete_secrets)
    number_update_secrets = len(list_update_secrets)
    number_delete_orders = len(list_delete_orders)
    number_delete_containers = len(list_delete_containers)

    while continue_test:
        i += 1

        """ SECRET """
        secret_data = {
            "secret_type": "opaque",
            "name": 'secret_{}'.format(str(i)),
            "algorithm": "aes",
            "payload_content_type": "text/plain",
            "mode": "cbc",
            "bit_length": 256,
            "payload": 'data_secret_{}'.format(str(i))
        }

        # Store secret
        send_request(secrets_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(secret_data))

        # Update secret
        update_secret = list_update_secrets[int(i % number_update_secrets)]
        update_secret_ref = update_secret['secret_ref']
        send_request(update_secret_ref, method='PUT', headers=update_headers,
                     data='fake')

        # Get secret
        delete_secret = list_delete_secrets[int(i % number_delete_secrets)]
        delete_secret_ref = delete_secret['secret_ref']
        send_request(url=delete_secret_ref, method='GET', headers=headers)

        # Delete secret
        send_request(delete_secret_ref, method='DELETE', headers=headers)

        """ ORDER """
        order_data = {
            "type": "key",
            "meta":
                {
                    "name": 'order_{}'.format(str(i)),
                    "algorithm": "AES",
                    "bit_length": 256,
                    "mode": "cbc",
                    "payload_content_type": "application/octet-stream"
                }
        }
        # Create order
        send_request(orders_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(order_data))

        # Get order
        delete_order = list_delete_orders[int(i % number_delete_orders)]
        delete_order_ref = delete_order['order_ref']
        send_request(delete_order_ref, method='GET', headers=headers)

        # Delete order
        send_request(delete_order_ref, method='DELETE', headers=headers)

        """ CONTAINER """
        container_data = {
            "type": "generic",
            "name": 'container_{}'.format(str(i)),
            "secret_refs": [
            ]
        }
        # Create container
        send_request(containers_url, method='POST',
                     headers=headers,
                     data=json.JSONEncoder().encode(container_data))

        # Get container
        delete_container = list_delete_containers[
            int(i % number_delete_containers)]
        delete_container_ref = delete_container['container_ref']
        send_request(delete_container_ref, method='GET', headers=headers)

        # Delete order
        send_request(delete_container_ref, method='DELETE', headers=headers)


if __name__ == '__main__':
    # prepare_test_env()
    test()
    print("DONE!!!")
