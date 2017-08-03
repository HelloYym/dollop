# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_content, get_trunk
# from p2peye.items import FeatureItem
import json


class XiangqingSpider(scrapy.Spider):
    name = "xiangqing"
    allowed_domains = ["p2peye.com"]
    pipeline = ['UniqueItemPersistencePipeline']

    problems = {'ui-problem1': u'平台失联', 'ui-problem2': u'提现困难', 'ui-problem3': u'平台诈骗',
                'ui-problem4': u'警方介入', 'ui-problem5': u'终止运营', 'ui-problem6': u'跑路平台',
                'ui-problem8': u'良性退出', 'ui-problem9': u'暂停发标',
                }

    def __init__(self, from_id=1, to_id=1, *args, **kwargs):
        self.shortlist = xrange(int(from_id), int(to_id) + 1)
        self.mapping = {}
        super(XiangqingSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = FeatureItem.get_object_by_pk(i)
            self.mapping[obj.pin] = obj.id
            yield self.make_requests_from_url(obj.link)
            return

    def get_pin_from_url(self, url):
        purl = url.split('/')
        while not purl[-1]: purl.pop()

        return purl.pop().split('.')[0]

    def get_state(self, info):
        infos = info.split(' ');
        if len(infos) < 3: return None

        for each in infos:
            if self.problems.has_key(each):
                return self.problems.get(each)

        return None

    def parse(self, response):
        symbol = (self.mapping.get(self.get_pin_from_url(response.url)), response.url)
        self.logger.info('Parsing ID.%d p2peye Details From <%s>.' % symbol)

        item = FeatureItem()
        item['pin'] = self.get_pin_from_url(response.url)

        info = response.xpath('//div[@class="index-header"]/div/@class')
        state = self.get_state(get_content(info.extract(), skipBlank=False))

        if state:
            self.logger.info('Parsing ID.%d p2peye is a problem platform.', symbol[0])
            item['state'] = state
            item['problem_time'] = get_content(response.xpath('//div[@class="left"]/div/ul/li/span/text()').extract())

        platform = response.xpath('//div[@class="platform-list"]/table/tbody/tr')
        if platform:
            item['company'] = get_content(platform[0].xpath('./td[@class="list_le"]/div/text()').extract())
            item['legal_representative'] = get_content(
                platform[0].xpath('./td[@class="list_ri"]/span/text()').extract())
            item['scale'] = get_content(platform[1].xpath('./td[@class="list_le"]/span/text()').extract())
            item['auto_bid'] = get_content(platform[4].xpath('./td[@class="list_ri"]/span/text()').extract())
            item['debt_assignment'] = get_content(platform[3].xpath('./td[@class="list_ri"]/span/text()').extract())
            # item['funds_custody'] = get_content(platform[4].xpath('./td[@class="list"][1]/span/text()').extract())
            item['assurance_mode'] = get_content(platform[3].xpath('./td[@class="list_le"]/span/text()').extract())

            # details = platform[5].xpath('./td[@class="list"]/dl')
            #
            # if details:
            #     # create a dictionary for features
            #     feature_dict = {}
            #     for detail in details:
            #         feature_name = get_content(detail.xpath('./dt/em/text()').extract())
            #
            #         # remove the tag and return the text
            #         p = detail.xpath('./dd/p')
            #         detail_list = p.xpath('string(.)').extract()
            #
            #         # remove the leading and trailing ' \r\t\n' characters
            #         feature_detail_list = [each.strip(' \r\t\n') for each in detail_list]
            #
            #         feature_dict[feature_name] = feature_detail_list
            #
            #     # turn dictionary into json and save
            #     item['feature_detail'] =  json.dumps(feature_dict, ensure_ascii=False).encode('utf-8')

        # details = platform[5].xpath('./td[@class="list"]/dl')  # create a dictionary for features

        feature_dict = {}

        for detail in response.xpath('//div[contains(@class, "tag_ptsl")]'):

            feature_name = get_content(detail.xpath('text()').extract())

            # remove the tag and return the text
            p = detail.xpath('.//div[@class="content"]')
            detail_list = p.xpath('string(.)').extract()

            # remove the leading and trailing ' \r\t\n' characters
            feature_detail_list = [each.strip(' \r\t\n') for each in detail_list]

            feature_dict[feature_name] = feature_detail_list

        # turn dictionary into json and save
        item['feature_detail'] = json.dumps(feature_dict, ensure_ascii=False).encode('utf-8')


        # return item
