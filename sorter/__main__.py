"""
base web.py file for displaying the ranked data
"""
from urlparse import parse_qs

import os
import web

from sorter.lib.request_data import read_url
from sorter.lib.parse_xml import parse
from sorter.lib.data_handler import store_data, get_books, dump_data
from sorter.lib.sorter_logger import sorter_logger
from sorter.lib.rank import rank
from sorter.lib.asset_handler import asset
from sorter.lib.bootstrap import bootstrap

def is_test(): # pylint: disable=missing-docstring
    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

    return False # pragma: no cover

LOGGER = sorter_logger(__name__)

URLS = (
    '/', 'Index',
    '/import', 'Import',
    '/(assets/.+)', 'Assets'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')
RENDERPLAIN = web.template.render('templates/')

DB_NAME = ""
if not is_test():
    DB_NAME = 'data/sorter.db'              # pragma: no cover

class Index(object):       # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def GET():             # pylint: disable=invalid-name,missing-docstring
        db_file = os.path.abspath(DB_NAME)

        if os.path.isfile(db_file):
            data = get_books(db_file)
            books = rank(data)
        else:
            books = None

        return RENDER.index(books=books)

class Import(object):   # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def POST():         # pylint: disable=invalid-name,missing-docstring
        post_data = parse_qs(web.data())

        data_file = post_data['data_file'][0] # not sure why this returns a dict of lists...

        xml_data = read_url(data_file)

        filtered_data = parse(xml_data)

        db_file = os.path.abspath(DB_NAME)

        dump_data(db_file)

        bootstrap(DB_NAME, LOGGER)

        store_data(filtered_data, db_file)

        msg = "200 OK"
        LOGGER.info(msg)
        return RENDERPLAIN.status(msg=msg)

class Assets(object):       # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def GET(asset_path):    # pylint: disable=invalid-name,missing-docstring
        asset_data = asset('templates/' + asset_path)
        data = asset_data[0]
        header_type = asset_data[1]

        web.header('Content-Type', header_type, unique=True)
        return RENDERPLAIN.status(msg=data)


if (not is_test()) and __name__ == '__main__': # pragma: no cover
    APP.run()                                  # pragma: no cover
