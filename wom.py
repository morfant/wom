# -*- coding:utf-8 -*-
import sys
import cgi
import urllib
import webapp2
import random

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

        <form method="get" action="/data">
            <div>
                <input type="submit" value="printDB">
            </div>
        </form>

        <form method="get" action="/find">
            <div>
                <input type="text" size="100" name="searchingWord">
                <input type="submit" value="searchInDB">
            </div>
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

DATA_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    </head>

    <body>
        <form method="GET" action="/">
            <div><input type='submit' value='RETURN'></div>
        </form>
        <form method="GET" action="/data">
            <div><input type='submit' value='CLEARDB'></div>
        </form>
    </body>
</html>
"""

DEFAULT = "hello"
DATA_FLIE = "data.txt"

def makeKey(wordToTrans = DEFAULT):
    return ndb.Key("Words", wordToTrans)

class WOM(ndb.Model):
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    
    print (sys.getdefaultencoding())

    def get(self):
        clearExistingDB()
        self.response.out.write(MAIN_PAGE_HTML)
        readFileToNdb()

    def post(self):
        userInputVal = self.request.get(u'userInput2', DEFAULT)
        print("userInputVal: %s %s %s" % (userInputVal, type(userInputVal), unicode(userInputVal,'utf-8')))
        wom = WOM(parent=makeKey(unicode(userInputVal,'utf-8')))
        wom.content = self.request.get('userInput2')
        wom.put()
        self.response.write('<b>%s</b> puted.' % wom.content)

        self.response.write('<b>%s</b> list.' % wom)

"""
    def readFileToNdb(filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            #print type(line)
            tline = line.split(" : ") #: 으로 나누는 것과 ' : '으로 나누는 것은 dic이 되었을 때 결과값이 다르다.
            key = tline[0]
            escapeNvalue = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
            
            wom = WOM(parent=makeKey(key))
            wom.keyword = self.request.get(key)
            wom.content = wom.content.append(self.request.get(escapeNvalue))
            wom.put()
            """

def clearExistingDB():
    allwomqueries = WOM.query().fetch(9999, keys_only=True)
    #'_multi' 함수의 인자인 keys 를 만들기 위해서는 keys_only 옵션을 이용해서 entity가 아니라 key만 return 되도록 해야 한다.
    ndb.delete_multi(allwomqueries)
    ndb.get_context().clear_cache()

def readFileToNdb():
    f = open(DATA_FLIE, 'r')
    lines = f.readlines()
    for line in lines:
        #print type(line)
        tline = line.split(" : ") #: 으로 나누는 것과 ' : '으로 나누는 것은 dic이 되었을 때 결과값이 다르다.
        key = tline[0]
        print key
        escapeNvalue = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
        print escapeNvalue

        wom = WOM(parent=makeKey(key))
        wom.keyword = key
        wom.content = escapeNvalue
        wom.put()
    f.close()


class FillDB(webapp2.RequestHandler):
    def get(self):
        readFileToNdb()


class FindDB(webapp2.RequestHandler):
    def get(self):
        tempvaluelist = []
        keylist = []
        toFind = self.request.get('searchingWord')
        womquery = WOM.query(WOM.keyword == toFind)
        queryReturns = womquery.fetch(10)

        #print transedWords        
        self.response.write('keyword / content<br>')
        for queryReturn in queryReturns:
            if queryReturn.content:
                tempvaluelist.append(queryReturn.content)
                keylist.append(queryReturn.keyword)

        self.response.write(' %s / %s <br>' % (queryReturn.keyword, tempvaluelist[random.randint(0, len(tempvaluelist)-1)]))




class ViewDB(webapp2.RequestHandler):
    def get(self):
        womquery = WOM.query().order(-WOM.date)
        queryReturns = womquery.fetch(20)

        #print transedWords        
        self.response.write('keyword / content<br>')
        for queryReturn in queryReturns:
            if queryReturn.content:
                self.response.write(' %s / %s / %s <br>' % \
                    (queryReturn.keyword, queryReturn.content, queryReturn.date))

        self.response.write(DATA_PAGE_HTML)


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
    ('/data', ViewDB),
    ('/find', FindDB)
    #('/del', DelDB)
	], debug=True)