'''
Topic Modeling 
Akond Rahman 
Oct 17 2018 
'''
import pandas as pd
import numpy as np

def constructQuestionDataset(answer_df, raw_ans_df_, ques_df, out_fil):
    at_least_one_postID_list = np.unique( answer_df[answer_df['INSECURE_SNIPPET_CNT'] > 0 ]['ID'].tolist() )
    none_postID_list         = np.unique( answer_df[answer_df['INSECURE_SNIPPET_CNT'] <= 0 ]['ID'].tolist() )

    at_least_one_ans_df = raw_ans_df_[raw_ans_df_['Id'].isin( at_least_one_postID_list )]
    none_ans_df         = raw_ans_df_[raw_ans_df_['Id'].isin( none_postID_list )]    

    at_least_one_ques_list = np.unique( at_least_one_ans_df['ParentId'].tolist() )
    none_ques_list         = np.unique( none_ans_df['ParentId'].tolist() )
    print 'Questions with at least one insecure answer: {}, no insecure answer:{}'.format(len(at_least_one_ques_list), len(none_ques_list))

    at_least_one_ques_df = ques_df[ques_df['Id'].isin(at_least_one_ques_list)]
    none_ques_df         = ques_df[ques_df['Id'].isin(none_ques_list)]

    at_least_one_ques_df.to_csv('ATLEAST_ONE_' + out_fil )
    none_ques_df.to_csv('NONE_' + out_fil ) 

if __name__=='__main__':
   answer_file = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ANS_RES.csv'
   answer_df   = pd.read_csv(answer_file)

   raw_ans_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_GH_PYTHON_ANS_DETAILS.csv'
   raw_ans_df  = pd.read_csv(raw_ans_fil)

   ques_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_GH_PY_QUES_DETAILS.csv'
   ques_df  = pd.read_csv(ques_fil)

   constructQuestionDataset(answer_df, raw_ans_df, ques_df, '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/QUES_DF.csv')

