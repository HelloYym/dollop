# -*- coding: utf-8 -*-

import scrapy
from utils.webpage import get_trunk, get_content
from xianjindai.items import XjdProductItem


class XjdSpider(scrapy.Spider):
    name = "xjd"
    allowed_domains = ["xianjindaikuan.com"]
    pipeline = ['UniqueItemPersistencePipeline']

    start_urls = ['http://www.xianjindaikuan.com/index.php?m=content&c=index&a=lists&catid=19',
                  'http://www.xianjindaikuan.com/index.php?m=content&c=index&a=lists&catid=20',
                  'http://www.xianjindaikuan.com/index.php?m=content&c=index&a=lists&catid=21',
                  'http://www.xianjindaikuan.com/index.php?m=content&c=index&a=lists&catid=22']
    category = ['小微速贷', '手机微贷', '信用卡贷款', '大学生贷款']

    def start_requests(self):
        for i in range(4):
            yield scrapy.Request(url=self.start_urls[i],
                                 meta={'category': self.category[i]},
                                 dont_filter=True)

    def parse(self, response):
        for product_item in response.xpath('//div[contains(@class,"product-item")]'):

            product = XjdProductItem()
            product['category'] = response.meta['category']
            product['name'] = get_content(product_item.xpath('.//div[@class="tit"]/span/text()').extract())
            product['comment'] = get_content(product_item.xpath('.//div[@class="tit"]/span/em/text()').extract())
            product['logo'] = get_content(product_item.xpath('.//div[@class="tit"]/img/@src').extract())
            product['amount'] = get_content(product_item.xpath('.//ul[@class="pro-desc"]/li[1]/p/text()').extract())
            product['term'] = get_content(product_item.xpath('.//ul[@class="pro-desc"]/li[2]/p/text()').extract())
            product['interest'] = get_content(product_item.xpath('.//ul[@class="pro-desc"]/li[3]/p/text()').extract())

            product['repay'] = get_content(product_item.xpath('string(.//div[@class="pro-item-right"]/p[1])').extract())
            product['speed'] = get_content(product_item.xpath('string(.//div[@class="pro-item-right"]/p[2])').extract())
            product['link'] = get_content(product_item.xpath('.//div[@class="pro-item-right"]/a/@href').extract())

            yield product
