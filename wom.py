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
DATA_FILE = "data.txt"
DATA_FILE_1 = "data_1.txt"
DATA_FILE_2 = "data_2.txt"
DATA_FILE_3 = "data_3.txt"
DATA_FILE_4 = "data_4.txt"
#data.txt의 마지막 줄에는 내용 없는 엔터가 필요하다. 마지막 줄 끝에 \n 이 입력되어야 하기 때문에.


#################################### GLOBAL VARIABLE ####################################
keys = ""
keys_ENG = ""
korIdx = 0
engIdx = 0

class StaticKeys :
    keys = ""
    keys_ENG = ""

#################################### HTML ####################################
MAIN_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

        <style type="text/css">
            body {
                position: relative;
                top: 50px;
                }
            footer {
                position: fixed;
                right: 20px;
                bottom: 20px;
                font-size: 10px;
                line-height: 0.1;
                }
            p {
                font-size: 12px;
                }
        </style>

    </head>

    <body>
        <div>
            <form method="get" action="/findData">
                <div align="center">
                    <input type="text" size="100" name="searchingWord">
                </div>
                <div style="position: relative; top: 50px" align="center">
                    <input type="submit" value="번역 / Translate">
                </div>
            </form>
            <div style="position: relative; top: 200px" align="center">
                <p>
                한국어와 영어 입력이 가능합니다.
                <br>
                한국어 입력 시에는 한국어 결과가, 영어 입력시에는 영어 결과가 출력됩니다.
                <br>
                한국어와 영어를 함께 사용하는 경우에는 이미지가 출력 됩니다.
                </p>
                <p>
                KOREAN and ENGLISH are both available.
                <br>
                Entering words in each language makes different result(s);
                Entering words in KOREAN makes result(s) in KOREAN, and entering words in ENGLISH makes result(s) in ENGLISH.
                <br>
                If you enter words in KOREAN and ENGLISH at the same time, random image will be displayed.
                </p>

            </div>
        </div>
    </body>

    <footer>
        <div align="right">
            <p>TaewonKim </p>
            <p> & </p>
            <p>giy</p>
            <p>taewonnice@naver.com</p>
        </div>
    </footer>

</html>
"""

FIND_PAGE_HTML = """\
<!DOCTYPE html>
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >

    <style type="text/css">
        body {margin-top: 50px;}
        footer {
            position: fixed;
            right: 20px;
            bottom: 20px;
            font-size: 10px;
            line-height: 0.1;
            }
        p {
            font-size: 12px;
            }


    </style>

    </head>
    <body>
        <div align="center">
            <form method="get" action="/">
                <div style="margin-top: 30px">
                    <input type="submit" value="돌아가기 / Go back">
                </div>
            </form>
        </div>
    </body>

    <footer>
        <div align="right">
            <p>TaewonKim </p>
            <p> & </p>
            <p>giy</p>
            <p>giy.hands@gmail.com</p>
        </div>
    </footer>

