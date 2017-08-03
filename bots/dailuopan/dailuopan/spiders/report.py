# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from dailuopan.items import ReportItem


class ReportSpider(scrapy.Spider):
    name = "report"
    allowed_domains = ["http://www.dailuopan.com"]
    pipeline = ['UniqueItemPersistencePipeline']
    start_url = 'http://www.dailuopan.com/P2PReports/'
    category_list = ['wdzj', 'p2peye', 'dlp', 'rong360', 'yifei', 'xinghuo', 'qita']

    def start_requests(self):
        for category in self.category_list:
            yield scrapy.Request(url=self.start_url + category,
                                 meta={'category': category},
                                 callback=self.parse_report_list,
                                 dont_filter=True)

    def parse_report_list(self, response):
        for report in response.xpath('//ul[@class="reportList"]/li/a'):
            title = get_content(report.xpath('./text()').extract())
            link = 'http://www.dailuopan.com' + get_content(report.xpath('./@href').extract())
            print(link)
            yield scrapy.Request(url=link,
                                 meta={'category': response.meta['category']},
                                 callback=self.parse_detail,
                                 dont_filter=True)

    def get_id_from_url(self, url):
        return url.split('=')[-1]

    def parse_detail(self, response):
        report = ReportItem()
        report['thread'] = self.get_id_from_url(response.url)
        report['category'] = response.meta['category']
        report['link'] = response.url
        report['title'] = get_content(response.xpath('//div[@class="report"]/h1/text()').extract())
        report['created'] = get_content(response.xpath('//span[@class="inputtime"]/text()').extract())[-10:]

        article = response.xpath('//div[@class="dianping"]')
        report['raw_content'] = article.extract_first()
        report['content'] = ''.join(
            [get_trunk(c) for c in article.xpath('.//text()').extract()])

        report['image_url'] = '#'.join([get_trunk(c) for c in article.xpath('.//img/@src').extract()]) or None

        yield report
