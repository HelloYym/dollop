# -*- coding: utf-8 -*-

import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from scrapy.loader import ItemLoader
from news.items import WDZJNavigationItem
import news.settings
import re
import time
import json
import MySQLdb as mdb


class WDZJNavigationSpider(scrapy.Spider):
    name = "wdzj_navigation"
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

    '''def start_requests(self):
        for u in self.start_urls:
            yield Request.Request(u,headers=self.common_header,callback=self.parse)
    '''

    allPlatDocEntryUrls={}

    #####
    all_names=[]    #爬取之前先取出所有的name,后面碰到重复的就不用再继续了
    #on_which="aliyun"

    def __init__(self,on_which=news.settings.DEFAULT_ON_WHICH,**kwargs):
        self.logger.debug(locals())
        self.on_which=on_which.lower()
        self.__dict__.update(kwargs) ##important


    def parse(self, response):
        '''从Json中获取所有平台的拼音缩写并拼接成URL'''
        prefix='http://www.wdzj.com/dangan/'
        '''
        filtered=[]
        for p in eval(response.body):
            if p['platName'] not in self.all_names:
                filtered.append(p)

        self.allPlatDocEntryUrls= {}
        for t in filtered:'''
        for t in eval(response.body):
            self.allPlatDocEntryUrls[prefix+t['platPin']+'/']=t

        #print len(self.allentryUrls)
        for i in self.allPlatDocEntryUrls.keys():
            r=Request.Request(i,headers=self.common_header,callback=self.parse2,meta=self.allPlatDocEntryUrls[i])
            yield r


    def parse2(self,response):

        #print "[url: %s || status: %s]"%(response.url,response.status)


        retitem=WDZJNavigationItem()
        try:
            retitem["name"]=response.meta['platName'].decode("utf8") #这个是从网页json里拿到的，需要解码
            retitem["platPin"]=response.meta['platPin']
            retitem["allPin"]=response.meta['allPlatPin']
            retitem["icon_url"]=response.meta['platIconUrl']
        except BaseException as e:
            raise e
        #il.add_value("link",response.url)
        try:
            #il.add_value("title",response.xpath("//div[@class='title']/h1/text()").extract()[0])
            retitem["province"]=response.xpath("//div[@class='title']/span/em/text()").extract()[0].split(u"·")[0].strip()
            retitem["launched_time"]=response.xpath("//div[@class='title']/span/em/text()").extract()[1].split(u"上线")[0]
            registered_website=response.xpath("//div[@class='da-ggxx']")[1].xpath(".//tr")[0].xpath("./td/text()")[1].extract()
            if registered_website.find(".")==-1:#备案域名无效或者不合法，尝试在右上角的连接
                retitem["link"]=response.xpath("//div[@class='on4']/a/@href").extract()[0]
            else:
                retitem["link"]=registered_website


        except BaseException:
            pass

        return retitem
        

    def closed(self,reason):
        print "\n\n\n\n\n"+reason
        #pass

    