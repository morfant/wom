# -*- coding:utf-8 -*-
import sys

argList = []

def trans(sentence, word="hi", chWord="안녕"):
    if type(sentence) == list:
        print "this is a list"
        for i in range(0, len(sentence)):
            print sentence[i]
            pos = sentence[i].find(word)
            print pos
            if pos != -1:
                sentence[i].replace(word, "babo")
            else:
                print "Nothing matched!"



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
    trans(makeArgvToList())