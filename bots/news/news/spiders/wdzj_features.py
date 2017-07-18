# -*- coding: utf-8 -*-

import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from scrapy.loader import ItemLoader
from news.items import WDZJFeaturesItem
import news.settings
import re
import time
import json
import MySQLdb as mdb


class WDZJSpider(scrapy.Spider):
    name = "wdzj_features"
    allowed_domains = ["wdzj.com"]
    start_urls = (
        'http://www.wdzj.com/wdzj/html/json/dangan_search.json',
    )

    pipeline = ['UniqueItemPersistencePipeline']
    #download_delay=0.55###

    common_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'DNT':'1',
'Host':'www.wdzj.com',
'Upgrade-Insecure-Requests':'0',
'Referer':'http://www.wdzj.com/',

'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
             }


    allPlatDocEntryUrls={}

    #####
    all_names=[]    #爬取之前先取出所有的name,后面碰到重复的就不用再继续了
    #on_which="test"

    def __init__(self,on_which=news.settings.DEFAULT_ON_WHICH,**kwargs):
        self.logger.debug(locals())
        self.on_which=on_which.lower()
        self.__dict__.update(kwargs) ##important


    #####


    def parse(self, response):
        '''从Json中获取所有平台的拼音缩写并拼接成URL'''
        #print "[url: %s || status: %s]"%(response.url,response.status)



        prefix='http://www.wdzj.com/dangan/'
        '''
        filtered=[]
        for p in eval(response.body):
            if p['platName'] not in self.all_names:
                filtered.append(p)

        self.allPlatDocEntryUrls= {}
        for t in filtered:'''
        for t in eval(response.body):
            self.allPlatDocEntryUrls[prefix+t['platPin']+'/']=[t['platName'],t['platPin']]

        #print len(self.allentryUrls)
        for i in self.allPlatDocEntryUrls.keys():
            r=Request.Request(i,headers=self.common_header,callback=self.parse2,meta={"m_platname":self.allPlatDocEntryUrls[i][0],"m_platpin":self.allPlatDocEntryUrls[i][1]})
            yield r


    def parse2(self,response):

        retitem=WDZJFeaturesItem()
        try:
            retitem["name"]=response.meta['m_platname'].decode("utf8") #这个是从网页json里拿到的，需要解码
            retitem["platPin"]=response.meta['m_platpin']
        except BaseException as e:
            raise e
        #retitem["link"]=response.url)
        try:
            #retitem["title"]=response.xpath("//div[@class='title']/h1/text()").extract()[0])
            retitem["company_tag"]=response.xpath("//div[@class='bq-box']")[0].xpath("./span/text()").extract()[0].strip()

        except BaseException:
            pass

        try:
            #retitem["title"]=response.xpath("//div[@class='title']/h1/text()").extract()[0])
            retitem["trouble_tag"]=response.xpath("//div[@class='bq-box']")[0].xpath("./span/text()").extract()[1].strip()

        except BaseException:
            pass


        try:
            retitem["overall_rating"]=response.xpath("//div[@class='dianpinbox']/b/text()").extract()[0].strip()

            retitem["cashing_rating"]=response.xpath("//div[@class='pf-box']//dd/em/text()").extract()[0]
            retitem["guarding_rating"]=response.xpath("//div[@class='pf-box']//dd/em/text()").extract()[1]
            retitem["service_rating"]=response.xpath("//div[@class='pf-box']//dd/em/text()").extract()[2]
            retitem["experience_rating"]=response.xpath("//div[@class='pf-box']//dd/em/text()").extract()[3]
        except BaseException:
            pass

            
        try:
            retitem["cashing_desc"]=response.xpath("//div[@class='pf-box']//dd/span/text()").extract()[0].strip().replace("'",r"\'")
            retitem["guarding_desc"]=response.xpath("//div[@class='pf-box']//dd/span/text()").extract()[1].strip().replace("'",r"\'")
            retitem["service_desc"]=response.xpath("//div[@class='pf-box']//dd/span/text()").extract()[2].strip().replace("'",r"\'")
            retitem["experience_desc"]=response.xpath("//div[@class='pf-box']//dd/span/text()").extract()[3].strip().replace("'",r"\'")
        except BaseException:
            pass

        #保存了简介中原有的<p>等格式
        try:
            impression_str=''
            for i in response.xpath("//div[@class='yx-box']//dd/text()").extract():
                impression_str=impression_str+i.strip()+"#"
            retitem["impression"]=impression_str.replace("'",r"\'")

        except BaseException:
            pass
        #print dict(product)
        return retitem
        

    def closed(self,reason):
        print "\n\n\n\n\n"+reason

    