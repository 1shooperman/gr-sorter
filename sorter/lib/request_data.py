''' request_data.py '''
import urllib2
from urllib2 import HTTPError
import time

from sorter.lib.sorter_logger import sorter_logger
LOGGER = sorter_logger(__name__)

def read_url(api_url):
    ''' read data from a url '''
    LOGGER.info("Requesting: %s", api_url)
    body = None
    request = None
    try:
        request = urllib2.urlopen(api_url)
        body = request.read()
        request.close()
    except HTTPError as err:
        LOGGER.warn(err)

    # per goodreads policy, we can't call the API more than once a second.
    # this will be a stopgap until a better solution is put in place
    time.sleep(1)
    return body
