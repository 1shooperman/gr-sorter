''' request_data.py '''
import urllib2

from sorter.lib.sorter_logger import sorter_logger
LOGGER = sorter_logger(__name__)

def read_url(api_url):
    ''' read data from a url '''
    request = urllib2.urlopen(api_url)
    body = request.read()
    request.close()
    LOGGER.info("Requesting: %s", api_url)
    return body
