# -*- coding: utf-8 -*-

'''
Created on 2016-07-13

@author: freemannow
@email: fightforphp@gmail.com
'''
import urllib2
import re
from bs4 import BeautifulSoup
import random
import time
import sys


class Csdn(object):

    def __init__(self,url):

        self.url = url
        self.user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        ]
        # self.ip_list = ['60.220.204.2:63000', '123.150.92.91:80',
        #               '121.248.150.107:8080', '61.185.21.175:8080', 
        #               '222.216.109.114:3128', '118.144.54.190:8118', 
        #               '1.50.235.82:80', '203.80.144.4:80']

        print "spider is going to work!\n"

    def open(self):
        # ip = random.choice(self.ip_list)
        # print '使用的代理ip地址： ' + ip
        # proxy_support = urllib2.ProxyHandler({'http': 'http://' + ip})
        # opener = urllib2.build_opener(proxy_support)
        # urllib2.install_opener(opener)

        agent = random.choice(self.user_agents)
        req = urllib2.Request(self.url)

        req.add_header('User-Agent', agent)
        req.add_header('Host', 'blog.csdn.net')

        req.add_header('Accept', '*/*')
        req.add_header(
            'Referer', 'http://blog.csdn.net/mangoer_ys?viewmode=list')
        req.add_header('GET', self.url)
        html = urllib2.urlopen(req)

        page_type = sys.getfilesystemencoding()
        page = html.read().decode("UTF-8").encode(page_type)  # 关键

        self.page = page
        self.title = self.getTitle()
        self.content = self.getContent()
        print self.title
        self.store()

    def getTitle(self):
        rex = re.compile('<title>(.*?)</title>', re.DOTALL)
        match = rex.search(self.page)
        if match:
            return match.group(1)

        return 'NO TITLE'


    def getContent(self):
        bs = BeautifulSoup(self.page, 'html.parser', from_encoding="gb18030")
        #print bs
        html_content_list = bs.findAll('div',{'id':'article_content','class':'article_content'})
        html_content = str(html_content_list[0])
        #print html_content

        rex_p = re.compile(r'(?:.*?)>(.*?)<(?:.*?)',re.DOTALL)
        p_list = rex_p.findall(html_content)

        
        return "".join(p_list)
        
    def getNextArticle(self):
        bs2 = BeautifulSoup(self.page, 'html.parser', from_encoding="gb18030")
        html_nextArticle_list = bs2.findAll('li',{'class':'prev_article'})
        # print str(html_nextArticle_list[0])
        if len(html_nextArticle_list) >0 :
            html_nextArticle = str(html_nextArticle_list[0])
        else:
            return None
        # print html_nextArticle

        rex_link = re.compile(r'<a href=\"(.*?)\"',re.DOTALL)
        link = rex_link.search(html_nextArticle)

        if link:
            next_url = 'http://blog.csdn.net' + link.group(1)
            return next_url

        return None

    def store(self):
        self.saveFile()
        # self.storeToMysql()


    def saveFile(self):
        outfile = open('new2.txt','a')
        outfile.write(self.content)
        outfile.close()

    def printInfo(self):
        print(u"已下载 url:" + self.url + '\n')



def main():
    sys.setrecursionlimit(1000000000) 
    #start_url = raw_input('请输入开始的url:')
    #http://blog.csdn.net/youzhouliu/article/details/51821195
    #http://blog.csdn.net/youzhouliu/article/details/51908700
    start_url = 'http://blog.csdn.net/youzhouliu/article/details/51821195'
    csdn = Csdn(start_url)
    csdn.open()
    csdn.printInfo()

    next_url = csdn.getNextArticle()

    while True:
        if next_url == None:
            print 'nothing to download!'
            break
        if csdn.url != next_url:
            csdn.url = next_url
            csdn.open()
            csdn.printInfo()
            
        elif csdn.url == next_url:
            print 'All article haved been downloaded!'
            break
        next_url = csdn.getNextArticle()


if __name__ == "__main__":
    main()
