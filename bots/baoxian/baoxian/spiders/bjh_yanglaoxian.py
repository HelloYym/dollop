# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import YanglaoxianItem
import json


class BjhYanglaoSpider(scrapy.Spider):
    name = "bjh_yanglaoxian"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    request_url = 'http://www.circ.gov.cn/web/site0/tab5204/module14412/page{page}.htm'

    def start_requests(self):
        # total_page = 3
        for page in range(1, 3):
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

        shoutuo_jf = None
        touzi_jf = None
        weituo_jf = None
        shoutuo_zc = None
        touzi_zc = None
        weituo_zc = None

        for tbody in response.xpath('//tbody'):
            if len(tbody.xpath('tr')) > 5:
                for tr in tbody.xpath('tr'):
                    # try:
                    if len(tr.xpath('td')) == 4:
                        name = get_content(tr.xpath('string(td[1])').extract())
                        weituo_jf = get_content(tr.xpath('string(td[2])').extract())
                        shoutuo_jf = get_content(tr.xpath('string(td[3])').extract())
                        touzi_jf = get_content(tr.xpath('string(td[4])').extract())
                    elif len(tr.xpath('td')) == 7:
                        name = get_content(tr.xpath('string(td[1])').extract())
                        shoutuo_jf = get_content(tr.xpath('string(td[2])').extract())
                        touzi_jf = get_content(tr.xpath('string(td[3])').extract())
                        weituo_jf = get_content(tr.xpath('string(td[4])').extract())
                        shoutuo_zc = get_content(tr.xpath('string(td[5])').extract())
                        touzi_zc = get_content(tr.xpath('string(td[6])').extract())
                        weituo_zc = get_content(tr.xpath('string(td[7])').extract())
                    else:
                        continue

                    if shoutuo_jf and shoutuo_jf.find(u'企业') >= 0:
                        continue

                    if name and name.find(u'简称') < 0:
                        company = YanglaoxianItem()
                        company['title'] = title
                        company['year'] = year
                        company['month'] = month
                        company['link'] = link
                        company['company_name'] = name
                        company['shoutuo_jf'] = shoutuo_jf
                        company['touzi_jf'] = touzi_jf
                        company['weituo_jf'] = weituo_jf
                        company['shoutuo_zc'] = shoutuo_zc
                        company['touzi_zc'] = touzi_zc
                        company['weituo_zc'] = weituo_zc
                        company['content'] = content
                        company['created'] = created
                        yield company
                        # except:
                        #     print(name)
                        #     print(len(tr.xpath('td')))
                        #     print(shoutuo_jf)

                        # yield company
