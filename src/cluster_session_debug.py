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

def getDebugCountForClusters(sess_with_labels_dict, valid_sess_p):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
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

def getDebugIntervalForClusters(sess_with_labels_dict, valid_sess_p):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
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
            debug_interval = float(med_debug_inte)/float(debug_event_cnt) #  median debug interval, normalized by counts
            debug_interval = round(debug_interval, 5)
            if sess_label==1:
               high_grp.append(debug_interval)
            else:
               low_grp.append(debug_interval)

    return high_grp, low_grp

def getNormalizedDebugReason(list_):
    dict2Ret, finalDict = {}, {}
    temp_debug_reason_cnt_holder = []
    for sess_data in list_:
        dist_, reason_cnt = sess_data
        temp_debug_reason_cnt_holder.append(reason_cnt)
        for d_reason, reason_cnt in dist_.iteritems():
            if d_reason not in dict2Ret:
               dict2Ret[d_reason] = [reason_cnt]
            else:
               dict2Ret[d_reason] = dict2Ret[d_reason] + [reason_cnt]
    #print dict2Ret
    all_reason_cnt = sum(temp_debug_reason_cnt_holder)
    #print all_reason_cnt
    for type_, tot_cnt in dict2Ret.iteritems():
        if type_ not in finalDict:
            percentage       = round(float(sum(tot_cnt))/float(all_reason_cnt), 5)*100
            finalDict[type_] = percentage
    return finalDict


def getDebugReasonsForClusters(sess_with_labels_dict, valid_sess_p):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_debug_df = debug_df[debug_df['SESS_ID']==sess_id]
        # need to filter out debug actions that occur for exceptions
        non_exception_debug_df = matched_debug_df[matched_debug_df['ACTION']=='dbgExecutionActionDefault']
        debug_event_cnt = len(non_exception_debug_df.index)

        debug_types = non_exception_debug_df['REASON'].tolist()
        debug_type_dist = dict(Counter(debug_types))
        debug_type_tup  = (debug_type_dist, debug_event_cnt)
        if sess_label==1:
           high_grp.append(debug_type_tup)
        else:
           low_grp.append(debug_type_tup)
    h_d_dist_dict = getNormalizedDebugReason(high_grp)
    l_d_dist_dict = getNormalizedDebugReason(low_grp)
    return h_d_dist_dict, l_d_dist_dict

def getDebugStepCountForClusters(sess_with_labels_dict, valid_sess_p):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_debug_df = debug_df[debug_df['SESS_ID']==sess_id]
        # need to filter out debug actions that occur for exceptions
        non_exception_debug_df = matched_debug_df[matched_debug_df['ACTION']=='dbgExecutionActionDefault']
        debug_event_cnt = len(non_exception_debug_df.index)

        debug_step_df = non_exception_debug_df[non_exception_debug_df['REASON']=='dbgEventReasonStep']
        debug_step_cnt = len(debug_step_df.index)

        if ((debug_event_cnt > 0) and (debug_step_cnt > 0)):
           norm_debug_step = float(debug_step_cnt)/float(debug_event_cnt)

           if sess_label==1:
              high_grp.append(norm_debug_step)
           else:
              low_grp.append(norm_debug_step)

    return high_grp, low_grp


