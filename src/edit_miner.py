'''
Akond Rahman
Oct 29, 2017
Sunday
Mining Extracted Data
'''
'''
for solution and navigation, the first five columsn will be imported: others all
edit_ds_file   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/LOCKED_ALL_SOLUTION_CONTENT.csv'
edit_df        = pd.read_csv(edit_ds_file, usecols=[0, 1, 2, 3, 4])
'''


import os, time, datetime
import pandas as pd

def giveTimeStamp():

  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

if __name__=='__main__':
   print "Started at:", giveTimeStamp()
   print '='*100
   edit_ds_file   = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/TESTRUN2_ALL_NAVIGATION_CONTENT.csv'
   edit_df        = pd.read_csv(edit_ds_file)
   print edit_df.head()

   print '='*100
   print "Ended at:", giveTimeStamp()
   print '='*100