</html>
"""

#################################### NDB CLASS ####################################
class WOM(ndb.Model) :
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    idx = ndb.IntegerProperty(indexed=True)

class WOM_ENG(ndb.Model) :
    keyword = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    idx = ndb.IntegerProperty(indexed=True)

#################################### PAGES ####################################
class MainPage(webapp2.RequestHandler) :
    # print (sys.getdefaultencoding())
    def get(self) :
        self.response.out.write(MAIN_PAGE_HTML)

class DelDB(webapp2.RequestHandler) :
    def get(self) :
        clearExistingDB()
        self.response.write("DB is deleted.")

class FillDB_ALL(webapp2.RequestHandler) :
    def get(self) :
        clearExistingDB()
        readAllDataFileToNdb()
        self.response.write("DB is filled.")

class FillDB_1(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(1)
        self.response.write("DB is filled with data_1.")

class FillDB_2(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(2)
        self.response.write("DB is filled with data_2.")

class FillDB_3(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(3)
        self.response.write("DB is filled with data_3.")

class FillDB_4(webapp2.RequestHandler) :
    def get(self) :
        readFileToNdb(4)
        self.response.write("DB is filled with data_4.")

class SetupDB(webapp2.RequestHandler) :
    def get(self) :
        global keys
        global keys_ENG

        # keys = makeKeyList()
        # keys_ENG = makeKeyList_ENG()
        # for key in keys :
        #     print ("key %s" % key)
        # for key in keys_ENG :
        #     print ("key_ENG %s" % key)


        StaticKeys.keys = makeKeyList()
        StaticKeys.keys_ENG = makeKeyList_ENG()

        print StaticKeys.keys
        print StaticKeys.keys_ENG


        self.response.write("DB is set.")


class FindDB(webapp2.RequestHandler) :
    def get(self) :
        global keys
        global keys_ENG
        lenOfKORWords = len(StaticKeys.keys)
        lenOfENGWords = len(StaticKeys.keys_ENG)
        toFindstrLists = []
        #os.system('say wait')
        #print sys.platform
        # imgPrinted = False
        toFindstr = ' '
        # numOfmatch = 0
        #print keys
        toFind = self.request.get('searchingWord') #unicode
        if toFind == "" :
            # print ("nothing is in.")
            randImgDisplay(self, 34)
        else :
            # if len(keys) == 0 :
            #     keys = makeKeyList()
            #     keys_ENG = makeKeyList_ENG()

            if lenOfKORWords == 0 :
                print ("len of KOR words is 0")
                StaticKeys.keys = makeKeyList()
                lenOfKORWords = len(StaticKeys.keys)
                print StaticKeys.keys
            if lenOfENGWords == 0 :
                print ("len of ENG words is 0")
                StaticKeys.keys_ENG = makeKeyList_ENG()
                lenOfENGWords = len(StaticKeys.keys_ENG)
                print StaticKeys.keys_ENG



            toFindstr = toFind.encode('utf-8')
            toFindstrList = toFindstr.split(' ')
            for element in toFindstrList: #make a list that space attached to each end of word.
                toFindstrLists.append(element + " ")
            # print ("toFindstrLists: %s" % toFindstrLists)
            resultSentence = " "

            isKoreanToListResult = isKoreanToList(toFindstrList)

            if isKoreanToListResult == 0 : #All kor words
                if isExactlyMatchToList(toFindstrList, StaticKeys.keys) :
                    for word in toFindstrList: #split by space
                        result = randDBOutInMatchingWord(WOM, word)
                        self.response.write('<div align = "center", padding-top: 50px>' \
                        + result + '</div>')
                else :
                    resultSentence = randDBOutInRandomWord(WOM, lenOfKORWords)
                    self.response.write('<div align = "center", padding-top: 50px>' \
                    + resultSentence + '</div>')

            elif isKoreanToListResult == 1 : #All eng words
                if isExactlyMatchToList(toFindstrList, StaticKeys.keys_ENG) :
                    for word in toFindstrList: #split by space
                        result = randDBOutInMatchingWord(WOM_ENG, word)
                        self.response.write('<div align = "center", padding-top: 50px>' \
                        + result + '</div>')
                else :
                    resultSentence = randDBOutInRandomWord(WOM_ENG, lenOfENGWords)
                    self.response.write('<div align = "center", padding-top: 50px>' \
                    + resultSentence + '</div>')

            elif isKoreanToListResult == 2 : #kor + eng
                randImgDisplay(self, 34)

            # else :
            #     if isExactlyMatchToList(toFindstrList, StaticKeys.keys) :
            #         for word in toFindstrList: #split by space
            #             # print ("\nFinding word: %s" % word)

            #             # numOfmatchInWord = 0;

            #             if isKorean(word) :
            #                 result = randDBOutInMatchingWord(WOM, word)
            #                 self.response.write('<div align = "center", padding-top: 50px>' \
            #                 + result + '</div>')

            #             else: #for eng
            #                 resultSentence = randDBOutInMatchingWord(WOM_ENG, word)
            #                 self.response.write('<div align = "center", padding-top: 50px>' \
            #                 + resultSentence + '</div>')
            #     else :
            #         if isKorean()

            #                     randomKeyIdx = random.randint(1, len(StaticKeys.keys) - 1)
            #                     resultSentence = randDBOutInMatchingWord(WOM, StaticKeys.keys[randomKeyIdx])
            #                     self.response.write('<div align = "center", padding-top: 50px>' \
            #                     + resultSentence + '</div>')                        
                            # # for key in keys :
                            # for key in StaticKeys.keys :
                            #     # print ("key: %s" % key)
                            #     # print("isKorean: %s" % isKorean(word))
                            #     if word.find(key) is not -1: #something matched in KOREAN
                            #         #print("Matched in KOREAN!")
                            #         randomResultStr = randDBOutInMatchingWord(WOM, key)
                            #         #print ("content_K: %s" % randomResultStr)
                            #         resultSentence = resultSentence + word.replace(key, randomResultStr)
                            #         #print ("resultSentence", resultSentence)

                            #         numOfmatchInWord = numOfmatchInWord + 1
                            #         numOfmatch = numOfmatch + 1
                            #         break

                        # else : #english word


                            # else:
                            #     randomKeyIdx = random.randint(1, len(StaticKeys.keys_ENG) - 1)
                            #     resultSentence = randDBOutInMatchingWord(WOM_ENG, StaticKeys.keys_ENG[randomKeyIdx])
                            #     self.response.write('<div align = "center", padding-top: 50px>' \
                            #     + resultSentence + '</div>')                        

                    # # for key in keys_ENG :
                    # for key in StaticKeys.keys_ENG :
                    #     if word.find(key + " ") is not -1: #something matched in ENGLISH
                    #         #print("Matched in ENGLISH!")
                    #         randomResultStr = randDBOutInMatchingWord(WOM_ENG, key)
                    #         #print ("content_E: %s" % randomResultStr)
                    #         resultSentence = resultSentence + " " + randomResultStr
                    #         #print ("resultSentence", resultSentence)

                    #         numOfmatchInWord = numOfmatchInWord + 1
                    #         numOfmatch = numOfmatch + 1
                    #         break

                # if numOfmatchInWord == 0 :
                #     #print("Nothing matched in one DB loop with %s" % word)
                #     resultSentence = resultSentence + " " + word

            # if numOfmatch :
            #     self.response.write('<div align = "center", padding-top: 50px>' + resultSentence + '</div>')
            # else :
            #     #print ("Nothing matched at all!\n")
            #     # if coin() == 1 and len(keys) != 0 and len(keys_ENG) != 0: #random DB out
            #     if coin() == 1 and len(StaticKeys.keys) != 0 and len(StaticKeys.keys_ENG) != 0: #random DB out
            #         #print ("situation 1\n")
            #         if isKorean(word) : #for KOR
            #             #print ("situation 1 - 1\n")
            #             # randomKeyIdx = random.randint(1, len(keys) - 1)
            #             # resultSentence = randDBOutInMatchingWord(WOM, keys[randomKeyIdx])
            #             randomKeyIdx = random.randint(1, len(StaticKeys.keys) - 1)
            #             resultSentence = randDBOutInMatchingWord(WOM, StaticKeys.keys[randomKeyIdx])
            #             self.response.write('<div align = "center", padding-top: 50px>' \
            #                 + resultSentence + '</div>')

            #         else : #for Eng
            #             #print ("situation 1 - 2\n")
            #             # randomKeyIdx = random.randint(1, len(keys_ENG) - 1)
            #             # resultSentence = randDBOutInMatchingWord(WOM_ENG, keys_ENG[randomKeyIdx])
            #             randomKeyIdx = random.randint(1, len(StaticKeys.keys_ENG) - 1)
            #             resultSentence = randDBOutInMatchingWord(WOM_ENG, StaticKeys.keys_ENG[randomKeyIdx])
            #             self.response.write('<div align = "center", padding-top: 50px>' \
            #                 + resultSentence + '</div>')

            #     else : # random Img out
            #         if imgPrinted is False : #준비된 이미지를 랜덤하게 선택해서 보여준다.
            #             #print ("situation 2\n")
            #             randImgDisplay(self, 34) #34 = max image number
            #             imgPrinted = True

        self.response.out.write(FIND_PAGE_HTML)




#################################### FUNCTIONS ####################################
def randImgDisplay(target, maxImgNum) :
    ranImgNum = random.randint(1, maxImgNum)
    target.response.out.write('<div align = "center", padding-top: 100px>\
        <img src=/img/' + str(ranImgNum) + '.png height = "400" width = "400"/></div>')


def isExactlyMatch(word, DBList) :
    print len(DBList)
    lenOfDB = len(DBList)
    for j in range(0, lenOfDB) :
        # print wordList[i]
        print j
        print DBList[j]
        if DBList[j] == word :
            print "Exactly same!!"
            return True
        else:
            if j == (lenOfDB - 1) :
                print "Not same!!"
                return False

def isExactlyMatchToList(wordList, DBList) :
    same = 0
    # print len(DBList)
    # print len(wordList)
    lenOfWordList = len(wordList)
    lenOfDB = len(DBList)
    for i in range(0, lenOfWordList) :
        for j in range(0, lenOfDB) :
            # print wordList[i]
            # print j
            # print DBList[j]
            if DBList[j] == wordList[i] :
                same = same + 1
                break
        print ("same : %s " % same)

    if same == lenOfWordList :
        print "Exactly same!!"
        return True
    else :
        print "Not same!!"
        return False


def randDBOutInRandomWord(dataBase, DBLength) :
    print ("DBLength : %s" % DBLength)
    randomIdx = random.randint(0, DBLength - 1)
    print ("randomIdx : %s" % randomIdx)
    womquery = dataBase.query(dataBase.idx == randomIdx)
    queryReturn = womquery.fetch(1)
    print queryReturn
    resultContentList = queryReturn[0].content.split(' _ ')
    print resultContentList
    randomResult = resultContentList[random.randint(0, len(resultContentList) - 1)]
    randomResultStr = randomResult.encode('utf-8')
    return randomResultStr


def randDBOutInMatchingWord(dataBase, matchingWord) :
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

def readFileToNdb(numOfDB) :
    global korIdx
    global engIdx
    
    if numOfDB == 1:
        f = open(DATA_FILE_1, 'r')
    elif numOfDB == 2:
        f = open(DATA_FILE_2, 'r')
    elif numOfDB == 3:
        f = open(DATA_FILE_3, 'r')
    elif numOfDB == 4:
        f = open(DATA_FILE_4, 'r')

    key_list = []
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
            wom.idx = korIdx
            wom.put()
            korIdx = korIdx + 1

        else :
            wom = WOM_ENG(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.idx = engIdx
            wom.put()
            engIdx = engIdx + 1
    f.close()

def readAllDataFileToNdb() :
    korIdx = 0
    engIdx = 0
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
            wom.idx = korIdx
            wom.put()
            korIdx = korIdx + 1


        else :
            wom = WOM_ENG(parent = makeKey(key))
            wom.keyword = key
            wom.content = escapeNvalue
            wom.idx = engIdx
            wom.put()
            engIdx = engIdx + 1
    f.close()


#정규표현식을 이용하여 한글이 포함되어 있는지를 판단한다.
def isKorean(word) :
    return bool(re.search(r'(([\x7f-\xfe])+)', word))

def isKoreanToList(wordList) :
    numOfWord = len(wordList)
    print numOfWord
    kor = 0
    eng = 0
    if numOfWord != 0 :
        for word in wordList :
            if isKorean(word) :
                kor = kor + 1
                # print ("kor : %s " % kor)
            else :
                eng = eng + 1
                print ("eng : %s " % eng)

        if eng == 0 :
            print "The wordlist is korean"
            return 0 #All kor

        elif kor == 0 :
            print "The wordlist is ENGLISH"
            return 1 #All eng

        else :
            print "The wordlist is korean + ENGLISH"
            return 2 #kor + eng



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
#Not using at online version yet. 
def getFileNum(targetFolder, extension) :
    listOfFiles = glob.glob(targetFolder + '/*.' + extension)
    return len(listOfFiles)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/delData', DelDB),
    ('/fillData', FillDB_ALL),
    ('/fillData_1', FillDB_1),
    ('/fillData_2', FillDB_2),
    ('/fillData_3', FillDB_3),
    ('/fillData_4', FillDB_4),
    ('/setData', SetupDB),
    ('/findData', FindDB)
    #('/del', DelDB)
    ], debug=True)