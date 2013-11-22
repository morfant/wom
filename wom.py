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

        <style type="text/css">
            body {margin-top: 50px;}
        </style>

    </head>

    <body>
        <div align="center">
            <form method="get" action="/findData">
                <div>
                    <input type="text" size="100" name="searchingWord">
                    <input type="submit" value="Translate!">
                </div>
            </form>

            <form method="get" action="/delData">
                <div>
                    <input type="submit" value="deleteDB">
                </div>
            </form>

            <form method="get" action="/fillData">
                <div>
                    <input type="submit" value="FillDB">
                </div>
            </form>
        </div>
    </body>
</html>
"""

FIND_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    <style type="text/css">
        body {margin-top: 50px;}
    </style>

    </head>
    <body>
        <div align="center">
            <form method="get" action="/">
                <div style="margin-top: 30px">
                    <input type="submit" value="Back">
                </div>
            </form>
        </div>
    </body>
</html>
"""


#################################### NDB CLASS ####################################
class WOM(ndb.Model) :
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class WOM_ENG(ndb.Model) :
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


#################################### PAGES ####################################
class MainPage(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(MAIN_PAGE_HTML)

class DelDB(webapp2.RequestHandler) :
    def get(self) :
        clearExistingDB()
        self.response.write("DB is deleted.")

class FillDB(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb()
        self.response.write("DB is filled.")

class FindDB(webapp2.RequestHandler) :
    def get(self) :
        toFindstrLists = []
        #os.system('say wait')
        #print sys.platform
        imgPrinted = False
        toFindstr = ' '
        numOfmatch = 0
        keys = makeKeyList()
        keys_ENG = makeKeyList_ENG()
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

            if isKorean(word) :
                for key in keys :
                    print ("key: %s" % key)
                    print("isKorean: %s" % isKorean(word))
                    if word.find(key) is not -1: #something matched in KOREAN
                        print("Matched in KOREAN!")
                        randomResultStr = randDBOut(WOM, key)
                        print ("content_K: %s" % randomResultStr)
                        resultSentence = resultSentence + word.replace(key, randomResultStr)
                        print ("resultSentence", resultSentence)

                        numOfmatchInWord = numOfmatchInWord + 1
                        numOfmatch = numOfmatch + 1
                        break

            else :
                for key in keys_ENG :
                    if word.find(key + " ") is not -1: #something matched in ENGLISH
                        print("Matched in ENGLISH!")
                        randomResultStr = randDBOut(WOM_ENG, key)
                        print ("content_E: %s" % randomResultStr)
                        resultSentence = resultSentence + " " + randomResultStr
                        print ("resultSentence", resultSentence)

                        numOfmatchInWord = numOfmatchInWord + 1
                        numOfmatch = numOfmatch + 1
                        break

            if numOfmatchInWord == 0 :
                print("Nothing matched in one DB loop with %s" % word)
                resultSentence = resultSentence + " " + word

        if numOfmatch :
            self.response.write('<div align = "center", padding-top: 50px>' + resultSentence + '</div>')
        else :
            print ("Nothing matched at all!\n")
            if coin() == 1 : #random DB out
                if coin() == 1 : #for korean
                    randomKeyIdx = random.randint(1, len(keys) - 1)
                    resultSentence = randDBOut(WOM, keys[randomKeyIdx])
                    self.response.write('<div align = "center", padding-top: 50px>' + resultSentence + '</div>')

                else : #for Eng
                    randomKeyIdx = random.randint(1, len(keys_ENG) - 1)
                    resultSentence = randDBOut(WOM_ENG, keys_ENG[randomKeyIdx])
                    self.response.write('<div align = "center", padding-top: 50px>' + resultSentence + '</div>')

            else : # random Img out
                if imgPrinted is False : #준비된 이미지를 랜덤하게 선택해서 보여준다.
                    numOfImgs = getFileNum('img', 'png')
                    ranImgNum = random.randint(1, numOfImgs)
                    self.response.write('<div align = "center", padding-top: 100px>\
                        <img src=/img/' + str(ranImgNum) + '.png height = "400" width = "400"/></div>')
                    imgPrinted = True

        self.response.out.write(FIND_PAGE_HTML)




#################################### FUNCTIONS ####################################
def randDBOut(dataBase, matchingWord) :
    womquery = dataBase.query(dataBase.keyword == matchingWord)
    queryReturn = womquery.fetch(1)
    resultContentList = queryReturn[0].content.split(' _ ')
    randomResult = resultContentList[random.randint(0, len(resultContentList) - 1)]
    randomResultStr = randomResult.encode('utf-8')
    return randomResultStr

def coin() :
    return random.randint(1, 2)

def makeKey(wordToTrans = DEFAULT) :
    return ndb.Key("Words", wordToTrans)

def clearExistingDB() :
    allwomqueries = WOM.query().fetch(9999, keys_only = True)
    allwomqueries_ENG = WOM_ENG.query().fetch(9999, keys_only = True)
    #'_multi' 함수의 인자인 keys 를 만들기 위해서는 keys_only 옵션을 이용해서 entity가 아니라 key만 return 되도록 해야 한다.
    ndb.delete_multi(allwomqueries)
    ndb.delete_multi(allwomqueries_ENG)
    ndb.get_context().clear_cache()


def readFileToNdb() :
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
            wom.put()

        else :
            wom = WOM_ENG(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.put()
    f.close()


#정규표현식을 이용하여 한글이 포함되어 있는지를 판단한다.
def isKorean(word) :
    return bool(re.search(r'(([\x7f-\xfe])+)', word))

#긴 단어부터, 뒷 철자부터 정열된 keyList 를 만든다.
def makeKeyList() :
    womquery = WOM.query().order(-WOM.keyword)
    key_list = []
    for wom in womquery :
        key = wom.keyword.encode('utf-8')
        #print key
        key_list.append(key) # make key list
    return key_list

def makeKeyList_ENG() :
    womquery = WOM_ENG.query().order(-WOM_ENG.keyword)
    key_list = []
    for wom in womquery :
        key = wom.keyword.encode('utf-8')
        #print key
        key_list.append(key) # make key list
    return key_list

#targetFolder에 들어있는 특정 확장자 파일의 갯수를 돌려준다.
def getFileNum(targetFolder, extension) :
    listOfFiles = glob.glob(targetFolder + '/*.' + extension)
    return len(listOfFiles)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/delData', DelDB),
    ('/fillData', FillDB),
    ('/findData', FindDB)
    #('/del', DelDB)
    ], debug=True)