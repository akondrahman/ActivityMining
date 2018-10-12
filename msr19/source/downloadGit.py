'''
Oct 12, 2018 
Akond Rahman 
Script to download Python files 
'''
import os 
import urllib
import pandas as pd 
import numpy as np 
import cPickle as pickle 

def downloadFiles(df_, out_dir_):
    tracker_dict = {}
    testfile = urllib.URLopener()
    python_file_links =  np.unique( df_['pythonLink'].tolist() )
    cnt, err_cnt = 1, 1
    for link_ in python_file_links:
         file2save = link_.split('/')[-1]
         dir2save  = link_.split('/')[-2]
         dir_      = out_dir_ + dir2save 
         if not os.path.exists(dir_):
            os.makedirs(dir_)
         out_fil   = dir_ + '/' + file2save 
         if os.path.exists(out_fil) == False:
            try:
                testfile.retrieve(link_, out_fil)
                print 'Download completed for:{}, {} processed so far ...'.format(file2save, cnt)
            except IOError: 
                print 'So far not downloaded :{} python files'.format(err_cnt)
                err_cnt += 1 
         cnt += 1 
         '''
         keep track of IDs so that it can be mapped later on 
         '''
         link_specific_df = df_[df_['pythonLink']==link_]
         if out_fil not in tracker_dict:
            tracker_dict[out_fil] = link_specific_df
    pickle.dump( tracker_dict, open( out_dir_ + 'GH.PY.TRACKER.PKL', 'wb'))          
    

if __name__=='__main__':
   the_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/OUT_FIL_GH_DAT.csv'
   the_df  = pd.read_csv(the_dat)
   out_dir = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/python_files/'
   downloadFiles(the_df, out_dir) 