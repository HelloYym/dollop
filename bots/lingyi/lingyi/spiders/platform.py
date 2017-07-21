# -*- coding: utf-8 -*-
import scrapy
import json
import copy
from datetime import datetime
from lingyi.items import PlatformItem


class PlatformSpider(scrapy.Spider):
    name = "platform"
    allowed_domains = ["01caijing.com"]
    pipeline = ['UniqueItemPersistencePipeline']

    request_url = 'http://www.01caijing.com/remote/api.json'
    platform_list = 'cond%5BplatformName%5D=&cond%5Bselectdate%5D=%E6%9C%88&cond%5Bprovince%5D=&cond%5Binterest%5D=&cond%5Bperiod%5D=&cond%5Btype%5D=&cond%5Bdata%5D=%E6%9C%89%E6%95%B0%E6%8D%AE&cond%5Bnewlist%5D=1%2C2%2C4%2C5%2C6%2C19%2C&cond%5Bcheck_page%5D={page}&cond%5BpageIndex%5D={page}&pageIndex={page}&path=%2Fp2p-api%2Fplatform%2Fsearch.json'
    amount_body = 'path=%2Fp2p-api%2Fplatform%2Famount.json&cond%5Bwebsite%5D={platform}&cond%5BgroupBy%5D=day'
    interest_body = 'path=%2Fp2p-api%2Fplatform%2Finterest.json&cond%5Bwebsite%5D={platform}&cond%5BgroupBy%5D=day'
    period_body = 'path=%2Fp2p-api%2Fplatform%2Fperiod.json&cond%5Bwebsite%5D={platform}&cond%5BgroupBy%5D=day'
    borrower_cnt_body = 'path=%2Fp2p-api%2Fplatform%2Fborrower.json&cond%5Bwebsite%5D={platform}&cond%5BgroupBy%5D=day'
    borrower_avg_body = 'cond%5Bwebsite%5D=www.lup2p.com&cond%5BgroupBy%5D=day&path=%2Fp2p-api%2Fplatform%2Fborrower%2Favg.json'
    investor_cnt_body = 'cond%5Bwebsite%5D=www.lup2p.com&cond%5BgroupBy%5D=day&path=%2Fp2p-api%2Fplatform%2Finvestor.json'
    investor_avg_body = 'cond%5Bwebsite%5D=www.lup2p.com&cond%5BgroupBy%5D=day&path=%2Fp2p-api%2Fplatform%2Finvestor%2Favg.json'
    balance_body = 'cond%5Bwebsite%5D=www.lup2p.com&cond%5BgroupBy%5D=day&path=%2Fp2p-api%2Fplatform%2Fbalance.json'
    days = 7

    def start_requests(self):
        total_page = 10
        for page in range(total_page, 0, -1):
            yield scrapy.Request(url=self.request_url,
                                 method="POST",
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 body=self.platform_list.format(page=str(page)),
                                 callback=self.parse_platform_list,
                                 dont_filter=True)


    def parse_platform_list(self, response):
        platform_list = json.loads(response.body.decode(response.encoding))['data']['data']
        for platform_info in platform_list:
            platform = PlatformItem()
            platform['code'] = platform_info['id']
            platform['name'] = platform_info['platformname']
            platform['website'] = platform_info['companywebsite']
            platform['online_time'] = platform_info['td_19']
            platform['platname'] = platform_info['platname']

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.amount_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key1': 'borrow_cnt', 'key2': 'borrow_amount'},
                                     callback=self.parse_multi_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.interest_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key': 'interest'},
                                     callback=self.parse_single_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.period_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key': 'period'},
                                     callback=self.parse_single_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.borrower_cnt_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key': 'borrower_cnt'},
                                     callback=self.parse_single_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.borrower_avg_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key': 'borrower_avg'},
                                     callback=self.parse_single_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.investor_cnt_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key': 'investor_cnt'},
                                     callback=self.parse_single_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.investor_avg_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key': 'investor_avg'},
                                     callback=self.parse_single_value,
                                     dont_filter=True)

            yield scrapy.FormRequest(url=self.request_url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=self.balance_body.format(platform=platform_info['platname']),
                                     meta={'platform': platform, 'key1': 'repay', 'key2': 'stay'},
                                     callback=self.parse_multi_value,
                                     dont_filter=True)


    def parse_multi_value(self, response):
        data = json.loads(response.body.decode(response.encoding))['data']
        for (timestamp, value1, value2) in data[-self.days:]:
            platform = copy.deepcopy(response.meta['platform'])
            platform['date'] = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            platform[response.meta['key1']] = value1
            platform[response.meta['key2']] = value2
            yield platform

    def parse_single_value(self, response):
        data = json.loads(response.body.decode(response.encoding))['data']
        for (timestamp, value) in data[-self.days:]:
            platform = copy.deepcopy(response.meta['platform'])
            platform['date'] = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            platform[response.meta['key']] = value
            yield platform
