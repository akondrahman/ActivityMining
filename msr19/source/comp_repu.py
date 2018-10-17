'''
Compare reputation
Akond Rahman 
Oct 17 2018 
'''
from scipy import stats
import pandas as pd
import numpy as np
import cliffsDelta
from datetime import date

def compareDists(ls_1, ls_2, type_):
    print "Interest metric:", type_
    print "List#1 values [MEDIAN]:{}, [MEAN]:{}, [COUNT]:{}".format(np.median(list(ls_1)), np.mean(list(ls_1)), len(ls_1))
    print "List#2 values [MEDIAN]:{}, [MEAN]:{}, [COUNT]:{}".format(np.median(list(ls_2)), np.mean(list(ls_2)), len(ls_2))
    try:
        TS, p = stats.mannwhitneyu(list(ls_1), list(ls_2), alternative='greater')
    except ValueError:
        TS, p = 0.01, 0.95
    cliffs_delta = cliffsDelta.cliffsDelta(list(ls_1), list(ls_2))
    print '*'*25
    print 'Pee value:{}, cliffs:{}, type:{}'.format(p, cliffs_delta, type_)
    print '*'*25

def getDurationInSO(end_, start_):
    end_dat = end_.split(' ')[0]
    sta_dat = start_.split(' ')[0]

    end_date = end_dat.split('-')
    end_date = [int(x_) for x_ in end_date]
    sta_date = sta_dat.split('-')   
    sta_date = [int(x_) for x_ in sta_date]

    d0 = date(sta_date[0], sta_date[1], sta_date[2])
    d1 = date(end_date[0], end_date[1], end_date[2])
    delta_ = d1 - d0
    print   delta_.days , delta_.months     
    return  delta_.days , delta_.months     

def getNormalizedRepu(user_data_df):
    repu  = user_data_df['Reputation'].tolist()[0]
    start = user_data_df['CreateDate'].tolist()[0]
    end   = user_data_df['LastAccDate'].tolist()[0]

    dura_days, dura_mont  = getDurationInSO(end, start )

    norm_repu = float(repu) / float(dura_days) 
    
    return norm_repu

def compareReputation(user_df, user_post_df, answer_df):
    filtered_user_post_df = user_post_df[user_post_df['UserID'] != 0]

    total_df = answer_df[answer_df['TYPE']=='TOTAL']

    at_least_one_postID_list = np.unique( total_df[total_df['INSECURE_SNIPPET_CNT'] > 0 ]['ID'].tolist() )
    none_postID_list         = np.unique( total_df[total_df['INSECURE_SNIPPET_CNT'] <= 0 ]['ID'].tolist() )

    '''
    first get user IDs
    '''

    none_user_IDs, atleast_one_user_IDs = [], []

    for postID in none_postID_list:
        userID = filtered_user_post_df[filtered_user_post_df['PostID']==postID]['UserID'].tolist()[0]
        none_user_IDs.append(userID)

    for postID in at_least_one_postID_list:
        userID = filtered_user_post_df[filtered_user_post_df['PostID']==postID]['UserID'].tolist()[0]
        atleast_one_user_IDs.append(userID)

    '''
    then get reputations 
    '''
    none_user_repu, atleast_one_user_repu = [], []

    for userID in none_user_IDs:
        userID_DF = user_df[user_df['AccountID']==userID]
        norm_repu = getNormalizedRepu(userID_DF) 
        none_user_repu.append(norm_repu)

    for userID in atleast_one_user_IDs:
        userID_DF = user_df[user_df['AccountID']==userID]
        norm_repu = getNormalizedRepu(userID_DF) 
        atleast_one_user_repu.append(norm_repu)



if __name__=='__main__':
   user_file_ = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_PY_ANS_USERS.csv'
   user_df_   = pd.read_csv(user_file_)
   
   
   user_post_file = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_PY_ANS_USERID.csv'
   user_post_df   = pd.read_csv(user_post_file)

   answer_file = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ANS_RES.csv'
   answer_df   = pd.read_csv(answer_file)

   compareReputation(user_df_, user_post_df, answer_df)


