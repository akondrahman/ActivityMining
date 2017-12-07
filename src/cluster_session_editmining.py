'''
CLUSTERING PROJECT
AKOND RAHMAN
OCT 29, 2017
SUNDAY
'''
import os
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn import cluster
import utils
import datetime,  time
import cPickle as pickle

def makeTimeHuman(single_val):
    #2016-05-07T00:22:34.7609533+02:00 , timestamp string
    dt_  = single_val.split('T')[1]
    ts_  = dt_.split('+')[0]
    x = time.strptime(ts_.split('.')[0],'%H:%M:%S')
    second2ret = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return second2ret

def getUnderstandabilityOfAllSessions(datafile_path):
   complexity_df   = pd.read_csv(datafile_path)
   complexity_df   = complexity_df.drop('TIME', 1)
   #print complexity_df.head()

   filtered_df            = complexity_df[complexity_df['UNI_MET_CNT'] > 0]
   filtered_df            = filtered_df.drop_duplicates()
   filtered_df['MOD_MED_DIF'] = filtered_df['MED_MET_DIF'] + 1
   filtered_df['MED_VOL'] = filtered_df['MED_MET_EFF'] /filtered_df['MOD_MED_DIF']
   # print filtered_df.head()
   # print '-'*50
   df2ret          = filtered_df[['SESS_ID', 'MED_MET_DIF','MED_VOL', 'MED_PAR_CNT', 'UNI_MET_CNT']]
   ### NORMALIZATION
   df2ret['NORM_MED_DIF'] = df2ret['MED_MET_DIF'] / df2ret['UNI_MET_CNT']
   df2ret['NORM_MED_VOL'] = df2ret['MED_VOL'] / df2ret['UNI_MET_CNT']
   df2ret['NORM_PARAMS']  = df2ret['MED_PAR_CNT'] / df2ret['UNI_MET_CNT']

   df2ret   = df2ret[['SESS_ID', 'NORM_MED_DIF', 'NORM_MED_VOL', 'NORM_PARAMS']]

   allSessIDs = np.unique(df2ret['SESS_ID'].tolist())
   print '='*50
   print 'UNIQUE SESSION COUNT:', len(allSessIDs)
   print '-'*50
   all_sess_data = []
   for sessID in allSessIDs:
       per_sess_difficulty = df2ret[df2ret['SESS_ID']==sessID]['NORM_MED_DIF'].tolist()
       per_sess_volume     = df2ret[df2ret['SESS_ID']==sessID]['NORM_MED_VOL'].tolist()
       per_sess_param_cnt  = df2ret[df2ret['SESS_ID']==sessID]['NORM_PARAMS'].tolist()
       #print per_sess_difficulty
       per_sess_med_dif, per_sess_med_vol, per_sess_med_pcnt = np.median(per_sess_difficulty), np.median(per_sess_volume), np.median(per_sess_param_cnt)
       per_sess_ = (sessID, per_sess_med_dif, per_sess_med_vol, per_sess_med_pcnt)
       all_sess_data.append(per_sess_)
   df_ = pd.DataFrame.from_records(all_sess_data)
   #print df_.head()
   return df_

def determineBestCluster(df_param):
    clust_cnt = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    for clus_ in clust_cnt:
             clusteringType = cluster.KMeans(n_clusters=clus_)
             clusteringType.fit(df_param)
             cluster_labels = clusteringType.labels_
             silhouette_avg = silhouette_score(df_param, cluster_labels)
             print 'ClusterCount#{}#Sil#{}'.format(clus_, silhouette_avg)
    print '='*50
def clusterByKmeans(df_to_label, versionLabels):
  labeledVersions ={}
  df_row_cnt = len(df_to_label.index)
  if(len(df_to_label)==len(versionLabels)):
     for index_ in xrange(len(versionLabels)):
         labeledVersions[index_] = versionLabels[index_]
  return labeledVersions

