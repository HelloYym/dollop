# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from utils.webpage import get_content, get_thread_from_news_url
from utils.get_thread import get_max_thread_from_news
from exporterHelper.items import ExporterItem

################################################################################################################
#                                                                                                              #
# USAGE: nohup scrapy crawl wangjia_news -a from_id=1 -a to_id=1 -a category=1 --loglevel=INFO --logfile=log & #
#                                                                                                              #
################################################################################################################

class WangjiaNewsJsonSpider(scrapy.Spider):
    name = 'wangjia_news'
    allowed_domains = ['wdzj.com']
    start_formated_url = 'http://www.wdzj.com/news/{category}/p{page_id}.html'
    pipeline = ['CacheFileExporterPersistencePipeline']
    tab = ['', 'hangye', 'zhengce', 'pingtai', 'shuju', 'licai', 'guowai', 'guandian', 'yanjiu', 'jiedai',   \
           'jinrong', 'gundong', 'xiaodai', 'danbao', 'diandang', 'hydongtai', 'zhifu', 'zhongchou',         \
           'huobi', 'baogao', 'xiehui']
    tab_category = {'hangye': u'网贷行业', 'zhengce': u'政策协会', 'pingtai': u'平台动态', 'shuju': u'行业数据',
                    'licai': u'P2P投资理财', 'guowai': u'国外网贷', 'guandian': u'行业观点', 'yanjiu': u'行业研究',
                    'jiedai': u'民间借贷', 'jinrong': u'互联网金融', 'gundong': u'滚动', 'xiaodai': u'资金借贷',
                    'danbao': u'担保机构', 'diandang': u'典当行业', 'hydongtai': u'互金行业', 'zhifu': u'网络支付',
                    'zhongchou': u'众筹行业', 'huobi': u'虚拟货币', 'baogao': u'数据报告', 'xiehui': u'行业协会'}

    #NOTE: (zacky, 2016.JUN.7th) JUST MARK UP BLACK TAB HERE.
    black_tab = ['fangtan', 'zhuanlan', 'video']

    def __init__(self, from_id=1, to_id=1, category=1, *args, **kwargs):
        self.logger.debug(locals())
        to_id = max(int(from_id), int(to_id))
        self.shortlist = xrange(int(from_id), int(to_id) + 1)
        if int(category):
            self.max_thread = get_max_thread_from_news(self.tab_category[self.tab[int(category)]])
            self.category = self.tab[int(category)]
        else:
            self.max_thread = [get_max_thread_from_news(self.tab_category[self.tab[i]]) for i in range(1, 21)]
            self.category = [self.tab[i] for i in range(1, 21)]
        super(WangjiaNewsJsonSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            if isinstance(self.category, list):
                for j in range(0, 20):
                    url = self.start_formated_url.format(category=self.category[j], page_id=i)
                    yield Request(url, dont_filter=True, meta={"category": self.category[j], "max_thread": self.max_thread[j]})
            else:
                url = self.start_formated_url.format(category=self.category, page_id=i)
                yield Request(url, dont_filter=True, meta={"category": self.category, "max_thread": self.max_thread})

    def parse(self, response):
        category = response.meta.get("category")
        max_thread = response.meta.get("max_thread")
        self.logger.info('Parsing Wangjia News %s URLs From <%s>.' % (category, response.url))

        item = ExporterItem()
        elements = response.xpath('//ul[@class="zllist"]/li')
        for ele in elements:
            url = get_content(ele.xpath('div[2]/h3/a/@href').extract())
            if url.find(category) == -1: continue

            thread = get_thread_from_news_url(url)
            if int(max_thread) < int(thread):
                item.set_record(url)

        return item
