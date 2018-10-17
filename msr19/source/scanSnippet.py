'''
Akond Rahman 
Oct 13, 2018 
Scan code snippet 
'''
import pandas as pd 
import re 
import cPickle as pickle 

regex_string = r'code>.*</code'

'''
##reff: https://docs.openstack.org/bandit/1.4.0/blacklists/blacklist_calls.html

func_list = [ 'pickle.loads', 'pickle.load', 'pickle.Unpickler', 'cPickle.loads', 'cPickle.load', 'cPickle.Unpickler', 
'marshal.loads', 'marshal.load', 'hashlib.md5', 'cryptography.hazmat.primitives .hashes.MD5', 'Crypto.Hash.MD2.new', 
'Crypto.Hash.MD4.new', 'Crypto.Hash.MD5.new', 'Crypto.Cipher.ARC2.new', 'Crypto.Cipher.ARC4.new', 'Crypto.Cipher.Blowfish.new',   
'Crypto.Cipher.DES.new', 'Crypto.Cipher.XOR.new', 'cryptography.hazmat.primitives .ciphers.algorithms.ARC4', 'cryptography.hazmat.primitives .ciphers.algorithms.Blowfish', 
'cryptography.hazmat.primitives .ciphers.algorithms.IDEA', 'cryptography.hazmat.primitives .ciphers.modes.ECB', 
'tempfile.mktemp', 'eval', 'django.utils.safestring.mark_safe', 'httplib.HTTPSConnection', 'http.client.HTTPSConnection', 
'six.moves.http_client.HTTPSConnection', 'urllib.urlopen', 'urllib.request.urlopen', 'urllib.urlretrieve', 'urllib.request.urlretrieve',
'urllib.URLopener', 'urllib.request.URLopener', 'urllib.FancyURLopener', 'urllib.request.FancyURLopener', 'urllib2.urlopen',
'urllib2.Request', 'six.moves.urllib.request.urlopen', 'six.moves.urllib.request.urlretrieve', 'six.moves.urllib.request .URLopener', 
'six.moves.urllib.request.FancyURLopener', 'random.random', 'random.randrange', 'random.randint', 'random.choice', 'random.uniform', 
'random.triangular', 'telnetlib.*', 'xml.etree.cElementTree.parse', 'xml.etree.cElementTree.iterparse', 'xml.etree.cElementTree.fromstring', 
'xml.etree.cElementTree.XMLParser', 'xml.etree.ElementTree.parse', 'xml.etree.ElementTree.iterparse', 'xml.etree.ElementTree.fromstring', 
'xml.etree.ElementTree.XMLParser', 'xml.sax.expatreader.create_parser', 'xml.dom.expatbuilder.parse', 'xml.dom.expatbuilder.parseString',
'xml.sax.parse', 'xml.sax.parseString', 'xml.sax.make_parser', 'xml.dom.minidom.parse', 'xml.dom.minidom.parseString', 
'xml.dom.pulldom.parse', 'xml.dom.pulldom.parseString', 'lxml.etree.parse', 'lxml.etree.fromstring', 'lxml.etree.RestrictedElement', 
'xml.etree.GlobalParserTLS', 'lxml.etree.getDefaultParser', 'lxml.etree.check_docinfo', 'ftplib.*', 'input'
]
'''

