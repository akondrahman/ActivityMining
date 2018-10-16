'''
Akond Rahman 
Oct 16 2018 
Compare code snippets for accepted and non-accepted answers 
'''
import pandas as pd 
import numpy as np 


def compareAccNonAcc(acc_df, all_df):
    print 'Before: all answer dataframe size:', all_df.shape 
    acc_IDs = acc_df['ID'].tolist()
    for acc_ID in acc_IDs:
        all_df = all_df[all_df['ID'] != acc_ID]
    print 'After: all answer dataframe size:', all_df.shape 
    types = np.unique( acc_df['TYPE'].tolist() )
    # for typ in types:
    #     acc_insecure_snippet_list = acc_df[acc_df['TYPE']==typ]['INSECURE_SNIPPET_PROP'].tolist()
    #     all_insecure_snippet_list = non_acc_df[non_acc_df['TYPE']==typ]['INSECURE_SNIPPET_PROP'].tolist()

if __name__=='__main__':
   acc_ans_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ACC_ANS_RES.csv'
   all_ans_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ANS_RES.csv'

   acc_ans_df = pd.read_csv(acc_ans_fil)
   all_ans_df = pd.read_csv(all_ans_fil)