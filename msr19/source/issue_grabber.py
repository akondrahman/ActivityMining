'''
Dec 23, 2018 
Script to extract issues for one repo 
'''

import json 
import requests
import cPickle as pickle 


def getIssues():

    list_of_dicts = []
    for x_ in xrange(155):
        x_ = x_ + 1
        print 'Processing page#', x_ 
        issue_response = requests.get("https://api.github.com/repos/JuliaLang/julia/issues?page=" + str(x_) + "&per_page=100", headers={ 'Authorization': 'token <TOKEN_GOES_HERE>'})
        issues_dict = json.loads(issue_response.text) 
        list_of_dicts.append(issues_dict)

    print '='*50

    cnt = 0 
    for issues_dict_ in list_of_dicts:
        for issue in issues_dict_:
            print issue
            cnt += 1 
    print 'Total issues:', cnt 

    print '='*50

    with open('PAGINATED_ISSUES_JSON_PKL', 'wb') as f_:
        pickle.dump(list_of_dicts, f_)

    print '='*50

def processIssues(lis): 
    cnt = 0  
    for issues_dict_ in lis:
        issue_num = 0 
        issue_state = 'closed'
        for issue in issues_dict_:
            if 'state' in issue:
                issue_state = issue['state']
            if 'number' in issue:
                issue_num = issue['number']
            if 'labels' in issue:
                issue_labels = issue['labels'] 
                for labe in issue_labels:
                    if 'name' in labe:  
                        label_name = labe['name']
                        print  issue_num, issue_state,  label_name
            cnt += 1 
    print 'Total issues:', cnt 


if __name__=='__main__':
   getIssues() 


#    fileName = 'PAGINATED_ISSUES_JSON_PKL'
#    pkl_lis = pickle.load(open(fileName, 'rb'))  ## list of lists 
#    processIssues(pkl_lis)