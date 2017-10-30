'''
Akond Rahman
Oct 30, 2017
Monday
Build data mining for clustered sessions
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

def getTestCountForClusters(sess_with_labels):
    test_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_TEST_CONTENT.csv'
    test_df   = pd.read_csv(test_ds_path)
    h_aborted, l_aborted, high_grp, low_grp = [], [], [], []
    for sess_id, sess_label in sess_with_labels.iteritems():
        matched_test_df = test_df[test_df['SESS_ID']==sess_id]

        valid_test_df   = matched_test_df[matched_test_df['ABORT']==False]
        invalid_test_df = matched_test_df[matched_test_df['ABORT']==True]

        valid_test_event_cnt   = len(valid_test_df.index)
        invalid_test_event_cnt = len(invalid_test_df.index)

        if sess_label==1:
           high_grp.append(valid_test_event_cnt)
           h_aborted.append(invalid_test_event_cnt)
        else:
           low_grp.append(valid_test_event_cnt)
           l_aborted.append(invalid_test_event_cnt)
    return high_grp, low_grp, h_aborted, l_aborted


if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    high_count = 0
    final_sess_with_labels = pickle.load(open('/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/edit_mining/SESSION.LABELS.DUMP', 'rb' ) )
    for index_key, cluster_label in final_sess_with_labels.iteritems():
        if cluster_label==1:
            high_count += 1
    print 'Total Sessions With Method Usage:{}, High:{}, Low:{}'.format(len(final_sess_with_labels), high_count, len(final_sess_with_labels) - high_count)
    print '='*50
    h_grp_t_cnt, l_grp_t_cnt, abort_h, abort_l = getTestCountForClusters(final_sess_with_labels)
    dumpValuesToFile(h_grp_t_cnt, 'H_TEST_COUNT.csv')
    dumpValuesToFile(l_grp_t_cnt, 'L_TEST_COUNT.csv')
    valid_test_cnt_tot   = sum(h_grp_t_cnt) + sum(l_grp_t_cnt)
    invalid_test_cnt_tot = sum(abort_h) + sum(abort_l)
    print 'TEST count data extracted ...'
    print '='*50
    print '[TOTAL TEST COUNT]=> VALID:{}, INVALID:{}'.format(valid_test_cnt_tot, invalid_test_cnt_tot)
    print '='*50
    utils.compareTwoGroups(h_grp_t_cnt, l_grp_t_cnt, 'TEST_COUNT')
    print '='*50
