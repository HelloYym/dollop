# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from utils.exporter import read_cache
from p2peye.items import NewsItem


class newsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["p2peye.com"]
    image_url_prefix = 'http://www.p2peye.com/'
    news_list_url = "http://news.p2peye.com/jkgl/{page}.html"
    pipeline = ['UniqueItemPersistencePipeline']

    start_urls = ['http://news.p2peye.com/wdxw/',
                  'http://news.p2peye.com/hygd/',
                  'http://news.p2peye.com/wdzl/',
                  'http://news.p2peye.com/hlwjr/',
                  'http://news.p2peye.com/tzlc/',
                  'http://news.p2peye.com/ptdt/',
                  'http://news.p2peye.com/jkgl/']

    def modify_image_url(self, url):
        if not url.startswith('http'):
            return self.image_url_prefix + url
        return url

    # def start_requests(self):
    #     '''首先尝试请求全部产品数'''
    #     yield scrapy.Request(url=self.news_list_url.replace('{page}', '1'),
    #                          callback=self.parse_total_page,
    #                          dont_filter=True)


    def parse(self, response):
        total_page = int(response.xpath('//div[@class="c-page"]/a[last()]/@href').re_first(r'\d+'))

        # print(total_page)

        # 每天爬前10页
        # total_page = 1

        for page in range(total_page, 0, -1):
            yield scrapy.Request(url=response.url + str(page) + '.html',
                                 callback=self.parse_news_list,
                                 dont_filter=True)

    def parse_news_list(self, response):

        for news_abs in response.xpath('//div[contains(@class, "mod-news")]'):
            href = news_abs.xpath('.//div[@class="hd"]/a/@href').extract_first()
            author = news_abs.xpath('.//div[@class="fd"]/span[1]/a/text()').extract_first()
            category = news_abs.xpath('.//div[@class="fd"]/span[2]/a/text()').extract_first()
            created = news_abs.xpath('.//div[@class="fd"]/span[3]/text()').extract_first()
            summary = news_abs.xpath('.//div[@class="bd"]/text()').extract_first()
            yield scrapy.Request(url=href,
                                 callback=self.parse_news_detail,
                                 meta={'author': author, 'category': category, 'created': created, 'summary': summary},
                                 dont_filter=True)

    def get_thread_from_url(self, url):
        if url.find('-') != -1: return url.split('-')[1]
        if url.find('=') != -1: return url.split('=')[-1]
        return None

    def parse_news_detail(self, response):

        news = NewsItem()
        news['thread'] = self.get_thread_from_url(response.url)
        news['source'] = response.url
        news['title'] = get_content(response.xpath('//h1/text()').extract())

        news['created'] = response.meta['created']
        news['author'] = response.meta['author']

        news['category'] = response.meta['category']

        news['summary'] = response.meta['summary']

        article = response.xpath('//td[@id="article_content"]')
        news['raw_content'] = article.extract_first()
        news['content'] = ''.join(
            [get_trunk(c) for c in article.xpath('.//p[contains(@class, "ke-editor-inner-p")]/text()').extract()])

        news['image_url'] = '#'.join([self.modify_image_url(get_trunk(c)) for c in article.xpath('.//img/@src').extract()]) or None

        yield news
