"""
base web.py file for displaying the ranked data
"""
import web
from lib.request_data import Data
from lib.parse_xml import Xml

URLS = (
    '/', 'Index',
    '/import', 'Import'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')

class Index(object):       # pylint: disable=too-few-public-methods
    @staticmethod
    def GET():             # pylint: disable=invalid-name
        """ GET handler for index route """
        dataParser = Data('http://localhost:8081/sample.xml')
        xmlData = dataParser.read()

        xmlParser = Xml()
        parsedData = Xml.parse(xmlData)

        pagedata = parsedData

        return RENDER.index(pagedata = pagedata)

class Import(object):
    @staticmethod
    def GET():
        dataParser = Data('http://localhost:8081/sample.xml')
        xmlData = dataParser.read()

        xmlParser = Xml()
        parsedData = Xml.parse(xmlData)

        pagedata = parsedData 
        # rank / store the data
        
        msg = "Status - OK"
        return RENDER.status(msg = msg)


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
