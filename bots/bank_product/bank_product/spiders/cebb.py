# -*- coding: utf-8 -*-
import scrapy

from bank_product.items import BankProductItem
from datetime import datetime
import logging


class CebbSpider(scrapy.Spider):
    # 增量爬虫：每天只请求前20页

    name = "cebb"
    allowed_domains = ["cebbank.com"]
    pipeline = ['BankProductPipeline']
    url = 'http://www.cebbank.com/eportal/ui?moduleId=12073&struts.portlet.action=/app/yglcAction!listProduct.action'

    request_body_str = 'codeOrName=&TZBZMC=&QGJE=&QGJELEFT=&QGJERIGHT=&CATEGORY=&CPQXLEFT=&CPQXRIGHT=&CPFXDJ=&SFZS=&CPTJLX=&qxrUp=Y&qxrDown=&dqrUp=&dqrDown=&qdjeUp=&qdjeDown=&qxUp=&qxDown=&yqnhsylUp=&yqnhsylDown=&page={page}&pageSize=5&channelIds%5B%5D=yxl94&channelIds%5B%5D=ygelc79&channelIds%5B%5D=hqb30&channelIds%5B%5D=dhb2&channelIds%5B%5D=cjh&channelIds%5B%5D=gylc70&channelIds%5B%5D=Ajh67&channelIds%5B%5D=Ajh84&channelIds%5B%5D=901776&channelIds%5B%5D=Bjh91&channelIds%5B%5D=Ejh99&channelIds%5B%5D=Tjh70&channelIds%5B%5D=tcjh96&channelIds%5B%5D=ts43&channelIds%5B%5D=ygjylhzhMOM25&channelIds%5B%5D=yxyg87&channelIds%5B%5D=zcpzjh64&channelIds%5B%5D=wjyh1&channelIds%5B%5D=smjjb9&channelIds%5B%5D=ty90&channelIds%5B%5D=tx16&channelIds%5B%5D=ghjx6&channelIds%5B%5D=wf36&channelIds%5B%5D=ygxgt59&channelIds%5B%5D=wbtcjh3&channelIds%5B%5D=wbBjh77&channelIds%5B%5D=wbTjh28&channelIds%5B%5D=sycfxl&channelIds%5B%5D=cfTjh&channelIds%5B%5D=jgdhb&channelIds%5B%5D=tydhb&channelIds%5B%5D=jgxck&channelIds%5B%5D=jgyxl&channelIds%5B%5D=tyyxl&channelIds%5B%5D=dgBTAcp&channelIds%5B%5D=27637097&channelIds%5B%5D=27637101&channelIds%5B%5D=27637105&channelIds%5B%5D=27637109&channelIds%5B%5D=27637113&channelIds%5B%5D=27637117&channelIds%5B%5D=27637121&channelIds%5B%5D=27637125&channelIds%5B%5D=27637129&channelIds%5B%5D=27637133'

    def start_requests(self):
        self.log_file = open('bank_product.log', 'w')

        body = self.request_body_str.replace('{page}', '1')
        request = scrapy.Request(url=self.url,
                                 method="POST",
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 body=body,
                                 callback=self.parse_total_page)
        yield request

    def parse_total_page(self, response):
        total_page = int(response.xpath('//span[@id="totalpage"]/text()').extract_first().strip())
        for page in range(total_page, total_page - 20, -1):
            body = self.request_body_str.replace('{page}', str(page))
            request = scrapy.Request(url=self.url,
                                     method="POST",
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     body=body,
                                     meta={'page': page},
                                     callback=self.parse_product_list)
            yield request

    def parse_product_list(self, response):
        if len(response.xpath('//a[@class="lb_title"]')) != 5:
            self.log_file.write(str(response.meta['page']) + '\n')

        for detail_link in response.xpath('//a[@class="lb_title"]'):
            detail_url = detail_link.xpath('./@href').extract_first()
            currency = detail_link.xpath('../../td[2]/text()').extract_first()
            yield scrapy.Request(url='http://www.cebbank.com/' + detail_url, callback=self.parse,
                                 meta={'currency': currency})

    def parse(self, response):
        product = BankProductItem()

        product['bank_domain'] = 'cebbank.com'
        product['currency'] = response.meta['currency']
        product['link'] = response.url

        try:
            product['name'] = response.xpath('//div[@class="xq_tit"]/text()').extract_first().strip()
            product['code'] = response.xpath('//div[@class="xq_bm"]/text()').extract_first().strip()

            product['min_amount'] = response.xpath(
                '//div[contains(@class, "xq_qgje")]//div[@class="qgje_sz"]/text()').extract_first().strip()
            product['risk'] = response.xpath(
                '//div[contains(@class, "xq_fxdj")]//div[@class="qgje_sz"]/text()').extract_first().strip()

            # 递增金额人民币和外币单位不一样，考虑改成字符串类型
            product['ascend_amount'] = response.xpath(
                '//ul[@class="fdsy_con_nr fl"]/li[1]/text()').extract_first().strip()

            product['product_type'] = response.xpath(
                '//ul[@class="fdsy_con_nr fl"]/li[last()]/text()').extract_first().strip()
            # product['remaining_quota'] = response.xpath('//*[@id="remainAccount"]/text()').extract_first()
            product['finance_type'] = response.xpath('//*[@id="nav_brd"]/span/span/a[5]/text()').extract_first().strip()

            # 判断产品是否开始
            if len(response.xpath('//li/text()').re(r'开放日')) == 0:

                # 判断收益率是否存在数字
                if len(response.xpath('//div[@class="syl_sz"]/text()').re(r'\d+\.?\d*')) > 0:

                    try:
                        # 预期收益可能是范围，考虑添加字段
                        if len(response.xpath('//div[@class="fdsy_tab fl"]')):
                            rates = response.xpath(
                                '//div[@class="fdsy_tab fl"]//div[@class="tab_tr fl"]/div[@class="tab_td_2 fl"]/text()').re(
                                r'\d+\.?\d*')

                            # 选取最大收益
                            # response.xpath('(//div[@class="fdsy_tab fl"]//div[@class="tab_tr fl"]/div[@class="tab_td_2 fl"])[last()]/text()').re(r'\d+\.?\d*')
                            product['anticipate_rate'] = rates[-1]
                            product['extra'] = {'分段收益': rates}
                        else:
                            product['anticipate_rate'] = response.xpath('//div[@class="syl_sz"]/text()').re_first(
                                r'\d+\.?\d*')
                    except:
                        pass

                product['limit_time'] = response.xpath('//div[@class="lcqx_sz"]/text()').extract_first().strip()

                try:
                    product['income_start_date'] = response.xpath(
                        '//ul[@class="fdsy_con_nr1 fl"]/li[1]/text()').extract_first().strip()
                    product['product_end_date'] = response.xpath(
                        '//ul[@class="fdsy_con_nr1 fl"]/li[2]/text()').extract_first().strip()
                    product['ipo_start_date'] = response.xpath(
                        '//ul[@class="fdsy_con_nr1 fl"]/li[3]/text()').extract_first().strip()
                    product['ipo_end_date'] = response.xpath(
                        '//ul[@class="fdsy_con_nr1 fl"]/li[4]/text()').extract_first().strip()
                except:
                    pass

            # print(product)
            yield product
        except:
            self.log_file.writelines(response.url)


            # \d+\.?\d*
            # 匹配整数和小数
