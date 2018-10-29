'''
'''
import pandas as pd 
import numpy  as np 
import cliffsDelta
from scipy import stats

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

def quantifyChanges(answer_df, ans_churn_df):
    at_least_one_postID_list = np.unique( answer_df[answer_df['INSECURE_SNIPPET_CNT'] > 0 ]['ID'].tolist() )
    none_postID_list         = np.unique( answer_df[answer_df['INSECURE_SNIPPET_CNT'] <= 0 ]['ID'].tolist() )

    atleast_one_churn_df = ans_churn_df[ans_churn_df['PostID'].isin(at_least_one_postID_list)]
    none_churn_df = ans_churn_df[ans_churn_df['PostID'].isin(none_postID_list)] 

    # print atleast_one_churn_df

    atleast_one_churn_IDs = np.unique(atleast_one_churn_df['PostID'].tolist())
    none_churn_IDs        = np.unique(none_churn_df['PostID'].tolist())

    print 'Number of insecure answers that changed:', len(atleast_one_churn_IDs)
    print 'Number of secure answers that changed:', len(none_churn_IDs) 

    atleast_one_chnage_cnt, none_chnage_cnt = [], []
    for churnID in atleast_one_churn_IDs:
        perChurnID_DF = atleast_one_churn_df[atleast_one_churn_df['PostID']==churnID]    
        r_, c_ = perChurnID_DF.shape 
        atleast_one_chnage_cnt.append(r_)
    for churnID in none_churn_IDs:
        perChurnID_DF = none_churn_df[none_churn_df['PostID']==churnID]    
        r_, c_ = perChurnID_DF.shape 
        none_chnage_cnt.append(r_)    
    compareDists(atleast_one_chnage_cnt, none_chnage_cnt, 'Number of changes per answer')    

if __name__=='__main__':
   answer_file = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ANS_RES.csv'
   answer_df   = pd.read_csv(answer_file)

   ans_churn_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_PY_ANS_HISTORY.csv'
   ans_churn_df_ = pd.read_csv(ans_churn_fil)

   quantifyChanges(answer_df, ans_churn_df_)



