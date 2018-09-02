"""
base web.py file for displaying the ranked data
"""
from urlparse import parse_qs

import os
import web

from sorter.lib.request_data import read_url
from sorter.lib.parse_xml import parse
from sorter.lib.first_run import init
from sorter.lib.store_data import store_data
from sorter.lib.sorter_logger import sorter_logger

# TESTING ONLY
from sorter.lib.db import DB
# END _ TESTING ONLY

LOGGER = sorter_logger(__name__)

URLS = (
    '/', 'Index',
    '/import', 'Import'
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
        # TESTING ONLY
        db = DB(DB_FILE)

        db.create_connection()

        qry = "select * from rankings"
        data = db.query(qry)

        db.close_connection()
        print data
        # END _ TESTING ONLY

        pagedata = data

        return RENDER.index(pagedata=pagedata)

class Import(object): # pylint: disable=too-few-public-methods,missing-docstring
    @staticmethod
    def POST(): # pylint: disable=invalid-name,missing-docstring
        LOGGER.info('ran import handler')
        post_data = parse_qs(web.data())
        data_file = post_data['data_file'][0] # not sure why this returns a dict of lists...

        #dataParser = Data('http://localhost:8081/sample.xml')
        xml_data = read_url(data_file)

        filtered_data = parse(xml_data)

        store_data(filtered_data, DB_FILE)

        msg = "Status - OK"
        LOGGER.info(msg)
        return RENDERPLAIN.status(msg=msg)


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
