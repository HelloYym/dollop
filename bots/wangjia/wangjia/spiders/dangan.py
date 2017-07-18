# -*- coding: utf-8 -*-
import scrapy
import requests
from utils.webpage import get_content, get_trunk
from wangjia.items import ProvinceItem, DanganItem
from stalk.models.wqmodels import wdzj_navigation

class DanganSpider(scrapy.Spider):
    name = 'dangan'
    url_prefix = 'http://www.wdzj.com/dangan/'
    pipeline = ['UniqueItemPersistencePipeline']

    map_ch2en = {
        u'银行存管': 'trust_funds',
        u'股权上市': 'stock_market_status',
        u'融资记录': 'financing_record',
        u'监管协会': 'regulatory_association',
        u'自动投标': 'automatic_bid',
        u'债权转让': 'equitable_assignment',
        u'投标保障': 'tender_security',
        u'保障模式': 'security_mode',
        u'担保机构': 'guarantee_institutions',
        u'风险准备金存管': 'emergency_funds',
        u"服务电话：": 'phone_400',
        u"座机电话：": 'phone',
        u"服务邮箱：": 'email',
        u"传真：": 'fax',
        u"办公地址：": 'contact_address',
    }

    problem_label = (u'停业', u'跑路', u'提现困难')

    def get_pin_from_wdzj_navigation(self):
        pins = wdzj_navigation.objects.values_list("platPin")
        return [p[0] for p in pins]

    def start_requests(self):
        for pin in self.get_pin_from_wdzj_navigation():
            url = self.url_prefix + pin + '/'
            yield scrapy.Request(url=url, meta={'pin': pin}, dont_filter=True)

    def parse(self, response):
        self.logger.info('Parsing Wangjia Archive From <%s>.' % response.url)

        item = DanganItem()

        item['pin'] = response.meta.get('pin')
        item['logo_url'] = get_content(response.xpath('//div[@class="pt-logo"]/img/@src').extract())

        web_url = get_content(response.xpath('//div[@class="on4"]/a[1]/@href').extract())
        if web_url and 'javascript' not in web_url:
            item['web_url'] = web_url
        if response.xpath('//div[@class="bq-box"]')[0].xpath('.//span'):
            tag = get_content(response.xpath('//div[@class="bq-box"]')[0].xpath('.//span')[-1].xpath('text()').extract())
            if tag in self.problem_label:
                item['product_state'] = tag

        intro = response.xpath('//div[@class="cen-zk"]')
        item['introduction'] = ''.join([get_trunk(c) for c in intro.xpath('.//text()').extract()])

        title_div = response.xpath('//div[@class="title"]')

        item['launch_time'] = get_content(title_div.xpath('span[2]/em/text()').extract()).replace(u"上线", '')

        item['product_name'] = get_content(title_div.xpath('h1/text()').extract())

        location = get_content(title_div.xpath('span[1]/em/text()').extract())
        if len(location.split(u'·')) > 1:
            item['province'] = location.split(u'·')[0].strip()
            item['city'] = location.split(u'·')[1].strip()
        else:
            item['province'] = location.strip()

        business_icp = response.xpath('//div[@class="da-ggxx"]')
        if business_icp and len(business_icp) > 1:
            # 工商信息
            business_info = response.xpath('//div[@class="da-ggxx"]')[0]
            if business_info:
                part1 = business_info.xpath('table[1]//tr')
                item['company_name'] = get_content(part1[0].xpath('td[2]/text()').extract())
                item['artificial_person'] = get_content(part1[1].xpath('td[2]/text()').extract())
                item['company_type'] = get_content(part1[2].xpath('td[2]/text()').extract())
                item['ownership_structure'] = get_content(part1[3].xpath('td[2]/text()').extract()).replace("--", '')

                part2 = business_info.xpath('table[2]//tr')
                item['registered_capital'] = get_content(part2[0].xpath('td[2]/text()').extract())
                item['contributed_capital'] = get_content(part2[1].xpath('td[2]/text()').extract())
                item['registered_address'] = get_content(part2[2].xpath('td[2]/text()').extract())

                part3 = business_info.xpath('table[3]//tr')
                item['opening_date'] = get_content(part3[0].xpath('td[2]/text()').extract())
                item['approved_date'] = get_content(part3[1].xpath('td[2]/text()').extract())
                item['registration_authority'] = get_content(part3[2].xpath('td[2]/text()').extract())
                item['business_licence'] = get_content(part3[3].xpath('td[2]/text()').extract())
                item['institutional_framework'] = get_content(part3[4].xpath('td[2]/text()').extract())
                item['tax_registration_num'] = get_content(part3[5].xpath('td[2]/text()').extract())

                item['business_scope'] = get_content(business_info.xpath('table[4]/tr/td[2]/text()').extract())

            # 备案信息
            icp_info = response.xpath('//div[@class="da-ggxx"]')[1].xpath('table//tr')
            if icp_info:
                item['domain_name'] = get_content(icp_info[0].xpath('td[2]/text()').extract())
                item['domain_date'] = get_content(icp_info[1].xpath('td[2]/text()').extract())
                item['domain_company_type'] = get_content(icp_info[2].xpath('td[2]/text()').extract())
                item['domain_company_name'] = get_content(icp_info[3].xpath('td[2]/text()').extract())
                item['ICP_number'] = get_content(icp_info[4].xpath('td[2]/text()').extract())
                item['ICP_approval_number'] = get_content(icp_info[5].xpath('td[2]/text()').extract())

        elif business_icp and len(business_icp) == 1:
            icp_info = response.xpath('//div[@class="da-ggxx"]')[0].xpath('table//tr')
            if len(icp_info) == 6:
                # 备案信息
                item['domain_name'] = get_content(icp_info[0].xpath('td[2]/text()').extract())
                item['domain_date'] = get_content(icp_info[1].xpath('td[2]/text()').extract())
                item['domain_company_type'] = get_content(icp_info[2].xpath('td[2]/text()').extract())
                item['domain_company_name'] = get_content(icp_info[3].xpath('td[2]/text()').extract())
                item['ICP_number'] = get_content(icp_info[4].xpath('td[2]/text()').extract())
                item['ICP_approval_number'] = get_content(icp_info[5].xpath('td[2]/text()').extract())
            else:
                business_info = response.xpath('//div[@class="da-ggxx"]')[0]
                # 工商信息
                part1 = business_info.xpath('table[1]//tr')
                item['company_name'] = get_content(part1[0].xpath('td[2]/text()').extract())
                item['artificial_person'] = get_content(part1[1].xpath('td[2]/text()').extract())
                item['company_type'] = get_content(part1[2].xpath('td[2]/text()').extract())
                item['ownership_structure'] = get_content(part1[3].xpath('td[2]/text()').extract()).replace("--", '')

                part2 = business_info.xpath('table[2]//tr')
                item['registered_capital'] = get_content(part2[0].xpath('td[2]/text()').extract())
                item['contributed_capital'] = get_content(part2[1].xpath('td[2]/text()').extract())
                item['registered_address'] = get_content(part2[2].xpath('td[2]/text()').extract())

                part3 = business_info.xpath('table[3]//tr')
                item['opening_date'] = get_content(part3[0].xpath('td[2]/text()').extract())
                item['approved_date'] = get_content(part3[1].xpath('td[2]/text()').extract())
                item['registration_authority'] = get_content(part3[2].xpath('td[2]/text()').extract())
                item['business_licence'] = get_content(part3[3].xpath('td[2]/text()').extract())
                item['institutional_framework'] = get_content(part3[4].xpath('td[2]/text()').extract())
                item['tax_registration_num'] = get_content(part3[5].xpath('td[2]/text()').extract())

                item['business_scope'] = get_content(business_info.xpath('table[4]/tr/td[2]/text()').extract())

        # 平台费用
        plat_fee = response.xpath('//div[@class="da-ptfy"]//dl')
        if plat_fee:
            item['account_fee'] = get_content(plat_fee[0].xpath('dt/em/text()').extract())
            item['cash_fee'] = get_content(plat_fee[1].xpath('dt/em/text()').extract())
            item['fueling_fee'] = get_content(plat_fee[2].xpath('dt/em/text()').extract())
            item['transfer_fee'] = get_content(plat_fee[3].xpath('dt/em/text()').extract())
            item['vip_fee'] = get_content(plat_fee[4].xpath('dt/em/text()').extract())

        # 联系方式
        contact = response.xpath('//div[@class="da-lxfs zzfwbox"]//dd')
        for ele in contact:
            key = ele.xpath(".//div[@class='l']/em/text()").extract()[0].strip()
            value = get_content(ele.xpath(".//div[@class='r']").xpath("string(.)").extract())
            if self.map_ch2en.has_key(key):
                item[self.map_ch2en[key]] = value

        # 实力资质 平台服务
        basic_info = response.xpath("//div[@class='bgbox-bt zzfwbox']//dd")
        for ele in basic_info:
            key = ele.xpath(".//div[@class='l']/em/text()").extract()[0].strip()
            if self.map_ch2en.has_key(key):
                if key == u'担保机构':
                    value = get_content(ele.xpath(".//div[@class='r dbjg']").xpath("string(.)").extract())
                else:
                    value = get_content(ele.xpath(".//div[@class='r']").xpath("string(.)").extract())
                item[self.map_ch2en[key]] = value

        return item


