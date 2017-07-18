# -*- coding: utf-8 -*-
import scrapy
import requests
from utils.webpage import get_content
from wangjia.items import BusinessmanItem
from stalk.models.wqmodels import wdzj_navigation

class GaoguanSpider(scrapy.Spider):
    name = 'gaoguan'
    url_prefix = 'http://www.wdzj.com/dangan/'
    pipeline = ['UniqueItemPersistencePipeline']

    def get_pin_from_wdzj_navigation(self):
        pins = wdzj_navigation.objects.values_list("platPin")
        return [p[0] for p in pins]

    def start_requests(self):
        for pin in self.get_pin_from_wdzj_navigation():
            url = self.url_prefix + pin + '/'
            yield scrapy.Request(url=url, meta={'pin': pin}, dont_filter=True)

    def parse(self, response):
        self.logger.info('Parsing Wangjia Gaoguan From <%s>.' % response.url)

        item_list = []
        gglist = response.xpath('//ul[@class="gglist"]//li')
        ggshow = response.xpath('//div[contains(@class, "ggshow")]')
        if len(gglist) != len(ggshow):
            self.logger.warning("The number of gaoguan list and gaoguan intro not the same!")
        else:
            for i in xrange(len(ggshow)):
                item = BusinessmanItem()
                item['pin'] = response.meta.get('pin')
                item['product_name'] = get_content(response.xpath('//div[@class="title"]/h1/text()').extract())
                item['name'] = get_content(gglist[i].xpath('a/span/text()').extract())
                item['post'] = get_content(gglist[i].xpath('a/p/text()').extract())
                img_url = get_content(ggshow[i].xpath('img/@src').extract())
                if img_url and 'javascript' not in img_url:
                    item['image_url'] = img_url
                item['introduction'] = get_content(ggshow[i].xpath('div/p/text()').extract())
                item_list.append(item)

        return item_list