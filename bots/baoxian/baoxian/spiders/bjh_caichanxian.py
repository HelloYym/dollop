# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import CaichanxianItem
import json


class BjhCcxSpider(scrapy.Spider):
    name = "bjh_caichanxian"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    request_url = 'http://www.circ.gov.cn/web/site0/tab5202/module14410/page{page}.htm'

    def start_requests(self):
        total_page = 15
        for page in range(total_page):
            # page = 11
            yield scrapy.Request(url=self.request_url.format(page=page),
                                 callback=self.parse_list,
                                 dont_filter=True)

    def parse_title(self, title):
        year = title[:4]
        if title.find(u'月') > 0:
            if title.find('-') > 0:
                month = title[title.find('-') + 1: title.find(u'月')]
            else:
                month = title[title.find(u'年') + 1: title.find(u'月')]
        else:
            month = '12'

        return year, month

    def parse_list(self, response):
        for report_item in response.xpath('//table[contains(@id, "ListC_Info_LstC_Info")]/tr'):
            title = get_content(report_item.xpath('.//td[@class="hui14"]//a/text()').extract())
            id = get_content(report_item.xpath('.//td[@class="hui14"]//a/@id').re(r'\d+'))
            link = 'http://www.circ.gov.cn' + get_content(report_item.xpath('.//td[@class="hui14"]//a/@href').extract())
            created = get_content(report_item.xpath('.//td[@class="hui14"]/../td[last()]/text()').extract())[1:-1]
            yield scrapy.Request(url=link,
                                 callback=self.parse_detail,
                                 meta={'title': title, 'id': id, 'created': created},
                                 dont_filter=True)

    def parse_detail(self, response):

        title = response.meta['title']
        year, month = self.parse_title(title)
        created = response.meta['created']
        link = response.url
        capital_structure = None
        content = ' '.join([get_trunk(c) for c in response.xpath('//p//text()').extract()])
        share = None
        flag = False

        for tbody in response.xpath('//tbody'):
            if len(tbody.xpath('tr')) > 10:
                for tr in tbody.xpath('tr'):
                    if len(tr.xpath('td')) == 3:
                        if flag:
                            name = get_content(tr.xpath('string(td[1])').extract())
                            income = get_content(tr.xpath('string(td[2])').extract())
                            share = get_content(tr.xpath('string(td[3])').extract())
                        else:
                            name = get_content(tr.xpath('string(td[2])').extract())
                            income = get_content(tr.xpath('string(td[3])').extract())
                            try:
                                if get_content(tr.xpath('string(td[1])').extract()).find(u'资') >= 0:
                                    capital_structure = get_content(tr.xpath('string(td[1])').extract())
                            except:
                                pass
                    elif len(tr.xpath('td')) == 2:
                        name = get_content(tr.xpath('string(td[1])').extract())
                        income = get_content(tr.xpath('string(td[2])').extract())
                    elif len(tr.xpath('td')) == 4:
                        try:
                            if get_content(tr.xpath('string(td[1])').extract()).find(u'资') >= 0:
                                capital_structure = get_content(tr.xpath('string(td[1])').extract())
                        except:
                            pass
                        name = get_content(tr.xpath('string(td[3])').extract())
                        income = get_content(tr.xpath('string(td[4])').extract())

                    else:
                        continue

                    if income and income.find(u'份额') >= 0:
                        flag = True
                    if name and income and name.find(u'公司名称') < 0 and name.find(u'小计') < 0 and name.find(u'合计') < 0:
                        if income.find(u'万元') >= 0 or income.find(u'保费') >= 0 or income.find(u'份额') >= 0: continue
                        company = CaichanxianItem()
                        company['title'] = title
                        company['year'] = year
                        company['month'] = month
                        company['link'] = link
                        company['company_name'] = name
                        company['income'] = income
                        company['capital_structure'] = capital_structure
                        company['content'] = content
                        company['created'] = created
                        if flag:
                            company['share'] = share
                        yield company
