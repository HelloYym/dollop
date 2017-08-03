# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import RegionItem
import json


class BjhRegionSpider(scrapy.Spider):
    name = "bjh_region"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    request_url = 'http://www.circ.gov.cn/web/site0/tab5205/module14413/page{page}.htm'

    def start_requests(self):
        # total_page = 3
        for page in range(1, 10):
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

        amount = None
        caichanxian = None
        shouxian = None
        yiwaixian = None
        jiankangxian = None

        for tbody in response.xpath('//tbody'):
            if len(tbody.xpath('tr')) > 5:
                for tr in tbody.xpath('tr'):
                    # try:
                    if len(tr.xpath('td')) == 6:
                        region_name = get_content(tr.xpath('string(td[1])').extract())
                        amount = get_content(tr.xpath('string(td[2])').extract())
                        caichanxian = get_content(tr.xpath('string(td[3])').extract())
                        shouxian = get_content(tr.xpath('string(td[4])').extract())
                        yiwaixian = get_content(tr.xpath('string(td[5])').extract())
                        jiankangxian = get_content(tr.xpath('string(td[6])').extract())
                    else:
                        continue

                    if region_name and region_name.find(u'地区') < 0:
                        region = RegionItem()
                        region['title'] = title
                        region['year'] = year
                        region['month'] = month
                        region['link'] = link
                        region['region'] = region_name
                        region['amount'] = amount
                        region['caichanxian'] = caichanxian
                        region['shouxian'] = shouxian
                        region['yiwaixian'] = yiwaixian
                        region['jiankangxian'] = jiankangxian
                        region['content'] = content
                        region['created'] = created

                        yield region
