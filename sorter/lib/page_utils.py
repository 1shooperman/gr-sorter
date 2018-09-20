''' page_utils.py '''
import os

from urlparse import parse_qs, urlsplit

from sorter.lib.data_handler import store_data, dump_data
from sorter.lib.parse_xml import parse
from sorter.lib.bootstrap import bootstrap
from sorter.lib.sorter_logger import sorter_logger

LOGGER = sorter_logger(__name__)

def page_loop(xml_data, db_name, new_data=False):
    ''' retrieving and storing multipage data '''
    filtered_data = parse(xml_data)

    db_file = os.path.abspath(db_name)

    if new_data is True:
        dump_data(db_file)
        bootstrap(db_name, LOGGER)

    store_data(filtered_data, db_file)

def page_vars(post_data):
    '''
    Get page vars from POST data
    '''
    _, _, _, query, _ = urlsplit(post_data)
    args = parse_qs(query)

    new_data = False
    per_page = None
    api_key = None
    user_id = None

    try:
        new_data = int(args['new'][0]) == 1
        per_page = int(args['per_page'][0])
        api_key = args['api_key'][0]
        user_id = args['user_id'][0]
    except ValueError:
        LOGGER.warn(ValueError)
    except KeyError:
        LOGGER.warn(KeyError)

    return (new_data, per_page, api_key, user_id)
