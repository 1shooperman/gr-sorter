import web

urls = (
    '/', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base='layout')

class Index(object):
    def GET(self):
        return render.index()


if __name__ == '__main__': # pragma: no cover
    app.run()              # pragma: no cover
