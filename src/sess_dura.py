'''
Session Duration
Akond Rahman
Dec 07, 2017
'''

def makeTimeHuman(single_val):
    #2016-05-17T01:28:02.8130763+02:00 , timestamp string
    dt_  = single_val.split('T')[1]
    ts_  = dt_.split('+')[0]
    x = time.strptime(ts_.split('.')[0],'%H:%M:%S')
    second2ret = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return second2ret


def getDuration(df_param):
    df_param['FORMATTED_TIME'] = df_param['TIME'].apply(makeTimeHuman)
    all_time_sec = df_param['FORMATTED_TIME'].tolist()
    sta, end = min(all_time_sec), max(all_time_sec)
    dur = end - sta
    return dur


def getSessionDuration(file_path):
   all_dur = []
   full_df   = pd.read_csv(file_path)
   allSessIDs = np.unique(df2ret['SESS_ID'].tolist())
   print '='*50
   print 'UNIQUE SESSION COUNT:', len(allSessIDs)
   print '-'*50
   for sessID in allSessIDs:
       per_sess_df = full_df[full_df['SESS_ID']==sessID]
       per_sess_dura = getDuration(per_sess_df)
       tup = (sessID, per_sess_dura)
       all_dur.append(tup)
   dura_df_ = pd.DataFrame.from_records(all_dur, columns=['SESS_ID', 'DURA'])
   ### Summary of all data
   print dura_df_.describe()
   return dura_df_

if __name__=='__main__':
  file_name  = '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/datasets/LOCKED_ALL_COMMAND_CONTENT.csv'
  all_sess_dur =getSessionDuration(file_name) ### all_sess_dur is a datgrame where duration is measured in seconds
