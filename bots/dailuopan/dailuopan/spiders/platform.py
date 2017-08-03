# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from dailuopan.items import DailyDataItem, InvestorItem, HonorItem, RateItem, FlowItem
from datetime import datetime, timedelta
import copy
import json


class PlatformSpider(scrapy.Spider):
    name = "platform"
    allowed_domains = ["http://www.dailuopan.com"]
    pipeline = ['UniqueItemPersistencePipeline']
    get_daily_data_url = 'http://www.dailuopan.com/P2P/GetdatabaseJson'
    platform_list_url = 'http://www.dailuopan.com/pingji/all'
    start_urls = ['http://www.dailuopan.com/flow/all']
    flow_date = None

    def parse(self, response):

        self.flow_date = response.xpath('//div[@class="page-hd"]/span/text()').extract_first().strip()[-14:-4]

        # 首先获取流量指数更新日期
        yield scrapy.Request(url=self.platform_list_url,
                             callback=self.parse_platform_list,
                             dont_filter=True)

    def parse_platform_list(self, response):
        for info in response.xpath('//tbody/tr'):
            href = 'http://www.dailuopan.com' + info.xpath('./td[last()]/a/@href').extract_first()
            name = get_content(info.xpath('./td[2]/a[1]/text()').extract())
            yield scrapy.Request(url=href,
                                 callback=self.parse_detail,
                                 meta={'name': name, 'link': href},
                                 dont_filter=True)
            # return

    def parse_detail(self, response):

        thread = response.xpath('//input[@type="hidden"]/@value').extract_first()
        name = response.meta['name']
        link = response.meta['link']

        yield scrapy.FormRequest(url=self.get_daily_data_url,
                                 formdata={'id': thread},
                                 method='GET',
                                 callback=self.parse_history_daily_data,
                                 meta={'thread': thread, 'name': name, 'link': link},
                                 dont_filter=True)

        yield self.parse_investor(response, thread, name, link)
        yield self.parse_platform_honor(response, thread, name, link)
        for rate_item in self.parse_platform_rate(response, thread, name, link):
            yield rate_item

        for flow_item in self.parse_flow_index(response, thread, name, link):
            yield flow_item

    def parse_investor(self, response, thread, name, link):

        investor = InvestorItem()
        investor['thread'] = thread
        investor['name'] = name
        investor['link'] = link
        investor['date'] = datetime.now().strftime('%Y-%m-%d')

        investor['age_distribution'] = [propo + '%' for propo in
                                        response.xpath('//div[@id="ageList"]/dl/dd/span[1]/em/text()').extract()]

        investor['sex_distribution'] = response.xpath(
            '//div[contains(@class, "index-investors-sex")]/script/text()').re_first(
            r'= (.*);')

        investor['tag_list'] = '#'.join(
            [get_trunk(tag) for tag in response.xpath('//div[@id="index_tag"]/a/text()').extract()])
        return investor

    def parse_platform_honor(self, response, thread, name, link):

        platform_honor = HonorItem()
        platform_honor['thread'] = thread
        platform_honor['name'] = name
        platform_honor['link'] = link

        platform_honor['honor_list'] = [get_trunk(honor) for honor in
                                        response.xpath('//div[contains(@class, "honor")]/ul/li/text()').extract()]

        return platform_honor

    def parse_platform_rate(self, response, thread, name, link):

        for rate_info in response.xpath('//dl[contains(@class, "rate-info")]'):
            # if rate_info.xpath('.//text()').re(r'无评级'): continue
            platform_rate = RateItem()
            platform_rate['thread'] = thread
            platform_rate['name'] = name
            platform_rate['link'] = link
            platform_rate['institution'] = rate_info.xpath('.//span[@class="tit"]/text()').extract_first()
            try:
                rate_list = json.loads(rate_info.xpath('.//script/text()').re_first(r'list=(.*?);').strip())
            except:
                continue
            for rate in rate_list:
                rate_item = copy.deepcopy(platform_rate)
                rate_item['date'] = rate['date_str']
                rate_item['rate'] = rate['datavalue']
                rate_item['unit'] = 'day' if rate['date_str'].find('-') > 0 else 'month'
                yield rate_item

    def parse_flow_index(self, response, thread, name, link):

        platform_flow = FlowItem()
        platform_flow['thread'] = thread
        platform_flow['name'] = name
        platform_flow['link'] = link

        flow_date = datetime.strptime(self.flow_date, '%Y-%m-%d')
        flow_monitoring = response.xpath('//div[@class="flow-monitoring"]')
        for index_info in flow_monitoring.xpath('./div[@class="bd"]/dl'):
            index_list = list(json.loads(index_info.xpath('./script/text()').re_first(r'=(.*?);').strip()))

            platform_flow_item = copy.deepcopy(platform_flow)
            platform_flow_item['institution'] = get_content(index_info.xpath('./dt/text()').extract())
            platform_flow_item['date'] = flow_date.strftime('%Y-%m-%d')
            platform_flow_item['flow'] = index_list[-1]
            yield platform_flow_item

            # history
            # for i, index_value in enumerate(index_list[::-1]):
            #     platform_flow_item = copy.deepcopy(platform_flow)
            #     platform_flow_item['institution'] = get_content(index_info.xpath('./dt/text()').extract())
            #     platform_flow_item['date'] = (flow_date - timedelta(days=i)).strftime('%Y-%m-%d')
            #     platform_flow_item['flow'] = index_value
            #     yield platform_flow_item

        platform_flow_item = copy.deepcopy(platform_flow)
        platform_flow_item['institution'] = '综合指数'
        platform_flow_item['date'] = flow_date.strftime('%Y-%m-%d')
        platform_flow_item['flow'] = get_content(flow_monitoring.xpath('./div[@class="hd"]/strong/text()').extract())
        yield platform_flow_item

    def parse_history_daily_data(self, response):

        data_list = json.loads(response.body.decode(response.encoding))

        for daily_data_info in data_list:
            daily_data = DailyDataItem()
            daily_data['thread'] = response.meta['thread']
            daily_data['name'] = response.meta['name']
            daily_data['link'] = response.meta['link']
            daily_data['date'] = daily_data_info['date_str']

            daily_data['amount'] = daily_data_info['amount']
            daily_data['inamount'] = daily_data_info['inamount']
            daily_data['stay_still_day'] = daily_data_info['stayStill']
            daily_data['stay_still_total'] = daily_data_info['stayStillOfTotal']
            daily_data['invest_amount_avg'] = daily_data_info['avgBidMoney']
            daily_data['borrow_amount_avg'] = daily_data_info['avgBorrowMoney']

            daily_data['invest_num_day'] = daily_data_info['bidderNum']
            daily_data['borrow_num_day'] = daily_data_info['borrowerNum']
            daily_data['invest_num_stay'] = daily_data_info['bidderWaitNum']
            daily_data['borrow_num_stay'] = daily_data_info['borrowWaitNum']

            daily_data['top10_investor_prop'] = daily_data_info['top10DueInProportion']
            daily_data['top10_borrower_prop'] = daily_data_info['top10StayStillProportion']

            daily_data['rate'] = daily_data_info['rate']
            daily_data['loan_period'] = daily_data_info['loanPeriod']
            daily_data['full_loan_time'] = daily_data_info['fullloanTime']
            daily_data['total_loan_num'] = daily_data_info['totalLoanNum']

            yield daily_data

    def parse_daily_data(self, response):
        # 在网页中获取一天的数据

        daily_data = DailyDataItem()

        daily_data['thread'] = response.meta['thread']
        daily_data['name'] = response.meta['name']
        daily_data['link'] = response.url
        daily_data['date'] = response.xpath('//h4[@class="corerate-tit"]/span/text()').extract_first()[-11:-1]

        corerate_trading = response.xpath('(//dl[@class="corerate"])[1]')
        daily_data['turnover'] = get_content(corerate_trading.xpath('./dd[1]/text()').extract())
        daily_data['fund_flow'] = get_content(corerate_trading.xpath('./dd[2]/text()').extract())
        daily_data['repay_day'] = get_content(corerate_trading.xpath('./dd[3]/text()').extract())
        daily_data['repay_total'] = get_content(corerate_trading.xpath('./dd[4]/text()').extract())
        daily_data['invest_amount_avg'] = get_content(corerate_trading.xpath('./dd[5]/text()').extract())
        daily_data['borrow_amount_avg'] = get_content(corerate_trading.xpath('./dd[6]/text()').extract())

        corerate_user = response.xpath('(//dl[@class="corerate"])[2]')
        daily_data['invest_num_day'] = get_content(corerate_user.xpath('./dd[1]/text()').extract())
        daily_data['borrow_num_day'] = get_content(corerate_user.xpath('./dd[2]/text()').extract())
        daily_data['invest_num_stay'] = get_content(corerate_user.xpath('./dd[3]/text()').extract())
        daily_data['borrow_num_stay'] = get_content(corerate_user.xpath('./dd[4]/text()').extract())

        corerate_prop = response.xpath('(//dl[@class="corerate"])[3]')
        daily_data['top_investor_prop'] = get_content(corerate_prop.xpath('./dd[1]/text()').extract())
        daily_data['top_borrower_prop'] = get_content(corerate_prop.xpath('./dd[2]/text()').extract())

        corerate_other = response.xpath('(//dl[@class="corerate"])[4]')
        daily_data['rate'] = get_content(corerate_other.xpath('./dd[1]/text()').extract())
        daily_data['term_avg'] = get_content(corerate_other.xpath('./dd[2]/text()').extract())
        daily_data['time_used'] = get_content(corerate_other.xpath('./dd[3]/text()').extract())

        return daily_data
