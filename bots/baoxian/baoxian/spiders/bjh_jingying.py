# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from baoxian.items import JingyingItem
import json


class BjhJingyingSpider(scrapy.Spider):
    name = "bjh_jingying"
    pipeline = ['UniqueItemPersistencePipeline']
    allowed_domains = ["http://www.circ.gov.cn/"]
    request_url = 'http://www.circ.gov.cn/web/site0/tab5201/module14497/page{page}.htm'

    def start_requests(self):
        total_page = 15
        for page in range(total_page):
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
            title = get_content(report_item.xpath('.//td[@class="hui14"]/a/text()').extract())
            id = get_content(report_item.xpath('.//td[@class="hui14"]/a/@id').re(r'\d+'))
            link = 'http://www.circ.gov.cn' + get_content(report_item.xpath('.//td[@class="hui14"]/a/@href').extract())
            created = get_content(report_item.xpath('.//td[@class="hui14"]/../td[last()]/text()').extract())[1:-1]
            yield scrapy.Request(url=link,
                                 callback=self.parse_detail,
                                 meta={'title': title, 'id': id, 'created': created},
                                 dont_filter=True)

    def parse_detail(self, response):

        report = JingyingItem()
        report['title'] = response.meta['title']
        year, month = self.parse_title(report['title'])
        report['year'] = year
        report['month'] = month

        report['id'] = response.meta['id']
        report['link'] = response.url
        report['created'] = response.meta['created']

        # data = dict()
        data = list()
        content_p = list()
        content = None

        if len(response.xpath('//*[@id="zoom"]/div/table/tbody/tr/td/div[2]/table/tbody/tr')) > 0:
            for item in response.xpath('//*[@id="zoom"]/div/table/tbody/tr/td/div[2]/table/tbody/tr'):
                key = get_content(item.xpath('string(td[1])').extract())
                value = get_content(item.xpath('string(td[2])').extract())
                if key and value:
                    # data[key] = value
                    data.append((key, value))
            content = response.xpath('//*[@id="zoom"]/div/table/tbody/tr/td/div[3]/table/tbody/tr/td[2]/p')
        elif len(response.xpath('//*[@id="zoom"]/table/tbody/tr[1]/td/table/tbody/tr')) > 0:
            for item in response.xpath('//*[@id="zoom"]/table/tbody/tr[1]/td/table/tbody/tr'):
                key = get_content(item.xpath('string(td[1])').extract())
                value = get_content(item.xpath('string(td[2])').extract())
                if key and value:
                    data.append((key, value))
                if key and not value:
                    content_p.append(key)
            content = response.xpath('//span[@id="zoom"]')
        elif len(response.xpath('//*[@id="zoom"]/table/tbody/tr')) > 0:
            for item in response.xpath('//*[@id="zoom"]/table/tbody/tr'):
                key = get_content(item.xpath('string(td[1])').extract())
                value = get_content(item.xpath('string(td[2])').extract())
                if key and value:
                    data.append((key, value))
                if key and not value:
                    content_p.append(key)
            content = response.xpath('//span[@id="zoom"]')
        elif len(response.xpath('//*[@id="zoom"]/table/tr')) > 0:
            for item in response.xpath('//*[@id="zoom"]/table/tr'):
                key = get_content(item.xpath('string(td[1])').extract())
                value = get_content(item.xpath('string(td[2])').extract())
                if key and value:
                    data.append((key, value))
                if key and not value:
                    content_p.append(key)
            content = response.xpath('//span[@id="zoom"]')
        elif len(response.xpath('//*[@id="zoom"]/div/table/tbody/tr')) > 0:
            for item in response.xpath('//*[@id="zoom"]/div/table/tbody/tr'):
                key = get_content(item.xpath('string(td[1])').extract())
                value = get_content(item.xpath('string(td[2])').extract())
                if key and value:
                    data.append((key, value))
                if key and not value:
                    content_p.append(key)
            content = response.xpath('//span[@id="zoom"]')
        else:
            for item in response.xpath('//*[@id="zoom"]/strong/table/tbody/tr'):
                key = get_content(item.xpath('string(td[1])').extract())
                value = get_content(item.xpath('string(td[2])').extract())
                if key and value:
                    data.append((key, value))
                if key and not value:
                    content_p.append(key)
            content = response.xpath('//span[@id="zoom"]')

        flag = False
        for key, value in data:
            if key.find(u'收入') >= 0:
                report['income'] = value
            elif key.find(u'保户投资') >= 0:
                report['baohu_xz'] = value
            elif key.find(u'独立账户') >= 0:
                report['duli_xz'] = value
            elif key.find(u'给付') >= 0 or key.find(u'赔付支出') >= 0:
                report['expense'] = value
                flag = True
            elif key.find(u'年金缴费') >= 0:
                report['yanglao_cost'] = value
            elif key.find(u'受托') >= 0:
                report['yanglao_shoutuo'] = value
            elif key.find(u'年金投资管理') >= 0:
                report['yanglao_touzi'] = value
            elif key.find(u'业务') >= 0 or key.find(u'营业') >= 0:
                report['manage_fee'] = value
            elif key.find(u'银行存款') >= 0:
                report['bank_deposits'] = value
            elif key.find(u'投资') >= 0:
                report['invest'] = value
            elif key.find(u'资产总额') >= 0:
                report['amount'] = value
            elif key.find(u'财产险') >= 0:
                if flag:
                    report['caichanxian2'] = value
                else:
                    report['caichanxian1'] = value
            elif key.find(u'人身险') >= 0:
                if flag:
                    report['renshenxian2'] = value
                else:
                    report['renshenxian1'] = value
            elif key.find(u'寿险') >= 0:
                if flag:
                    report['shouxian2'] = value
                else:
                    report['shouxian1'] = value
            elif key.find(u'健康险') >= 0:
                if flag:
                    report['jiankangxian2'] = value
                else:
                    report['jiankangxian1'] = value
            elif key.find(u'意外') >= 0:
                if flag:
                    report['yiwaixian2'] = value
                else:
                    report['yiwaixian1'] = value

        report['data'] = json.dumps(data, encoding="UTF-8", ensure_ascii=False)
        report['raw_content'] = content.extract_first()
        if len(content_p) > 1:
            report['content'] = ' '.join(content_p)
        else:
            report['content'] = ''.join(
                [get_trunk(c) for c in content.xpath('.//p/text() or string(span)').extract()])
        report['image_url'] = '#'.join([get_trunk(c) for c in content.xpath('.//img/@src').extract()]) or None

        yield report
