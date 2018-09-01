"""
base web.py file for displaying the ranked data
"""
import web
import os

from urlparse import parse_qs

from lib.request_data import Data
from lib.parse_xml import parse
from lib.rank import rank
from lib.first_run import init
from lib.store_data import store_data

# TESTING ONLY
from lib.db import DB
# END _ TESTING ONLY


URLS = (
    '/', 'Index',
    '/import', 'Import'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')
RENDERPLAIN = web.template.render('templates/')

db_file = os.path.abspath('data/sorter.db')
if (os.path.isfile(db_file) == False):
    init(db_file)

class Index(object):       # pylint: disable=too-few-public-methods
    @staticmethod
    def GET():             # pylint: disable=invalid-name
        """ GET handler for index route """
        # TESTING ONLY
        db = DB(db_file)

        db.get_connection()

        qry = "select * from rankings"
        data = db.query(qry)

        db.close_connection()
        print data
        # END _ TESTING ONLY
        
        pagedata = data

        return RENDER.index(pagedata = pagedata)

class Import(object):
    @staticmethod
    def POST():
        post_data = parse_qs(web.data())
        data_file = post_data['data_file'][0] # not sure why this returns a dict of lists...

        #dataParser = Data('http://localhost:8081/sample.xml')
        data_parser = Data(data_file)

        xml_data = data_parser.read()

        filtered_data = parse(xml_data)

        store_data(filtered_data, db_file)
        
        msg = "Status - OK"
        return RENDERPLAIN.status(msg = msg)


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
