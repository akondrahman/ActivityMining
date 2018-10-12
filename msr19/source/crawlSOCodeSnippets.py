'''
Akond Rahman 
Oct 12, 2018 
Mine stack overflow code snippets 
'''
import pandas as pd 
import numpy as np 
from BeautifulSoup import BeautifulSoup
import urllib2
import json 
import os 
import cPickle as pickle


def getCode(html_data):
    code_snippets = []
    unparsed_dumps = html_data.body.findAll('code')
    for code_snippet in unparsed_dumps:
        code_ = str(code_snippet)
        if (('>' in code_) and ('<' in code_)):
            code_str = code_.split('>')[1].split('<')[0]
        else:
            code_str = 'NOT_FOUND'            
        code_snippets.append(code_str)
    return code_snippets

def getTitle(html_data):
    unparsed_dump = html_data.title
    code_ = str(unparsed_dump)
    if (('>' in code_) and ('<' in code_)):
            title_ = code_.split('>')[1].split('<')[0]
    else:
            title_ = 'NOT_FOUND'            
    return title_    

def getUniquePostDetails(df_):
    out_dict = {}
    uni_post_IDs = np.unique(df_['sopostID'].tolist())
    for postID in uni_post_IDs:
            full_url  = 'https://stackoverflow.com/questions/' + str(postID) + '/'
            response_ = urllib2.urlopen(full_url)
            html_dump = response_.read()
            parsed_html    = BeautifulSoup(html_dump)
            code_snippets  = getCode(parsed_html)
            title          = getTitle(parsed_html)    
            if postID not in out_dict: 
                out_dict[postID] = (title, code_snippets)    
    return out_dict

def getPostDetails(df_, py_out_dir_):
    uni_post_dict =getUniquePostDetails(df_)
    out_dic  = {}
    file_cnt = 0 
    python_file_links =  np.unique( df_['pythonLink'].tolist() )
    for link_ in python_file_links:
         file_cnt += 1 
         so_post_IDs = df_[df_['pythonLink']==link_]['sopostID'].tolist()

         file2save = link_.split('/')[-1]
         dir2save  = link_.split('/')[-2]
         dir_      = py_out_dir_ + dir2save 
         if not os.path.exists(dir_):
            os.makedirs(dir_)
         out_fil   = dir_ + '/' + file2save 
         post_details = []
         print 'Processing {}, which has {} posts'.format(link_, len(so_post_IDs))
         uni_so_post_IDs = np.unique(so_post_IDs)
         for postID in uni_so_post_IDs:
             if postID in uni_post_dict:
                title, code_snippets = uni_post_dict[postID]
                post_details.append((postID, title, code_snippets))
         if out_fil not in out_dic:
           out_dic[out_fil] = post_details
    return out_dic



if __name__=='__main__':
   the_dat     = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/OUT_FIL_GH_DAT.csv'
   the_df      = pd.read_csv(the_dat)
   out_dir     = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/'
   py_out_dir  = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/python_files/'
   
   post_gh_dic = getPostDetails(the_df, py_out_dir) 
   pickle.dump( post_gh_dic, open( out_dir + 'GH.PY.SO.TRACKER.PKL', 'wb'))          
