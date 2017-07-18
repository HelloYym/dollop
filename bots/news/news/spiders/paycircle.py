# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from news.items import PaycircleNewsItem
import news.settings
import urllib
import os
import re
from utils.exporter import read_cache



class Sp1Spider(scrapy.Spider):
    name = "paycircle_news"
    allowed_domains = ["paycircle.cn"]
    start_urls = []

    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self,cache='news_cache',from_date="2016-01-01",to_date="2099-12-31",**kwargs):
        self.logger.debug(locals())
        self.cache=cache+".ch"
        self.from_date=from_date
        self.to_date=to_date
        self.__dict__.update(kwargs) ##important

        self.start_urls=read_cache('news_cache',self.cache)


    def parse(self,response):

    	retitem=PaycircleNewsItem()
    	retitem["link"]=response.url
    	retitem["title"]=response.xpath("//title/text()").extract()[0].split(u"_支付")[0]
        retitem["category"]=response.xpath("//div[@class='step step_new']/a/text()").extract()[2]

    	#p=re.compile("[0-9]*-[0-9]*-[0-9]*")
    	date_source_author_groups=response.xpath("//div[@class='wzsx_right']/text()").extract()[0].split(u"\xa0\xa0")

    	if(len(date_source_author_groups)>=2):
    		source=date_source_author_groups[1].split(u"：")[-1]
    		retitem["source"]=source

    	if(len(date_source_author_groups)>=3):
			author=date_source_author_groups[2].split(u"：")[-1] #并没有错，数据库里这个字段是空的是因为12月之后的新闻太少，而且没有作者
			retitem["author"]=author

    	
    	dates=response.url.split("/")[-3:-1]
    	datestr=dates[0][:4]+"-"+dates[0][4:]+"-"+dates[1]

        if not (self.from_date<=datestr<=self.to_date):
            return None
        else:
            retitem["date"]=datestr

    	thread_id=response.url.split("/")[-1].split(".")[0]
    	retitem["thread_id"]=thread_id

    	try:
    		retitem["abstract"]=response.xpath("//div[@class='introduce']/text()").extract()[0][24:]
    	except BaseException:
    		pass

        ####
        ######
        #用//img而非/a/img是为了保存顶部图片，那个图片并不影响什么，干脆留着
            
        raw_html_str="\n".join(response.xpath("//div[@id='article']/div").extract())

        #去掉所有外链超链接
        #raw_html_str,chcount_raw=re.subn("<blockquote[^>]*>.*</blockquote>","",raw_html_str.strip()) 

        raw_html_str,chcount_raw=re.subn("<a[^>]*>|</a>","",raw_html_str.strip())
        #去掉所有内嵌脚本
        raw_html_str,chcount_raw=re.subn("<script[^>]*>.*</script>","",raw_html_str.strip())
        raw_html_str=raw_html_str.replace("<div","<p").replace("</div>","</p>")
 


        raw_html_str=raw_html_str.replace("'",r"\'")#important!

        retitem["raw_html_content"]="<div>%s</div>"%raw_html_str

        res_content,chcount=re.subn("<[^>]*>","",raw_html_str)

        ####

        if len(res_content.strip())<100:
            #这种情况出现在所有段落都没有<div>分割，都挤在div[@id=article]里面
            #或者有的时候用div去格式化东西，剩下许多正文没放在<div>中
            #或者不用div而是用了<p>
            #导致最后去掉左右空白的res_content为空或者字数很少
            #板式乱七八糟，这样的新闻不要也罢
            return None
        else:
            retitem["content"]=res_content


        allimglinks=response.xpath("//div[@id='article']/div/img/@src").extract()


    	try:
            #仅仅填充image_urls
            retitem["image_urls"]="#".join([ i.split("?")[0].split("!")[0] for i in allimglinks])
        except BaseException:
            pass


    	return retitem


    