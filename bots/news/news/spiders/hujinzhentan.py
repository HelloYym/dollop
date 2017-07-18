# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from news.items import HujinzhentanExposureItem
import os
import re
import time
import urllib
import news.settings
from utils.exporter import read_cache

from scrapy.http.response.html import HtmlResponse as HR
from scrapy.loader import ItemLoader
from news.items import ExporterItem
from selenium import webdriver

class HujinzhentanSpider(scrapy.Spider):
    name = "hujinzhentan"
    allowed_domains = ["example.com"]
    start_urls = ["http://www.example.com"]

    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self,cache='news_cache',**kwargs):
        self.logger.debug(locals())
        self.cache=cache+".ch"
        
        self.__dict__.update(kwargs) ##important

        #self.start_urls=read_cache('news_cache',self.cache)

    #def start_requests(self):
    #    for u in self.start_urls:
    #        yield Request.Request(u,headers=self.common_header,callback=self.parse)


    def parse(self,response):
        #print "[url: %s || status: %s]"%(response.url,response.status)
        essay_urls=read_cache('news_cache',self.cache)
        driver=webdriver.PhantomJS()

        for essay_url in essay_urls:
            try:
                retitem=HujinzhentanExposureItem()

                driver.get(essay_url)
                resp=HR("",200,{},driver.page_source.encode("utf8"))#把抓回的内容封装为HtmlResponse只是利用HtmlResponse的XPATH而已

                retitem["link"]=essay_url

                for i in essay_url.split("&"):
                    if i.startswith("mid"):
                        retitem["thread_id"]=i.split("=")[1][-9:]

                retitem["abstract"]=""

                retitem["title"]=resp.xpath("//h2[@class='rich_media_title']/text()").extract()[0].strip()

                retitem["date"]=resp.xpath("//em[@id='post-date']/text()").extract()[0]


                #根据日期再过滤一下
                allparts=resp.xpath("//div[@id='js_content']/*")

                #retitem["raw_html_content"]=allparts.extract()[1:-1]

                raw_paras=[]
                paras=[]
                source_para=""
                img_urls=[]

                for i in allparts:
                    s=i.xpath("string(.)").extract()[0].strip()
                    if len(s)>0:
                        if s.startswith(u"来源："):
                            source_para=s
                            break
                        paras.append(s)
                    
                    raw_paras.append(i.extract())

                    if i.xpath(".//img/@data-src").extract().__len__()>0:
                         img_urls+=i.xpath(".//img/@data-src").extract()

                retitem["content"]="\n".join(paras)
                retitem["raw_html_content"]="".join(raw_paras)

                try:
                    retitem["source"]=source_para.split(u"：")[1]
                except BaseException:
                    retitem["source"]=u"互金侦探"


                retitem["category"]="曝光"

               
                retitem["image_urls"]="#".join(img_urls)
                

                yield retitem
            except BaseException:
                continue

    