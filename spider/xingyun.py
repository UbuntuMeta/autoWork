# -*- coding: utf-8 -*-
import requests, time, string
from bs4 import BeautifulSoup

def getGoodChannel(content):
	if len(content) <= 0:
		return ''
	allLinks = BeautifulSoup(content, 'html.parser').find_all("tr")
	greenLinks = []
	for link in allLinks:
		if "良好" in str(link):
			greenLinks.append(link)
	
	return '<br/>'.join(str(v) for v in greenLinks)
	 
def loginAndGet(username,password):
    sessiona = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    data = {
        "authenticity_token" : "XPUWie8/pucc/HjUFnAjA9fYrhcLWm/aNjq0oemgGKY=",
        "email":username,
        "password":password,
        "commit": "登 录",
        "act": "login"
    }
	
    resp = sessiona.post('http://home.dutoo.net/portal/login',data,headers=headers).content
    content = sessiona.get('http://home.dutoo.net/home/main_servers').content
    # 单独采集那些状态良好的线路
    content = getGoodChannel(content)
   
    with open('todayVpn.html','w') as f:
            f.write(content)
            print("create  file success!")
 
if __name__ == "__main__":
    loginAndGet('xxxx.com','2323233ddd')