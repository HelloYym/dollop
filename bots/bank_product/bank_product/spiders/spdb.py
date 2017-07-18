# -*- coding: utf-8 -*-
import scrapy
import json

from bank_product.items import BankProductItem
from datetime import datetime


class SpdbSpider(scrapy.Spider):

    # 增量爬虫：每天重新爬一遍

    name = "spdb"
    allowed_domains = ["ebank.spdb.com.cn"]
    start_urls = {
        '固定期限': 'https://ebank.spdb.com.cn/nbper/FinanceFixListQuery.do?FinanceSearchType=01&CurrencyNo=&BeginNumber=0&QueryNumber=1000',
        '现金管理': 'https://ebank.spdb.com.cn/nbper/FinanceFixListQuery.do?FinanceSearchType=02&CurrencyNo=&BeginNumber=0&QueryNumber=1000',
        '汇理财': 'https://ebank.spdb.com.cn/nbper/FinanceFixListQuery.do?FinanceSearchType=05&CurrencyNo=&BeginNumber=0&QueryNumber=1000',
        '净值类': 'https://ebank.spdb.com.cn/nbper/FinanceFixListQuery.do?FinanceSearchType=04&CurrencyNo=&BeginNumber=0&QueryNumber=1000', }

    detail_url = 'https://ebank.spdb.com.cn/nbper/PreBankFinanceBuy.do?FinanceNo='
    pipeline = ['BankProductPipeline']

    def start_requests(self):
        yield scrapy.Request(self.start_urls['固定期限'], callback=self.parse1, meta={'type': '固定期限'})
        yield scrapy.Request(self.start_urls['现金管理'], callback=self.parse1, meta={'type': '现金管理'})
        yield scrapy.Request(self.start_urls['汇理财'], callback=self.parse1, meta={'type': '汇理财'})
        yield scrapy.Request(self.start_urls['净值类'], callback=self.parse2, meta={'type': '净值类'})

    def parse1(self, response):
        for product_item in response.xpath('//tbody/tr'):
            product = BankProductItem()

            # 直接获取产品的json格式完整信息，在购买链接的请求中
            json_info = product_item.xpath('./td[7]/a[1]/@onclick').re_first(r'(?<=\{)[^}]*(?=\})')
            json_info = json_info.replace("'", '"')
            product_info = json.loads('{' + json_info + '}')

            product['code'] = product_info['FinanceNo']
            product['link'] = self.detail_url + product['code']
            product['name'] = product_info['FinanceAllName'].strip()
            product['anticipate_rate'] = product_info['FinanceAnticipateRate']
            product['min_amount'] = product_info['FinanceIndiIpoMinAmnt']
            product['ascend_amount'] = product_info['FinanceIndiSaddIpoAmnt']

            product['limit_time'] = product_item.xpath('./td[3]/text()').extract_first().strip().replace('-', '0')
            product['risk'] = product_item.xpath('./td[5]/text()').extract_first().strip()

            product['product_type'] = response.meta['type']
            product['finance_type'] = product_info['FinanceType']

            product['ipo_start_date'] = datetime.strptime(product_info['FinanceIpoStartDate'], '%Y%m%d')
            product['ipo_end_date'] = datetime.strptime(product_info['FinanceIpoEndDate'], '%Y%m%d')
            product['income_start_date'] = datetime.strptime(product_info['FinanceIncomeStartDate'], '%Y%m%d')
            product['product_end_date'] = datetime.strptime(product_info['FinanceProductEndDate'], '%Y%m%d')

            product['bank_domain'] = 'ebank.spdb.com.cn'

            currency_values = {
                '01': '人民币',
                '12': '英镑',
                '13': '港币',
                '14': '美元',
                'XX': '其它',
            }
            product['currency'] = currency_values.get(product_info['FinanceCurrency'])

            yield product

    # 净值类产品页面有变化
    def parse2(self, response):
        for product_item in response.xpath('//tbody/tr'):
            product = BankProductItem()

            # 直接获取产品的json格式完整信息，在购买链接的请求中
            json_info = product_item.xpath('./td[1]//a[1]/@onclick').re_first(r'(?<=\{)[^}]*(?=\})')
            json_info = json_info.replace("'", '"')
            product_info = json.loads('{' + json_info + '}')

            product['code'] = product_info['FinanceNo']
            product['link'] = self.detail_url + product['code']
            product['name'] = product_info['FinanceAllName'].strip()
            product['anticipate_rate'] = product_info['FinanceAnticipateRate']
            product['min_amount'] = product_info['FinanceIndiIpoMinAmnt']
            product['ascend_amount'] = product_info['FinanceIndiSaddIpoAmnt']

            product['limit_time'] = product_info['FinanceLimitTime']
            product['risk'] = product_item.xpath('./td[5]/text()').extract_first().strip()

            product['product_type'] = response.meta['type']
            product['finance_type'] = product_info['FinanceType']

            product['ipo_start_date'] = datetime.strptime(product_info['FinanceIpoStartDate'], '%Y%m%d')
            product['ipo_end_date'] = datetime.strptime(product_info['FinanceIpoEndDate'], '%Y%m%d')
            product['income_start_date'] = datetime.strptime(product_info['FinanceIncomeStartDate'], '%Y%m%d')
            product['product_end_date'] = datetime.strptime(product_info['FinanceProductEndDate'], '%Y%m%d')

            product['bank_domain'] = 'ebank.spdb.com.cn'

            currency_values = {
                '01': '人民币',
                '12': '英镑',
                '13': '港币',
                '14': '美元',
                'XX': '其它',
            }
            product['currency'] = currency_values.get(product_info['FinanceCurrency'])

            yield product