"""
xmit

Transmit data to the back end.
"""

""" EDMC Imports """
from config import appname

""" Other Imports """
import sys
import logging
import os
import time
import traceback
import requests

plugin_dir = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f"{appname}.{plugin_dir}")

XMIT_URL = 'http://forthemug.com:4567'
DEFAULT_TIMEOUT = 7
COMPRESSED_OCTET_STREAM = {'content-type': 'application/octet-stream', 'content-encoding': 'zlib'}

FAILED = False

def request(path_or_url, base=XMIT_URL, method='get', parse=True, **kwargs):
    """
    GET or POST the JSON at ``path_or_url``.

    If ``path_or_url`` starts with ``/``, treat it as a path under ``base``.
    Else, treat it as a full URL.

    Returns:

     * None on an exception or ``status_code`` not in [200, 204]
     * '' on 204
     * JSON-parsed text if 200 and ``parse``
     * Text if 200 and not ``parse``
    """

    assert isinstance(path_or_url, str)
    assert isinstance(base, str)
    assert method in ['get', 'post']
    assert isinstance(parse, bool)

    if path_or_url[:1] == '/':
        url = base + path_or_url
    else:
        url = path_or_url

    try:
        began = time.time()
        FAILED = False
        response = getattr(requests, method)(url, timeout=DEFAULT_TIMEOUT, **kwargs)
        delay = (time.time() - began) * 1000

        if response.status_code == 200:
            if parse:
                try:
                    return response.json()

                except ValueError:
                    FAILED = True
                    logger.error("Unable to parse JSON: ")
                    pass

            else:
                return response.content

        elif response.status_code == 204:
            return ''

        FAILED = True
        logger.error("{} {} {} ms={:.0f}".format(response.status_code, method.upper(), url, delay))
        logger.error("{}".format(repr(response.content)))

        return None

    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error("{}".format("\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))))
        return None


def get(path, **kwargs):
    "Get the JSON at ``path``. See request_json for return details."
    return request(path, method='get', **kwargs)


def post(path, data, **kwargs):
    "Post ``data`` to ``path``. See request_json for return details."
    return request(path, method='post', data=data, **kwargs)
