import glob
import os

def getFileNum(targetFolder, extension):
    listOfFiles = glob.glob(targetFolder + '/*.' + extension):
    return len(listOfFiles)