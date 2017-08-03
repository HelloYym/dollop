# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import ExposureCompanyItem
import json
import copy


class BhxExposureSpider(scrapy.Spider):
    name = "bhx_exposure"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    request_url = 'http://www.circ.gov.cn/web/site0/tab5257/module14498/page{page}.htm'

    def start_requests(self):

        yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/getChildColumns.do',
                                 method='GET',
                                 formdata={'supColumnId': '201509301401'},
                                 callback=self.parse_column,
                                 dont_filter=True)

    def parse_column(self, response):
        column_list = json.loads(response.body.decode(response.encoding))['data']
        for column in column_list:
            columnname = column['columnname']
            columnid = column['columnid']
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/leafColComType.do',
                                     method='POST',
                                     formdata={'columnid': columnid},
                                     meta={'columnname': columnname, 'columnid': columnid},
                                     callback=self.parse_company_list,
                                     dont_filter=True)

    def parse_company_list(self, response):
        for company_item in response.xpath('//div[@class="jie_nei"]/ul/li/a'):
            info = json.loads(
                company_item.xpath('@onclick').re_first(r'company0(.*?);').replace('(', '[').replace(')', ']').replace(
                    '\'', '\"'))
            company_code, info_no, zj = info
            attr = response.xpath('//input[@id="attr"]/@value').extract_first()

            company = ExposureCompanyItem()
            company['column_id'] = response.meta['columnid']
            company['company_code'] = company_code
            company['info_no'] = info_no
            company['zj'] = zj
            company['name'] = company_item.xpath('text()').extract_first()

            # 披露公司详情信息
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/getCompanyInfos.do',
                                     method='POST',
                                     formdata={'columnid': response.meta['columnid'],
                                               'comCode': company_code,
                                               'informationno': info_no, 'zj': zj, 'attr': attr},
                                     meta={'company': company},
                                     callback=self.parse_company_detail,
                                     dont_filter=True)

    def parse_company_detail(self, response):
        company = response.meta['company']
        data_dict = dict()
        for entry in response.xpath('//div[@class="jie_nei"]/ul/li'):
            key = get_content(entry.xpath('p[1]/text()').extract())
            value = get_content(entry.xpath('string(p[2])').extract())
            data_dict[key] = value

        company['detail_info'] = json.dumps(data_dict, encoding="UTF-8", ensure_ascii=False)

        # 二级分公司信息
        yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllBranch.do',
                                 method='POST',
                                 formdata={'columnid': company['column_id'],
                                           'internetInformationNo': company['info_no'],
                                           'informationno': company['info_no'],
                                           'zj': company['zj']},
                                 meta={'company': company},
                                 callback=self.parse_sub_company_list,
                                 dont_filter=True)

    def parse_sub_company_list(self, response):
        company = response.meta['company']

        sub_company_list = list()
        for entry in response.xpath('//div[@class="ge"]/ul/li'):
            name = get_content(entry.xpath('string(p[1])').extract())
            address = get_content(entry.xpath('string(p[2])').extract())
            phone = get_content(entry.xpath('string(p[3])').extract())
            sub_company_list.append({'name': name, 'address': address, 'phone': phone})

        company['sub_company_list'] = json.dumps(sub_company_list, encoding="UTF-8", ensure_ascii=False)

        # 当前保险产品信息
        yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllPros.do',
                                 method='POST',
                                 formdata={'columnid': company['column_id'],
                                           'internetInformationNo': company['info_no'],
                                           'informationno': company['info_no'],
                                           'zj': company['zj']},
                                 meta={'company': company, 'type': 'cur'},
                                 callback=self.parse_product_list,
                                 dont_filter=True)

    def parse_product_list(self, response):
        company = response.meta['company']

        product_list = list()
        for entry in response.xpath('//div[@class="ge"]/ul/li'):
            actual_name = get_content(entry.xpath('string(p[1])').extract())
            record_name = get_content(entry.xpath('string(p[2])').extract())
            record_no = get_content(entry.xpath('string(p[3])').extract())
            product_list.append(
                {'actual_name': actual_name, 'record_name': record_name, 'record_no': record_no})
        if response.meta['type'] == 'cur':
            company['cur_product_list'] = json.dumps(product_list, encoding="UTF-8", ensure_ascii=False)
            # 历史保险产品信息
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllProsHis.do',
                                     method='POST',
                                     formdata={'columnid': company['column_id'],
                                               'internetInformationNo': company['info_no'],
                                               'informationno': company['info_no'],
                                               'zj': company['zj']},
                                     meta={'company': company, 'type': 'his'},
                                     callback=self.parse_product_list,
                                     dont_filter=True)

        else:
            company['his_product_list'] = json.dumps(product_list, encoding="UTF-8", ensure_ascii=False)
            company['type'] = ['人身险', '财产险', '中介类'][int(company['column_id'][-1]) - 1]
            yield company
