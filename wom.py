# -*- coding:utf-8 -*-
import sys
import cgi
import urllib
import webapp2
import random
import glob, os
import re

from google.appengine.api import users
from google.appengine.ext import ndb

#################################### MACRO ####################################
DEFAULT = "hello"
DATA_FILE = "data_s.txt"
#data.txt의 마지막 줄에는 내용 없는 엔터가 필요하다. 마지막 줄 끝에 \n 이 입력되어야 하기 때문에.


#################################### HTML ####################################
MAIN_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
    </head>

    <body>
        <div align = "center", padding-top: 50px>
            <form method="get" action="/findData">
                <div>
                    <input type="text" size="100" name="searchingWord">
                    <input type="submit" value="searchInDB">
                </div>
            </form>

            <form method="get" action="/delData">
                <div>
                    <input type = "submit" value="deleteDB">
                </div>
            </form>

            <form method="get" action="/fillData">
                <div>
                    <input type = "submit" value="FillDB">
                </div>
            </form>


        </div>
    </body>
</html>
"""

DEL_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" >

    </head>

    <body>
        <form method="GET" action="/">
            <div id = "demo2"><input type='submit' value='RETURN'></div>
        </form>
    </body>
</html>
"""

#################################### NDB CLASS ####################################
class WOM(ndb.Model):
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    language = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


#################################### PAGES ####################################
class MainPage(webapp2.RequestHandler):
    # print (sys.getdefaultencoding())
    def get(self):
        self.response.out.write(MAIN_PAGE_HTML)

class DelDB(webapp2.RequestHandler):
    def get(self):
            clearExistingDB()

class FillDB(webapp2.RequestHandler):
    def get(self):
        readFileToNdb()

class FindDB(webapp2.RequestHandler):
    def get(self):
        toFindstrLists = []
        #os.system('say wait')
        #print sys.platform
        imgPrinted = False
        toFindstr = ' '
        numOfmatch = 0
        keys = makeKeyList()
        #print keys
        toFind = self.request.get('searchingWord') #unicode
        toFindstr = toFind.encode('utf-8')
        toFindstrList = toFindstr.split(' ')
        for element in toFindstrList: #make a list that space attached to each end of word.
            toFindstrLists.append(element + " ")
        print ("toFindstrLists: %s" % toFindstrLists)
        resultSentence = " "

        for word in toFindstrLists: #split by space
            print ("\nFinding word: %s" % word)

            numOfmatchInWord = 0;

            for key in keys:
                print ("key: %s" % key)
                if isKorean(word) :
                    print("isKorean: %s" % isKorean(word))
                    if word.find(key) is not -1: #something matched in KOREAN
                        print("Matched in KOREAN!")
                        womquery = WOM.query(WOM.language == "KOR", WOM.keyword == key)
                        queryReturn = womquery.fetch(1)
                        print queryReturn
                        resultContentList = queryReturn[0].content.split(' _ ')
                        randomResult = resultContentList[random.randint(0, len(resultContentList)-1)]
                        randomResultStr = randomResult.encode('utf-8')
                        print ("content_K: %s" % randomResultStr)
                        #toFindstr = toFindstr.replace(key, randomResultStr)
                        resultSentence = resultSentence + word.replace(key, randomResultStr)
                        #resultSentence = resultSentence + " " + randomResultStr
                        print ("resultSentence", resultSentence)

                        numOfmatchInWord = numOfmatchInWord + 1
                        numOfmatch = numOfmatch + 1
                        break

                else : # ENGLISH word
                    if word.find(key + " ") is not -1: #something matched in ENGLISH
                        print("Matched in ENGLISH!")
                        womquery = WOM.query(WOM.language == "ENG", WOM.keyword == key)
                        queryReturn = womquery.fetch(1)
                        resultContentList = queryReturn[0].content.split(' _ ')
                        randomResult = resultContentList[random.randint(0, len(resultContentList)-1)]
                        randomResultStr = randomResult.encode('utf-8')
                        print ("content_E: %s" % randomResultStr)
                        #toFindstr = toFindstr.replace(key, randomResultStr)
                        # resultSentence = resultSentence + toFindstr.replace(key, randomResultStr)
                        resultSentence = resultSentence + " " + randomResultStr
                        print ("resultSentence", resultSentence)

                        numOfmatchInWord = numOfmatchInWord + 1
                        numOfmatch = numOfmatch + 1
                        break

            if numOfmatchInWord == 0 :
                print("Nothing matched in one DB loop with %s" % word)
                resultSentence = resultSentence + " " + word

        #print numOfmatch
        if numOfmatch :
            #self.response.write(toFindstr)
            self.response.write(resultSentence)
        else :
            print ("Nothing matched at all!\n")
            if imgPrinted is False : #준비된 이미지를 랜덤하게 선택해서 보여준다.
                #print ("nothing matched!")
                numOfImgs = getFileNum('img', 'png')
                #print numOfImgs
                ranImgNum = random.randint(1, numOfImgs)
                self.response.write('<img src=/img/' + str(ranImgNum) + '.png />')
                imgPrinted = True



#################################### FUNCTIONS ####################################
def makeKey(wordToTrans = DEFAULT):
    return ndb.Key("Words", wordToTrans)

def clearExistingDB():
    allwomqueries = WOM.query().fetch(9999, keys_only = True)
    #'_multi' 함수의 인자인 keys 를 만들기 위해서는 keys_only 옵션을 이용해서 entity가 아니라 key만 return 되도록 해야 한다.
    ndb.delete_multi(allwomqueries)
    ndb.get_context().clear_cache()

def readFileToNdb():
    key_list = []
    f = open(DATA_FILE, 'r')
    lines = f.readlines()
    for line in lines:
        #print type(line)
        tline = line.split(" : ") #: 으로 나누는 것과 ' : '으로 나누는 것은 dic이 되었을 때 결과값이 다르다.
        key = tline[0]
        #print key
        escapeNvalue = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
        #print escapeNvalue

        if isKorean(key) :
            wom = WOM(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.language = "KOR"
            wom.put()

        else :
            wom = WOM(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.language = "ENG"
            wom.put()
    f.close()

def isKorean(word):
    return bool(re.search(r'(([\x7f-\xfe])+)', word))

def makeKeyList():
    womquery = WOM.query().order(-WOM.keyword)
    key_list = []
    for wom in womquery :
        key = wom.keyword.encode('utf-8')
        #print key
        key_list.append(key) # make key list
    return key_list

def getFileNum(targetFolder, extension):
    listOfFiles = glob.glob(targetFolder + '/*.' + extension)
    return len(listOfFiles)







application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/delData', DelDB),
    ('/fillData', FillDB),
    ('/findData', FindDB)
    #('/del', DelDB)
    ], debug=True)