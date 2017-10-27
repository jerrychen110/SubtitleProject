# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import urllib
import urllib2
import requests
import pycurl
import StringIO
class SubtitleProjectPipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        #file_name = url.replace('/','_').replace(':','_')
        file_name = item['name']
        new_file_name = file_name.decode('utf-8')
        
        ##### init the env ###########
        c = pycurl.Curl()
        c.setopt(pycurl.COOKIEFILE, "cookie_file_name")#把cookie保存在该文件中
        c.setopt(pycurl.COOKIEJAR, "cookie_file_name")
        c.setopt(pycurl.FOLLOWLOCATION, 1) #允许跟踪来源
        c.setopt(pycurl.MAXREDIRS, 5)
        #设置代理 如果有需要请去掉注释，并设置合适的参数
        #c.setopt(pycurl.PROXY, 'http://11.11.11.11:8080')
        #c.setopt(pycurl.PROXYUSERPWD, 'aaa:aaa')
        ########### get the data && save to file ###########
        head = ['Accept:*/*','User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0']
        buf = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, buf.write)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER,  head)
        c.perform()
        the_page =buf.getvalue()
        buf.close()
        f = open('F:/nltk_work/SubtitleProject/SubtitleProject/result/'+new_file_name, 'wb')
        f.write(the_page)
        f.close()
        #fp = open('F:/nltk_work/SubtitleProject/SubtitleProject/result/'+file_name, 'w')
        #fp.write(item['body'])
        #fp.close()
        return item
