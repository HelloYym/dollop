# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from scrapy.loader import ItemLoader
from news.items import ExporterItem
import os
import re
import time
import urllib
import news.settings
import MySQLdb as mdb
import sys


class WeiyangNewsSpider(scrapy.Spider):
    name = "weiyang_list"
    allowed_domains = ["weiyangx.com"]
    start_urls = (
        'http://www.weiyangx.com/category/tranditional-financial-institution',
        'http://www.weiyangx.com/category/based-on-internet',
        'http://www.weiyangx.com/category/new-modes',
        'http://www.weiyangx.com/category/financial-information-service',
        'http://www.weiyangx.com/category/internet-economy',
        'http://www.weiyangx.com/category/macroscopic-monetary',
        'http://www.weiyangx.com/category/investment-and-financing',
        'http://www.weiyangx.com/category/block-chain',
    )

    pipeline = ['CacheFileExporterPersistencePipeline']

    common_header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.weiyangx.com',
        'Upgrade-Insecure-Requests': '0',
        'Referer': 'http://www.weiyangx.com/',

        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    }

    def start_requests(self):
        for u in self.start_urls:
            yield Request.Request(u, headers=self.common_header, callback=self.parse)

    #####
    all_threadid = []  # 爬取之前先取出所有的thread_id,后面碰到重复的就不用再继续了
    # on_which="aliyun"

    is_empty_table = False

    def __init__(self, top_page_count="5", on_which=news.settings.DEFAULT_ON_WHICH, **kwargs):
        self.logger.debug(locals())
        self.on_which = on_which.lower()
        self.top_page_count = int(top_page_count)
        self.__dict__.update(kwargs)  ##important

        dbParams = news.settings.allDBParams[on_which]
        tableNames = news.settings.allTableNames[on_which]

        db = mdb.connect(dbParams['addr'], dbParams['username'], dbParams['password'], dbParams['dbname'])
        cur = db.cursor()
        cur.execute("select thread_id from %s" % 'weiyang_news')

        self.all_threadid = [i[0] for i in cur.fetchall()]
        if len(self.all_threadid) == 0:
            self.is_empty_table = True

        cur.close()
        db.close()

    #####

    def parse(self, response):
        '''抽取每个分类中的总页数，并对每一页分发请求'''
        # print "[url: %s || status: %s]"%(response.url,response.status)

        pagecount = int(
            response.xpath("//div[@class='page-list-others scroll-style']/a[last()]/@href").extract()[0].split("/")[-2])

        if self.is_empty_table:
            pagelimit = pagecount / 4
        else:
            pagelimit = self.top_page_count

        for i in range(1, min(pagelimit, pagecount) + 1):  # min(3,int(pagecount)+1)):#这个网站更新得也不快
            r = Request.Request(response.url + r"/page/" + str(i), headers=self.common_header, callback=self.parse2)
            yield r

    def parse2(self, response):
        '''此时获取到新闻列表页，抽取新闻列表页中的所有新闻链接'''
        # print "[url: %s || status: %s]"%(response.url,response.status)
        retitem = ExporterItem()

        essays = response.xpath('//div[@class="uk-width-1-1 uk-clearfix category-post-node"]/a/@href').extract()

        for essay in essays:
            threadid_essay = essay.split("/")[-1].split(".")[0]
            # 注意数据库内这个字段是int的，要转换类型
            if int(threadid_essay) in self.all_threadid:  # 如果数据库里有记录，则跳过
                print("%s already crawled in database" % threadid_essay)
                pass
            else:
                retitem.set_record(essay)

        return retitem
