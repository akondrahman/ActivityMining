'''
msr data challenge 2018
Akond Rahman
Extract EDIT, BUILD, TEST META DATA
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
    headerDict = {'build':'SESS_ID,SESS_DOC,EVENT_DURA,TIME,BUILD_RES,BUILD_DURA,',
                  'edit' :'SESS_ID,SESS_DOC,EVENT_DURA,TIME,CNG_SIZE,CNG_CNT,',
                  'test' :'SESS_ID,ABORT,SESS_DOC,EVENT_DURA,TIME,TEST_RES,TEST_DURA,',
                  'error':'CONTEXT,STACKTRACE,',
                  'debug':'SESS_ID,SESS_DOC,EVENT_DURA,TIME,MODE,REASON,ACTION,',
                   #'navigation':'SESS_ID,SESS_DOC,TIME,TYPE,LOCA,TARGET,',
                  'navigation':'SESS_ID,SESS_DOC,TIME,TYPE,',
                  'profile':'PROFILE_ID,CODE_REV,EXP_CS,EXP_ALL,SMALL_TEAM,MED_TEAM,LARG_TEAM,SESS_ID,PERSONAL_PROJ,POSITION,SOLO_TEAM,SHARE_PROJ_SMA,SHARE_PROJ_MED,SHARE_PROJ_LAR,',
                  'control':'SESS_ID,DURA,SOLN,SESS_DOC,TIME,VCS_TYPE,VCS_TIME,',
                  'solution':'SESS_ID,SESS_SOLN,SESS_DURA,SESS_DOC,SESS_ACT,SOLN_TIME,',
                  'info':'SESS_ID,SESS_SOLN,SESS_DURA,SESS_DOC,SESS_ACT,SOLN_TIME,',
                  'command':'SESS_ID,TIME,COMMAND'
                  }
    return headerDict[key_param]

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP)
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def getTestDataFromDict(dict_param):
    str2Write = ''
    if(('WasAborted' in dict_param) and ('IDESessionUUID' in dict_param) and ('ActiveDocument' in dict_param) and ('Duration' in dict_param) and ('TriggeredAt' in dict_param) and ('Tests' in dict_param)):
        abort     = dict_param['WasAborted']
        sessID    = dict_param['IDESessionUUID']
        docu      = dict_param['ActiveDocument']
        sessDur   = dict_param['Duration']
        tstamp_   = dict_param['TriggeredAt']
        tests     = dict_param['Tests']
        for test_dict_ in tests:
           if (('Result' in test_dict_) and ('Duration' in test_dict_)):
              test_res = test_dict_['Result']
              test_dur = test_dict_['Duration']
              str2Write = str2Write + str(sessID) + ',' + str(abort) + ',' + str(docu) + ',' + str(sessDur) + ',' + str(tstamp_) + ',' + str(test_res) + ',' + str(test_dur) + ',' + '\n'
    return str2Write


def getBuildDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('ActiveDocument' in dict_param) and ('Duration' in dict_param) and ('TriggeredAt' in dict_param) and ('Targets' in dict_param)):
        sessID    = dict_param['IDESessionUUID']
        docu      = dict_param['ActiveDocument']
        dura_     = dict_param['Duration']
        tstamp_   = dict_param['TriggeredAt']
        builds    = dict_param['Targets']
        for build_dict_ in builds:
           if (('Successful' in build_dict_) and ('Duration' in build_dict_)):
              build_res = build_dict_['Successful']
              build_dur = build_dict_['Duration']
              str2Write = str2Write + str(sessID) + ',' + str(docu) + ',' + str(dura_) + ',' + str(tstamp_) + ',' + str(build_res) + ',' + str(build_dur) + ',' + '\n'
              #print str2Write
    #print str2Write
    return str2Write

def getEditDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('SizeOfChanges' in dict_param) and ('Duration' in dict_param) and ('TriggeredAt' in dict_param) and ('NumberOfChanges' in dict_param) and ('ActiveDocument' in dict_param)):
        sessID      = dict_param['IDESessionUUID']
        docu        = dict_param['ActiveDocument']
        dura_       = dict_param['Duration']
        tstamp_     = dict_param['TriggeredAt']
        change_size = dict_param['SizeOfChanges']
        change_cnt  = dict_param['NumberOfChanges']
        str2Write = str2Write + str(sessID) + ',' + str(docu) + ',' + str(dura_) + ',' + str(tstamp_) + ',' + str(change_size) + ',' + str(change_cnt) + ',' + '\n'

    return str2Write


def getDebugDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('Mode' in dict_param) and ('Duration' in dict_param) and ('TriggeredAt' in dict_param) and ('Reason' in dict_param) and ('ActiveDocument' in dict_param) and ('Action' in dict_param)):
        sessID      = dict_param['IDESessionUUID']
        docu        = dict_param['ActiveDocument']
        dura_       = dict_param['Duration']
        tstamp_     = dict_param['TriggeredAt']
        mode        = dict_param['Mode']
        reason_     = dict_param['Reason']
        action_     = dict_param['Action']

        str2Write = str2Write + str(sessID) + ',' + str(docu) + ',' + str(dura_) + ',' + str(tstamp_) + ',' + str(mode) + ',' + str(reason_) + ',' + str(action_) + ',' + '\n'

    return str2Write

def getNavigationDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('TypeOfNavigation' in dict_param) and ('TriggeredAt' in dict_param) and ('Location' in dict_param) and ('ActiveDocument' in dict_param) and ('Target' in dict_param)):
        sessID      = dict_param['IDESessionUUID']
        docu        = dict_param['ActiveDocument']
        tstamp_     = dict_param['TriggeredAt']
        type_       = dict_param['TypeOfNavigation']
        locat_      = dict_param['Location']
        target_     = dict_param['Target']

        # str2Write = str2Write + str(sessID) + ',' + str(docu) + ',' + str(tstamp_) + ',' + str(type_) + ',' + str(locat_) + ',' + str(target_) + ',' + '\n'
        str2Write = str2Write + str(sessID) + ',' + str(docu) + ',' + str(tstamp_) + ',' + str(type_) + ',' + '\n'
    return str2Write

def getUserProfileDataFromDict(dict_param):
    str2Write = ''
    if( ('CodeReviews' in dict_param) and ('ProgrammingCSharp' in dict_param) and ('TeamsMedium' in dict_param)    and
        ('IDESessionUUID' in dict_param) and ('ProgrammingGeneral' in dict_param) and ('TeamsLarge' in dict_param) and
        ('TeamsSmall' in dict_param) and ('ProjectsPersonal' in dict_param) and ('ProfileId' in dict_param) and
        ('Position' in dict_param) and ('TeamsSolo' in dict_param) and
        ('ProjectsSharedSmall' in dict_param) and ('ProjectsSharedMedium' in dict_param) and ('ProjectsSharedLarge' in dict_param)):

        profileID    = dict_param['ProfileId']
        code_rev     = dict_param['CodeReviews']

        exp_csha     = dict_param['ProgrammingCSharp']
        exp_gene     = dict_param['ProgrammingGeneral']

        team_siz_sma = dict_param['TeamsSmall']
        team_siz_med = dict_param['TeamsMedium']
        team_siz_lar = dict_param['TeamsLarge']

        sessID       = dict_param['IDESessionUUID']
        pers_proj    = dict_param['ProjectsPersonal']
        position     = dict_param['Position']
        team_solo    = dict_param['TeamsSolo']

        proj_share_s = dict_param['ProjectsSharedSmall']
        proj_share_m = dict_param['ProjectsSharedMedium']
        proj_share_l = dict_param['ProjectsSharedLarge']

        vals = [profileID, code_rev, exp_csha, exp_gene, team_siz_sma, team_siz_med, team_siz_lar,
                sessID, pers_proj, position, team_solo, proj_share_s, proj_share_m, proj_share_l
               ]
        content_str=''
        for val_ in vals:
            content_str = content_str + str(val_) + ','

        str2Write = str2Write + content_str + '\n'


    return str2Write

def getVersionControlDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('Solution' in dict_param) and ('Actions' in dict_param) and ('ActiveDocument' in dict_param) and ('TriggeredAt' in dict_param) and ('Duration' in dict_param)):
        sessID  = dict_param['IDESessionUUID']
        soln    = dict_param['Solution']
        actions = dict_param['Actions']
        docu    = dict_param['ActiveDocument']
        tstamp  = dict_param['TriggeredAt']
        dura    = dict_param['Duration']
        for action_dict in actions:
            if(('ActionType' in action_dict) and ('ExecutedAt' in action_dict)):
                vcs_action_type = action_dict['ActionType']
                vcs_action_ts   = action_dict['ExecutedAt']
                str2Write = str2Write + str(sessID) + ',' + str(dura) + ',' + str(soln) + ',' + str(docu) + ',' + str(tstamp) + ',' + str(vcs_action_type) + ',' + str(vcs_action_ts) + ',' + '\n'
    return str2Write


def getSolutionDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('Target' in dict_param) and ('Duration' in dict_param) and ('ActiveDocument' in dict_param) and ('Action' in dict_param) and ('TriggeredAt' in dict_param)):
        sessID  = dict_param['IDESessionUUID']
        soln    = dict_param['Target']
        dura    = dict_param['Duration']
        docu    = dict_param['ActiveDocument']
        action  = dict_param['Action']
        tstamp  = dict_param['TriggeredAt']

        str2Write = str2Write + str(sessID) + ',' + str(soln) + ',' + str(dura) + ',' + str(docu) + ',' + str(action) + ',' + str(tstamp) + ',' + '\n'
    return str2Write

def getInfoDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('Target' in dict_param) and ('Duration' in dict_param) and ('ActiveDocument' in dict_param) and ('Action' in dict_param) and ('TriggeredAt' in dict_param)):
        sessID  = dict_param['IDESessionUUID']
        soln    = dict_param['Target']
        dura    = dict_param['Duration']
        docu    = dict_param['ActiveDocument']
        action  = dict_param['Action']
        tstamp  = dict_param['TriggeredAt']

        str2Write = str2Write + str(sessID) + ',' + str(soln) + ',' + str(dura) + ',' + str(docu) + ',' + str(action) + ',' + str(tstamp) + ',' + '\n'
    return str2Write

def getCommandDataFromDict(dict_param):
    str2Write = ''
    if( ('IDESessionUUID' in dict_param) and ('TriggeredAt' in dict_param) and ('CommandId' in dict_param)):
        sessID  = dict_param['IDESessionUUID']
        tstamp  = dict_param['TriggeredAt']
        cmdID   = dict_param['CommandId']

        cmdID = cmdID.replace("{", "_")
        cmdID = cmdID.replace("}", "_")
        cmdID = cmdID.replace(":", "_")
        cmdID = cmdID.replace(".", "_")
        str2Write = str2Write + str(sessID) + ',' + str(tstamp) + ','  + cmdID + ',' + '\n'
    return str2Write

def readJSONFileContent(json_path, key_to_see='test'):
    str2Write = ''
    onlyfiles = [f_ for f_ in os.listdir(json_path) if isfile(join(json_path, f_))]
    full_path_files = [join(json_path, f_) for f_ in os.listdir(json_path) ]
    only_json_files = [f_ for f_ in full_path_files if '.json' in f_]
    str2Write = ''
    for json_file in only_json_files:
        with open(json_file) as json_data:
             d_ = json.load(json_data)
             #print d_
             if ('$type' in d_):
                 val2see = d_['$type'].lower()
                 if(key_to_see in val2see):
                    # print d_
                    # print '*'*25
                    '''
                    get the data you need
                    '''
                    if key_to_see=='test':
                       strFromDict = getTestDataFromDict(d_)
                    elif key_to_see=='build':
                       strFromDict = getBuildDataFromDict(d_)
                    elif key_to_see=='edit':
                       strFromDict = getEditDataFromDict(d_)
                    elif key_to_see=='debug':
                       strFromDict = getDebugDataFromDict(d_)
                    elif key_to_see=='navigation':
                       strFromDict = getNavigationDataFromDict(d_)
                    elif key_to_see=='profile':
                       strFromDict = getUserProfileDataFromDict(d_)
                    elif key_to_see=='control':
                       strFromDict = getVersionControlDataFromDict(d_)
                    elif key_to_see=='solution':
                       strFromDict = getSolutionDataFromDict(d_)
                    elif key_to_see=='command':
                       strFromDict = getCommandDataFromDict(d_)
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
    #print all_sub_dirs
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
   # ds_path   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/Events-170301/'

   # following already completed
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_BUILD_CONTENT.csv'
   # key_to_look = 'build'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_TEST_CONTENT.csv'
   # key_to_look = 'test'


   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_EDIT_CONTENT.csv'
   # key_to_look = 'edit'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_DEBUG_CONTENT.csv'
   # key_to_look = 'debug'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_NAVIGATION_CONTENT.csv'
   # key_to_look = 'navigation'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_PROFILE_CONTENT.csv'
   # key_to_look = 'profile'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_VCS_CONTENT.csv'
   # key_to_look = 'control'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_SOLUTION_CONTENT.csv'
   # key_to_look = 'solution'

   # following already compelted
   # file2save = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/ALL_COMMAND_CONTENT.csv'
   # key_to_look = 'command'

   get_all_data(ds_path, key_to_look, file2save)
   print "Ended at:", giveTimeStamp()
   print '='*100
