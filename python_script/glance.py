import json

from config import *
from utils import *
from get_token import TOKEN

##################
##### CONFIG #####
##################
CHUNKSIZE = 1024 * 64  # 64kB
image_path = 'cirros-0.3.5-x86_64-disk.img'

# We must have an image for update testing
IMAGE_ID = "329b1487-d80f-483d-b180-47b1d81700d9"

# Create image data: use POST and PUT method.
# NOTE: put_data  and put_url will be formatted later
post_url = 'http://{}:9292/v2/images'.format(IP)
post_data = {
    "container_format": "bare",
    "disk_format": "qcow2",
    # more than one image can have similar name
    "name": "testing",
    "visibility": "public"
}
post_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/json'
}

put_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/octet-stream'
}

# Update image: use PATCH method.
# NOTE: patch_url will be formatted later
patch_data = [{
    "path": "/name",
    "value": "testing_newname",
    "op": "replace"
}]
patch_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/openstack-images-v2.1-json-patch'
}

# Get image(s)
get_headers = {
    'X-Auth-Token': TOKEN
}

# Delete image
# We should have list image for delete testing (all image have similar name)
delete_headers = put_headers

list_image_url = 'http://{}:9292/v2/images?name=in:"{}"'.format(IP, "testing")
future = send_request(list_image_url, 'GET', headers=get_headers)
result = future.result().content
result = json.loads(result)
list_images = result.get("images")




################
def _chunk_body(body):
    # Source: https://github.com/openstack/python-glanceclient/blob/master/glanceclient/common/http.py#L62
    chunk = body
    while chunk:
        chunk = body.read(CHUNKSIZE)
        if not chunk:
            break
        yield chunk


if __name__ == '__main__':
    while True:
        time.sleep(0.3)
        try:
            # Create image
            future = send_request(post_url, 'POST',
                                  headers=post_headers, data=json.JSONEncoder().encode(post_data))
            content = future.result().content

            # Delete images
            image = list_images.pop()
            delete_url = "http://{}:9292/v2/images/{}".format(IP, image.get('id'))
            send_request(delete_url, 'DELETE',
                         headers=get_headers)
        except KeyboardInterrupt:
            time.sleep(3)
            break
        except:
            continue

        image_id = json.loads(content).get('id')

        # Upload image binary data
        put_url = 'http://{}:9292/v2/images/{}/file'.format(IP, image_id)
        f = open(image_path, 'rb')
        chunk_data = _chunk_body(f)
        put_result = send_request(put_url, 'PUT',
                                  headers=put_headers, data=chunk_data, stream=True)

        # Update image
        # Actually, we just rename on the first time run bellow stuffs
        patch_url = "http://{}:9292/v2/images/{}".format(IP, IMAGE_ID)
        send_request(patch_url, 'PATCH',
                     headers=patch_headers, data=json.JSONEncoder().encode(patch_data))

        # Get image
        get_url = patch_url
        send_request(get_url, 'GET',
                     headers=get_headers)

    # Collect error codes
    footer()
