'''
Akond Rahman
Dec 07, 2017
Halestad's metric details
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

def getHalstedDetails():
   halstead_path = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_EDIT_SST_CONTENT.csv'
   complexity_df   = pd.read_csv(halstead_path)
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
       # print per_sess_difficulty
       per_sess_med_dif, per_sess_med_vol, per_sess_med_pcnt = np.median(per_sess_difficulty), np.median(per_sess_volume), np.median(per_sess_param_cnt)
       per_sess_ = (sessID, per_sess_med_dif, per_sess_med_vol, per_sess_med_pcnt)
       all_sess_data.append(per_sess_)
   df_ = pd.DataFrame.from_records(all_sess_data, columns=['SESSID', 'DIFF', 'VOLU', 'PARA'])
   # print df_.head()
   ### Summary of all data
   print df_.describe()
   return df_



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
    getHalstedDetails()
    print '='*50
