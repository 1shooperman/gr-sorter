"""
base web.py file for displaying the ranked data
"""
from urlparse import parse_qs, urlsplit

import os
import web

from sorter.lib.request_data import read_url
from sorter.lib.parse_xml import get_total_pages
from sorter.lib.data_handler import get_books, clean_data
from sorter.lib.sorter_logger import sorter_logger
from sorter.lib.rank import rank
from sorter.lib.asset_handler import asset
from sorter.lib.page_utils import page_loop
from sorter.lib.defaults import Defaults

LOGGER = sorter_logger(__name__)

URLS = (
    '/', 'Index',
    '/import', 'Import',
    '/(assets/.+)', 'Assets',
    '/admin', 'Admin'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')
RENDERPLAIN = web.template.render('templates/')

DB_NAME = ""
if not Defaults.is_test():
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
        _, _, _, query, _ = urlsplit(web.data())
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
        except KeyError:
            LOGGER.warn(KeyError)

        defaults = Defaults(api_key, per_page, ['to-read'])

        #_, data_file = path.split('=')
        data_file = defaults.get_shelf_url(user_id)

        xml_data = read_url(data_file)

        total_pages, document_page = get_total_pages(xml_data)
        if total_pages > 0:
            for page_num in range(total_pages):
                # if this is page 1, we can assume we already have the data
                if page_num == 0 and document_page == 1:
                    page_loop(xml_data, DB_NAME, new_data)
                else:
                    page_string = "?page=%s" % (page_num + 1)
                    if document_page != (page_num + 1):
                        xml_data = read_url(data_file + page_string)

                    page_loop(xml_data, DB_NAME, False)

        clean_data(DB_NAME)

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
        return data

class Admin(object):        # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def GET():              # pylint: disable=invalid-name,missing-docstring
        return RENDER.admin()


if (not Defaults.is_test()) and __name__ == '__main__': # pragma: no cover
    APP.run()                                  # pragma: no cover
