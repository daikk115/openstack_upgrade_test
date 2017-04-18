import json

from config import *
from utils import *
from get_auth import TOKEN

get_headers = {
    'X-Auth-Token': TOKEN,
    'Content-Type': 'application/openstack-images-v2.1-json-patch'
}
# We should have list image for delete testing (all image have similar name)
list_image_url = 'http://{}:9292/v2/images?name=in:"{}"'.format(IP, "testing")

future = send_request(list_image_url, 'GET', headers=get_headers)


