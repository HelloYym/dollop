# -*- coding: utf-8 -*-
import scrapy
import json

from bank_product.items import BankProductItem
from datetime import datetime


class NbcbSpider(scrapy.Spider):

    # 增量爬虫：数据太多了，每天爬前几页，并且判断code是否存在过

    name = "nbcb"
    allowed_domains = ["nbcb.com.cn"]
    pipeline = ['BankProductPipeline']
    start_url = 'https://zxyh.nbcb.com.cn/desktop/InvestListQry.do'
    invest_detail_url = 'https://zxyh.nbcb.com.cn/desktop/InvestDetailsQry.do'
    investor_url = 'https://zxyh.nbcb.com.cn/desktop/InvestorQry.do'
    page_size = 200

    def start_requests(self):
        '''首先尝试请求全部产品数'''
        yield scrapy.FormRequest(url=self.start_url,
                                 formdata={'PageNum': '0', 'PageCount': '0'},
                                 callback=self.parse_total_num)

    def parse_total_num(self, response):
        # 根据产品数进行分页请求产品列表
        total_num = int(json.loads(response.body.decode(response.encoding))['TotalNum'])
        # 爬取全部
        # for page_num in range(total_num / self.page_size + 1, 0, -1):

        # 每天爬取第一页就够了
        for page_num in [1, ]:
            yield scrapy.FormRequest(url=self.start_url,
                                     formdata={'PageNum': str(page_num), 'PageCount': str(self.page_size)},
                                     callback=self.parse_invest_no)

    def parse_invest_no(self, response):
        '''从产品列表中提取投资号，请求详细信息

        '''
        product_list = json.loads(response.body.decode(response.encoding))['List']
        for product_info in product_list:
            invest_no = product_info['InvestProdno']
            yield scrapy.FormRequest(url=self.invest_detail_url,
                                     formdata={'InvestNo': str(invest_no)},
                                     callback=self.parse_invest_detail)

    def parse_invest_detail(self, response):
        product_info = json.loads(response.body.decode(response.encoding))

        product = BankProductItem()
        product['bank_domain'] = self.allowed_domains[0]
        product['code'] = product_info['InvestNo']
        product['name'] = product_info['ProjectName']
        product['anticipate_rate'] = product_info['ExptEarn']
        product['limit_time'] = product_info['InvestLimit']
        # product['min_amount'] = product_info['PfirstAmt']
        product['ascend_amount'] = product_info['FinaProgress']
        # # product['risk'] = product_item.xpath('./td[5]/text()').extract_first().strip()
        product['remaining_quota'] = product_info['SurplusInstAmt']

        # product['product_type'] = product_info['PrdType']
        # # product['finance_type'] = product_info['FinanceType']
        product['ipo_start_date'] = datetime.strptime(product_info['BeginDate'], '%Y%m%d')
        product['ipo_end_date'] = datetime.strptime(product_info['TenderEndDate'], '%Y%m%d')
        product['income_start_date'] = datetime.strptime(product_info['LatestRateDate'], '%Y%m%d')
        product['product_end_date'] = datetime.strptime(product_info['CloseDate'], '%Y%m%d')

        yield scrapy.FormRequest(url=self.investor_url,
                                 formdata={'ProjectCode': product['code']},
                                 meta={'product': product},
                                 callback=self.parse_investor)

    def parse_investor(self, response):
        '''获得产品的投资人列表，考虑建立新表，外键关联'''
        product = response.meta['product']
        product['investor_list'] = json.loads(response.body.decode(response.encoding))['List']

        yield product
