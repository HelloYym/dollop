# -*- coding: utf-8 -*-
import scrapy
import json
from chinawealth.items import ChanpinItem
from utils.webpage import get_trunk

class QuyuSpider(scrapy.Spider):
    name = "quyu"
    allowed_domains = ["chinawealth.com.cn"]
    search_url = "http://www.chinawealth.com.cn/cpxsqyQuery.go"
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=1, *args, **kwargs):
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.mapping = {}
        super(QuyuSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = ChanpinItem.get_object_by_pk(i)
            self.mapping[obj.pid] = obj.id
            body = {'cpid':obj.pid}
            yield scrapy.FormRequest(self.search_url, formdata=body, dont_filter=True, meta=body)

    def parse(self, response):
        symbol = (self.mapping[response.meta['cpid']], response.meta['cpid'])
        self.logger.info('Parsing ID.%d Chinawealth Area Info From Pid:%s' % symbol)

        item = ChanpinItem()
        data = json.loads(response.body)
        provinces = data.get('List', [])
        areas = '#'.join(get_trunk(each.get('cpxsqy','')) for each in provinces)
        item['pid'] = symbol[1]
        item['area'] = areas
        return item


