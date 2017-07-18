# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from news.items import WeiyangReportItem
import os
import re
import time
import urllib
import news.settings
from utils.exporter import read_cache


class WeiyangReportSpider(scrapy.Spider):
    name = "weiyang_report"
    allowed_domains = ["weiyangx.com"]
    start_urls = []
    pipeline = ['UniqueItemPersistencePipeline']


    #download_delay=0.55###

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

    def start_requests(self):
        for u in self.start_urls:
            yield Request.Request(u,headers=self.common_header,callback=self.parse,meta={"m_cat":u.split("/")[-1]})

    #####
    
    def __init__(self,cache='news_cache',from_date="2012-01-01",to_date="2099-12-31",**kwargs):
        self.logger.debug(locals())
        self.cache=cache+".ch"
        self.from_date=from_date
        self.to_date=to_date
        self.__dict__.update(kwargs) ##important

        self.start_urls=read_cache('news_cache',self.cache)

    def parse(self,response):

        #print "[url: %s || status: %s]"%(response.url,response.status)
    	retitem=WeiyangReportItem()
    	retitem["link"]=response.url
    	retitem["title"]=response.xpath("//h1/text()").extract()[0]

    	#p=re.compile("[0-9]*-[0-9]*-[0-9]*")
        datestr_list=re.findall("((?:[0-9]+[-])+[0-9]+)",response.xpath("//div[@class='uk-align-left']").extract()[0])

        if not datestr_list:#例如‘4小时前’这种不符合yyyy-mm-dd的，就设定为今天
            datestr="%s-%s-%s"%time.gmtime()[:3]
        else:
            yyddmm=datestr_list[0].split("-")
            if len(yyddmm)<3: #09-21这种没年份的形式
                datestr="%s-%s-%s"%(time.gmtime()[0],yyddmm[0],yyddmm[1])
            else:
                datestr="%s-%s-%s"%(yyddmm[0],yyddmm[1],yyddmm[2])

        
        if not (self.from_date<=datestr<=self.to_date):
            return None
        else:
            retitem["date"]=datestr
        

    	thread_id=response.url.split("/")[-1].split(".")[0]

    	retitem["thread_id"]=thread_id

        try:
            author,source=response.xpath("//div[@class='uk-align-left']/p/b/text()").extract()[0].split("|")
            retitem["author"]=author.strip(u'译者：').strip()
            retitem["source"]=source.strip().strip(u"来源：").strip()
        except BaseException:
            pass


        cate=response.xpath("//div[@class='wyt-post-header-breadcrumb']")[0].xpath(".//a/text()").extract()
        cate_str=''
        for i in cate:
            cate_str=cate_str+i+" "
        retitem["category"]=cate_str

        
        if response.xpath("//div[@id='wyt-post-international-cn']").extract().__len__()==0:
            raw_html_str="\n".join(response.xpath("//article/p[not(@class)]").extract())            
        else:
            raw_html_str="\n".join(response.xpath("//div[@id='wyt-post-international-cn']/p[not(@class)]").extract())



        #去掉所有外链超链接
        raw_html_str,chcount_raw=re.subn("<a[^>]*>|</a>","",raw_html_str.strip())
        #去掉所有内嵌脚本
        raw_html_str,chcount_raw=re.subn("<script[^>]*>.*</script>","",raw_html_str.strip()) 


    	retitem["raw_html_content"]=raw_html_str.replace("'",r"\'")#important!

        #article段内并不是所有p/text()都是正文内容，只能从最后一行关键字所在的行那里割开
        #lastkeywordline=response.xpath("//a[@class='wyt-post-tag']").extract()[-1]

        #这一行之后是其他内容，夹在lastkeywordline和divideline之前的才是正文
        #divideline=u'<div class="wp-link-pages uk-width-1-1 uk-text-center">\r\n    </div>'

        #res_content=raw_html_str.split(lastkeywordline)[1].split(divideline)[0]

        #有的里面还会有一半英文正文，此时正文里会残留有微信分享，要去掉
        #res_content=res_content.split('<div id="wechat-share" class="uk-modal">')[0]
        
        res_content,chcount=re.subn("<[^>]*>","",raw_html_str.strip())

    	retitem["content"]=res_content.rstrip()
        if res_content.strip()=="":
            #这种情况出现在所有段落都没有<div>分割，都挤在div[@id=article]里面，如果里面有图片就没发处理了，这样的新闻不要也罢
            return None
        else:
            retitem["content"]=res_content


        if response.xpath("//div[@id='wyt-post-international-cn']").extract().__len__()==0:
            #必须用/p/a限定，否则article中还会有许多乱七八糟的src
            allimglinks=response.xpath("//article/p/a/img/@src").extract()
                       
        else:
            allimglinks=response.xpath("//div[@id='wyt-post-international-cn']/p/a/img/@src").extract()
            

        #顶部主题图片不要了
        try:
            #仅仅填充image_urls
            retitem["image_urls"]="#".join([ i.split("?")[0].split("!")[0] for i in allimglinks])
        except BaseException:
            pass

        return retitem