# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import ExposureCompanyItem, CooperationItem
import json


class BhxCooperationSpider(scrapy.Spider):
    name = "bhx_cooperation"
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
            column_id = response.meta['columnid']
            company = ExposureCompanyItem.get_company(column_id, company_code, info_no)

            # 合作中介列表
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllZJ.do',
                                     method='POST',
                                     formdata={'columnid': column_id,
                                               'internetInformationNo': info_no,
                                               'informationno': info_no,
                                               'zj': zj},
                                     meta={'company': company},
                                     callback=self.parse_cooperation_list,
                                     dont_filter=True)

            # 合作中介列表 历史
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllZJHis.do',
                                     method='POST',
                                     formdata={'columnid': column_id,
                                               'internetInformationNo': info_no,
                                               'informationno': info_no,
                                               'zj': zj},
                                     meta={'company': company},
                                     callback=self.parse_cooperation_list,
                                     dont_filter=True)

            # 合作第三方列表
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllSecond.do',
                                     method='POST',
                                     formdata={'columnid': column_id,
                                               'internetInformationNo': info_no,
                                               'informationno': info_no,
                                               'zj': zj},
                                     meta={'company': company},
                                     callback=self.parse_cooperation_list,
                                     dont_filter=True)

            # 合作第三方列表 历史
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllSecondHis.do',
                                     method='POST',
                                     formdata={'columnid': column_id,
                                               'internetInformationNo': info_no,
                                               'informationno': info_no,
                                               'zj': zj},
                                     meta={'company': company},
                                     callback=self.parse_cooperation_list,
                                     dont_filter=True)

    def parse_cooperation_list(self, response):

        company = response.meta['company']

        for company_item in response.xpath('//div[@class="xz_nei"]/ul/li/p/a'):
            info = json.loads(
                company_item.xpath('@onclick').re_first(r'zjDetail(.*?);').replace('(', '[').replace(')', ']').replace(
                    '\'', '\"'))
            # flag 01:当前 00:历史
            # type 01:中介 02:第三方
            terrace_no, old_terrace_no, flag, type = info

            cooperation = CooperationItem()
            cooperation['terrace_no'] = terrace_no
            cooperation['old_terrace_no'] = old_terrace_no
            cooperation['flag'] = flag
            cooperation['type'] = type
            cooperation['company'] = company

            if flag == '01':
                # 合作中介列表
                yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewTerraceProduct.do',
                                         method='POST',
                                         formdata={'columnid': company.column_id,
                                                   'internetInformationNo': company.info_no,
                                                   'informationno': company.info_no,
                                                   'zj': company.zj,
                                                   'terraceNo': terrace_no,
                                                   'oldTerraceNo': old_terrace_no,
                                                   'type': flag,
                                                   'comType': type},
                                         meta={'cooperation': cooperation},
                                         callback=self.parse_cooperation_detail,
                                         dont_filter=True)
            elif flag == '00':
                # 合作中介列表 历史
                yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewTerraceProductHis.do',
                                         method='POST',
                                         formdata={'columnid': company.column_id,
                                                   'internetInformationNo': company.info_no,
                                                   'informationno': company.info_no,
                                                   'zj': company.zj,
                                                   'terraceNo': terrace_no,
                                                   'oldTerraceNo': old_terrace_no,
                                                   'type': flag,
                                                   'comType': type},
                                         meta={'cooperation': cooperation},
                                         callback=self.parse_cooperation_detail,
                                         dont_filter=True)

    def parse_cooperation_detail(self, response):
        cooperation = response.meta['cooperation']
        company = cooperation['company']

        for entry in response.xpath('//div[@class="ppp"]/p'):
            key = get_content(entry.xpath('span/text()').extract())
            value = get_content(entry.xpath('text()').extract()).replace(u'：', '')

            if u'全称' in key:
                cooperation['full_name'] = value
            elif u'简称' in key:
                cooperation['short_name'] = value
            elif u'地址' in key:
                cooperation['website'] = value
            elif u'备案' in key:
                cooperation['records'] = value
            elif u'范围' in key:
                cooperation['scope'] = value
            elif u'起始' in key:
                cooperation['start_date'] = value
            elif u'终止' in key:
                cooperation['end_date'] = value

        yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllPro.do',
                                 method='POST',
                                 formdata={'columnid': company.column_id,
                                           'internetInformationNo': company.info_no,
                                           'zj': company.zj,
                                           'terraceNo': cooperation['terrace_no'],
                                           'oldTerraceNo': cooperation['old_terrace_no'],
                                           'type': cooperation['flag'],
                                           'comType': cooperation['type']},
                                 meta={'cooperation': cooperation, 'type': 'cur'},
                                 callback=self.parse_cooperation_product_list,
                                 dont_filter=True)

    def parse_cooperation_product_list(self, response):

        cooperation = response.meta['cooperation']

        product_list = list()
        for entry in response.xpath('//div[@class="xz_nei_lxf"]/ul/li'):
            actual_name = get_content(entry.xpath('string(p[1])').extract())
            record_name = get_content(entry.xpath('string(p[2])').extract())
            product_list.append({'actual_name': actual_name, 'record_name': record_name})

        if response.meta['type'] == 'cur':
            cooperation['cur_product_list'] = json.dumps(product_list, encoding="UTF-8", ensure_ascii=False)
            # 历史
            company = cooperation['company']
            yield scrapy.FormRequest(url='http://icid.iachina.cn/ICID/front/viewAllProHis.do',
                                     method='POST',
                                     formdata={'columnid': company.column_id,
                                               'internetInformationNo': company.info_no,
                                               'zj': company.zj,
                                               'terraceNo': cooperation['terrace_no'],
                                               'oldTerraceNo': cooperation['old_terrace_no'],
                                               'type': cooperation['flag'],
                                               'comType': cooperation['type']},
                                     meta={'cooperation': cooperation, 'type': 'his'},
                                     callback=self.parse_cooperation_product_list,
                                     dont_filter=True)

        else:
            cooperation['his_product_list'] = json.dumps(product_list, encoding="UTF-8", ensure_ascii=False)
            yield cooperation