def getDebugStepIntervalForClusters(sess_with_labels_dict, valid_sess_p):
    debug_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_DEBUG_CONTENT.csv'
    debug_df      = pd.read_csv(debug_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_debug_df = debug_df[debug_df['SESS_ID']==sess_id]
        # need to filter out debug actions that occur for exceptions
        non_exception_debug_df = matched_debug_df[matched_debug_df['ACTION']=='dbgExecutionActionDefault']
        debug_event_cnt = len(non_exception_debug_df.index)

        non_exception_debug_df = non_exception_debug_df.sort_values(['TIME'])
        non_exception_debug_df['FORMATTED_TS'] = non_exception_debug_df['TIME'].apply(makeTimeHuman)
        all_debug_time_list  = non_exception_debug_df['FORMATTED_TS'].tolist()
        alldebug_inter_list  = np.ediff1d(all_debug_time_list)

        debug_step_df = non_exception_debug_df[non_exception_debug_df['REASON']=='dbgEventReasonStep']
        debug_step_cnt = len(debug_step_df.index)

        formatted_time_list = debug_step_df['FORMATTED_TS'].tolist()
        debugstep_interval_list  = np.ediff1d(formatted_time_list)

        if ((debug_step_cnt > 0) and (len(debugstep_interval_list) > 0)):
            med_debugstep_inte = round(np.median(debugstep_interval_list), 5)
            # med_debugstep_inte = round(np.mean(debugstep_interval_list), 5)
            med_all_debug_int_list = np.median(alldebug_inter_list)
            if (med_debugstep_inte < 0):
                med_debugstep_inte = 0.0
            debug_step_interval = float(med_debugstep_inte)/float(debug_step_cnt) #  median debug step interval, normalized by counts
            debug_step_interval = round(debug_step_interval, 5)
            if sess_label==1:
               high_grp.append(debug_step_interval)
            else:
               low_grp.append(debug_step_interval)

    return high_grp, low_grp

if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    high_count, low_count  = 0, 0
    final_sess_with_labels = pickle.load( open('/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/src/SESSION.LABELS.DUMP', 'rb' ) )
    '''
    TO handle filtered sessions absed on duration
    '''
    valid_sess = pickle.load( open('/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/VALID.SESSION.IDS.LIST', 'rb'))
    for sessID, cluster_label in final_sess_with_labels.iteritems():
      if sessID in valid_sess:
        if cluster_label==1:
            high_count += 1
        else:
            low_count +=  1
    print '[SESSIONS] Total:{}, High:{}, Low:{}'.format(high_count + low_count, high_count, low_count)
    print '='*50
    h_grp_d_cnt, l_grp_d_cnt = getDebugCountForClusters(final_sess_with_labels, valid_sess)
    total_debug_event_cnt = sum(h_grp_d_cnt) + sum(l_grp_d_cnt)
    dumpValuesToFile(h_grp_d_cnt, 'H_DEBUG_COUNT.csv')
    dumpValuesToFile(l_grp_d_cnt, 'L_DEBUG_COUNT.csv')
    print 'TOTAL DEBUG EVENT COUNT: {}, HIGH DEBUG EVENT COUNT:{}, LOW DEBUG EVENT COUNT:{}'.format(total_debug_event_cnt, sum(h_grp_d_cnt), sum(l_grp_d_cnt))
    print '='*50
    print 'Debugging count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_d_cnt, l_grp_d_cnt, 'DEBUG_COUNT')
    print '='*50
    h_grp_debug_int, l_grp_debug_int = getDebugIntervalForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_debug_int, 'H_DEBUG_INTERVAL.csv')
    dumpValuesToFile(l_grp_debug_int, 'L_DEBUG_INTERVAL.csv')
    print 'Debug interval (seconds) data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_debug_int, l_grp_debug_int, 'NORM_DEBUG_INTERVAL')
    print '='*50
    h_dist_dict, l_dist_dict = getDebugReasonsForClusters(final_sess_with_labels, valid_sess)
    print 'HIGH (NUMBERS ARE IN %):'
    print h_dist_dict
    print '-'*50
    print 'LOW (NUMBERS ARE IN %):'
    print l_dist_dict
    print '-'*50
    h_debug_step_cnt, l_debug_step_cnt = getDebugStepCountForClusters(final_sess_with_labels, valid_sess)
    print 'Debug step count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_debug_step_cnt, l_debug_step_cnt, 'DEBUG_STEP_COUNT')
    dumpValuesToFile(h_debug_step_cnt, 'H_DEBUG_COUNT.csv')
    dumpValuesToFile(l_debug_step_cnt, 'L_DEBUG_COUNT.csv')
    print 'Debug step count data extracted ...'
    print '='*50
    h_grp_debug_step_int, l_grp_debug_step_int = getDebugStepIntervalForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_debug_step_int, 'H_DEBUG_STEP_INTERVAL.csv')
    dumpValuesToFile(l_grp_debug_step_int, 'L_DEBUG_STEP_INTERVAL.csv')
    print 'Debug step interval (seconds) data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_debug_int, l_grp_debug_int, 'NORM_DEBUG_STEP_INTERVAL')
    print '='*50
    print '='*100
    print "Ended at:", utils.giveTimeStamp()
    print '='*100
