# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from utils.exporter import read_cache
from lingyi.items import NewsItem


class newsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["01caijing.com"]

    image_url_prefix = 'http://www.p2peye.com/'

    pipeline = ['UniqueItemPersistencePipeline']

    category_ids = ['1014', '1002', '1010', '1022', '1003']

    request_url = 'http://www.01caijing.com/articles_loading.json'

    def modify_image_url(self, url):
        if not url.startswith('http'):
            return self.image_url_prefix + url
        return url

    def get_thread_from_url(self, url):
        return url.split('/')[-1].split('.')[0]

    def start_requests(self):

        # 每天请求的个数
        page_size = 100
        for category_id in self.category_ids:
            yield scrapy.FormRequest(url=self.request_url,
                                     formdata={'categoryId': category_id, 'pageSize': str(page_size), 'pageIndex': '1'},
                                     meta={'categoryId': category_id},
                                     callback=self.parse_article_list)

    def parse_article_list(self, response):

        for article_abs in response.xpath('//div[@class="single-article"]'):
            body = article_abs.xpath('.//div[@class="media-body"]')

            href = body.xpath('.//a/@href').extract_first()
            title = body.xpath('.//a/text()').extract_first()

            # author = body.xpath('./small/text()').extract_first()
            # created = article_abs.xpath('.//div[@class="fd"]/span[3]/text()').extract_first()

            category = response.meta['categoryId']

            summary = get_content(body.xpath('./p/text()').extract())

            print(href, title, summary)

            yield scrapy.FormRequest(url=href,
                                     callback=self.parse_news_detail,
                                     meta={})

    def parse_news_detail(self, response):

        news = NewsItem()
        news['thread'] = self.get_thread_from_url(response.url)
        news['source'] = response.url
        news['title'] = get_content(response.xpath('//title/text()').extract())

        news['created'] = get_content(response.xpath('//small/span[last()]/text()').extract())
        news['author'] = response.xpath('//meta[@name="author"]/@content').extract_first()

        news['summary'] = response.xpath('//meta[@name="description"]/@content').extract_first()

        news['keywords'] = response.xpath('//meta[@name="keywords"]/@content').extract_first()

        news['category'] = get_content(
            response.xpath('//small/span[1]/a/text()').extract())

        article = response.xpath('//div[@class="article-txt"]')
        news['raw_content'] = article.extract_first()
        news['content'] = ''.join(
            [get_trunk(c) for c in article.xpath('.//text()').extract()])

        news['image_url'] = '#'.join([get_trunk(c) for c in article.xpath('.//img/@src').extract()]) or None

        # print(news)
        yield news