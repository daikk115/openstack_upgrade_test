"""This script reponsible put all of send_get_request() function results
into list and return analytics via footer function()
"""
import time
import signal

from requests_futures.sessions import FuturesSession

tasks = []
future_session = FuturesSession()
stop_test  = False


def bg_cb(sess, resp):
    """ Callback function when requests done

    :param sess:
    :param resp:
    :return:
    """

    timestamp = time.time() * 1000
    tasks.append({
        "timestamp": timestamp,
        "status": resp.status_code
    })
    print("%d - %d - %s" % (timestamp, resp.status_code, resp.request.method))
    print("via: {}" .format(resp.url))


def footer():
    """ Return result of testing process

    :return:
    """

    is_find_start = True
    count = 0
    start, end = 0, 0  # assign this vars prepare if we dont' have downtime
    error_dict = {}

    for task in tasks:
        if is_find_start:
            if task.get('status') >= 500:
                is_find_start = False
                start = task.get('timestamp')
        else:
            try:
                error_dict[task.get('status')] += 1
            except:
                error_dict[task.get('status')] = 1
                if task.get('status') / 100 < 4:
                    end = task.get('timestamp')

    for key in error_dict:
        if (int(key) / 100) == 5:
            count += error_dict.get(key)
    print("Downtime for rolling upgrade process: {} ms".format(end - start))
    print("Number of fail requests (status code >= 500): {}".format(count))
    print(error_dict)


def send_request(url, method, headers=None, data=None, **kwargs):
    if method == 'GET':
        return future_session.get(url, headers=headers,
                                  background_callback=bg_cb, **kwargs)
    elif method == 'POST':
        return future_session.post(url, headers=headers,
                                   data=data, background_callback=bg_cb, **kwargs)
    elif method == 'PUT':
        return future_session.put(url, headers=headers,
                                  data=data, background_callback=bg_cb, **kwargs)
    elif method == 'PATCH':
        return future_session.patch(url, headers=headers,
                                    data=data, background_callback=bg_cb, **kwargs)
    elif method == 'DELETE':
        return future_session.delete(url, headers=headers, background_callback=bg_cb, **kwargs)
    else:
        print("Method does not support: {}".format(method))

