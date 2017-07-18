import scrapy
from utils.webpage import log_empty_fields, get_url_param, get_trunk, get_content
from utils.my_datetime import get_timestamp, get_date_list
from wangjia.items import ShujuItem, DaohangItem
import json

#############################################################################################################
#                                                                                                           #
# USAGE: nohup scrapy crawl buchong -a from_id=1 -a to_id=10 --loglevel=INFO --logfile=log & #
#                                                                                                           #
#############################################################################################################

class BuchongSpider(scrapy.Spider):
    name = 'buchong'
    allowed_domains = ['wdzj.com']
    start_url = 'http://shuju.wdzj.com/plat-info-initialize.html'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=30, to_id=30, *args, **kwargs):
        self.logger.debug(locals())
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.mapping = {}
        super(BuchongSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = DaohangItem.get_object_by_pk(i)
            if obj.plat_id:
                plat_id = obj.plat_id
                self.mapping[plat_id] = obj
                body = {'wdzjPlatId': str(plat_id)}

                yield scrapy.FormRequest(self.start_url, formdata=body, meta = body, dont_filter=True)

    def parse(self, response):
        symbol = (response.meta.get('wdzjPlatId'), response.url)
        self.logger.info('Parsing ID.%s Wangjia Data From <%s>.' % symbol)

        obj = self.mapping[symbol[0]]

        try:
            content = json.loads(response.body)
            if not content or not len(content) or not content.get('amountValue'):
                raise ValueError
        except Exception as e:
            self.logger.warning('Empty Response Of %s Wangjia Data From <%s>.' % symbol)
            return None

        # timestamp, data_list = get_timestamp(symbol[0], '-'), []
        data_list = []
        length = len(content.get('amountValue'))
        for i in xrange(length):
            timestamp = get_timestamp(content['date'][i], '-')
            if timestamp > '20160601' and timestamp < '20161231':
                item = ShujuItem()
                item['name'] = obj.name
                item['timestamp'] = timestamp
                item['volume'] = content['amountValue'][i]
                item['investment_passenger'] = content['bidValue'][i]
                item['loan_passenger'] = content['borValue'][i]
                if item.get_uk(): data_list.append(item)
        return data_list

        # for data in content:
        #     item = ShujuItem()
        #     item['timestamp'] = timestamp
        #     item['name'] = data['platName']
        #     item['volume'] = data['amount']
        #     item['investment_passenger'] = data['bidderNum']
        #     item['loan_passenger'] = data['borrowerNum']
        #     item['average_interest_rate'] = data['incomeRate']
        #     item['average_loan_period'] = data['loanPeriod']
        #     item['loan_bid'] = data['totalLoanNum']
        #     item['registered_capital'] = data['regCapital']
        #     item['time_for_full_bid'] = data['fullloanTime']
        #     item['accounted_revenue'] = data['stayStillOfTotal']
        #     item['capital_inflow_in_30_days'] = data['netInflowOfThirty']
        #     item['volumn_weighted_time'] = data['weightedAmount']
        #     item['accounted_revenue_in_60_days'] = data['stayStillOfNextSixty']
        #     item['proportion_of_top_10_tuhao_accounted_revenue'] = data['top10DueInProportion']
        #     item['average_investment_amount'] = data['avgBidMoney']
        #     item['proportion_of_top_10_borrower_accounted_revenue'] = data['top10StayStillProportion']
        #     item['average_loan_amount'] = data['avgBorrowMoney']
        #     item['capital_lever'] = data['currentLeverageAmount']
        #     item['operation_time'] = data['timeOperation']
        #
        #     #log_empty_fields(item, self.logger)
        #     if item.get_uk(): data_list.append(item)
        #
        # return data_list
