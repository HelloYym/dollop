# -*- coding: utf-8 -*-
import scrapy
import json
from utils.webpage import get_trunk, get_content
from baoxian.items import ProductItem



class BhxProductSpider(scrapy.Spider):
    name = "bhx_product"
    allowed_domains = ["iachina.cn"]
    pipeline = ['UniqueItemPersistencePipeline']
    start_urls = ['http://iachina.cn/']
    request_url = 'http://tiaokuan.iachina.cn:8090/sinopipi/loginServlet/publicQueryResult.do'

    def start_requests(self):

        page_size = '10000'

        for i in range(5):
            for j in range(5):
                prod_type_code = 'ProdTypeCode_0' + str(i) + '_0' + str(j);
                yield scrapy.FormRequest(url=self.request_url,
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                         formdata={'prodTermsShow.prodTypeCode': prod_type_code,
                                                   'pageSize': page_size,
                                                   'pageNo': '1'},
                                         dont_filter=True,
                                         callback=self.parse_list)

        yield scrapy.FormRequest(url=self.request_url,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 formdata={'prodTermsShow.prodTypeCode': 'ProdTypeCode_03',
                                           'pageSize': page_size,
                                           'pageNo': '1'},
                                 dont_filter=True,
                                 callback=self.parse_list)

        for i in range(5):
            prod_type_code = 'ProdTypeCode_02_01_0' + str(i);
            yield scrapy.FormRequest(url=self.request_url,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     formdata={'prodTermsShow.prodTypeCode': prod_type_code,
                                               'pageSize': page_size,
                                               'pageNo': '1'},
                                     dont_filter=True,
                                     callback=self.parse_list)
            for j in range(5):
                prod_type_code = 'ProdTypeCode_02_01_0' + str(i) + '_0' + str(j);
                yield scrapy.FormRequest(url=self.request_url,
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                         formdata={'prodTermsShow.prodTypeCode': prod_type_code,
                                                   'pageSize': page_size,
                                                   'pageNo': '1'},
                                         dont_filter=True,
                                         callback=self.parse_list)

    def parse_list(self, response):
        cnt = 0
        # for product_item in response.xpath('//tr[@class="common1"]'):
        #     name = get_content(product_item.xpath('td[2]/text()').extract())
        #     print(name)
        #     cnt += 1
        for info in response.xpath('//input[contains(@id, "detailed")]'):
            # link = get_content(info.xpath('@onclick').extract())
            s = info.xpath('@onclick').extract_first()
            s = '[' + s.split('(')[-1]
            s = s.split(')')[0] + ']'
            ss = json.loads(s.replace('\'', '\"'))
            # link = ss[-1] + ss[0] + '.html'
            code = ss[0]
            link = 'http://www.iachina.cn/IC/tkk/02/' + code + '.html'
            yield scrapy.Request(url=link,
                                 dont_filter=True,
                                 meta={'code': code},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        product = ProductItem()
        code = response.meta['code']
        product['code'] = code
        product['pdf'] = 'http://www.iachina.cn/IC/tkk/03/' + code + '_TERMS.PDF'
        product['link'] = response.url

        update_fields_list = ['link', 'company_name', 'product_name', 'product_type', 'design_type', 'feature',
                              'insured',
                              'period_type', 'pay_type', 'clause', 'state', 'end_date', 'summary', 'pdf']

        for entry in response.xpath('//table[@class="biaoge"]/tr'):
            key = get_content(entry.xpath('string(td[1])').extract())
            value = get_content(entry.xpath('string(td[2])').extract())
            if key.find(u'公司名称') >= 0:
                product['company_name'] = value
            elif key.find(u'产品名称') >= 0:
                product['product_name'] = value
            elif key.find(u'产品类别') >= 0:
                product['product_type'] = value
            elif key.find(u'设计类型') >= 0:
                product['design_type'] = value
            elif key.find(u'产品特殊属性') >= 0:
                product['feature'] = value
            elif key.find(u'承保方式') >= 0:
                product['insured'] = value
            elif key.find(u'保险期间类型') >= 0:
                product['period_type'] = value
            elif key.find(u'产品交费方式') >= 0:
                product['pay_type'] = value
            elif key.find(u'条款文字编码') >= 0:
                product['clause'] = value
            elif key.find(u'销售状态') >= 0:
                product['state'] = value
            elif key.find(u'停止销售日期') >= 0:
                product['end_date'] = value

        yield product







