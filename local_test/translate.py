# -*- coding:utf-8 -*-
import sys
import random

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
        escapeNvalue = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
        if tline[0] in dicts:
            #print "1"
            dicts[tline[0]].append(escapeNvalue)
            #print dicts
        else:
            #print "2"
            dicts[tline[0]] = [escapeNvalue]
            #print dicts
        #print(line)
    #keys = dicts.keys()
    #contents = dicts.values()
    #print dicts
    #print keys
    #print contents
    return dicts

def translate(sentence, dicts): #not find(), just replace() directly.
    keys = dicts.keys()
    for key in keys:
        if len(dicts[key]) > 1:
            randnum = random.randint(0, (len(dicts[key]) - 1))
            sentence = sentence.replace(key, dicts[key][randnum])
    #print sentence
    return sentence

def makeArgvToList():
    args = sys.argv
    if len(args) > 1:
        for i in range(1, len(args)):
            argList.append(sys.argv[i])
            print sys.argv[i]

        print argList
        return argList

if __name__ == '__main__':
    #print sampleText
    #readFileToDic(sys.argv[1])
    """
    kkkk = readFileToDic(sys.argv[1]).keys()
    print kkkk
    for k in kkkk:
        print sampleText.find(k)
        """
    print("%s" % translate(sys.argv[2], readFileToDic(sys.argv[1])))
