# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import MemberItem
import json


class BhxMemberSpider(scrapy.Spider):
    name = "bhx_member"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    start_urls = ['http://old.iachina.cn/about/hyxx/gshy/jtgs/',
                  'http://old.iachina.cn/about/hyxx/gshy/ccbxgs/',
                  'http://old.iachina.cn/about/hyxx/gshy/rsbxgs/',
                  'http://old.iachina.cn/about/hyxx/gshy/zbxgs/',
                  'http://old.iachina.cn/about/hyxx/gshy/zcglgs/',
                  'http://old.iachina.cn/about/hyxx/gshy/bxzjgs/',
                  'http://old.iachina.cn/about/hyxx/dfxhhy/']

    table_url = 'http://old.iachina.cn/about/cwls/'

    def start_requests(self):
        for url in self.start_urls:
            for page in range(10):
                yield scrapy.Request(url=url + str(page) + '.html',
                                     callback=self.parse_list,
                                     dont_filter=True)

        # yield scrapy.Request(url=self.table_url,
        #                      callback=self.parse_company_list,
        #                      dont_filter=True)

    def parse_company_list(self, response):
        for member_info in response.xpath('//*[@id="hysjbox"]/div[2]/table/tbody/tr'):
            name = get_content(member_info.xpath('string(./td[2])').extract())
            if MemberItem.get_member(name=name):
                member = MemberItem()
                member['name'] = name
                member['position'] = get_content(member_info.xpath('string(./td[3])').extract())
                member['represent'] = get_content(member_info.xpath('string(./td[4])').extract())
                member['type'] = get_content(member_info.xpath('string(./td[5])').extract())
                yield member


    def parse_list(self, response):
        for member in response.xpath('//div[@class="memberab_lsit" or @class="memtab_list"]/ul/li/a'):
            name = get_content(member.xpath('text()').extract())
            link = 'http://old.iachina.cn/' + get_content(member.xpath('@href').extract())
            yield scrapy.Request(url=link,
                                 callback=self.parse_detail,
                                 dont_filter=True)

    def parse_detail(self, response):

        member = MemberItem()

        info = response.xpath('//div[@id="tytext"]')
        member['name'] = get_content(info.xpath('h1/text()').extract())
        member['date'] = get_content(info.xpath('p[@class="tytdate"]/text()').extract())
        member['link'] = response.url
        if len(info.xpath('./div/p')) > 0:
            for p in info.xpath('./div/p'):
                content = get_content(p.xpath('string(.)').extract())
                print(member['name'])
                print(content)
                print('--------1')
                if content == None: continue
                if content.find(u'网址') >= 0:
                    member['website'] = content.split(':')[-1]
                elif content.find(u'电话') >= 0:
                    member['phone'] = content.split(':')[-1]
                elif content.find(u'地址') >= 0:
                    member['address'] = content.split(':')[-1]
                elif content.find(u'邮编') >= 0:
                    member['zip'] = content.split(':')[-1]
        elif len(info.xpath('./p')) < 4:
            content = info.xpath('string(./p[2])').extract_first().split('\n')

            for s in content:
                print(s)
                print('--------2')
                value = get_trunk(s.split(u'：')[-1])
                if s.find(u'网址') >= 0:
                    member['website'] = value
                elif s.find(u'电话') >= 0:
                    member['phone'] = value
                elif s.find(u'地址') >= 0:
                    member['address'] = value
                elif s.find(u'邮编') >= 0:
                    member['zip'] = value
        else:
            for p in info.xpath('./p'):
                content = get_content(p.xpath('string(.)').extract())
                print(member['name'])
                print(content)
                print('--------3')
                if content == None: continue
                if content.find(u'网址') >= 0:
                    member['website'] = content.split(':')[-1]
                elif content.find(u'电话') >= 0:
                    member['phone'] = content.split(':')[-1]
                elif content.find(u'地址') >= 0:
                    member['address'] = content.split(':')[-1]
                elif content.find(u'邮编') >= 0:
                    member['zip'] = content.split(':')[-1]

        if member['website'][0] == '/':
            member['website'] = 'http:' + member['website']
        yield member
