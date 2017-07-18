# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from scrapy.loader import ItemLoader
from news.items import ExporterItem
import os
import re
import urllib
import news.settings
import MySQLdb as mdb

class JrzjNewsSpider(scrapy.Spider):
    name = "jrzj_list"
    allowed_domains = ["jrzj.com"]
    start_urls = (
        'http://www.jrzj.com/global/',
        'http://www.jrzj.com/fund/',
        'http://www.jrzj.com/p2p/',
        'http://www.jrzj.com/insurance/',
        'http://www.jrzj.com/vcpe/',
        'http://www.jrzj.com/zhongchou/',
    )

    pipeline = ['CacheFileExporterPersistencePipeline']


    #####
    all_threadid=[]    #爬取之前先取出所有的thread_id,后面碰到重复的就不用再继续了
    #on_which="aliyun"

    is_empty_table=False

    def __init__(self,top_page_count="10",on_which=news.settings.DEFAULT_ON_WHICH,**kwargs):
        self.logger.debug(locals())
        self.on_which=on_which.lower()
        self.top_page_count=int(top_page_count)
        self.__dict__.update(kwargs) ##important
        

        dbParams=news.settings.allDBParams[on_which]
        tableNames=news.settings.allTableNames[on_which]


        db=mdb.connect(dbParams['addr'],dbParams['username'],dbParams['password'],dbParams['dbname'])
        cur=db.cursor()
        cur.execute("select thread_id from %s"%'jrzj_news')
        
        
        self.all_threadid=[ i[0] for i in cur.fetchall()]
        if len(self.all_threadid)==0:
            self.is_empty_table=True

        #print self.all_threadid

        cur.close()
        db.close()


    #####


    def parse(self, response):
    	'''make requests for every single pages of news'''
        pagecount=int(response.xpath("//div[@class='fy_big']/a[last()-1]/text()").extract()[0])

        common_suffix=response.xpath("//div[@class='fy_big']/a[last()-1]/@href").extract()[0]
        common_suffixes=common_suffix.split('-')

        if self.is_empty_table:
            pagelimit=pagecount/4
        else:
            pagelimit=self.top_page_count#10 对于金融之家这个要大一点，更新的比较频繁

        for i in range(1,min(pagelimit,pagecount)+1):#min(5,int(pagecount)+1)): # we assume that newly added news will not surpass 5 pages 
            #int(pagecount)+1):
       		r=Request.Request(response.url+common_suffixes[0]+"-"+common_suffixes[1]+"-"+str(i)+"-"+common_suffixes[3],callback=self.parse2)
       		#r.meta['grandfather']=response.meta['grandfather']
       		#r.meta['father']=essay
       		yield r

    def parse2(self, response):
    	'''extract all news links from every single page of news'''
        retitem=ExporterItem()
        essays=response.xpath("//div[@class='infor_line']/a/@href").extract()

        for essay in essays:
            threadid_essay=essay.split("/")[-1].split(".")[0]
            if not threadid_essay.isdigit(): #有些zf开头的奇怪链接
                continue
            #注意数据库内这个字段是int的，要转换类型
            if int(threadid_essay) in self.all_threadid: #如果数据库里有记录，则跳过
                print "%s already crawled in database"%threadid_essay
                pass
            else:
                retitem.set_record(essay)
                #r=Request.Request(essay,self.parse3,meta={"m_cat":response.meta["m_cat"]})
                #yield r
        return retitem


    