'''
Akond Rahman
Oct 27, 2017
EXTRACT HIERARCHY AND SST DATA
'''

import os
from os.path import isfile, join
import zipfile
import json
from ijson import items
import shutil

def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def getHeaderStr(key_param):
    headerDict = {'build':'SESS_ID,SESS_DOC,EVENT_DURA,TIME,BUILD_RES,BUILD_DURA',
                  'edit':'SESS_ID,SESS_DOC,EVENT_DURA,TIME,CNG_SIZE,CNG_CNT',
                  'test':'SESS_ID,ABORT,SESS_DOC,EVENT_DURA,TIME,TEST_RES,TEST_DURA'}
    return headerDict[key_param]

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def getHierarchyDataFromDict(dict_param):
    str2Write = ''
    return str2Write
