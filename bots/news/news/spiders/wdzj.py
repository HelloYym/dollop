# -*- coding: utf-8 -*-

import scrapy
import scrapy.http.request as Request
import scrapy.http.response as Response
from scrapy.loader import ItemLoader
from news.items import WDZJArchiveItem
import news.settings
import re
import time
import json
import MySQLdb as mdb

map_ch2en={
    u'注册资金':'registered_capital',
    u'银行存管':'yinhangcunguan',
    u'融资记录':'assembly_record',
    u'监管协会':'administration',
    u'ICP号':'ICP',
    u'股权上市':'stockmarket_status',
    u'自动投标':'auto_bid',
    u'债权转让':'debt_transfer',
    u'投标保障':'bid_guarantee',
    u'保障模式':'guarantee_mode',
    u'风险准备金存管':'risk_guarantee',
    u'担保机构':'guarantee_institute'
}


class WDZJSpider(scrapy.Spider):
    name = "wdzj_archive"
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
    #all_names=[]    #爬取之前先取出所有的name,后面碰到重复的就不用再继续了
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

        #print "[url: %s || status: %s]"%(response.url,response.status)


    	retitem=WDZJArchiveItem()
        try:
            retitem["name"]=response.meta['m_platname'].decode("utf8") #这个是从网页json里拿到的，需要解码
            retitem["platPin"]=response.meta['m_platpin']
        except BaseException as e:
            raise e
    	#retitem["link"]=response.url)
        try:
            #retitem["title"]=response.xpath("//div[@class='title']/h1/text()").extract()[0])
            retitem["location"]=response.xpath("//div[@class='title']/span/em/text()").extract()[0]
            retitem["launched_time"]=response.xpath("//div[@class='title']/span/em/text()").extract()[1].split(u"上线")[0]

        except BaseException:
            pass


        allInfoPiece=response.xpath("//div[@class='bgbox-bt zzfwbox']//dd")
        for i in allInfoPiece:
            try:
                pieceLabel=i.xpath(".//div[@class='l']/em/text()").extract()[0].strip()
                if pieceLabel==u'担保机构':
                    corr_text=i.xpath(".//div[@class='r dbjg']").xpath("string(.)").extract()[0].strip()
                else:
                    corr_text=i.xpath(".//div[@class='r']").xpath("string(.)").extract()[0].strip()

                retitem[map_ch2en[pieceLabel]]=corr_text.replace("'",r"\'")
            except BaseException:
                pass


        try:
            enterprise_name_str=response.xpath("//div[@class='da-ggxx']")[0].xpath(".//tr")[0].xpath(".//td/text()").extract()[1].strip()
            if enterprise_name_str.find(".")==-1: #这个字符串里如果有"."则说明抓到的是官网地址，说明网页里缺这个字段
                retitem["enterprise_name"]=enterprise_name_str
            else:
                pass
        except BaseException:
            pass


        #保存了简介中原有的<p>等格式
        try:
            intro_block_html=response.xpath("//div[@class='cen-zk']").extract()[0]

            #去掉所有外链超链接
            intro_block_html,chcount_raw=re.subn("<a[^>]*>|</a>","",intro_block_html.strip())
            #去掉所有内嵌脚本
            intro_block_html,chcount_raw=re.subn("<script[^>]*>.*</script>","",intro_block_html.strip()) 

            intro_content,chcount=re.subn("<[^>]*>","",intro_block_html)


            retitem["introduction"]=intro_content.strip().replace("'",r"\'")#important!

            registered_website=response.xpath("//div[@class='da-ggxx']")[1].xpath(".//tr")[0].xpath("./td/text()")[1].extract()
            if registered_website.find(".")==-1:#备案域名无效或者不合法，尝试在右上角的连接
                retitem["official_website"]=response.xpath("//div[@class='on4']/a/@href").extract()[0]
            else:
                retitem["official_website"]=registered_website

        except BaseException:
            pass

        #pingtaifeiyong
        try:
            retitem["account_fee"]=response.xpath("//div[@class='da-ptfy']//em/text()").extract()[0].strip().replace("'",r"\'")
            retitem["cash_fee"]=response.xpath("//div[@class='da-ptfy']//em/text()").extract()[1].strip().replace("'",r"\'")
            retitem["fueling_fee"]=response.xpath("//div[@class='da-ptfy']//em/text()").extract()[2].strip().replace("'",r"\'")
            retitem["transfer_fee"]=response.xpath("//div[@class='da-ptfy']//em/text()").extract()[3].strip().replace("'",r"\'")
            retitem["vip_fee"]=response.xpath("//div[@class='da-ptfy']//em/text()").extract()[4].strip().replace("'",r"\'")
        except BaseException:
            pass

    	#print dict(product)
    	return retitem
    	

    def closed(self,reason):
    	print("\n\n\n\n\n"+reason)

    