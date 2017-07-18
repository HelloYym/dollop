# -*- coding: utf-8 -*-
import scrapy
import json

from bank_product.items import BankProductItem
from datetime import datetime


class JsbSpider(scrapy.Spider):

    # 增量爬虫：数据比较少，每天重新爬一遍

    name = "jsb"
    allowed_domains = ["jsbchina.cn"]
    pipeline = ['BankProductPipeline']
    start_urls = [
        'https://mybank.jsbchina.cn/pweb/BidListQry.do?BankId=9999&OffSet=1&QueryNum=10000&UserType=1&TerminalType=5&ChannelId=5']

    detail_url = 'https://mybank.jsbchina.cn/pweb/static/index.html#/mainView/BidInfoQry/mod___nav=2&preCode='

    investor_url = 'https://mybank.jsbchina.cn/pweb/ProductInvestInfoQry.do?BankId=9999&OffSet=1&QueryNum=10000&UserType=1&TerminalType=5&ChannelId=5&PrdCode='

    def parse(self, response):
        product_list = json.loads(response.body.decode(response.encoding))['List']
        for product_info in product_list:
            product = BankProductItem()
            product['code'] = product_info['PrdCode']
            product['link'] = self.detail_url + product['code']
            product['name'] = product_info['PrdName']
            product['anticipate_rate'] = product_info['GuestRatedeal']
            product['limit_time'] = product_info['PrdEndLine']
            product['min_amount'] = product_info['PfirstAmt']
            prd_sale_amt = float(product_info['PrdSaleAmt'])
            prd_iss_amt = float(product_info['PrdIssAmt'])

            # if prd_sale_amt < prd_iss_amt:
            #     product['remaining_quota'] = prd_sale_amt * 10 - prd_iss_amt
            # else:

            product['remaining_quota'] = prd_iss_amt - prd_sale_amt

            product['product_type'] = product_info['PrdType']
            product['ipo_start_date'] = datetime.strptime(product_info['IpoStartDate'], '%Y%m%d')
            product['ipo_end_date'] = datetime.strptime(product_info['IpoEndDate'], '%Y%m%d')
            product['income_start_date'] = datetime.strptime(product_info['EstabDate'], '%Y%m%d')
            product['product_end_date'] = datetime.strptime(product_info['EndDate'], '%Y%m%d')

            product['bank_domain'] = 'mybank.jsbchina.cn'

            yield scrapy.Request(url=self.investor_url + product_info['PrdCode'],
                                 meta={'product': product},
                                 callback=self.parse_investor)

    def parse_investor(self, response):
        '''获得产品的投资人列表，考虑建立新表，外键关联'''

        product = response.meta['product']
        product['investor_list'] = json.loads(response.body.decode(response.encoding))['List']

        yield product













