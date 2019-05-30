import webapp2

from google.appengine.ext import ndb


class Book(ndb.Model):
    name = ndb.StringProperty()
    pass


class MainPage(webapp2.RequestHandler):
    def get(self):
        query = Book.query()

        results = [book for book in query.fetch()]

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Books:\n\n')
        self.response.write('\n'.join([str(book) for book in results]))


class CreatePage(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name', default_value='sample book (python27)')
        book = Book(
            name=name,
        )
        book.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(book)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create', CreatePage)
], debug=True)
