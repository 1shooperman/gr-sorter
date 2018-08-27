"""
base web.py file for displaying the ranked data
"""
import web

URLS = (
    '/', 'Index'
)

APP = web.application(URLS, globals())

RENDER = web.template.render('templates/', base='layout')

class Index(object):       # pylint: disable=too-few-public-methods
    """ web.py handler class for index route """
    def GET(self):         # pylint: disable=invalid-name,no-self-use
        """ GET handler for index route """
        return RENDER.index()


if __name__ == '__main__': # pragma: no cover
    APP.run()              # pragma: no cover
