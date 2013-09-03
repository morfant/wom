# -*- coding:utf-8 -*-
import sys
import cgi
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


MAIN_PAGE_HTML = """\
<html>
	<body>

        keyword:
        <div><input type="text" size="100" name="userInput1"></div>
        <div><input type='submit' value='input'></div>
		<form method="post">
        content:
        <div><input type="text" size="100" name="userInput2"></div>
        <div><input type='submit' value='input'></div>
		</form>
	</body>
</html>
"""
DEFAULT = "hello"

def makeKey(wordToTrans = DEFAULT):
	return ndb.Key("Words", wordToTrans)

class WOM(ndb.Model):
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    
    print (sys.getdefaultencoding())

    def get(self):
        print (u'안녕씹'.encode('utf-8'))
        self.response.write(MAIN_PAGE_HTML)

        wordToTrans = self.request.get('userInput', DEFAULT)

        print("1: %s" % wordToTrans)

        transQuery = WOM.query(
            ancestor=makeKey(wordToTrans)).order(-WOM.date)
        transedWords = transQuery.fetch(10)

        for transedWord in transedWords:
            if transedWord.content:
                self.response.write('<b>%s</b>' % transedWord.content)

    def post(self):
        userInputVal = self.request.get(u'userInput2', DEFAULT)
        print("userInputVal: %s %s %s" % (userInputVal, type(userInputVal), unicode(userInputVal,'utf-8')))
        wom = WOM(parent=makeKey(unicode(userInputVal,'utf-8')))
        wom.content = self.request.get('userInput2')
        wom.put()
        self.response.write('<b>%s</b> puted.' % wom.content)

        self.response.write('<b>%s</b> list.' % wom)



class SecondPage(webapp2.RequestHandler):
    
    def post(self):

        wordToTrans = self.request.get('userInput', DEFAULT)
        print("2: %s" % wordToTrans)
        print (wordToTrans.encode('utf-8'))
        wom = WOM(parent=makeKey(wordToTrans))
        wom.keyword = self.request.get('userInput1')
        wom.content = self.request.get('userInput2')
        wom.put()

        transQuery = WOM.query(
            ancestor=makeKey(wordToTrans)).order(-WOM.date)

        transedWords = transQuery.fetch(10)
        print transedWords        
        for transedWord in transedWords:
            if transedWord.content:
                self.response.write('<b>%s</b>' % transedWord.content)




application = webapp2.WSGIApplication([
	('/', MainPage),
	('/test', SecondPage),
	], debug=True)