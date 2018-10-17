'''
Akond Rahman 
Oct 16 2018 
Compare code snippets for accepted and non-accepted answers 
'''
from scipy import stats
import pandas as pd
import numpy as np
import cliffsDelta


def compareDists(ls_1, ls_2, type_):
    print "Insecure coding practice:", type_
    print "List#1 values [MEDIAN]:{}, [MEAN]:{}, [COUNT]:{}".format(np.median(list(ls_1)), np.mean(list(ls_1)), len(ls_1))
    print "List#2 values [MEDIAN]:{}, [MEAN]:{}, [COUNT]:{}".format(np.median(list(ls_2)), np.mean(list(ls_2)), len(ls_2))
    try:
        TS, p = stats.mannwhitneyu(list(ls_1), list(ls_2), alternative='greater')
    except ValueError:
        TS, p = 0.01, 0.94
    cliffs_delta = cliffsDelta.cliffsDelta(list(ls_1), list(ls_2))
    print '*'*25
    print 'Pee value:{}, cliffs:{}, type:{}'.format(p, cliffs_delta, type_)
    print '*'*25

def compareAccNonAcc(acc_df, all_df):
    print 'Before: all answer dataframe size:', all_df.shape 
    acc_IDs = acc_df['ID'].tolist()
    reduced_all_df = all_df[~ all_df['ID'].isin(acc_IDs)]
    print 'After: all answer dataframe size:', reduced_all_df.shape 
    types = np.unique( acc_df['TYPE'].tolist() )
    for typ in types:
        acc_insecure_snippet_list = acc_df[acc_df['TYPE']==typ]['INSECURE_SNIPPET_CNT'].tolist()
        non_acc_insecure_snippet_list = reduced_all_df[reduced_all_df['TYPE']==typ]['INSECURE_SNIPPET_CNT'].tolist()

        compareDists(non_acc_insecure_snippet_list, acc_insecure_snippet_list, typ)
        print '~'*100
        compareDists(acc_insecure_snippet_list, non_acc_insecure_snippet_list, typ)
        print '~'*100

if __name__=='__main__':
   acc_ans_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ACC_ANS_RES.csv'
   all_ans_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ANS_RES.csv'

   acc_ans_df = pd.read_csv(acc_ans_fil)
   all_ans_df = pd.read_csv(all_ans_fil)

   compareAccNonAcc(acc_ans_df, all_ans_df)