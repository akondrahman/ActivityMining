'''
Compare interests
Akond Rahman 
Oct 16 2018 
'''
import pandas as pd
import numpy as np
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

def constructList(df_p, interest):
    lis = []
    IDs = np.unique(df_p['ID'].tolist())
    for ID_ in IDs:
        intesrest_val = df_p[df_p['ID']==ID_][interest].tolist()[0]
        lis.append(intesrest_val)
    return lis 

def compareInterests(df_, interest_metric):
    total_df = df_[df_['TYPE']=='TOTAL']

    at_least_one_df = total_df[total_df['INSECURE_SNIPPET_CNT'] > 0 ]
    none_df         = total_df[total_df['INSECURE_SNIPPET_CNT'] <= 0 ]
    
    atleast = constructList(at_least_one_df, interest_metric)
    none    = constructList(none_df, interest_metric)

    compareDists(atleast, none, interest_metric)
    print '~'*100
    compareDists(none, atleast, interest_metric)
    print '~'*100    



if __name__=='__main__':
   file_ = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/INTEREST_SO_GH_PY_ANS_RES.csv'
   df_   = pd.read_csv(file_)
   compareInterests(df_, 'FAVORITE')  #SCORE  VIEW  COMMENT  FAVORITE 
