''' page_utils.py '''
import os
import re

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

def query_vars(get_data):
    '''
    Get page vars from GET query string
    '''
    return (get_data.api_key, None)

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
    except ValueError as err:
        LOGGER.warn('ValueError with message: %s', err)
    except KeyError as err:
        LOGGER.warn('KeyError for key %s', err)

    try:
        per_page = int(args['per_page'][0])
    except ValueError as err:
        LOGGER.warn('ValueError with message: %s', err)
    except KeyError as err:
        LOGGER.warn('KeyError for key %s', err)

    try:
        api_key = args['api_key'][0]
    except KeyError as err:
        LOGGER.warn('KeyError for key %s', err)

    try:
        user_id = args['user_id'][0]
    except KeyError as err:
        LOGGER.warn('KeyError for key %s', err)


    return (new_data, per_page, api_key, user_id)

def from_post(post_data):
    '''
    Get arbitrary variables from POST
    '''
    args = parse_qs(post_data)

    attr, book_id, value = None, None, None
    books = []
    for key in args:
        if '-' in key:
            attr, book_id = key.split('-')
            value = args[key][0]

            attr = attr.replace(' ', '_')

            # sanitize the inputs!
            attr = re.sub('[^a-zA-Z0-9_]+', '', attr)
            book_id = re.sub('[^a-zA-Z0-9]+', '', book_id)
            value = re.sub('[^a-zA-Z0-9 _:/.-]+', '', value)

            attr = attr.lower()

            books.append({
                'book_id': int(book_id),
                'attr': attr,
                'value': value
            })

    return books

def get_paginated(books):
    return len(books) / 10