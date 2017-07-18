# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from scrapy.loader import ItemLoader
from news.items import ExporterItem
import news.settings
import urllib
import os
import re
import MySQLdb as mdb
import sys


class PaycircleNewsSpider(scrapy.Spider):
    name = "paycircle_list"
    allowed_domains = ["paycircle.cn"]
    start_urls = (
        'http://www.paycircle.cn/news/guoneizixun/1.html',
    )

    pipeline = ['CacheFileExporterPersistencePipeline']


    sub_entries=[]

    
    #####
    all_threadid=[]    #爬取之前先取出所有的thread_id,后面碰到重复的就不用再继续了
    #on_which="aliyun"

    is_empty_table=False

    def __init__(self,top_page_count="1",on_which=news.settings.DEFAULT_ON_WHICH,**kwargs):
        self.logger.debug(locals())
        self.on_which=on_which.lower()
        self.top_page_count=int(top_page_count)
        self.__dict__.update(kwargs) ##important


        dbParams=news.settings.allDBParams[on_which]
        tableNames=news.settings.allTableNames[on_which]


        db=mdb.connect(dbParams['addr'],dbParams['username'],dbParams['password'],dbParams['dbname'])
        cur=db.cursor()
        cur.execute("select thread_id from %s"%"paycircle_news")
        
        
        self.all_threadid=[ i[0] for i in cur.fetchall()]
        if len(self.all_threadid)==0:
            self.is_empty_table=True

        print self.all_threadid

        cur.close()
        db.close()


    #####

    def parse(self, response):
    	'''get first level entries'''
    	
    	sub_entries=response.xpath("//div[@class='box_body']/table").xpath(".//a/@href").extract()
    	
    	for i in sub_entries:
    		r=Request.Request(i,callback=self.parse2)
    		yield r
    	


    def parse2(self, response):
    	'''make requests for every single pages of news'''
        pagecount=int(response.xpath("//div[@class='pages']/label/span/text()").extract()[0])

        if self.is_empty_table:
            pagelimit=min(5,pagecount)
        else:
            pagelimit=self.top_page_count

        for i in range(1,min(pagelimit,pagecount)+1):
       		r=Request.Request(response.url+str(i)+".html",self.parse3)
       		yield r

    def parse3(self, response):
    	'''extract all news links from every single page of news'''
        retitem=ExporterItem()

        essays=response.xpath("//div[@class='catlist']/ul").xpath(".//a/@href").extract()
        for essay in essays:
            threadid_essay=essay.split("/")[-1].split(".")[0]            
            #注意数据库内这个字段是int的，要转换类型
            if int(threadid_essay) in self.all_threadid: #如果数据库里有记录，则跳过
                print "%s already crawled in database"%threadid_essay
                pass
            else:
                retitem.set_record(essay)
        
        return retitem


    