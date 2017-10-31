'''
Akond Rahman
Oct 30, 2017
Mine navigation data for clustered sessions
'''
import os
import pandas as pd
import utils
import datetime,  time
import cPickle as pickle
import numpy as np

def makeTimeHuman(single_val):
    #2016-05-17T01:28:02.8130763+02:00 , timestamp string
    dt_  = single_val.split('T')[1]
    ts_  = dt_.split('+')[0]
    x = time.strptime(ts_.split('.')[0],'%H:%M:%S')
    second2ret = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return second2ret


def dumpValuesToFile(list_param, file2save):
    str2write = ''
    for elem in list_param:
        str2write = str2write + str(elem) + ',' + '\n'
    feature_name = file2save.split('.')[0]
    str2write = feature_name + ',' + '\n' + str2write
    os_bytes = utils.dumpContentIntoFile(str2write, file2save)
    print 'DUMPED A FILE OF {} BYTES'.format(os_bytes)
    return os_bytes

def getNavigationCountForClusters(sess_with_labels_dict):
    navi_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_NAVIGATION_CONTENT.csv'
    navi_df      = pd.read_csv(navi_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
        matched_navi_df = navi_df[navi_df['SESS_ID']==sess_id]
        navi_event_cnt = len(matched_navi_df.index)
        if sess_label==1:
           high_grp.append(navi_event_cnt)
        else:
           low_grp.append(navi_event_cnt)
    return high_grp, low_grp
