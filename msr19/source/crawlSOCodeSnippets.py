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
    unparsed_dump = html_data.body.find('title')
    code_ = str(unparsed_dump)
    if (('>' in code_) and ('<' in code_)):
            title_ = code_.split('>')[1].split('<')[0]
    else:
            title_ = 'NOT_FOUND'            
    return title_    

def getPostDetails(df_, out_dir):
    python_file_links =  np.unique( df_['pythonLink'].tolist() )
    for link_ in python_file_links:
         so_post_IDs = df_[df_['pythonLink']==link_]['sopostID'].tolist()
         for postID in so_post_IDs:
            full_url  = 'https://stackoverflow.com/questions/' + str(postID) + '/'
            response_ = urllib2.urlopen(full_url)
            html_dump = response_.read()
            parsed_html    = BeautifulSoup(html_dump)
            code_snippets  = getCode(parsed_html)
            title          = getTitle(parsed_html)
            print full_url, title
            print code_snippets
            print '='*50




if __name__=='__main__':
   the_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/OUT_FIL_GH_DAT.csv'
   the_df  = pd.read_csv(the_dat)
   out_dir = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/so_code_snippets/'
   getPostDetails(the_df, out_dir) 
