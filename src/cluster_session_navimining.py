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

if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    high_count = 0
    final_sess_with_labels = pickle.load( open('/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/edit_mining/SESSION.LABELS.DUMP', 'rb' ) )
    for index_key, cluster_label in final_sess_with_labels.iteritems():
        if cluster_label==1:
            high_count += 1
    print 'Total:{}, High:{}, Low:{}'.format(len(final_sess_with_labels), high_count, len(final_sess_with_labels) - high_count)
    print '='*50
    h_grp_n_cnt, l_grp_n_cnt = getNavigationCountForClusters(final_sess_with_labels)
    total_navi_event_cnt = sum(h_grp_n_cnt) + sum(l_grp_n_cnt)
    dumpValuesToFile(h_grp_n_cnt, 'H_NAVI_COUNT.csv')
    dumpValuesToFile(l_grp_n_cnt, 'L_NAVI_COUNT.csv')
    print 'TOTAL NAVIGATION EVENT COUNT:', total_navi_event_cnt
    print '='*50
    print 'Navigation count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_n_cnt, l_grp_n_cnt, 'NAVI_COUNT')
    print '='*50
    print '='*100
    print "Ended at:", utils.giveTimeStamp()
    print '='*100