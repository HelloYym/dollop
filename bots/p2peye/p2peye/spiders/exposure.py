# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from utils.exporter import read_cache
from p2peye.items import ExposureItem


class ExposureSpider(scrapy.Spider):
    name = "exposure"
    allowed_domains = ["p2peye.com"]
    image_url_prefix = 'http://www.p2peye.com/'
    exposure_list_url = "http://www.p2peye.com/forumlist-60-{page}.html"
    pipeline = ['UniqueItemPersistencePipeline']

    def modify_image_url(self, url):
        if not url.startswith('http'):
            return self.image_url_prefix + url
        return url

    def start_requests(self):
        '''首先尝试请求全部产品数'''
        yield scrapy.Request(url=self.exposure_list_url.replace('{page}', '1'),
                             callback=self.parse_total_page,
                             dont_filter=True)

    def parse_total_page(self, response):
        total_page = int(response.xpath('//div[@class="page_forumlist"]//label/span/text()').re_first(r'\d+'))

        # print(total_page)

        # 每天爬前10页
        total_page = 10

        for page in range(total_page, 0, -1):
            yield scrapy.Request(url=self.exposure_list_url.replace('{page}', str(page)),
                                 callback=self.parse_exposure_list,
                                 dont_filter=True)

    def parse_exposure_list(self, response):

        for exposure_abs in response.xpath('//div[contains(@class, "item")]'):
            href = exposure_abs.xpath('.//div[@class="forum-main left"]/a/@href').extract_first()
            title = get_content(exposure_abs.xpath('.//div[@class="forum-main left"]/a/div/text()').extract_first())

            yield scrapy.Request(url="http://www.p2peye.com" + href,
                                 callback=self.parse_exposure_detail,
                                 meta={'title': title},
                                 dont_filter=True)

    def get_thread_from_url(self, url):
        if url.find('-') != -1: return url.split('-')[1]
        if url.find('=') != -1: return url.split('=')[-1]
        return None

    def parse_exposure_detail(self, response):

        exposure = ExposureItem()
        exposure['thread'] = self.get_thread_from_url(response.url)
        exposure['source'] = response.url
        exposure['title'] = get_content(response.xpath('//span[@id="thread_subject"]/text()').extract())

        poston = response.xpath('(//div[@class="authi"])[2]/em/text()').extract_first()
        exposure['created'] = poston[poston.index(' ') + 1:]

        exposure['name'] = get_content(response.xpath('//div[@class="typeoption"]//tr[1]/td/text()').extract())
        exposure['link'] = get_content(response.xpath('//div[@class="typeoption"]//tr[2]/td/a/text()').extract())
        exposure['reason'] = get_content(response.xpath('//div[@class="typeoption"]//tr[3]/td/text()').extract())

        body = response.xpath('//td[contains(@id, "postmessage")]')

        exposure['content'] = ''.join([get_trunk(c) for c in body.xpath('.//text()').extract()])
        exposure['raw_content'] = body.extract_first()
        exposure['image_url'] = '#'.join([self.modify_image_url(get_trunk(c)) for c in response.xpath(
            '//ignore_js_op//img[re:test(@zoomfile, "^data")]/@zoomfile').extract()]) or None

        # exposure['image_url'] = response.xpath('//ignore_js_op//img[re:test(@src, "^data")]/@src').extract()

        # print(exposure)
        yield exposure
