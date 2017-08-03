# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content


class zfjgSpider(scrapy.Spider):
    name = "zfjg"
    allowed_domains = ["pbc.gov.cn"]

    pipeline = ['UniqueItemPersistencePipeline']

    start_url1 = 'http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/1923629/d6d180ae/index{page}.html'
    start_url2 = 'http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/2942702/224d927f/index{page}.html'

    def start_requests(self):

        # 每天请求的个数
        total_page = 1

        for page in range(total_page, 0, -1):
            yield scrapy.Request(url=self.start_url1.format(page=page),
                                 callback=self.parse_list)

    def parse_list(self, response):
        print(response)

        for info in response.xpath('//table'):
            title = info.xpath('.//a/@title').extract_first()

            print(title)

            # yield scrapy.FormRequest(url=href,
            #                          callback=self.parse_news_detail,
            #                          meta={})

    # def parse_news_detail(self, response):
    #
    #     news = NewsItem()
    #     news['thread'] = self.get_thread_from_url(response.url)
    #     news['source'] = response.url
    #     news['title'] = get_content(response.xpath('//title/text()').extract())
    #
    #     news['created'] = get_content(response.xpath('//small/span[last()]/text()').extract())
    #     news['author'] = response.xpath('//meta[@name="author"]/@content').extract_first()
    #
    #     news['summary'] = response.xpath('//meta[@name="description"]/@content').extract_first()
    #
    #     news['keywords'] = response.xpath('//meta[@name="keywords"]/@content').extract_first()
    #
    #     news['category'] = get_content(
    #         response.xpath('//small/span[1]/a/text()').extract())
    #
    #     article = response.xpath('//div[@class="article-txt"]')
    #     news['raw_content'] = article.extract_first()
    #     news['content'] = ''.join(
    #         [get_trunk(c) for c in article.xpath('.//text()').extract()])
    #
    #     news['image_url'] = '#'.join([get_trunk(c) for c in article.xpath('.//img/@src').extract()]) or None
    #
    #     # print(news)
    #     yield news
