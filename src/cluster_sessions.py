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

def getEditCountForClusters(sess_dict):
    edit_ds_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_CONTENT.csv'
    edit_df   = pd.read_csv(edit_ds_path)
    high_grp, low_grp = [], []
    for sess_id, sess_label in sess_dict.iteritems():
        matched_edit_df = edit_df[edit_df['SESS_ID']==sess_id]
        edit_cnt = len(matched_edit_df.index)
        if sess_label==1:
           high_grp.append(edit_cnt)
        else:
           low_grp.append(edit_cnt)
    return high_grp, low_grp
if __name__=='__main__':
    print "Started at:", utils.giveTimeStamp()
    print '='*100
    file_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_SST_CONTENT.csv'
    df = getUnderstandabilityOfAllSessions(file_path)
    df2Cluster = df.drop(df.columns[0], 1)
    #print df2Cluster
    determineBestCluster(df2Cluster)
    valsWithLabels = clusterValues(df2Cluster, 2) ## two cluter mechnsim as seen by Silhouette wirdth
    high_count = 0
    #print valsWithLabels
    final_sess_with_labels = {}
    for index_key, cluster_label in valsWithLabels.iteritems():
        sessID = df.iloc[index_key, 0]
        final_sess_with_labels[sessID] = cluster_label
        if cluster_label==1:
            high_count += 1
    print 'Total:{}, High:{}, Low:{}'.format(len(df.index), high_count, len(valsWithLabels) - high_count)
    print '='*50
    print 'Labeling completed for {} sessions'.format(len(final_sess_with_labels))
    print '='*50
    h_grp_edit_cnt, l_grp_edit_cnt = getEditCountForClusters(final_sess_with_labels)
    print 'Edit count data extracted ...'
    print '='*50
    utils.compareTwoGroups(h_grp_edit_cnt, l_grp_edit_cnt, 'EDIT_COUNT')
    print '='*100
    print "Ended at:", utils.giveTimeStamp()
    print '='*100
