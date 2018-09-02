"""
base web.py file for displaying the ranked data
"""
from urlparse import parse_qs
import os
import web
from sorter.lib.request_data import Data
from sorter.lib.parse_xml import parse
from sorter.lib.first_run import init
from sorter.lib.store_data import store_data

# TESTING ONLY
from sorter.lib.db import DB
# END _ TESTING ONLY

URLS = (
    '/', 'Index',
    '/import', 'Import'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')
RENDERPLAIN = web.template.render('templates/')

DB_FILE = os.path.abspath('data/sorter.db')
if os.path.isfile(DB_FILE) is False:
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
        post_data = parse_qs(web.data())
        data_file = post_data['data_file'][0] # not sure why this returns a dict of lists...

        #dataParser = Data('http://localhost:8081/sample.xml')
        data_parser = Data(data_file)

        xml_data = data_parser.read()

        filtered_data = parse(xml_data)

        store_data(filtered_data, DB_FILE)

        msg = "Status - OK"
        return RENDERPLAIN.status(msg=msg)


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
