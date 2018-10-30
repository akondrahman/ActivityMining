'''
Akond Rahman 
Oct 30 2018 
Answer to RQ1 
'''
import pandas as pd 
import numpy as np 

def getAllSnippetCount(df_p):
    IDs = np.unique(df_p['ID'].tolist())
    sum_ = 0 
    for ID_ in IDs : 
        ID_df = df_p[df_p['ID']==ID_] 
        ID_snippet_count = np.unique(ID_df['TOT_SNIP'].tolist())[0]
        sum_ = sum_ + ID_snippet_count
    return sum_ 

def getRawOccurences(df_p):
    IDs = np.unique(df_p['ID'].tolist())    
    print 'Total answers:' , len(IDs)
    types = np.unique(df_p['TYPE'].tolist())    
    for type_ in types:
        type_df = df_p[df_p['TYPE']==type_]
        ans_IDs = np.unique( type_df['ID'].tolist() )
        print 'Category:{}, raw count:{}, proportion:{}'.format(type_ , len(ans_IDs) , (len(ans_IDs) / len(IDs) ) * 100 )

if __name__=='__main__':
   the_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/output/IDS_SO_GH_PY_ANS_RES.csv'
   the_df  = pd.read_csv(the_fil)

   print 'All snippets count:', getAllSnippetCount(the_df)
   print 'Occurrences count'
   print '='*100
   getRawOccurences(the_df)
   print '='*100
