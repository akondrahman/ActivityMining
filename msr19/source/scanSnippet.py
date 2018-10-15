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
insecure_func_list = ['tempfile.mktemp', 'eval', 'httplib.HTTPSConnection', 'http.client.HTTPSConnection', 'six.moves.http_client.HTTPSConnection', 'telnetlib.*', 'input']
url_list = ['urllib.urlopen', 'urllib.request.urlopen', 'urllib.urlretrieve', 'urllib.request.urlretrieve',
'urllib.URLopener', 'urllib.request.URLopener', 'urllib.FancyURLopener', 'urllib.request.FancyURLopener', 'urllib2.urlopen',
'urllib2.Request', 'six.moves.urllib.request.urlopen', 'six.moves.urllib.request.urlretrieve', 'six.moves.urllib.request .URLopener', 
'six.moves.urllib.request.FancyURLopener']
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


def matchCode(body_para, bodyID_para):
    t_pkl_, t_marshal_, t_hash_, t_cipher_, t_xss_, t_func_, t_url_, t_rand_, t_xml_, t_ftp_ = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
    matches_ = re.findall(regex_string , body_para)
    for match in matches_:
        internal_matches = re.findall(regex_string, match)
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
    return  t_pkl_, t_marshal_, t_hash_, t_cipher_, t_xss_, t_func_, t_url_, t_rand_, t_xml_, t_ftp_ 


def processBody(bodies, full_df):
    dict_={}
    for body in bodies:
        body_df = full_df[full_df['Body']==body]
        body_ID = body_df['Id'].tolist()[0] 
        insecure_tup = matchCode(body, body_ID)
        print insecure_tup
        print '-'*50
        if body_ID not in dict_:
           dict_[body_ID] = insecure_tup
    return dict_


if __name__=='__main__':
   ans_dat = '/Users/akond/Documents/AkondOneDrive/MSR-MiningChallenge/msr19/data/SO_GH_PYTHON_ANS_DETAILS.csv'
   ans_df_ = pd.read_csv(ans_dat)
   bodies  = ans_df_['Body'].tolist()
   full_data_dict = processBody(bodies, ans_df_)
   pickle.dump( full_data_dict, open( 'SNIPPET_INSECURITY_DICT.PKL', 'wb'))     