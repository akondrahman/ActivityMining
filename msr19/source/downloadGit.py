'''
Oct 12, 2018 
Akond Rahman 
Script to download Python files 
'''
import os 
import urllib2
import pandas as pd 
import numpy as np 
import cPickle as pickle 

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def downloadFiles(df_, out_dir_):
    inaccessible_list, prior_inaccessible_list = [], []
    python_file_links =  np.unique( df_['GHUrl'].tolist() )
    cnt, err_cnt = 1, 1
    if os.path.exists('INACCESSIBLE.TRACKER.PKL'):
       prior_inaccessible_list = pickle.load(open('INACCESSIBLE.TRACKER.PKL', 'rb'))
    for link_ in python_file_links:
         file2save = link_.split('/')[-1]
         #dir2save  = link_.split('/')[-2]

         repoID = df_[df_['GHUrl']==link_]['RepoId'].tolist()[0]
         splitted_repoID  = repoID.split('/')
         owner, repo_name = splitted_repoID[0], splitted_repoID[1]
         out_fil = out_dir_ + owner + '_' + repo_name + '_' + file2save

         if ((os.path.exists(out_fil) == False) and (link_ not in prior_inaccessible_list)):
            try:
                req = urllib2.Request(link_) 

                resp = urllib2.urlopen(req)
                content = resp.read()
                out_byt = dumpContentIntoFile(content, out_fil)

                print 'Download completed for:{} with `{} bytes` using:{}...'.format(link_, out_byt , out_fil )
            except IOError: 
                print '[IOError] So far not downloaded :{} python files'.format(err_cnt)
                err_cnt += 1 
                inaccessible_list.append(link_)
                pickle.dump( inaccessible_list, open(  'INACCESSIBLE.TRACKER.PKL', 'wb'))          
         print 'So far processed:', cnt
         cnt += 1 
         print '*'*25

    

if __name__=='__main__':
   the_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/PYTHON_OUT_FIL_GH_DAT.csv'
   the_df  = pd.read_csv(the_dat)
   unique_repos = np.unique(the_df['RepoId'].tolist())
   print 'Unqiue repos 2 mine:', len(unique_repos)
   out_dir = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/python_files/'
   downloadFiles(the_df, out_dir) 