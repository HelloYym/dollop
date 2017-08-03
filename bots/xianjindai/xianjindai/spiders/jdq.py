# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import scrapy
from xianjindai.items import JdqProductItem
import json


class JdqSpider(scrapy.Spider):
    name = "jdq"
    allowed_domains = ["jiedianqian.com"]

    pipeline = ['UniqueItemPersistencePipeline']

    product_list_url = 'https://m.jiedianqian.com/api/rank/getRecommendation'
    product_list_body = 'loanTagId=&deviceType=MSite&rankType=default&leftRange=&rightRange=&returnType=returnList'

    product_detail_url = 'https://m.jiedianqian.com/api/rank/getProductDetail'
    product_detail_body = 'product_id={pid}'

    def start_requests(self):
        yield scrapy.Request(url=self.product_list_url,
                             method="POST",
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             body=self.product_list_body,
                             callback=self.parse_product_list,
                             dont_filter=True)

    def parse_product_list(self, response):
        product_list = json.loads(response.body.decode(response.encoding))['data']['allList']
        for product in product_list:
            pid = product['loan_id']
            yield scrapy.Request(url=self.product_detail_url,
                                 method="POST",
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 body=self.product_detail_body.format(pid=pid),
                                 callback=self.parse_product_detail,
                                 dont_filter=True)

    def parse_product_detail(self, response):
        product_info = json.loads(response.body.decode(response.encoding))['data']
        product = JdqProductItem()
        product['code'] = product_info['product_id']
        product['channel_name'] = product_info['channelName']
        product['name'] = product_info['name']
        product['logo'] = product_info['logo']
        product['apply_count'] = product_info['apply_count']
        product['success_rate'] = product_info['success_rate']
        product['description'] = product_info['description']
        product['min_amount'] = product_info['min_amount']
        product['max_amount'] = product_info['max_amount']
        product['min_terms'] = product_info['min_terms']
        product['max_terms'] = product_info['max_terms']
        product['interest'] = product_info['interestValue']
        product['interest_unit'] = ['日', '月'][product_info['interestUnit']]
        product['min_duration'] = product_info['min_duration']
        product['min_duration_unit'] = product_info['min_duration_unit']
        product['conditions'] = product_info['conditions']
        product['materials'] = product_info['materials']
        product['apply_url'] = product_info['apply_url']
        product['tag_list'] = '#'.join([tag['tagName'] for tag in product_info['tagList']])

        yield product
