# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from scrapy import Request
from scrapy.selector import Selector
from w3lib.html import remove_tags
from SubtitleProject.items import SubtitleProjectItem

class SubtitleSpider(scrapy.Spider):
    name = 'subtitle'
    allowed_domains = ['zimuku.net']
    start_urls = []
    for i in range(1, 10000):
        url = "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=%s" %(str(i))
        start_urls.append(url)

    # cookies = {'__cfduid=dcdad8820861378677ed85eb24ec130961502262529; PHPSESSID=5venv7diioebnrq22gm22vcq67; uv_cookie_118004=1; zmk_home_view_subid=59265; Hm_lvt_ac40dbf364ae6f4f564fa7e28274e286=1502262530; Hm_lpvt_ac40dbf364ae6f4f564fa7e28274e286=1502262581'}
    cookies = {}
    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def parse(self, response):
        hrefs = response.selector.xpath('//div[contains(@class, "persub")]/h1/a/@href').extract()
        for href in hrefs:
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        url = response.selector.xpath('//li[contains(@class, "dlsub")]/div/a/@href').extract()[0]
        print "processing: ", url
        request = scrapy.Request(url, callback=self.parse_file)
        yield request

    def parse_file(self, response):
        name = response.headers['Content-Disposition'].split('"')[1]
        body = response.body
        item = SubtitleProjectItem()
        item['url'] = response.url
        item['name'] = name
        item['body'] = body
        return item
