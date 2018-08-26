import web

urls = (
    '/', 'Index'
)

render = web.template.render('templates/', base='layout')

class Index(object):
    def GET(self):
        return render.index()


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
