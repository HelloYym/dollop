# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from nifa.items import BaseInfoItem, GovernInfoItem, SiteInfoItem, FinanceInfoItem, TradeLogItem
import json


class CompanySpider(scrapy.Spider):
    name = "company"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["dp.nifa.org.cn"]
    request_url = 'https://dp.nifa.org.cn/HomePage'

    def start_requests(self):
        total_page = 20
        for page in range(1, total_page + 1):
            yield scrapy.FormRequest(url=self.request_url,
                                     formdata={'method': 'getPublishedInfo', 'currentPage': str(page)},
                                     callback=self.parse_list,
                                     dont_filter=True)

    def parse_list(self, response):
        for company_id in response.xpath('//ul[@id="jigou"]/input/@value').extract():
            yield scrapy.FormRequest(url=self.request_url + '?method=getTargetOrgInfo&sorganation=' + company_id,
                                     # formdata={'method': 'getTargetOrgInfo', 'sorganation': company_id},
                                     meta={'code': company_id},
                                     callback=self.parse_detail,
                                     dont_filter=True)

    def parse_detail(self, response):

        # comp_intro = response.xpath('//div[@class="comp-intro"]')
        # icon = get_content(comp_intro.xpath('.//img[@class="intro-icon"]/src').extract())
        # intro_txt = comp_intro.xpath('.//div[@class="intro-txt"]/span')
        # short_name = get_content(intro_txt[0].xpath('string(.)').extract())
        # full_name = get_content(intro_txt[1].xpath('string(.)').extract())
        # address = get_content(intro_txt[2].xpath('string(.)').extract()).split(u'：')[-1]
        # website = get_content(intro_txt[3].xpath('string(.)').extract())

        yield self.parse_base_info(response)
        yield self.parse_govern_info(response)
        yield self.parse_site_info(response)
        yield self.parse_finance_info(response)
        for company_trade_log in self.parse_trade_log(response):
            yield company_trade_log

    def parse_trade_log(self, response):

        attr_list = response.xpath('//*[@id="trade-log"]/table[2]/tr[1]/td/text()').extract()
        date_list = response.xpath('//*[@id="trade-log"]/table[1]/tr/td[@class="table-label"]/text()').extract()

        date_list = [get_trunk(date) for date in date_list if
                     get_trunk(date) != '' and get_trunk(date).find(u'信息截止日期') < 0]


        for i, date in enumerate(date_list):
            company = TradeLogItem()
            company['link'] = response.url
            company['code'] = response.meta['code']
            name = get_content(
                response.xpath('//div[@class="comp-intro"]').xpath('.//div[@class="intro-txt"]/span')[0].xpath(
                    'string(.)').extract())
            company['name'] = name
            company['date'] = date

            log = dict()

            attr_value_list = response.xpath(
                '//*[@id="trade-log"]/table[2]/tr[{}]/td/text()'.format(str(i + 2))).extract()
            attr_value_list = [get_trunk(value) for value in attr_value_list]

            for j in range(len(attr_value_list)):
                log[attr_list[j]] = attr_value_list[j]

            company['log'] = json.dumps(log, encoding="UTF-8", ensure_ascii=False)
            yield company

    def parse_finance_info(self, response):
        company = FinanceInfoItem()
        company['link'] = response.url
        company['code'] = response.meta['code']
        company['name'] = get_content(
            response.xpath('//div[@class="comp-intro"]').xpath('.//div[@class="intro-txt"]/span')[0].xpath(
                'string(.)').extract())
        finance_info = response.xpath('//div[@id="finance"]')

        finance_list = list()
        for tr in finance_info.xpath('table/tbody/tr'):
            name = get_content(tr.xpath('td[2]/a/text()').extract())
            link = get_content(tr.xpath('td[2]/a/@href').extract())
            finance_list.append({'name': name, 'link': link})

        company['finance_list'] = json.dumps(finance_list, encoding="UTF-8", ensure_ascii=False)

        return company

    def parse_site_info(self, response):
        company = SiteInfoItem()
        company['link'] = response.url
        company['code'] = response.meta['code']
        site_info = response.xpath('//div[@id="site-plate"]')
        for tr in site_info.xpath('table[@class="table"]//tr'):
            key = get_content(tr.xpath('string(td[1])').extract())
            value = get_content(tr.xpath('string(td[2])').extract())
            if not key or not value: continue
            if key.find(u'平台地址') >= 0:
                company['website'] = value
            elif key.find(u'平台简称') >= 0:
                company['short_name'] = value
            elif key.find(u'上线运营时间') >= 0:
                company['online_time'] = value
            elif key.find(u'许可') >= 0:
                company['license'] = value
            elif key.find(u'应用') >= 0:
                company['app'] = value
            elif key.find(u'微信') >= 0:
                company['wechat'] = value

        certification = dict()
        for tr in site_info.xpath('table[@class="small-table"]/tbody/tr'):
            key = get_content(tr.xpath('string(td[1])').extract())
            value = get_content(tr.xpath('string(td[2])').extract())
            certification[key] = value
        company['certification'] = json.dumps(certification, encoding="UTF-8", ensure_ascii=False)

        return company

    def parse_govern_info(self, response):
        name = get_content(
            response.xpath('//div[@class="comp-intro"]').xpath('.//div[@class="intro-txt"]/span')[0].xpath(
                'string(.)').extract())

        company = GovernInfoItem()
        company['link'] = response.url
        company['name'] = name
        company['code'] = response.meta['code']

        govern_info = response.xpath('//div[@id="govern-info"]')

        company['structure'] = get_content(response.xpath('//div[@class="mask"]/img[@class="mask-img"]/@src').extract())

        relation = dict()
        for tr in govern_info.xpath('table[2]/tbody/tr'):
            key = get_content(tr.xpath('string(td[1])').extract())
            value = get_content(tr.xpath('string(td[2])').extract())
            relation[key] = value
        company['relation'] = json.dumps(relation, encoding="UTF-8", ensure_ascii=False)

        controller = govern_info.xpath('table[3]/tbody/tr[1]/td/text()').extract()
        company['controller'] = json.dumps(controller, encoding="UTF-8", ensure_ascii=False)

        shareholder_list = list()
        for tr in govern_info.xpath('table[4]/tbody/tr'):
            shareholder_list.append(
                [get_trunk(item) for item in tr.xpath('td//text()').extract() if get_trunk(item) != ''])

        company['shareholder_list'] = json.dumps(shareholder_list, encoding="UTF-8", ensure_ascii=False)

        manager_list = list()
        for tr in govern_info.xpath('table[5]/tbody/tr'):
            manager_list.append([get_trunk(item) for item in tr.xpath('td//text()').extract() if get_trunk(item) != ''])

        company['manager_list'] = json.dumps(manager_list, encoding="UTF-8", ensure_ascii=False)

        return company

    def parse_base_info(self, response):
        company = BaseInfoItem()
        company['link'] = response.url
        base_info = response.xpath('//div[@id="base-info"]')
        for tr in base_info.xpath('table[@class="table"]//tr'):
            key = get_content(tr.xpath('string(td[1])').extract())
            value = get_content(tr.xpath('string(td[2])').extract())

            if not key or not value: continue

            if key.find(u'中文名称') >= 0:
                company['full_name'] = value
            elif key.find(u'简称') >= 0:
                company['short_name'] = value
            elif key.find(u'从业机构编码') >= 0:
                company['code'] = value
            elif key.find(u'注册资本') >= 0:
                company['registered_capital'] = value
            elif key.find(u'注册地址国家') >= 0:
                company['zc_country'] = value
            elif key.find(u'注册地址省份') >= 0:
                company['zc_province'] = value
            elif key.find(u'注册地所在市') >= 0:
                company['zc_city'] = value
            elif key.find(u'注册具体地址') >= 0:
                company['zc_address'] = value
            elif key.find(u'地区代码') >= 0:
                company['zc_zip'] = value
            elif key.find(u'成立时间') >= 0:
                company['estab_date'] = value
            elif key.find(u'代表人') >= 0:
                company['legal_person'] = value
            elif key.find(u'经营范围') >= 0:
                company['scope'] = value
            elif key.find(u'传真') >= 0:
                company['fax'] = value
            elif key.find(u'电话') >= 0:
                company['phone'] = value
            elif key.find(u'邮箱') >= 0:
                company['email'] = value
            elif key.find(u'经营地所在国家') >= 0:
                company['jy_country'] = value
            elif key.find(u'经营地所在省份') >= 0:
                company['jy_province'] = value
            elif key.find(u'经营地所在市') >= 0:
                company['jy_city'] = value
            elif key.find(u'经营地具体地址') >= 0:
                company['jy_address'] = value
            elif key.find(u'实缴资本') >= 0:
                company['paidin_capital'] = value
            elif key.find(u'存管银行') >= 0:
                company['fund_bank'] = value
            elif key.find(u'存管说明') >= 0:
                company['fund_info'] = value
            elif key.find(u'注册协议模板') >= 0:
                company['agreement_pdf'] = get_content(tr.xpath('td[2]/a/@href').extract())

        partner_list = list()
        for tr in base_info.xpath('table[@class="small-table"]/tbody/tr'):
            partner_name = get_content(tr.xpath('string(td[2])').extract())
            partner_info = get_content(tr.xpath('string(td[3])').extract())
            partner_list.append({'partner_name': partner_name, 'partner_info': partner_info})
        company['partner_list'] = json.dumps(partner_list, encoding="UTF-8", ensure_ascii=False)

        return company
