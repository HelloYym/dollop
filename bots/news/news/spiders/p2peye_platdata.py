# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from news.items import P2peyePlatdataItem
import datetime
import news.settings

class P2peyePlatdataSpider(scrapy.Spider):
    name = "p2peye_platdata"
    allowed_domains = ["p2peye.com"]
    start_urls = [
        "http://www.p2peye.com/shuju/ptsj/"
    ]

    pipeline = ['UniqueItemPersistencePipeline']


    def __init__(self,**kwargs):
        self.logger.debug(locals())
        self.__dict__.update(kwargs) ##important

    def start_requests(self):
        for u in self.start_urls:
            yield Request.Request(u,callback=self.parse)


    def parse(self,response):
        #print "[url: %s || status: %s]"%(response.url,response.status)
        domain_names=["rank","name","chengjiaoe","zonghelilv","touziren","jiekuanzhouqi","jiekuanren","manbiaosudu","leijidaikuanyue","zijinjingliuru"]
    	date=(datetime.date.today()-datetime.timedelta(days=1)).__str__()
        val_groups=[i.xpath("./td").xpath("string(.)").extract() for i in response.xpath("//table[@id='platdata']/tbody/tr")]
        
        for val_group in val_groups:
            retitem=P2peyePlatdataItem()
            for i in range(10):
                retitem[domain_names[i]]=val_group[i].strip().split(" ")[-1]

            retitem["date"]=date

            yield retitem
    	
    