# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from news.items import JrzjNewsItem
import os
import re
import urllib
import news.settings
import sys
from utils.exporter import read_cache

class JrzjNewsSpider(scrapy.Spider):
    name = "jrzj_news"
    allowed_domains = ["jrzj.com"]
    start_urls = []

    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self,cache='news_cache',from_date=news.settings.START_DATE,to_date="2099-12-31",**kwargs):
        self.logger.debug(locals())
        self.cache=cache+".ch"
        self.from_date=from_date
        self.to_date=to_date
        self.__dict__.update(kwargs) ##important

        self.start_urls=read_cache('news_cache',self.cache)


    def parse(self,response):

    	retitem=JrzjNewsItem()
    	retitem["link"]=response.url
    	retitem["title"]=response.xpath("//h1[@id='syxbt']/text()").extract()[0]
        retitem["category"]=response.xpath("//a[@class='twofive_hover']/text()").extract()[0].strip()

    	#p=re.compile("[0-9]*-[0-9]*-[0-9]*")
        datestr=response.xpath("//div[@class='news_bt']/span/text()").extract()[0].strip().split(" ")[0]
    	if not (self.from_date<=datestr<=self.to_date):
            return None
        else:
            retitem["date"]=datestr

    	thread_id=response.url.split("/")[-1].split(".")[0]
    	retitem["thread_id"]=thread_id

    	try:
    		retitem["abstract"]=response.xpath("//blockquote/p/text()").extract()[0]
    	except BaseException:
    		pass

        ######
        #用//img而非/a/img是为了保存顶部图片，那个图片并不影响什么，干脆留着
        
        #allimglinks=response.xpath("//article//img/@src").extract()
        allparagraphs=response.xpath("//div[@class='news_content']/p[not(@style)]").extract()
        author_source_para=""

        if allparagraphs[0].strip().strip("<p>").startswith(u"文"):
            author_source_para=allparagraphs[0]
            allparagraphs=allparagraphs[1:]

        if allparagraphs[1].strip().strip("<p>").startswith(u"文"):
            author_source_para=allparagraphs[1]
            allparagraphs=allparagraphs[:1]+allparagraphs[2:]

        raw_html_str='\n'.join(allparagraphs)

        #去掉所有外链超链接
        #raw_html_str,chcount_raw=re.subn("<blockquote[^>]*>.*</blockquote>","",raw_html_str.strip()) 

        raw_html_str,chcount_raw=re.subn("<a[^>]*>|</a>","",raw_html_str.strip())
        #去掉所有内嵌脚本
        raw_html_str,chcount_raw=re.subn("<script[^>]*>.*</script>","",raw_html_str.strip())
        
        #author_source_str=re.findall(u"<p>(.*文[\ ]*[|][\ ]*[^<]*)</p>",author_source_para)
        #5种不同的竖线，真是日了狗
        author_source_str=author_source_para.lstrip("<p>").rstrip("</p>").strip().lstrip(u"文").strip().strip(u"︱").strip(u"︳").strip(u"丨").strip("|").strip(u"｜").strip()
        try:
            if author_source_str:
                if len(author_source_str.split(" "))==2:
                    source=author_source_str.split(" ")[0]
                    retitem["source"]=source
                    author=author_source_str.split(" ")[1]
                    retitem["author"]=author
                else:#没有作者或者作者和来源之间没有空格
                    source=author_source_str
                    retitem["source"]=source

            else:
                retitem["source"]=u"金融之家"
        except BaseException:
            pass

        raw_html_str,chcount=re.subn(u"<p>.*文[\ ]*[|][\ ]*[^<]*</p>","", raw_html_str.strip())
        raw_html_str,chcount=re.subn(u"<p>.*金融之家.*[0-9][0-9]?月[0-9][0-9]?日讯[， ]*","<p>", raw_html_str.strip())
 


        raw_html_str=raw_html_str.replace("'",r"\'")#important!

    	retitem["raw_html_content"]="<div>%s</div>"%raw_html_str.strip()

        #if raw_html_str.find("</blockquote")>=0:
        #    res_content=raw_html_str.split("</blockquote>")[1]
        #else:
        #    res_content=raw_html_str

        #res_content=raw_html_str.replace(u"金融之家","")
        res_content,chcount=re.subn("<[^>]*>","",raw_html_str)
        #res_content,chcount=re.subn(u"[0-9][0-9]?月[0-9][0-9]?日讯[， ]*",""]=res_content)
        '''
        在raw_html_str中已经过滤掉了
        try:
            res_content=res_content.split(u"免责声明")[0]
        except BaseException:
            pass

        try:
            res_content=res_content.split(u"责任编辑")[0]
        except BaseException:
            pass
        '''

    	####

        if len(res_content.strip())<60:
            #这种情况一般是格式跟普通的相比不合法
            #导致最后去掉左右空白的res_content为空或者字数很少
            #板式乱七八糟，这样的新闻不要也罢
            return None
        else:
            retitem["content"]=res_content

        ####
    	#retitem["category_id")


        allimglinks=response.xpath("//div[@class='news_content']/p[not(@style)]//img/@src").extract()

    	try:
            #仅仅填充image_urls
            retitem["image_urls"]="#".join([ i.split("?")[0].split("!")[0] for i in allimglinks])
    	except BaseException:
    		pass

    	return retitem
    	
