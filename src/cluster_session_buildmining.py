'''
Akond Rahman
Oct 30, 2017
Monday
Build data mining for clustered sessions
'''
import os
import cPickle as pickle
import pandas as pd
import utils

def dumpValuesToFile(list_param, file2save):
    str2write = ''
    for elem in list_param:
        str2write = str2write + str(elem) + ',' + '\n'
    feature_name = file2save.split('.')[0]
    str2write = feature_name + ',' + '\n' + str2write
    os_bytes = utils.dumpContentIntoFile(str2write, file2save)
    print 'DUMPED A FILE OF {} BYTES'.format(os_bytes)
    return os_bytes

def getBuildCountForClusters(sess_with_labels_dict):
    build_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_BUILD_CONTENT.csv'
    build_df   = pd.read_csv(build_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
        matched_build_df = build_df[build_df['SESS_ID']==sess_id]
        build_event_cnt = len(matched_build_df.index)
        if sess_label==1:
           high_grp.append(build_event_cnt)
        else:
           low_grp.append(build_event_cnt)
    return high_grp, low_grp

if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    high_count = 0
    final_sess_with_labels = pickle.load( open( '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/edit_mining/SESSION.LABELS.DUMP', 'rb' ) )
    for index_key, cluster_label in final_sess_with_labels.iteritems():
        if cluster_label==1:
            high_count += 1
    print 'Total:{}, High:{}, Low:{}'.format(len(final_sess_with_labels), high_count, len(final_sess_with_labels) - high_count)
    print '='*50
    h_grp_build_cnt, l_grp_build_cnt = getBuildCountForClusters(final_sess_with_labels)
    dumpValuesToFile(h_grp_build_cnt, 'H_BUILD_COUNT.csv')
    dumpValuesToFile(l_grp_build_cnt, 'L_BUILD_COUNT.csv')
    print 'Build count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_build_cnt, l_grp_build_cnt, 'BUILD_COUNT')
    print '='*50
