# -*- coding:utf-8 -*-
import sys
import cgi
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


MAIN_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    </head>

    <body>
        <form method="post" action="/test">
        keyword:
        <div id = "demo"><input type="text" size="100" name="userInput1"></div>
        content:
        <div id = "demo3"><input type="text" size="100" name="userInput2"></div>
        <div id = "demo2"><input type='submit' value='input'></div>
        </form>
    </body>
</html>
"""

SECOND_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    </head>

    <body>
        <form method="GET" action="/">
            <div id = "demo2"><input type='submit' value='RETURN'></div>
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

        #print("keyword : %s" % self.request.get('userInput1')) #한글을 입력하면 문제를 일으킨다
        #print("content : %s" % self.request.get('userInput2'))
        wordToTrans = self.request.get('userInput1', DEFAULT)
        #print("2: %s" % wordToTrans)
        #print (wordToTrans.encode('utf-8'))
        wom = WOM(parent=makeKey(wordToTrans))
        wom.keyword = self.request.get('userInput1')
        wom.content = self.request.get('userInput2')
        wom.put()

        #transQuery = WOM.query(ancestor=makeKey(wordToTrans)).order(-WOM.date)
        transQuery = WOM.query().order(-WOM.date)
        transedWords = transQuery.fetch(10)

        #print transedWords        
        for transedWord in transedWords:
            if transedWord.content:
                self.response.write('keyword: %s / content: %s <br>' % (transedWord.keyword, transedWord.content))

        self.response.write(SECOND_PAGE_HTML)
        self.response.write('<img src=/img/test.png />')



application = webapp2.WSGIApplication([
	('/', MainPage),
	('/test', SecondPage),
	], debug=True)