pickle_list  = ['pickle.loads', 'pickle.load', 'pickle.Unpickler', 'cPickle.loads', 'cPickle.load', 'cPickle.Unpickler']
marshal_list = ['marshal.loads', 'marshal.load']
wrong_hash_list = ['hashlib.md5', 'cryptography.hazmat.primitives .hashes.MD5', 'Crypto.Hash.MD2.new', 'Crypto.Hash.MD4.new', 'Crypto.Hash.MD5.new']
insecure_cipher_list = ['Crypto.Cipher.ARC2.new', 'Crypto.Cipher.ARC4.new', 'Crypto.Cipher.Blowfish.new',   
'Crypto.Cipher.DES.new', 'Crypto.Cipher.XOR.new', 'cryptography.hazmat.primitives.ciphers.algorithms.ARC4', 'cryptography.hazmat.primitives.ciphers.algorithms.Blowfish', 
'cryptography.hazmat.primitives.ciphers.algorithms.IDEA', 'cryptography.hazmat.primitives .ciphers.modes.ECB']
xss_scripting_list =  ['django.utils.safestring.mark_safe']
insecure_func_list = ['tempfile.mktemp', 'eval', 'httplib.HTTPSConnection', 'http.client.HTTPSConnection', 'six.moves.http_client.HTTPSConnection', 'telnetlib.*', 'input', 'mktemp']
url_list = ['urllib.urlopen', 'urllib.request.urlopen', 'urllib.urlretrieve', 'urllib.request.urlretrieve',
'urllib.URLopener', 'urllib.request.URLopener', 'urllib.FancyURLopener', 'urllib.request.FancyURLopener', 'urllib2.urlopen',
'urllib2.Request', 'six.moves.urllib.request.urlopen', 'six.moves.urllib.request.urlretrieve', 'six.moves.urllib.request .URLopener', 
'six.moves.urllib.request.FancyURLopener', 'urlopen', 'urlretrieve']
random_list = ['random.random', 'random.randrange', 'random.randint', 'random.choice', 'random.uniform', 'random.triangular']
xml_list = ['xml.etree.cElementTree.parse', 'xml.etree.cElementTree.iterparse', 'xml.etree.cElementTree.fromstring', 
'xml.etree.cElementTree.XMLParser', 'xml.etree.ElementTree.parse', 'xml.etree.ElementTree.iterparse', 'xml.etree.ElementTree.fromstring', 
'xml.etree.ElementTree.XMLParser', 'xml.sax.expatreader.create_parser', 'xml.dom.expatbuilder.parse', 'xml.dom.expatbuilder.parseString',
'xml.sax.parse', 'xml.sax.parseString', 'xml.sax.make_parser', 'xml.dom.minidom.parse', 'xml.dom.minidom.parseString', 
'xml.dom.pulldom.parse', 'xml.dom.pulldom.parseString', 'lxml.etree.parse', 'lxml.etree.fromstring', 'lxml.etree.RestrictedElement', 
'xml.etree.GlobalParserTLS', 'lxml.etree.getDefaultParser', 'lxml.etree.check_docinfo']
ftp_list = ['ftplib.*']

def matchSecurityWords(code_str):
    pkl_match_cnt, marshal_match_cnt, hash_match_cnt, cipher_match_cnt, xss_match_cnt, func_match_cnt, url_match_cnt, rand_match_cnt, xml_match_cnt, ftp_match_cnt = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 

    pkl_match_list = [kw for kw in pickle_list if kw in code_str]
    pkl_match_cnt  = len(pkl_match_list)

    marshal_match_list = [kw for kw in marshal_list if kw in code_str]
    marshal_match_cnt  = len(marshal_match_list)    

    hash_match_list = [kw for kw in wrong_hash_list if kw in code_str]
    hash_match_cnt  = len(hash_match_list)

    cipher_match_list = [kw for kw in insecure_cipher_list if kw in code_str]
    cipher_match_cnt  = len(cipher_match_list)        

    xss_match_list = [kw for kw in xss_scripting_list if kw in code_str]
    xss_match_cnt  = len(xss_match_list)    

    func_match_list = [kw for kw in insecure_func_list if kw in code_str]
    func_match_cnt  = len(func_match_list)

    url_match_list = [kw for kw in url_list if kw in code_str]
    url_match_cnt  = len(url_match_list)            

    rand_match_list = [kw for kw in random_list if kw in code_str]
    rand_match_cnt  = len(rand_match_list)    

    xml_match_list = [kw for kw in xml_list if kw in code_str]
    xml_match_cnt  = len(xml_match_list)

    ftp_match_list = [kw for kw in ftp_list if kw in code_str]
    ftp_match_cnt  = len(ftp_match_list)                

    return pkl_match_cnt, marshal_match_cnt, hash_match_cnt, cipher_match_cnt, xss_match_cnt, func_match_cnt, url_match_cnt, rand_match_cnt, xml_match_cnt, ftp_match_cnt

