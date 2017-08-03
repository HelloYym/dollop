# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import ReportItem


class BjhReportSpider(scrapy.Spider):
    name = "bjh_report"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    request_url = 'http://www.circ.gov.cn/web/site0/tab5257/module14498/page{page}.htm'

    def start_requests(self):
        total_page = 10
        for page in range(1, total_page + 1):
            yield scrapy.Request(url=self.request_url.format(page=page),
                                 callback=self.parse_list,
                                 dont_filter=True)

    def parse_list(self, response):
        for report_item in response.xpath('//table[contains(@id, "ListC_Info_LstC_Info")]/tr'):
            title = get_content(report_item.xpath('.//td[@class="hui14"]/a/text()').extract())
            id = get_content(report_item.xpath('.//td[@class="hui14"]/a/@id').re(r'\d+'))
            link = 'http://www.circ.gov.cn' + get_content(report_item.xpath('.//td[@class="hui14"]/a/@href').extract())
            created = get_content(report_item.xpath('.//td[@class="hui14"]/../td[last()]/text()').extract())[1:-1]

            if title.find(u'年报') > 0: continue

            yield scrapy.Request(url=link,
                                 callback=self.parse_detail,
                                 meta={'title': title, 'id': id, 'created': created},
                                 dont_filter=True)

    def parse_detail(self, response):
        report = ReportItem()
        report['title'] = response.meta['title']
        report['id'] = response.meta['id']
        report['link'] = response.url
        report['created'] = response.meta['created']

        content = response.xpath('//span[@id="zoom"]')

        report['raw_content'] = content.extract_first()
        report['content'] = ''.join(
            [get_trunk(c) for c in content.xpath('.//text()').extract()])
        report['image_url'] = '#'.join([get_trunk(c) for c in content.xpath('.//img/@src').extract()]) or None

        yield report
