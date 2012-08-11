import webapp2
from simplehandler import SimpleHandler

class MainPage(SimpleHandler):
	def get(self):
		self.render("index.html")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=False)