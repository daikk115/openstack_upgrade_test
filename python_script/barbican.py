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

VIP = "10.164.178.153"
barbican_endpoint = "http://{}:9311/v1/{}/{}"
secrets_url = 'http://{}:9311/v1/secrets'.format(VIP)
orders_url = 'http://{}:9311/v1/orders'.format(VIP)
containers_url = 'http://{}:9311/v1/containers'.format(VIP)


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


def get_list_test_items():
    import MySQLdb
    db = MySQLdb.connect(IP, "root", "abc123", "barbican")
    cursor = db.cursor()

    # List secrets
    cursor.execute(
        "SELECT * FROM secrets \
        WHERE deleted = 0 and name like '%delete_secret%';")
    db_items = cursor.fetchall()
    list_delete_secrets = []
    for secret in db_items:
        list_delete_secrets.append(
            barbican_endpoint.format(VIP, 'secrets', secret[0]))

    cursor.execute(
        "SELECT * FROM secrets WHERE deleted = 0 and name like '%no_payload%';")
    db_items = cursor.fetchall()
    list_update_secrets = []
    for secret in db_items:
        list_update_secrets.append(
            barbican_endpoint.format(VIP, 'secrets', secret[0]))

    # List order
    cursor.execute(
        "SELECT * FROM orders \
         WHERE deleted = 0 and meta like '%delete_order%';")
    db_items = cursor.fetchall()
    list_delete_orders = []
    for order in db_items:
        list_delete_orders.append(
            barbican_endpoint.format(VIP, 'orders', order[0]))

    # List order
    cursor.execute(
        "SELECT * FROM containers \
        WHERE deleted = 0 and name like '%delete_container%';")
    db_items = cursor.fetchall()
    list_delete_containers = []
    for container in db_items:
        list_delete_containers.append(
            barbican_endpoint.format(VIP, 'containers', container[0]))

    # disconnect from server
    db.close()

    return (
        list_delete_secrets,
        list_update_secrets,
        list_delete_orders,
        list_delete_containers
    )


def test():
    i = 3008
    """ GET LIST STUFFS """
    db_data = get_list_test_items()
    list_delete_secrets = db_data[0]
    list_update_secrets = db_data[1]
    list_delete_orders = db_data[2]
    list_delete_containers = db_data[3]

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
        update_secret_ref = list_update_secrets[int(i % number_update_secrets)]
        send_request(update_secret_ref, method='PUT', headers=update_headers,
                     data='fake')

        # Get secret
        delete_secret_ref = list_delete_secrets[int(i % number_delete_secrets)]
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
        delete_order_ref = list_delete_orders[int(i % number_delete_orders)]
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
        delete_container_ref = list_delete_containers[
            int(i % number_delete_containers)]
        send_request(delete_container_ref, method='GET', headers=headers)

        # Delete order
        send_request(delete_container_ref, method='DELETE', headers=headers)


if __name__ == '__main__':
    # prepare_test_env()
    test()
    print("DONE!!!")