def clusterValues(df_param, no_of_clusters):
    clusteringType = cluster.KMeans(n_clusters=no_of_clusters)
    clusteringType.fit(df_param)
    labels_ = clusteringType.labels_
    centroids = clusteringType.cluster_centers_
    print "And the centroids are .... ", centroids
    print '='*50
    valsWithLabels = clusterByKmeans( df_param , labels_)
    #print valsWithLabels
    return valsWithLabels

def dumpValuesToFile(list_param, file2save):
    str2write = ''
    for elem in list_param:
        str2write = str2write + str(elem) + ',' + '\n'
    feature_name = file2save.split('.')[0]
    str2write = feature_name + ',' + '\n' + str2write
    os_bytes = utils.dumpContentIntoFile(str2write, file2save)
    print 'DUMPED A FILE OF {} BYTES'.format(os_bytes)
    return os_bytes

def getEditCountForClusters(sess_dict, valid_sess_p):
    edit_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_CONTENT.csv'
    edit_df   = pd.read_csv(edit_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_edit_df = edit_df[edit_df['SESS_ID']==sess_id]
        edit_cnt = len(matched_edit_df.index)
        if sess_label==1:
           high_grp.append(edit_cnt)
        else:
           low_grp.append(edit_cnt)
    return high_grp, low_grp

def getEditIntervalForClusters(sess_dict, valid_sess_p):
    edit_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_CONTENT.csv'
    edit_df   = pd.read_csv(edit_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_edit_df = edit_df[edit_df['SESS_ID']==sess_id]
        matched_edit_df = matched_edit_df.sort_values(['TIME'])
        matched_edit_df['FORMATTED_TS'] = matched_edit_df['TIME'].apply(makeTimeHuman)

        edit_cnt = len(matched_edit_df.index)
        formatted_time_list = matched_edit_df['FORMATTED_TS'].tolist()

        edit_interval_list  = np.ediff1d(formatted_time_list)

        if ((edit_cnt > 0) and (len(edit_interval_list) > 0)):
            med_edit_inte = round(np.median(edit_interval_list), 5)
            # med_edit_inte = round(np.mean(edit_interval_list), 5)
            if (med_edit_inte < 0):
                med_edit_inte = 0.0
            edit_interval = float(med_edit_inte)/float(edit_cnt) #  median edit interval, normalized by counts
            edit_interval = round(edit_interval, 5)
            if sess_label==1:
               high_grp.append(edit_interval)
            else:
               low_grp.append(edit_interval)

    return high_grp, low_grp

def getEditSizeForClusters(sess_dict, valid_sess_p):
    edit_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_CONTENT.csv'
    edit_df   = pd.read_csv(edit_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_edit_df = edit_df[edit_df['SESS_ID']==sess_id]
        edit_event_cnt = len(matched_edit_df.index)
        medi_edit_size = np.median(matched_edit_df['CNG_SIZE'].tolist())
        # medi_edit_size = np.mean(matched_edit_df['CNG_SIZE'].tolist())
        norm_edit_size = round(float(medi_edit_size)/float(edit_event_cnt), 5)
        if sess_label==1:
           high_grp.append(norm_edit_size)
        else:
           low_grp.append(norm_edit_size)
    return high_grp, low_grp


def getEditLOCACHNGForClusters(sess_dict, valid_sess_p):
    edit_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_CONTENT.csv'
    edit_df   = pd.read_csv(edit_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_dict.iteritems():
      if sess_id in valid_sess_p:
        matched_edit_df   = edit_df[edit_df['SESS_ID']==sess_id]
        edit_event_cnt    = len(matched_edit_df.index)
        medi_edit_loc_cng = np.median(matched_edit_df['CNG_CNT'].tolist())
        # medi_edit_loc_cng = np.mean(matched_edit_df['CNG_CNT'].tolist())
        norm_edit_loc_cng = round(float(medi_edit_loc_cng)/float(edit_event_cnt), 5)
        if sess_label==1:
           high_grp.append(norm_edit_loc_cng)
        else:
           low_grp.append(norm_edit_loc_cng)
    return high_grp, low_grp

def getMethCntAllSessions(datafile_path, sess_dict_p, valid_sess_p):
    high_grp, low_grp = [], []
    meth_df   = pd.read_csv(datafile_path)

    for sess_id, sess_label in sess_dict_p.iteritems():
      if sess_id in valid_sess_p:
        matched_meth_df   = meth_df[meth_df['SESS_ID']==sess_id]
        matched_meth_cnt  = len(matched_meth_df.index)

        if sess_label==1:
           high_grp.append(matched_meth_cnt)
        else:
           low_grp.append(matched_meth_cnt)
    return high_grp, low_grp


if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    file_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_SST_CONTENT.csv'
    df = getUnderstandabilityOfAllSessions(file_path)
    df2Cluster = df.drop(df.columns[0], 1)
    #print df2Cluster
    # determineBestCluster(df2Cluster)
    valsWithLabels = clusterValues(df2Cluster, 2) ## two cluter mechnsim as seen by Silhouette wirdth
    high_count, low_count = 0, 0
    final_sess_with_labels = {}
    '''
    TO handle filtered sessions absed on duration
    '''
    valid_sess = pickle.load( open('/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/dataset/VALID.SESSION.IDS.LIST', 'rb'))
    for index_key, cluster_label in valsWithLabels.iteritems():
         sessID = df.iloc[index_key, 0]
         if sessID in valid_sess:
            cluster_label = valsWithLabels[index_key]
            final_sess_with_labels[sessID] = cluster_label
            if cluster_label==1:
                high_count += 1
            else:
                low_count += 1
    print 'Total:{}, High:{}, Low:{}'.format(high_count + low_count, high_count, low_count)
    print '='*50
    pickle.dump( final_sess_with_labels, open( "SESSION.LABELS.DUMP", "wb" ) )
    #print valsWithLabels

    print 'Labeling completed for {} sessions'.format(len(final_sess_with_labels))
    print '='*50
    h_grp_edit_cnt, l_grp_edit_cnt = getEditCountForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_edit_cnt, 'H_EDIT_COUNT.csv')
    dumpValuesToFile(l_grp_edit_cnt, 'L_EDIT_COUNT.csv')
    print 'Edit count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_edit_cnt, l_grp_edit_cnt, 'EDIT_COUNT')
    print '='*50
    h_grp_edit_inte, l_grp_edit_inte = getEditIntervalForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_edit_inte, 'H_NORM_EDIT_INTERVAL.csv')
    dumpValuesToFile(l_grp_edit_inte, 'L_NORM_EDIT_INTERVAL.csv')
    print 'Normalized median edit interval (seconds) data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_edit_inte, l_grp_edit_inte, 'NORM_EDIT_INTERVAL')
    print '='*50
    h_grp_edit_size, l_grp_edit_size = getEditSizeForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_edit_size, 'H_NORM_EDIT_SIZE.csv')
    dumpValuesToFile(l_grp_edit_size, 'L_NORM_EDIT_SIZE.csv')
    print 'Normalized median edit size extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_edit_size, l_grp_edit_size, 'NORM_EDIT_SIZE')
    h_grp_edit_loc_chng, l_grp_edit_loc_chng = getEditLOCACHNGForClusters(final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_edit_loc_chng, 'H_NORM_EDIT_LOC_CHNG.csv')
    dumpValuesToFile(l_grp_edit_loc_chng, 'L_NORM_EDIT_LOC_CHNG.csv')
    print 'Normalized median edit location-changes extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_edit_loc_chng, l_grp_edit_loc_chng, 'NORM_EDIT_LOC_CHNG')
    print '='*50
    h_grp_met_cnt, l_grp_met_cnt = getMethCntAllSessions(file_path, final_sess_with_labels, valid_sess)
    dumpValuesToFile(h_grp_met_cnt, 'H_METH_CNT.csv')
    dumpValuesToFile(l_grp_met_cnt, 'L_METH_CNT.csv')
    print 'Method count per session extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_met_cnt, l_grp_met_cnt, 'METHOD_COUNT')
    print '='*100
    print "Ended at:", utils.giveTimeStamp()
    print '='*100
