"""This script reponsible put all of send_get_request() function results
into list, gracefull exit any script import it and return analytics
"""
import time
import signal
import sys

from requests_futures.sessions import FuturesSession


tasks = []
session = FuturesSession()


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
    print(resp.url)


def footer():
    """ Return result of testing process

    :return:
    """

    is_find_start = True
    count = 0
    start, end = 0, 0 # assign this vars prepare if we dont' have downtime
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
    print("Downtime for rolling upgrade process: {} ms" .format(end-start))
    print("Number of fail requests (status code >= 500): {}" .format(count))
    print(error_dict)


def exit_gracefully(signum, frame):
    # Source: Antti Haapala - http://stackoverflow.com/a/18115530
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            footer()
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    signal.signal(signal.SIGINT, exit_gracefully)


def send_request(url, method, headers=None, data=None, **kwargs):
    if method == 'GET':
        return session.get(url, headers=headers,
                           background_callback=bg_cb, **kwargs)
    elif method == 'POST':
        return session.post(url, headers=headers,
                            data=data, background_callback=bg_cb, **kwargs)
    elif method == 'PUT':
        return session.put(url, headers=headers,
                           data=data, background_callback=bg_cb, **kwargs)
    elif method == 'PATCH':
        return session.patch(url, headers=headers,
                             data=data, background_callback=bg_cb, **kwargs)
    elif method == 'DELETE':
        return session.delete(url, headers=headers, background_callback=bg_cb, **kwargs)
    else:
        print("Method does not support: {}" .format(method))


original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)
