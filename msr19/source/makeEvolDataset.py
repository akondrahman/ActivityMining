'''
Akond Rahman 
Oct 16, 2018 
Construct Temporal Dataset 
'''
import cPickle as pickle 
import numpy as np 
import pandas as pd 

def makeEvolDataset(dataframe, out_fil):
    results = []
    months  = np.unique( dataframe['MONTH'].tolist()    )
    print 'Months of data:', len(months)    
    for mon_ in months:
        mon_df_ = dataframe[dataframe['MONTH']==mon_]
        answers = mon_df_['BODY_ID'].tolist()
        ans_cnt = len(answers)
        types   = np.unique(mon_df_['TYPE'].tolist())
        tot_snippets = sum(mon_df_['SNIPPET_CNT'].tolist())
        for type_ in types:
            cnt_typ = mon_df_[mon_df_['TYPE']==type_]['TYPE_COUNT'].tolist()
            cnt_per_ans = round(float(sum(cnt_typ)) / float(ans_cnt), 5)
            snippet_den = round(float(sum(cnt_typ))/float(tot_snippets), 5)
            results.append((mon_, ans_cnt, type_, sum(cnt_typ), cnt_per_ans, snippet_den))
        #print 'Analysis completed for:', mon_
    df_ = pd.DataFrame(results, columns=['MONTH', 'ANS_CNT', 'TYPE', 'INSECURE_SNIPPET_CNT', 'INSECURE_SNIPPET_PROP', 'SNIPPET_DENS'])
    print df_.head()
    df_.to_csv(out_fil)
    

if __name__=='__main__':
#    pkl_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/DF_SO_GH_PY_ANS_DETAILS.PKL'
#    out_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/DF_SO_GH_PY_ANS_RES.csv'

#    pkl_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/DF_SO_GH_PY_ACC_ANS_DETAILS.PKL'
#    out_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/DF_SO_GH_PY_ACC_ANS_RES.csv'

   df_ = pickle.load(open(pkl_fil, 'rb'))
   makeEvolDataset(df_, out_fil)