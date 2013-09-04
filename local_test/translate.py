# -*- coding:utf-8 -*-
import sys

argList = []
dicts = {}
keys = []
contents = []
isMatch = {}

sampleText = "너모씨key 안녕, hi루"

def readFileToDic(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        #print type(line)
        tline = line.split(" : ") #: 으로 나누는 것과 ' : '으로 나누는 것은 dic이 되었을 때 결과값이 다르다.
        dicts[tline[0]] = tline[1]
        #print(line)
    keys = dicts.keys()
    contents = dicts.values()
    print dicts
    #print keys
    #print contents
    return dicts

#def translate(sentence=sampleText, keys=keys, contents=contents):
def translate(sentence, dicts):
    keys = dicts.keys()
    #print sentence
    for key in keys:
        if sentence.find(key) == -1:
            isMatch[key] = False
            print "no match"
        else:
            print "match"
            isMatch[key] = True

    print isMatch

    for key in keys:
        if isMatch[key] == True:
            sentence.replace(key, dicts[key])
    print sentence

def trans(sentence, word="hi", chWord="안녕"):
    if type(sentence) == list:
        print "this is a list"
        for i in range(0, len(sentence)):
            #print sentence[i]
            pos = sentence[i].find(word)
            #print pos
            if pos != -1:
                sentence[i] = sentence[i].replace(word, chWord)
                #print sentence[i]
            else:
                print "Nothing matched!"

        for i in range(0, len(sentence)):
            print ("sentence[%d] : %s" % (i, sentence[i]))
    else:
        print "this is not a list"


def makeArgvToList():
    args = sys.argv
    if len(args) > 1:
        for i in range(1, len(args)):
            argList.append(sys.argv[i])
            print sys.argv[i]

        print argList
        return argList

if __name__ == '__main__':
    print sampleText
    """
    kkkk = readFileToDic(sys.argv[1]).keys()
    print kkkk
    for k in kkkk:
        print sampleText.find(k)
        """
    translate(sampleText, readFileToDic(sys.argv[1]))