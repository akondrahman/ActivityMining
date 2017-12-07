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

def getBuildCountForClusters(sess_with_labels_dict, valid_sess_p):
    build_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_BUILD_CONTENT.csv'
    build_df   = pd.read_csv(build_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_build_df = build_df[build_df['SESS_ID']==sess_id]
        build_event_cnt = len(matched_build_df.index)
        if sess_label==1:
           high_grp.append(build_event_cnt)
        else:
           low_grp.append(build_event_cnt)
    return high_grp, low_grp

def getBuildIntervalForClusters(sess_with_labels_dict, valid_sess_p):
    build_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_BUILD_CONTENT.csv'
    build_df   = pd.read_csv(build_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_build_df = build_df[build_df['SESS_ID']==sess_id]
        build_event_cnt = len(matched_build_df.index)

        matched_build_df = matched_build_df.sort_values(['TIME'])
        matched_build_df['FORMATTED_TS'] = matched_build_df['TIME'].apply(makeTimeHuman)
        formatted_time_list = matched_build_df['FORMATTED_TS'].tolist()
        build_interval_list  = np.ediff1d(formatted_time_list)

        if ((build_event_cnt > 0) and (len(build_interval_list) > 0)):
            med_build_inte = round(np.median(build_interval_list), 5)
            # med_build_inte = round(np.mean(build_interval_list), 5)
            if (med_build_inte < 0):
                med_build_inte = 0.0
            build_interval = float(med_build_inte)/float(build_event_cnt) #  median build interval, normalized by counts
            build_interval = round(build_interval, 5)
            if sess_label==1:
               high_grp.append(build_interval)
            else:
               low_grp.append(build_interval)

    return high_grp, low_grp


def getBuildPassRatioForClusters(sess_with_labels_dict, valid_sess_p):
    build_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_BUILD_CONTENT.csv'
    build_df   = pd.read_csv(build_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_with_labels_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_build_df = build_df[build_df['SESS_ID']==sess_id]
        build_event_cnt = len(matched_build_df.index)
        build_res_as_list  = matched_build_df['BUILD_RES'].tolist()
        if (len(build_res_as_list) > 0):
            pass_cnt, fail_cnt = 0, 0
            for build_res in build_res_as_list:
                if (build_res):
                    pass_cnt += 1
                else:
                    fail_cnt += 1
            pass_ratio = round(float(pass_cnt)/float(pass_cnt + fail_cnt), 5)
            if sess_label==1:
               high_grp.append(pass_ratio)
            else:
               low_grp.append(pass_ratio)
    return high_grp, low_grp

if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    high_count, low_count = 0, 0
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
    h_grp_build_cnt, l_grp_build_cnt = getBuildCountForClusters(final_sess_with_labels, valid_sess)
    total_build_cnt = sum(h_grp_build_cnt) + sum(l_grp_build_cnt)
    print 'TOTAL BUILD EVENT COUNT: {}, HIGH BUILD EVENT COUNT:{}, LOW BUILD EVENT COUNT:{}'.format(total_build_cnt, sum(h_grp_build_cnt), sum(l_grp_build_cnt))
    print '='*50
    dumpValuesToFile(h_grp_build_cnt, 'H_BUILD_COUNT.csv')
    dumpValuesToFile(l_grp_build_cnt, 'L_BUILD_COUNT.csv')
    print 'Build count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_build_cnt, l_grp_build_cnt, 'BUILD_COUNT')
    print '='*50
    h_grp_build_int, l_grp_build_int = getBuildIntervalForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_build_int, 'H_BUILD_INTERVAL.csv')
    dumpValuesToFile(l_grp_build_int, 'L_BUILD_INTERVAL.csv')
    print 'Build interval (seconds) data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_build_int, l_grp_build_int, 'NORM_BUILD_INTERVAL')
    print '='*50
    h_grp_build_pass, l_grp_build_pass = getBuildPassRatioForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_build_pass, 'H_BUILD_PASS_RATIO.csv')
    dumpValuesToFile(l_grp_build_pass, 'L_BUILD_PASS_RATIO.csv')
    print 'Build pass ratio data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_build_pass, l_grp_build_pass, 'NORM_BUILD_PASS_RATIO')
    print '='*50
    print '='*100
    print "Ended at:", utils.giveTimeStamp()
    print '='*100
