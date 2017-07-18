# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse as HR
import os
import re
import time
import urllib
import news.settings
import MySQLdb as mdb

from scrapy.loader import ItemLoader
from news.items import ExporterItem
from selenium import webdriver

class HujinzhentanListSpider(scrapy.Spider):
    name = "hujinzhentan_list"
    allowed_domains = ["example.com"]
    start_urls = (
    	"http://www.example.com", #no use
        
    )

    pipeline = ['CacheFileExporterPersistencePipeline']

    common_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'DNT':'1',
'Host':'www.weiyangx.com',
'Upgrade-Insecure-Requests':'0',
'Referer':'http://www.weiyangx.com/',

'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
             }

    #####
    #all_threadid=[]    #爬取之前先取出所有的thread_id,后面碰到重复的就不用再继续了
    #on_which="aliyun"

    #is_empty_table=False

    def __init__(self,top_page_count="5",on_which=news.settings.DEFAULT_ON_WHICH,**kwargs):
        self.logger.debug(locals())
        self.on_which=on_which.lower()
        self.top_page_count=int(top_page_count)
        self.__dict__.update(kwargs) ##important


        dbParams=news.settings.allDBParams[on_which]
        tableNames=news.settings.allTableNames[on_which]


        db=mdb.connect(dbParams['addr'],dbParams['username'],dbParams['password'],dbParams['dbname'])
        cur=db.cursor()
        cur.execute("select link from %s"%'hujinzhentan_exposure')
        
        
        self.all_urls=[ i[0].split("&sn")[0] for i in cur.fetchall()]

        cur.close()
        db.close()


    #####

    def parse(self, response):
    	'''抽取每个分类中的总页数，并对每一页分发请求'''
        #print "[url: %s || status: %s]"%(response.url,response.status)
    	retitem=ExporterItem()
    	urlprefix="http://mp.aiweibang.com/asyn/categoryarticleList?uid=311487&cid=75967&pageindex="
    	page_num=1

    	driver=webdriver.PhantomJS()
    	#essay_urls=[]

    	while True:
        	_url=urlprefix+str(page_num)
        	driver.get(_url)
        	resp=HR("",200,{},driver.page_source.encode("utf8"))#把抓回的内容封装为HtmlResponse只是利用HtmlResponse的XPATH而已
        	dic=eval(resp.xpath("//pre/text()").extract()[0])
        	if len(dic["list"])==0:
        		break
        	else:
        		for i in dic["list"]:
        			essay=i["url"]
        			if essay.split("&sn")[0] not in self.all_urls:
        				retitem.set_record(essay)
        	page_num+=1

        return retitem




    