'''
Utility file for mining data
Akond Rahman
Oct 30, 2017
Monday
'''
import cliffsDelta
import numpy as np
from scipy import stats 

def makeBoxPlots(h_list, l_list, feature_param):
    data_to_plot = [h_list, l_list,]
    plt.grid()
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_to_plot, showfliers=False)
    ax.set_xticklabels(['H:'+feature_param, 'L:'+feature_param])
    fig.savefig(feature_param + '.png', bbox_inches='tight')
    plt.clf()
    plt.close()

def compareTwoGroups(h_list, l_list, feature_name):
   print 'Filtered ({}): (count:{}, median:{}, mean:{})'.format(feature_name, len(h_list), np.median(h_list), np.mean(h_list))
   print '-'*25
   print 'Non Filtered ({}): (count:{}, median:{}, mean:{})'.format(feature_name, len(l_list), np.median(l_list), np.mean(l_list))
   print '-'*25
   TS, p = stats.mannwhitneyu(h_list, l_list, alternative='greater')
   cliffs_delta = cliffsDelta.cliffsDelta(h_list, l_list)
   print 'TS:{}, pee value:{}, cliffs:{}'.format(TS, p, cliffs_delta)
   print '-'*25
   makeBoxPlots(h_list, l_list, feature_name)
def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret
