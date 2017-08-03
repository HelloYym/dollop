# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import RecordProductItem


class BjhRecordProductSpider(scrapy.Spider):
    name = "bjh_record_product"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]

    start_urls = ['http://www.circ.gov.cn/tabid/5253/ctl/ViewOrgList/mid/16658/OrgTypeID/1/Default.aspx?ctlmode=none',
                  'http://www.circ.gov.cn/tabid/5253/ctl/ViewOrgList/mid/16658/OrgTypeID/2/Default.aspx?ctlmode=none']

    def get_code_from_url(self, url):
        return url.split('/')[-2]

    def parse(self, response):
        product_type = get_content(
            response.xpath('//span[@id="ess_ctr16658_ViewOrgList_lblClassName"]/text()').extract())
        for td in response.xpath('//td[@class="orglist_td"]'):
            company_link = 'http://www.circ.gov.cn' + get_content(td.xpath('a/@href').extract())
            company_name = get_content(td.xpath('a/text()').extract())
            company_code = self.get_code_from_url(company_link)
            yield scrapy.FormRequest(url=company_link,
                                     formdata={'ctlmode': 'none'},
                                     callback=self.parse_product_list,
                                     meta={'company_name': company_name, 'company_code': company_code,
                                           'company_link': company_link, 'product_type': product_type},
                                     dont_filter=True)

    def parse_product_list(self, response):
        for record in response.xpath('//table[@class="tableRecordProduct"]/tr'):
            product = RecordProductItem()
            if get_content(record.xpath('td[1]/text()').extract()).find(u'产品名称') >= 0: continue
            product['product_name'] = get_content(record.xpath('td[1]/text()').extract())
            product['record_date'] = get_content(record.xpath('td[2]/text()').extract())
            product['type'] = get_content(record.xpath('td[3]/text()').extract())
            product['product_type'] = response.meta['product_type']
            product['company_name'] = response.meta['company_name']
            product['company_code'] = response.meta['company_code']
            product['company_link'] = response.meta['company_link']

            yield product