def matchCode(body_para):
    snippets = 0 
    t_pkl_, t_marshal_, t_hash_, t_cipher_, t_xss_, t_func_, t_url_, t_rand_, t_xml_, t_ftp_ = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
    matches_ = re.findall(regex_string , body_para)
    snippets = snippets + len(matches_)
    for match in matches_:
        internal_matches = re.findall(regex_string, match)
        snippets = snippets + len(internal_matches)
        for a_match in internal_matches:
            pkl_, marshal_, hash_, cipher_, xss_, func_, url_, rand_, xml_, ftp_ = matchSecurityWords(a_match)
            t_pkl_ = t_pkl_ + pkl_
            t_marshal_ = t_marshal_ + marshal_
            t_hash_ = t_hash_ + hash_
            t_cipher_ = t_cipher_ + cipher_
            t_xss_ = t_xss_ + xss_
            t_func_ = t_func_ + func_
            t_url_ = t_url_ + url_
            t_rand_ = t_rand_ + rand_
            t_xml_ = t_xml_ + xml_
            t_ftp_  = t_ftp_ + ftp_

            pkl_, marshal_, hash_, cipher_, xss_, func_, url_, rand_, xml_, ftp_ = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
    return  [t_pkl_, t_marshal_, t_hash_, t_cipher_, t_xss_, t_func_, t_url_, t_rand_, t_xml_, t_ftp_, snippets] 

def matchVersionCode(body_para):
        t_pkl_, t_marshal_, t_hash_, t_cipher_, t_xss_, t_func_, t_url_, t_rand_, t_xml_, t_ftp_ = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 

        pkl_, marshal_, hash_, cipher_, xss_, func_, url_, rand_, xml_, ftp_ = matchSecurityWords(body_para)
        t_pkl_ = t_pkl_ + pkl_
        t_marshal_ = t_marshal_ + marshal_
        t_hash_ = t_hash_ + hash_
        t_cipher_ = t_cipher_ + cipher_
        t_xss_ = t_xss_ + xss_
        t_func_ = t_func_ + func_
        t_url_ = t_url_ + url_
        t_rand_ = t_rand_ + rand_
        t_xml_ = t_xml_ + xml_
        t_ftp_  = t_ftp_ + ftp_

        pkl_, marshal_, hash_, cipher_, xss_, func_, url_, rand_, xml_, ftp_ = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
        return  t_pkl_, t_marshal_, t_hash_, t_cipher_, t_xss_, t_func_, t_url_, t_rand_, t_xml_, t_ftp_     


def processBody(bodies, full_df):
    list_ = []
    cnt_ = 0
    for body in bodies:
        body_df = full_df[full_df['Body']==body]
        body_ID = body_df['Id'].tolist()[0] 
        post_ID = body_df['ParentId'].tolist()[0] 
        createDate = body_df['CreateDate'].tolist()[0] 
        score = body_df['Score'].tolist()[0] 
        view = body_df['Views'].tolist()[0] 
        comment = body_df['Comments'].tolist()[0] 
        favs = body_df['Favorites'].tolist()[0] 

        insecure_tup_with_snippets = matchCode(body)
        snip_cnt = insecure_tup_with_snippets.pop()
        insecure_tup = [x_ for x_ in insecure_tup_with_snippets]
        tot_insecurities = sum(insecure_tup)
        print body_ID
        print tot_insecurities,  insecure_tup
        print '{} left'.format(len(bodies) - cnt_ )
        print '-'*50
        x_      = body_df['CreateDate'].tolist()[0] 
        createDate = x_.split('-')[0] + '-' + x_.split('-')[1]

        list_.append((body_ID, 'TOTAL',   tot_insecurities, post_ID, createDate, snip_cnt, score, view, comment, favs))
        list_.append((body_ID, 'PICKLE',  insecure_tup[0], post_ID, createDate,  snip_cnt, score, view, comment, favs))        
        list_.append((body_ID, 'MARSHAL', insecure_tup[1], post_ID, createDate,  snip_cnt, score, view, comment, favs))
        list_.append((body_ID, 'HASH',    insecure_tup[2], post_ID, createDate,  snip_cnt, score, view, comment, favs))         
        list_.append((body_ID, 'CIPHER',  insecure_tup[3], post_ID, createDate,  snip_cnt, score, view, comment, favs))        
        list_.append((body_ID, 'XSS',     insecure_tup[4], post_ID, createDate,  snip_cnt, score, view, comment, favs))
        list_.append((body_ID, 'FUNC',    insecure_tup[5], post_ID, createDate,  snip_cnt, score, view, comment, favs))                        
        list_.append((body_ID, 'URL',     insecure_tup[6], post_ID, createDate,  snip_cnt, score, view, comment, favs))         
        list_.append((body_ID, 'RAND',    insecure_tup[7], post_ID, createDate,  snip_cnt, score, view, comment, favs))        
        list_.append((body_ID, 'XML',     insecure_tup[8], post_ID, createDate,  snip_cnt, score, view, comment, favs))
        list_.append((body_ID, 'FTP',     insecure_tup[9], post_ID, createDate,  snip_cnt, score, view, comment, favs))         
        
        cnt_ += 1
    df_ = pd.DataFrame(list_, columns=['BODY_ID', 'TYPE', 'TYPE_COUNT', 'PARENT_ID', 'MONTH', 'SNIPPET_CNT', 'SCORE', 'VIEW', 'COMMENT', 'FAVORITE'])
    return df_

