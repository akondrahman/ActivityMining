'''
Akond Rahman 
Oct 14, 2018 
Scanning 
'''

##reff: https://docs.openstack.org/bandit/1.4.0/blacklists/blacklist_calls.html

func_list = [ 'pickle.loads', 'pickle.load', 'pickle.Unpickler', 'cPickle.loads', 'cPickle.load', 'cPickle.Unpickler', 
'marshal.loads', 'marshal.load', 'hashlib.md5', 'cryptography.hazmat.primitives .hashes.MD5', 'Crypto.Hash.MD2.new', 
'Crypto.Hash.MD4.new', 'Crypto.Hash.MD5.new', 'Crypto.Cipher.ARC2.new', 'Crypto.Cipher.ARC4.new', 'Crypto.Cipher.Blowfish.new',   
'Crypto.Cipher.DES.new', 'Crypto.Cipher.XOR.new', 'cryptography.hazmat.primitives .ciphers.algorithms.ARC4', 'cryptography.hazmat.primitives .ciphers.algorithms.Blowfish', 
'cryptography.hazmat.primitives .ciphers.algorithms.IDEA', 'cryptography.hazmat.primitives .ciphers.modes.ECB', 
'tempfile.mktemp', 'eval', 'django.utils.safestring.mark_safe', 'httplib.HTTPSConnection', 'http.client.HTTPSConnection', 
'six.moves.http_client .HTTPSConnection', 'urllib.urlopen', 'urllib.request.urlopen', 'urllib.urlretrieve', 'urllib.request.urlretrieve',
'urllib.URLopener', 'urllib.request.URLopener', 'urllib.FancyURLopener', 'urllib.request.FancyURLopener', 'urllib2.urlopen',
'urllib2.Request', 'six.moves.urllib.request.urlopen', 'six.moves.urllib.request .urlretrieve', 'six.moves.urllib.request .URLopener', 
'six.moves.urllib.request .FancyURLopener', 'random.random', 'random.randrange', 'random.randint', 'random.choice', 'random.uniform', 
'random.triangular', 'telnetlib.*', 'xml.etree.cElementTree.parse', 'xml.etree.cElementTree.iterparse', 'xml.etree.cElementTree.fromstring', 
'xml.etree.cElementTree.XMLParser', 'xml.etree.ElementTree.parse', 'xml.etree.ElementTree.iterparse', 'xml.etree.ElementTree.fromstring', 
'xml.etree.ElementTree.XMLParser', 'xml.sax.expatreader.create_parser', 'xml.dom.expatbuilder.parse', 'xml.dom.expatbuilder.parseString',
'xml.sax.parse', 'xml.sax.parseString', 'xml.sax.make_parser', 'xml.dom.minidom.parse', 'xml.dom.minidom.parseString', 
'xml.dom.pulldom.parse', 'xml.dom.pulldom.parseString', 'lxml.etree.parse', 'lxml.etree.fromstring', 'lxml.etree.RestrictedElement', 
'xml.etree.GlobalParserTLS', 'lxml.etree.getDefaultParser', 'lxml.etree.check_docinfo', 'ftplib.*', 'input'
]

if __name__=='__main__':
   print 'Keywords to scan:', len(func_list)