# -*- coding: utf-8 -*-

import scrapy
from imageHelper.items import ImageItem

# For model support.
from bots.wangjia.wangjia.items import DaohangItem, BaoguangItem, XinwenItem, DanganItem, BusinessmanItem
from bots.news.news.items import WeiyangNewsItem,WeiyangReportItem,JrzjNewsItem,PaycircleNewsItem
from bots.p2peye.p2peye.items import BusinessmanItem as P2PBI, DanganItem as P2PDI

####################################################################################
#                                                                                  #
# USAGE: nohup scrapy crawl grabber -a from_id=1 -a to_id=1 -a category=exposure \ #
#        -a model=BaoguangItem -a field=image_url --loglevel=INFO --logfile=log &  #
#                                                                                  #
####################################################################################

class GrabberSpider(scrapy.Spider):
    name = 'grabber'
    allowed_domains = ['wdzj.com','weiyangx.com','paycircle.cn','jrzj.com']
    #NOTE: (zacky, 2015.JUN.2nd) FAKE URL TO PROCESS SUCCESSFULLY.
    fake_url = 'https://www.baidu.com/'
    start_urls = []

    DOWNLOAD_DELAY=6
    custom_settings = {"DOWNLOAD_DELAY": 0.5}


    def __init__(self, from_id=None, to_id=None, category='', model='', field='', *args, **kwargs):
        self.logger.debug(locals())
        self.model = model

        if model in ['WeiyangNewsItem','WeiyangReportItem','JrzjNewsItem','PaycircleNewsItem']:
            self.DOWNLOAD_DELAY=0.01

        if not from_id or not to_id:
            current_news = eval(self.model).django_model.objects.filter(img_grabber_executed = True).order_by('id').last()
            if not current_news:
                current_id = 1 #如果数据库内的数据经过全删重爬后，起始id不再是1，这种情况下这里会出错
            else:
                current_id = current_news.id
            max_id = eval(self.model).django_model.objects.all().last()
            self.shortlist = xrange(current_id, max_id.id+1)
        else:
            to_id = max(int(from_id), int(to_id))
            self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.category = category
        self.field = field
        self.queue = []
        super(GrabberSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = eval(self.model).get_object_by_pk(i)
            if not obj:
                continue
            urls = getattr(obj, self.field)
            if not urls:
                continue

            self.queue.append((urls, obj.get_uk_code()))
            img_grabber_executed = getattr(obj, "img_grabber_executed")
            if img_grabber_executed:
                continue
            setattr(obj, "img_grabber_executed", True)
            obj.save()
            yield self.make_requests_from_url(self.fake_url)

    def parse(self, response):
        if not self.model or not self.field: return None

        urls, uk_code = self.queue.pop(0)
        item = ImageItem()
        item['slug'] = uk_code
        item['image_urls'] = urls.split('#')

        return item
