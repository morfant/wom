import cgi
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


MAIN_PAGE_HTML = """\
<html>
	<body>
		<form method="post">
		<div><input type="text" size="100" name="userInput"></div>
		</form>
	</body>
</html>
"""
DEFAULT = "hello"

def makeKey(wordToTrans = DEFAULT):
	return ndb.Key("Words", wordToTrans)

class WOM(ndb.Model):
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
		

class MainPage(webapp2.RequestHandler):
    
    def get(self):
		self.response.write(MAIN_PAGE_HTML)

		wordToTrans = self.request.get('userInput', DEFAULT)
		transQuery = WOM.query(
    		ancestor=makeKey(wordToTrans)).order(-WOM.date)
		transedWords = transQuery.fetch(10)

		for transedWord in transedWords:
			if transedWord.content:
				self.response.write('<b>%s</b>' % transedWord.content)

    def post(self):
        self.response.write("kkkkk")

class SecondPage(webapp2.RequestHandler):

	def get(self):
		user = users.get_current_user()

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello, Again!\n')

		if user:
			self.redirect(users.create_logout_url(self.request.uri))
		else:
			self.response.write("login please")

	def post(self):
		self.response.write('<html><body>You wrote: <pre>')
		self.response.write(cgi.escape(self.request.get('userInput')))
		self.response.write('</pre></body></html>')



application = webapp2.WSGIApplication([
	('/', MainPage),
	('/test', SecondPage),
	], debug=True)