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

def getNavigationIntervalForClusters(sess_with_labels_dict):
    navi_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_NAVIGATION_CONTENT.csv'
    navi_df      = pd.read_csv(navi_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
        matched_navi_df = navi_df[navi_df['SESS_ID']==sess_id]
        navi_event_cnt = len(matched_navi_df.index)

        matched_navi_df = matched_navi_df.sort_values(['TIME'])
        matched_navi_df['FORMATTED_TS'] = matched_navi_df['TIME'].apply(makeTimeHuman)
        formatted_time_list = matched_navi_df['FORMATTED_TS'].tolist()
        navi_interval_list  = np.ediff1d(formatted_time_list)

        if ((navi_event_cnt > 0) and (len(navi_interval_list) > 0)):
            med_navi_inte = round(np.median(navi_interval_list), 5)
            # med_build_inte = round(np.mean(navi_interval_list), 5)
            if (med_navi_inte < 0):
                med_navi_inte = 0.0
            navi_interval = float(med_navi_inte)/float(navi_event_cnt) #  median navigation interval, normalized by counts
            navi_interval = round(navi_interval, 5)
            if sess_label==1:
               high_grp.append(navi_interval)
            else:
               low_grp.append(navi_interval)

    return high_grp, low_grp

def getNormalizedNavType(list_):
    dict2Ret, finalDict = {}, {}
    temp_nav_cnt_holder = []
    for sess_data in list_:
        dist_, event_cnt = sess_data
        temp_nav_cnt_holder.append(event_cnt)
        for navi_type, type_cnt in dist_.iteritems():
            if navi_type not in dict2Ret:
               dict2Ret[navi_type] = [type_cnt]
            else:
               dict2Ret[navi_type] = dict2Ret[navi_type] + [type_cnt]
    #print dict2Ret
    all_event_cnt = sum(temp_nav_cnt_holder)
    print all_event_cnt
    for type_, tot_cnt in dict2Ret.iteritems():
        if type_ not in finalDict:
            percentage       = round(float(sum(tot_cnt))/float(all_event_cnt), 5)*100
            finalDict[type_] = percentage
    return finalDict

def getNavigationTypesForClusters(sess_with_labels_dict):
    navi_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_NAVIGATION_CONTENT.csv'
    navi_df      = pd.read_csv(navi_ds_path)
    high_grp, low_grp = [], []
    dict2Ret = {}
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
        matched_navi_df = navi_df[navi_df['SESS_ID']==sess_id]
        navi_event_cnt = len(matched_navi_df.index)
        navi_types = matched_navi_df['TYPE'].tolist()
        navi_type_dist = dict(Counter(navi_types))
        navi_type_tup  = (navi_type_dist, navi_event_cnt)
        if sess_label==1:
           high_grp.append(navi_type_tup)
        else:
           low_grp.append(navi_type_tup)
    h_nav_dist_dict = getNormalizedNavType(high_grp)
    l_nav_dist_dict = getNormalizedNavType(low_grp)
    return h_nav_dist_dict, l_nav_dist_dict


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
    h_grp_n_cnt, l_grp_n_cnt = getNavigationCountForClusters(final_sess_with_labels)
    total_navi_event_cnt = sum(h_grp_n_cnt) + sum(l_grp_n_cnt)
    dumpValuesToFile(h_grp_n_cnt, 'H_NAVI_COUNT.csv')
    dumpValuesToFile(l_grp_n_cnt, 'L_NAVI_COUNT.csv')
    print 'TOTAL NAVIGATION EVENT COUNT: {}, HIGH NAVIGATION EVENT COUNT:{}, LOW NAVIGATION EVENT COUNT:{}'.format(total_navi_event_cnt, sum(h_grp_n_cnt), sum(l_grp_n_cnt))
    print '='*50
    print 'Navigation count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_n_cnt, l_grp_n_cnt, 'NAVI_COUNT')
    print '='*50
    # h_grp_navi_int, l_grp_navi_int = getNavigationIntervalForClusters(final_sess_with_labels)
    # dumpValuesToFile(h_grp_navi_int, 'H_NAVI_INTERVAL.csv')
    # dumpValuesToFile(l_grp_navi_int, 'L_NAVI_INTERVAL.csv')
    # print 'Navigation interval (seconds) data extracted ...'
    # print '='*50
    # utils.compareTwoGroups(h_grp_navi_int, l_grp_navi_int, 'NORM_NAVI_INTERVAL')
    # print '='*50
    h_dist_dict, l_dist_dict = getNavigationTypesForClusters(final_sess_with_labels)
    # print h_dist_dict
    # print '-'*50
    # print l_dist_dict
    # print '-'*50
    print '='*100
    print "Ended at:", utils.giveTimeStamp()
    print '='*100
