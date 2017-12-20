#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import user_agents
import random
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 

get_site_soup =lambda site:BeautifulSoup(urllib2.urlopen(urllib2.Request(site,None,{'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6','X-Requested-With':'XMLHttpRequest','User-Agent':random.choice(user_agents.user_agent_list)}),timeout=30).read(),'html.parser')
get_content = lambda site: get_site_soup(site).find(id="page-content").get_text().split('\n')
get_line_json_list = lambda site: [{'index':site.split('/')[-1].strip(),'content':content} for content in get_content(site)]
write_line = lambda line: open('scp_files/'+line['index']+'.txt','a').write(line['content'].strip().encode('utf-8')+'\n') if len(line['content']) is not 0 else 0 
write_content = lambda site:map(write_line,get_line_json_list('http://scp-wiki-cn.wikidot.com'+site))
main = lambda:ThreadPool(4).map(write_content,open('content_index.txt').readlines())

main()
