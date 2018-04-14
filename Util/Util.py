# -*- coding: UTF-8 -*-
'''
@author: andyh
'''
import datetime
import time
import os

def getDataPath(path=""):
    return os.path.abspath('..')+os.sep+"Data"+os.sep+path
def getDateInStr():
    lastday = datetime.datetime.now().day
    date = str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month) +"-"+str(lastday)
    return date