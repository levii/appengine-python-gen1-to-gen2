import webapp2

from google.appengine.ext import ndb


class Structured(ndb.Model):
    kind = ndb.StringProperty()
    value = ndb.StringProperty()


class Book(ndb.Model):
    name = ndb.StringProperty()
    structured = ndb.StructuredProperty(Structured)
    created_at = ndb.DateTimeProperty(auto_now_add=True)


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
            structured=Structured(kind='This is Kind', value='This is value.')
        )
        book.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(book)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create', CreatePage)
], debug=True)
