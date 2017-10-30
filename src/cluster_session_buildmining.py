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
    # h_grp_edit_cnt, l_grp_edit_cnt = getEditCountForClusters(final_sess_with_labels)
    # dumpValuesToFile(h_grp_edit_cnt, 'H_EDIT_COUNT.csv')
    # dumpValuesToFile(l_grp_edit_cnt, 'L_EDIT_COUNT.csv')
    # print 'Edit count data extracted ...'
    # print '='*50
    # utils.compareTwoGroups(h_grp_edit_cnt, l_grp_edit_cnt, 'EDIT_COUNT')
    # print '='*50
