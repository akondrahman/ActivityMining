'''
Oct 12, 2018 
Akond Rahman 
Script to download Python files 
'''

import urllib
import pandas as pd 
import numpy as np 

def downloadFiles(df_, out_dir_):
    testfile = urllib.URLopener()
    python_file_links =  np.unique( df_['pythonLink'].tolist() )
    cnt = 1
    for link_ in python_file_links:
         file2save = link_.split('/')[-1]
         dir2save  = link_.split('/')[-2]
         out_fil   = out_dir_ + dir2save + '/' + file2save 
         testfile.retrieve(link_, out_fil)
         print 'Download completed for:{}, {} processed so far ...'.format(file2save, cnt)
         cnt += 1 

if __name__=='__main__':
   the_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/OUT_FIL_GH_DAT.csv'
   the_df  = pd.read_csv(the_dat)
   out_dir = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/python_files/'
   downloadFiles(the_df, out_dir) 