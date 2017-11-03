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
import numpy as np
import math

def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def getHeaderStr(key_param):
    headerDict = {'hierarchy':'SESS_ID,TIME,PRO_HIE,DEL_HIE,MET_HIE,FIELDS,NES_TYP,EVE_HIE',
                  'sst':'SESS_ID,TIME,MET_CNT,DEL_CNT,PRO_CNT,FIE_CNT,EVE_CNT,AVG_MET_DIF,MED_MET_DIF,AVG_MET_EFF,MED_MET_EFF,AVG_MET_VOC,MED_MET_VOC,AVG_MET_LEN,MED_MET_LEN,AVG_PAR_CNT,MED_PAR_CNT,UNI_MET_CNT'}
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

def getMethInfo(meth_param):
   name_holder, param_holder = [], []
   if ('Body' in meth_param):
     meth_content_list=meth_param['Body']
     for meth_content in meth_content_list:
       if ('Expression' in meth_content):
           express_dict = meth_content['Expression']
           if(('MethodName' in express_dict) and ('Parameters' in express_dict)):
              meth_name, meth_param_cnt =   express_dict['MethodName'], len(express_dict['Parameters'])
              name_holder.append(meth_name)
              param_holder.append(meth_param_cnt)
   #print name_holder, param_holder
   return name_holder, param_holder

def getOperaInfo(meth_body):
   left_operand_list, right_operand_list, operator_list = [], [], []
   if ('Body' in meth_body):
     meth_content_list=meth_body['Body']
     for meth_content in meth_content_list:
       if (('$type' in meth_content) and ('Expression' in meth_content)):
           key2see = meth_content['$type'].lower()
           if('assignment' in key2see):
              expression_content =   meth_content['Expression']
              if(('Operator' in expression_content) and ('LeftOperand' in expression_content) and ('RightOperand' in expression_content)):
                  operator_list.append(expression_content['Operator'])
                  if('Reference' in expression_content['LeftOperand']):
                     if ('Identifier' in expression_content['LeftOperand']['Reference']):
                        left_operand_list.append(expression_content['LeftOperand']['Reference']['Identifier'])
                  if('Reference' in expression_content['RightOperand']):
                     if ('Identifier' in expression_content['RightOperand']['Reference']):
                        right_operand_list.append(expression_content['RightOperand']['Reference']['Identifier'])

                        #print left_operand_list, right_operand_list, operator_list
   return left_operand_list, right_operand_list, operator_list

def getSSTDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('TriggeredAt' in dict_param) and ('Context2' in dict_param)):
        sessID      = dict_param['IDESessionUUID']
        tstamp_     = dict_param['TriggeredAt']
        cont_dict   = dict_param['Context2']
        if('SST' in cont_dict):
            sst_dict =cont_dict['SST']
            #print sst_dict
            if(('Methods' in sst_dict) and ('Delegates' in sst_dict) and ('Properties' in sst_dict) and ('Fields' in sst_dict) and ('Events' in sst_dict)):
               meth_ls, dele_ls, prop_ls, fiel_ls, even_ls = sst_dict['Methods'], sst_dict['Delegates'], sst_dict['Properties'], sst_dict['Fields'], sst_dict['Events']
               meth_cnt = len(meth_ls)
               dele_cnt = len(dele_ls)
               prop_cnt = len(prop_ls)
               fiel_cnt = len(fiel_ls)
               even_cnt = len(even_ls)
               ### to get averga, median Halstead's metrics
               difficulty, effort, vocabulary, leng, meth_param_cnt =[], [], [], [], []
               ### initialization
               avg_diff, med_diff, avg_eff, med_eff       = 0, 0, 0, 0
               avg_voc, med_voc, avg_len, med_len         = 0, 0 , 0, 0
               avg_param_cnt, med_param_cnt, uni_meth_cnt = 0, 0, 0
               for meth_body_ in fiel_ls:           ### THIS WILL CHANGE FOR METHODS, DELEGATES, PROPETIES, FIELDS
                   ###1 . stuff for healstead
                   left_operand_list, right_operand_list, operator_list  = getOperaInfo(meth_body_)
                   operand_cnt= len(left_operand_list) + len(right_operand_list)
                   operator_cnt = len(operator_list)
                   uni_operator_cnt = len(np.unique(operator_list))
                   uni_operand_cnt  = len(np.unique(left_operand_list)) + len(np.unique(right_operand_list))
                   ### MCCabe's Calculcation: reff: https://en.wikipedia.org/wiki/Halstead_complexity_measures
                   if((operand_cnt > 0) and (uni_operator_cnt > 0) and (uni_operand_cnt > 0)):
                      meth_vocabulary  = uni_operator_cnt + uni_operator_cnt
                      meth_len         = operand_cnt + operator_cnt
                      meth_vol         = meth_len * math.log(meth_vocabulary, 2)
                      meth_diff        = (uni_operator_cnt / 2) * (operand_cnt / uni_operand_cnt)
                      meth_effo        = meth_vol * meth_diff
                      ### DO APPEND : difficulty, effort, volcabulary
                      difficulty.append(meth_diff)
                      effort.append(meth_effo)
                      vocabulary.append(meth_vocabulary)
                      leng.append(meth_len)
                   ###2. stuff for methods
                   meth_names, meth_param_cnt = getMethInfo(meth_body_)
                   uni_meth_names = np.unique(meth_names)
                   uni_meth_cnt   = len(uni_meth_names)
               if(len(difficulty)> 0):
                  avg_diff, med_diff = np.mean(difficulty), np.median(difficulty)
               if(len(effort)> 0):
                  avg_eff, med_eff   = np.mean(effort), np.median(effort)
               if(len(vocabulary) > 0 ):
                  avg_voc, med_voc   = np.mean(vocabulary), np.median(vocabulary)
               if(len(leng) > 0 ):
                  avg_len, med_len   = np.mean(leng), np.median(leng)
               if(len(meth_param_cnt)> 0):
                  avg_param_cnt, med_param_cnt   = np.mean(meth_param_cnt), np.median(meth_param_cnt)

               contentStr = str(meth_cnt) + ',' + str(dele_cnt) + ',' + str(prop_cnt) + ',' + str(fiel_cnt) + ',' + str(even_cnt) + ',' + str(avg_diff) + ',' + str(med_diff) + ',' + str(avg_eff) + ',' + str(med_eff) + ',' + str(avg_voc) + ',' + str(med_voc) + ',' + str(avg_len) + ',' + str(med_len) + ',' + str(avg_param_cnt) + ',' + str(med_param_cnt) + ',' + str(uni_meth_cnt) + ','
               str2Write = str2Write + str(sessID) + ',' + str(tstamp_) + ','  + contentStr + '\n'
               contentStr = ''

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
   # ds_path   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/TEST/'
   ds_path   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/Events-170301/'

   ## FOLOWWING IS DONE
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_EDIT_HIERARCHY_CONTENT.csv'
   # key_to_look = 'hierarchy'

   ## FOLOWWING IS DONE
   file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_FIELDS_COMPLEXITY_CONTENT.csv'
   key_to_look = 'sst'

   get_all_data(ds_path, key_to_look, file2save)
   print "Ended at:", giveTimeStamp()
   print '='*100
