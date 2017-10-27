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
    headerDict = {'hierarchy':'SESS_ID,TIME,PRO_HIE,DEL_HIE,MET_HIE,FIELDS,NES_TYP,EVE_HIE',
                  'test':'SESS_ID,ABORT,SESS_DOC,EVENT_DURA,TIME,TEST_RES,TEST_DURA'}
    return headerDict[key_param]

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def getHierarchyDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('TriggeredAt' in dict_param) and ('Context2' in dict_param)):
        sessID      = dict_param['IDESessionUUID']
        tstamp_     = dict_param['TriggeredAt']
        context     = dict_param['Context2']
        if('TypeShape' in context):
            type_shape_dict = context['TypeShape']
            if(('PropertyHierarchies' in type_shape_dict) and ('Delegates' in type_shape_dict) and ('MethodHierarchies' in type_shape_dict) and
               ('Fields' in type_shape_dict) and ('NestedTypes' in type_shape_dict) and ('EventHierarchies' in type_shape_dict)):
                  prop_h_cnt     = len(type_shape_dict['PropertyHierarchies'])
                  dele_h_cnt     = len(type_shape_dict['Delegates'])
                  meth_h_cnt     = len(type_shape_dict['MethodHierarchies'])
                  field_cnt      = len(type_shape_dict['Fields'])
                  nested_typ_cnt = len(type_shape_dict['NestedTypes'])
                  event_h_cnt    = len(type_shape_dict['EventHierarchies'])

                  str2Write = str2Write + str(sessID) + ',' + str(tstamp_) + ',' +str(prop_h_cnt) + ',' + str(dele_h_cnt) + ',' + str(meth_h_cnt) + ',' +str(field_cnt) + ',' + str(nested_typ_cnt) + ',' + str(event_h_cnt) + ',' + '\n'


    return str2Write

def getSSTDataFromDict(dict_param):
    str2Write = ''
    return str2Write

def readJSONFileContent(json_path, key_to_see):
    str2Write = ''
    onlyfiles = [f_ for f_ in os.listdir(json_path) if isfile(join(json_path, f_))]
    full_path_files = [join(json_path, f_) for f_ in os.listdir(json_path) ]
    only_json_files = [f_ for f_ in full_path_files if '.json' in f_]
    str2Write = ''
    for json_file in only_json_files:
        with open(json_file) as json_data:
             d_ = json.load(json_data)
             if ('$type' in d_):
                 val2see = d_['$type'].lower()
                 if('edit' in val2see):
                    '''
                    get the data you need
                    '''
                    if key_to_see=='hierarchy':
                       strFromDict = getHierarchyDataFromDict(d_)
                    elif key_to_see=='sst':
                       strFromDict = getSSTDataFromDict(d_)
                    else:
                       strFromDict = ''
                       print 'KEY IS WRONG ... CHECK!'
                    str2Write = str2Write + strFromDict

    print '-'*50
    return str2Write

def get_all_data(dir_p, key2look_p, file_to_save):
    all_content = ''
    all_sub_dirs = [dir_ for dir_ in os.listdir(dir_p)]
    all_sub_dirs = [x_ for x_ in all_sub_dirs if '-' in x_]
    headerStr=getHeaderStr(key2look_p)
    for sub_dir in all_sub_dirs:
        fullPathToDir = dir_p + sub_dir
        onlyfiles = [f_ for f_ in os.listdir(fullPathToDir) if isfile(join(fullPathToDir, f_))]
        full_path_files = [join(fullPathToDir, f_) for f_ in os.listdir(fullPathToDir) ]
        only_zip_files = [f_ for f_ in full_path_files if '.zip' in f_]
        #print only_zip_files
        for zip_file in only_zip_files:
            print 'Processing:', zip_file
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            file_name=os.path.basename(zip_file)
            file_    = os.path.splitext(file_name)[0]
            dir2extract = fullPathToDir + '/' + file_ + '/'
            #print dir2extract
            zip_ref.extractall(dir2extract)
            zip_ref.close()
            indi_content  = readJSONFileContent(dir2extract, key2look_p)
            all_content = all_content + indi_content
            print '-'*50
            shutil.rmtree(dir2extract)
    all_content = headerStr + '\n' + all_content
    status_ = dumpContentIntoFile(all_content, file_to_save)
    print '-'*50
    print 'Dumped a file of {} bytes'.format(status_)
    print '-'*50

if __name__=='__main__':
   print "Started at:", giveTimeStamp()
   print '='*100
   ds_path   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/TEST/'
   # ds_path   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/Events-170301/'

   file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_EDIT_HIERARCHY_CONTENT.csv'
   key_to_look = 'hierarchy'

   get_all_data(ds_path, key_to_look, file2save)
   print "Ended at:", giveTimeStamp()
   print '='*100
