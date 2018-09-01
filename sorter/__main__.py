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
from lib.store import store_ranked_data

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
        pagedata = "sorted data goes here"

        return RENDER.index(pagedata = pagedata)

class Import(object):
    @staticmethod
    def POST():
        post_data = parse_qs(web.data())
        data_file = post_data['data_file'][0] # not sure why this returns a dict of lists...

        #dataParser = Data('http://localhost:8081/sample.xml')
        dataParser = Data(data_file)

        xmlData = dataParser.read()

        filteredData = parse(xmlData)

        rankedData = rank(filteredData)

        store_ranked_data(rankedData)
        
        msg = "Status - OK"
        return RENDERPLAIN.status(msg = msg)


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
