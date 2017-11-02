'''
Akond Rahman
Nov 02, 2017
Thursday
Debugging for sessions
'''

import os
import pandas as pd
import utils
import datetime,  time
import cPickle as pickle
import numpy as np
from collections import Counter

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

def getDebugCountForClusters(sess_with_labels_dict):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
        matched_debug_df = debug_df[debug_df['SESS_ID']==sess_id]
        #debug_event_cnt = len(matched_debug_df.index)
        # need to filter out debug actions that occur for exceptions
        non_exception_debug_df = matched_debug_df[matched_debug_df['ACTION']=='dbgExecutionActionDefault']
        debug_event_cnt = len(non_exception_debug_df.index)
        if sess_label==1:
           high_grp.append(debug_event_cnt)
        else:
           low_grp.append(debug_event_cnt)
    return high_grp, low_grp

def getDebugIntervalForClusters(sess_with_labels_dict):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
        matched_debug_df = debug_df[debug_df['SESS_ID']==sess_id]
        # need to filter out debug actions that occur for exceptions
        non_exception_debug_df = matched_debug_df[matched_debug_df['ACTION']=='dbgExecutionActionDefault']
        debug_event_cnt = len(non_exception_debug_df.index)

        non_exception_debug_df = non_exception_debug_df.sort_values(['TIME'])
        non_exception_debug_df['FORMATTED_TS'] = non_exception_debug_df['TIME'].apply(makeTimeHuman)
        formatted_time_list = non_exception_debug_df['FORMATTED_TS'].tolist()
        debug_interval_list  = np.ediff1d(formatted_time_list)

        if ((debug_event_cnt > 0) and (len(debug_interval_list) > 0)):
            med_debug_inte = round(np.median(debug_interval_list), 5)
            # med_build_inte = round(np.mean(navi_interval_list), 5)
            if (med_debug_inte < 0):
                med_debug_inte = 0.0
            debug_interval = float(med_debug_inte)/float(debug_event_cnt) #  median navigation interval, normalized by counts
            debug_interval = round(debug_interval, 5)
            if sess_label==1:
               high_grp.append(debug_interval)
            else:
               low_grp.append(debug_interval)

    return high_grp, low_grp

if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    high_count = 0
    final_sess_with_labels = pickle.load( open('/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/edit_mining/SESSION.LABELS.DUMP', 'rb' ) )
    for index_key, cluster_label in final_sess_with_labels.iteritems():
        if cluster_label==1:
            high_count += 1
    print '[SESSIONS] Total:{}, High:{}, Low:{}'.format(len(final_sess_with_labels), high_count, len(final_sess_with_labels) - high_count)
    print '='*50
    h_grp_d_cnt, l_grp_d_cnt = getDebugCountForClusters(final_sess_with_labels)
    total_debug_event_cnt = sum(h_grp_d_cnt) + sum(l_grp_d_cnt)
    dumpValuesToFile(h_grp_d_cnt, 'H_DEBUG_COUNT.csv')
    dumpValuesToFile(l_grp_d_cnt, 'L_DEBUG_COUNT.csv')
    print 'TOTAL DEBUG EVENT COUNT: {}, HIGH DEBUG EVENT COUNT:{}, LOW DEBUG EVENT COUNT:{}'.format(total_debug_event_cnt, sum(h_grp_d_cnt), sum(l_grp_d_cnt))
    print '='*50
    print 'Debugging count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_d_cnt, l_grp_d_cnt, 'DEBUG_COUNT')
    print '='*50
    h_grp_debug_int, l_grp_debug_int = getDebugIntervalForClusters(final_sess_with_labels)
    dumpValuesToFile(h_grp_debug_int, 'H_DEBUG_INTERVAL.csv')
    dumpValuesToFile(l_grp_debug_int, 'L_DEBUG_INTERVAL.csv')
    print 'Debug interval (seconds) data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_debug_int, l_grp_debug_int, 'NORM_DEBUG_INTERVAL')
    print '='*50
