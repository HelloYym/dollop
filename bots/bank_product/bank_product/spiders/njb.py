# -*- coding: utf-8 -*-
import scrapy
import json

from bank_product.items import BankProductItem
from datetime import datetime


class NjbSpider(scrapy.Spider):
    # 增量爬虫：每天只请求最新列表，注意最新列表变化比较快

    name = "njb"
    allowed_domains = ["nihaobank.com"]
    pipeline = ['BankProductPipeline']
    invest_history_url = 'https://www.nihaobank.com/newdirectbank/investHistoryQry.do?_locale=zh_CN&BankId=9998&LoginType=P&MenuIndex=1&PaNo=0&OffSet='
    invest_new_url = 'https://www.nihaobank.com/newdirectbank/iWantToInvest.do?_locale=zh_CN&BankId=9998&LoginType=P&tp=1'
    detail_url = 'https://www.nihaobank.com/newdirectbank/LCBuyPre.do?_locale=zh_CN&BankId=9998&LoginType=P&ProductId='
    detail_url2 = 'https://www.nihaobank.com/newdirectbank/BillsBuyPre.do?_locale=zh_CN&BankId=9998&LoginType=P&ProductId='

    def start_requests(self):
        # 请求历史产品
        # yield scrapy.Request(url=self.invest_history_url + '1',
        #                      callback=self.start_history_requests)
        # 请求最新产品，注意：最新产品也会变成历史产品
        yield scrapy.Request(url=self.invest_new_url,
                             callback=self.parse_new_invest_list)

    def start_history_requests(self, response):

        total_page = int(response.xpath('//ul[@class="PageClass"]/li[2]/a/text()').re_first(r'\d+'))

        for page_num in range(total_page, 0, -1):
            # for page_num in []:
            yield scrapy.Request(url=self.invest_history_url + str(page_num),
                                 callback=self.parse_history_list)

    def parse_new_invest_list(self, response):

        for product_item in response.xpath('//div[@class="productlistboxe "]'):
            code = product_item.xpath('./@id').extract_first()

            if len(product_item.xpath('.//div[@class="right"]').re(r'募集进度')):
                yield scrapy.FormRequest(url=self.detail_url2 + code,
                                         meta={'code': code},
                                         callback=self.parse_detail_page)
            else:
                yield scrapy.FormRequest(url=self.detail_url + code,
                                         meta={'code': code},
                                         callback=self.parse_detail_page)

                # 新产品列表下面也有几个历史产品
                # for product_info in response.xpath('//div[@class="productlistboxe"]'):
                #     product = BankProductItem()
                #
                #     product['name'] = product_info.xpath('.//div[@class="prdDiv1"]/text()').extract_first().strip()
                #     product['product_type'] = product_info.xpath('.//div[@class="prdDiv"]/text()').re_first(u"[\u4e00-\u9fa5]+")
                #
                #     product['anticipate_rate'] = product_info.xpath(
                #         './/td[@class="second"]/text()').extract_first().strip()
                #
                #     product['limit_time'] = product_info.xpath(
                #         './/td[@class="other"][1]/text()').extract_first().strip()
                #     product['min_amount'] = product_info.xpath(
                #         './/td[@class="other"][last()]/text()').extract_first().strip()
                #
                #     product['bank_domain'] = 'nihaobank.com'
                #
                #     product['code'] = 'no_code'
                #
                #     yield product

    def parse_detail_page(self, response):
        '''解析产品详情页'''

        product = BankProductItem()

        product['bank_domain'] = 'nihaobank.com'

        product_box = response.xpath('//div[@class="productbox"]')
        product['name'] = product_box.xpath('./h1/text()').extract_first().strip()
        product['code'] = response.meta['code']
        product['link'] = response.url

        # border
        product_border = product_box.xpath('.//div[@class="border"]')

        if len(product_border.xpath('.//text()').re(r'起点金额')):

            product['anticipate_rate'] = product_border.xpath('./dl[1]/dd/text()').extract_first().strip()
            product['limit_time'] = product_border.xpath('./dl[2]/dd/text()').extract_first().strip()
            product['min_amount'] = product_border.xpath('./dl[3]/dd/text()').extract_first().strip()

            # table
            product_info_tbl = product_box.xpath('.//table[@class="cpxq"]')
            product['product_type'] = product_info_tbl.xpath('.//tr[1]/td[2]//text()').re_first(u"[\u4e00-\u9fa5]+")
            product['ipo_end_date'] = product_info_tbl.xpath('.//tr[1]/td[4]//text()').extract_first().strip()
            product['income_start_date'] = product_info_tbl.xpath('.//tr[2]/td[4]//text()').extract_first().strip()
            product['product_end_date'] = product_info_tbl.xpath('.//tr[3]/td[2]//text()').extract_first().strip()
            product['risk'] = product_info_tbl.xpath('.//tr[4]/td[2]//text()').re_first(u"[\u4e00-\u9fa5]+")

        elif len(product_border.xpath('.//text()').re(r'投资期限')):

            product['anticipate_rate'] = product_border.xpath('./dl[1]/dd/text()').extract_first().strip()
            product['limit_time'] = product_border.xpath('./dl[2]/dd/text()').extract_first().strip()
            product['min_amount'] = product_border.xpath('./dl[3]/dd/text()').extract_first().strip()

            # table
            product_info_tbl = product_box.xpath('.//table[@class="cpxq"]')
            product['remaining_quota'] = product_info_tbl.xpath('.//tr[1]/td[2]//text()').re_first(u"[\u4e00-\u9fa5]+")
            product['code'] = product_info_tbl.xpath('.//tr[1]/td[4]//text()').extract_first().strip()
            product['product_type'] = product_info_tbl.xpath('.//tr[2]/td[2]//text()').re_first(u"[\u4e00-\u9fa5]+")
            product['finance_type'] = product_info_tbl.xpath('.//tr[2]/td[4]//text()').re_first(u"[\u4e00-\u9fa5]+")
            product['ascend_amount'] = product_info_tbl.xpath('.//tr[3]/td[2]//text()').extract_first().strip()
            product['risk'] = product_info_tbl.xpath('.//tr[3]/td[4]//text()').re_first(u"[\u4e00-\u9fa5]+")
            product['ipo_start_date'] = product_info_tbl.xpath('.//tr[4]/td[2]//text()').extract_first().strip()
            product['ipo_end_date'] = product_info_tbl.xpath('.//tr[4]/td[4]//text()').extract_first().strip()
            product['product_end_date'] = product_info_tbl.xpath('.//tr[5]/td[2]//text()').extract_first().strip()

        elif len(product_border.xpath('.//text()').re(r'理财类型')):
            product['anticipate_rate'] = product_border.xpath('./dl[1]/dd/text()').extract_first().strip()
            product['finance_type'] = product_border.xpath('./dl[2]/dd/text()').extract_first().strip()
            product['min_amount'] = product_border.xpath('./dl[3]/dd/text()').extract_first().strip()

            # table
            product_info_tbl = product_box.xpath('.//table[@class="cpxq"]')
            product['code'] = product_info_tbl.xpath('.//tr[1]/td[2]//text()').extract_first().strip()
            product['risk'] = product_info_tbl.xpath('.//tr[1]/td[4]//text()').extract_first().strip()
            product['product_type'] = product_info_tbl.xpath('.//tr[2]/td[2]//text()').re_first(u"[\u4e00-\u9fa5]+")
            product['ascend_amount'] = product_info_tbl.xpath('.//tr[2]/td[4]//text()').extract_first().strip()

        yield product

    def parse_history_list(self, response):
        for product_info in response.xpath('//div[contains(@class, "productlistboxe")]'):
            product = BankProductItem()

            product['name'] = product_info.xpath('.//div[@class="prdDiv1"]/text()').extract_first().strip()
            product['product_type'] = product_info.xpath('.//div[@class="prdDiv"]/text()').re_first(u"[\u4e00-\u9fa5]+")

            product['anticipate_rate'] = product_info.xpath(
                './/td[@class="second"]/text()').extract_first().strip()

            product['limit_time'] = product_info.xpath(
                './/td[@class="other"][1]/text()').extract_first().strip()
            product['min_amount'] = product_info.xpath(
                './/td[@class="other"][last()]/text()').extract_first().strip()

            product['bank_domain'] = 'nihaobank.com'

            product['code'] = 'no_code'

            yield product