def processVersionBody(bodies, full_df):
    list_ = []
    cnt_ = 0
    for body in bodies:
        body_df = full_df[full_df['Body']==body]
        body_ID = body_df['Id'].tolist()[0] 
        post_ID = body_df['PostId'].tolist()[0] 
        insecure_tup = matchVersionCode(body)
        tot_insecurities = sum(insecure_tup)
        print body_ID
        print tot_insecurities,  insecure_tup
        print '{} left'.format(len(bodies) - cnt_ )
        print '-'*50
        x_      = body_df['CreateDate'].tolist()[0] 
        createDate = x_.split('-')[0] + '-' + x_.split('-')[1]
        list_.append((body_ID, 'TOTAL',   tot_insecurities, post_ID, createDate))
        list_.append((body_ID, 'PICKLE',  insecure_tup[0], post_ID, createDate))        
        list_.append((body_ID, 'MARSHAL', insecure_tup[1], post_ID, createDate))
        list_.append((body_ID, 'HASH',    insecure_tup[2], post_ID, createDate))         
        list_.append((body_ID, 'CIPHER',  insecure_tup[3], post_ID, createDate))        
        list_.append((body_ID, 'XSS',     insecure_tup[4], post_ID, createDate))
        list_.append((body_ID, 'FUNC',    insecure_tup[5], post_ID, createDate))                        
        list_.append((body_ID, 'URL',     insecure_tup[6], post_ID, createDate))         
        list_.append((body_ID, 'RAND',    insecure_tup[7], post_ID, createDate))        
        list_.append((body_ID, 'XML',     insecure_tup[8], post_ID, createDate))
        list_.append((body_ID, 'FTP',     insecure_tup[9], post_ID, createDate))         
        cnt_ += 1
    df_ = pd.DataFrame(list_, columns=['BODY_ID', 'TYPE', 'COUNT', 'PARENT_ID', 'MONTH'])
    return df_


if __name__=='__main__':
   ans_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_GH_PYTHON_ANS_DETAILS.csv'
   out_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/DF_SO_GH_PY_ANS_DETAILS.PKL'
   
#    ans_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_GH_PY_ACC_ANS_DETAILS.csv'
#    out_fil = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/DF_SO_GH_PY_ACC_ANS_DETAILS.PKL'

   ans_df_ = pd.read_csv(ans_dat)
   bodies  = ans_df_['Body'].tolist()
   
   full_data_df = processBody(bodies, ans_df_)
   print full_data_df.head()

   ## for version code 
   #full_data_dict = processVersionBody(bodies, ans_df_)

   pickle.dump( full_data_df, open( out_fil, 'wb'))     