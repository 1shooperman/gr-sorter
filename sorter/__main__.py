"""
base web.py file for displaying the ranked data
"""
from urlparse import parse_qs

import os
import web

from sorter.lib.request_data import read_url
from sorter.lib.parse_xml import parse
from sorter.lib.first_run import init
from sorter.lib.data_handler import store_data, get_books
from sorter.lib.sorter_logger import sorter_logger
from sorter.lib.rank import rank

LOGGER = sorter_logger(__name__)

URLS = (
    '/', 'Index',
    '/import', 'Import',
    '/(assets/.+)', 'Assets'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')
RENDERPLAIN = web.template.render('templates/')

DB_FILE = os.path.abspath('data/sorter.db')
if os.path.isfile(DB_FILE) is False:
    LOGGER.info('First run, initializing application')
    init(DB_FILE)

class Index(object):       # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def GET():             # pylint: disable=invalid-name,missing-docstring
        data = get_books(DB_FILE)

        ranked_data = rank(data)

        books = ranked_data

        return RENDER.index(books=books)

class Import(object):   # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def POST():         # pylint: disable=invalid-name,missing-docstring
        post_data = parse_qs(web.data())
        data_file = post_data['data_file'][0] # not sure why this returns a dict of lists...

        xml_data = read_url(data_file)

        filtered_data = parse(xml_data)

        store_data(filtered_data, DB_FILE)

        msg = "200 OK"
        LOGGER.info(msg)
        return RENDERPLAIN.status(msg=msg)

class Assets(object):       # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def GET(asset_path):    # pylint: disable=invalid-name,missing-docstring
        asset_file = os.path.abspath('templates/' + asset_path)
        if os.path.isfile(asset_file) is True:
            if '.js' in asset_path:
                header_type = 'application/javascript; charset=utf-8'
            elif '.css' in asset_path:
                header_type = 'text/css; charset=utf-8'
            else:
                header_type = 'text/plain; charset=utf-8'

            web.header('Content-Type', header_type, unique=True)
            with open(asset_file, 'r') as myfile:
                data = myfile.read()
        else:
            data = None

        return RENDERPLAIN.status(msg=data)


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
