#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import time
import user_agents
import random
import sys
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 

try:
    os.mkdir('scp_files')
except:
    pass
    

def get_site_soup(site):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(site,None,{'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':random.choice(user_agents.user_agent_list)
        }),timeout=30).read(),'html.parser')

def get_content(site):
    page_soup = get_site_soup(site)
    page_name = site.split('/')[-1]
    print 'Request successful'
    content = page_soup.find(id="page-content").get_text().split('\n')
    fh = open('scp_files/'+page_name+'.txt','w')
    for i in content:
        if i != '':
            fh.write(i.encode('utf-8')+'\n')
    
def get_page_names(site):
    page_soup = get_site_soup(site)
    page_soup = page_soup.find(id="page-content").find_all('ul')[1:-1]
    for item in page_soup:
        content_list = item.find_all('li')
        for i in content_list:
            result = i.find('a')['href']
            open('content_index.txt','a').write(result+'\n')

def spider_run(site):
    count = 0
    while 1:
        if count == 10:
            break
        try:
            get_content('http://scp-wiki-cn.wikidot.com'+site.strip())
            print site
            break
        except Exception,e:
            count+=1
            print site,e
            time.sleep(2)
def main():
    page_list = range(2,5)
    try:
        os.mkdir('scp_files')
    except:
        print 'dir exists'
    index = open('content_index.txt','r').readlines()
    pool = ThreadPool(30)
    pool.map(spider_run,index)
    pool.close()

main()



