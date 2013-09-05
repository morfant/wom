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
        dicts[tline[0]] = tline[1][:(len(tline[1]) - 1)] #마지막 문자인 '\n'을 제거한다.
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
            sentence = sentence.replace(key, dicts[key])
    print sentence
    return sentence

def translate2(sentence, dicts): #not find(), just replace() directly.
    keys = dicts.keys()
    for key in keys:
        sentence = sentence.replace(key, dicts[key])
    print sentence
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
    """
    kkkk = readFileToDic(sys.argv[1]).keys()
    print kkkk
    for k in kkkk:
        print sampleText.find(k)
        """
    print("1: %s" % translate(sys.argv[2], readFileToDic(sys.argv[1])))
    print("2: %s" % translate2(sys.argv[2], readFileToDic(sys.argv[1])))