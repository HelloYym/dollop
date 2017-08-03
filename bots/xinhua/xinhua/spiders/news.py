# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from utils.exporter import read_cache
from xinhua.items import NewsItem


class newsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["xinhua08.com"]

    pipeline = ['UniqueItemPersistencePipeline']

    start_urls_t1 = ['http://app.xinhua08.com/prop.php?pid=45&cid=5333',
                     'http://app.xinhua08.com/prop.php?pid=52&cid=5333',
                     ]

    start_urls_t2 = ['http://fintech.xinhua08.com/hlwjr/zf/',
                     'http://fintech.xinhua08.com/hlwjr/hlwyx/',
                     'http://fintech.xinhua08.com/hlwjr/zx/',
                     'http://fintech.xinhua08.com/fintech/gxjr/',
                     'http://fintech.xinhua08.com/hlwjr/zxlc/',
                     'http://fintech.xinhua08.com/hlwjr/wd/',
                     'http://fintech.xinhua08.com/hlwjr/zc/',
                     'http://bank.xinhua08.com/jgdx/',
                     'http://bank.xinhua08.com/zzyh/',
                     'http://bank.xinhua08.com/wzyh/',
                     'http://bank.xinhua08.com/yhj/',
                     'http://bank.xinhua08.com/lccp/',
                     'http://bank.xinhua08.com/yhbk/',
                     'http://bank.xinhua08.com/yhk/',
                     'http://bank.xinhua08.com/dfyh/',
                     'http://rmb.xinhua08.com/zgyh/',
                     'http://forex.xinhua08.com/yhdt/mlc/',
                     'http://forex.xinhua08.com/yhdt/ozyh/',
                     'http://forex.xinhua08.com/yhdt/ygyh/',
                     'http://forex.xinhua08.com/yhdt/rbyh/',
                     'http://forex.xinhua08.com/yhdt/jndyh/',
                     'http://forex.xinhua08.com/yhdt/adlyyh/',
                     'http://forex.xinhua08.com/yhdt/rsyh/',
                     'http://forex.xinhua08.com/yhdt/qt/'
                     ]

    def start_requests(self):
        for url in self.start_urls_t1:
            yield scrapy.Request(url, dont_filter=True, meta={'page_type': '1'})

        for url in self.start_urls_t2:
            yield scrapy.Request(url, dont_filter=True, meta={'page_type': '2'})

    def parse(self, response):
        total_page = int(response.xpath('//ul[@class="page_down"]/li[last()-1]/a/text()').re_first(r'\d+'))

        # 每天请求前五页
        total_page = 5

        for page_num in range(total_page, 0, -1):
            if response.meta['page_type'] == '1':
                yield scrapy.Request(response.url + '&page=' + str(page_num), dont_filter=True,
                                     callback=self.parse_article_list)
            else:
                yield scrapy.Request(response.url + str(page_num) + '.shtml', dont_filter=True,
                                     callback=self.parse_article_list)

    def parse_article_list(self, response):

        category = get_content(response.xpath('//h1/text()').extract())

        for article_abs in response.xpath('//article'):
            href = article_abs.xpath('./div[@class="newsinfo"]/a/@href').extract_first()

            title = article_abs.xpath('.//h4/text()').extract_first()

            created = article_abs.xpath('.//div[@class="cattime"]/text()').extract_first()

            if href.find('video') < 0 and href.find('forex') < 0:
                yield scrapy.FormRequest(url=href,
                                         callback=self.parse_news_detail,
                                         meta={'title': title, 'created': created, 'category': category},
                                         dont_filter=True)

    def parse_news_detail(self, response):

        news = NewsItem()

        news['thread'] = self.get_thread_from_url(response.url)
        news['source'] = response.url
        news['title'] = response.meta['title']
        # news['created'] = response.meta['created']
        news['created'] = get_content(response.xpath('//div[@class="reInfo"]/div[1]/span[2]/text()').extract())

        news['keywords'] = get_content(response.xpath('//meta[@name="keywords"]/@content').extract())
        news['summary'] = get_content(response.xpath('//meta[@name="description"]/@content').extract())

        # if response.xpath('//div[@class="reInfo"]/div[1]/span[last()]/a/text()'):
        #     news['category'] = get_content(
        #         response.xpath('//div[@class="reInfo"]/div[1]/span[last()]/a/text()').extract())
        # else:
        #     news['category'] = get_content(
        #         response.xpath('//div[@class="reInfo"]/span[last()]/a/text()').extract())

        news['category'] = response.meta['category']

        article = response.xpath('//div[@class="article-content" or @id="ctrlfscont"]') if response.xpath(
            '//div[@class="article-content" or @id="ctrlfscont"]') else response.xpath(
            '//div[@class="Custom_UnionStyle"]')

        news['raw_content'] = article.extract_first()
        news['content'] = ''.join(
            [get_trunk(c) for c in article.xpath('.//text()').extract()])
        news['image_url'] = '#'.join([get_trunk(c) for c in article.xpath('.//img/@src').extract()]) or None

        yield news

    def get_thread_from_url(self, url):
        return url.split('/')[-1].split('.')[0]
