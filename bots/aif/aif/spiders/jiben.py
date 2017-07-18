import scrapy, json
from scrapy.http import Request
from utils.webpage import log_empty_fields, get_url_param
from utils.exporter import read_cache
from utils.hmacsha1 import get_unix_time, get_access_signature
from utils.my_datetime import get_date_list
from aif.items import JibenItem

#################################################################################################
#                                                                                               #
# USAGE: nohup scrapy crawl jiben -a plat_id=1 -a need_token=1                                  #
#        -a formated_url='http://api.xxx.com/interface-basicdata?token={token}&date=yyyy-mm-dd' #
#        --loglevel=INFO --logfile=log &                                                        #
#                                                                                               #
#################################################################################################

class JibenSpider(scrapy.Spider):
    name = 'jiben'
    allowed_domains = ['zwgt.com', 'order.ddsoucai.com']
    start_formated_url = None
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, plat_id=None, method='0', need_token='0', formated_url='', password=None, from_date='20161008', to_date='20161008', is_json=0, is_upper=0, *args, **kwargs):
        self.logger.debug(locals())
        self.plat_id = plat_id
        self.method = bool(int(method))
        self.need_token = bool(int(need_token))
        self.start_formated_url = formated_url
        self.password = password
        self.from_date, self.to_date = from_date, to_date
        self.is_json = int(is_json)
        self.is_upper = int(is_upper)

        super(JibenSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.need_token:
            token = ''
            lines = read_cache('tokens', (self.plat_id or 'token')+'.tk')

            if self.need_token and lines: token = lines[0]

            timestamp = get_unix_time()
            signature = get_access_signature(token, timestamp, self.password, self.is_upper)

            for date in get_date_list(from_date=self.from_date, to_date=self.to_date, delimiter='-'):
                body = {'token': token, 'timestamp': timestamp, 'signature': signature, 'date': date}
                if self.is_json:
                    yield Request(self.start_formated_url, body=json.dumps(body), method='POST')
                else:
                    yield scrapy.FormRequest(self.start_formated_url, formdata=body, dont_filter=True)
        else:
            if self.method:
                for date in get_date_list(from_date=self.from_date, to_date=self.to_date, delimiter='-'):
                    yield scrapy.FormRequest(self.start_formated_url.format(date=date), method='GET', dont_filter=True)
            else:
                for date in get_date_list(from_date=self.from_date, to_date=self.to_date, delimiter='-'):
                    body = {'date': date}
                    if self.is_json:
                        yield Request(self.start_formated_url, body=json.dumps(body), method='POST')
                    else:
                        yield scrapy.FormRequest(self.start_formated_url, formdata=body, dont_filter=True)

    def parse(self, response):
        if self.method:
            symbol = (self.plat_id, get_url_param(response.url, 'date'), response.url)
        else:
            if self.is_json:
                symbol = (self.plat_id, json.loads(response.request.body)['date'], response.url)
            else:
                symbol = (self.plat_id, get_url_param(response.request.body, 'date'), response.url)
        self.logger.info('Parsing No.%s Plat %s Basic Data From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            self.logger.info(content)
            if isinstance(content.get('data', {}), list):
                internal_content = content.get('data', {})[0]
            else:
                internal_content = content.get('data', {})
            if int(content.get('result_code', -1)) != 1 or not internal_content:
                raise ValueError
        except Exception:
            self.logger.warning('Fail To Receive No.%s Plat %s Basic Data From <%s>.' % symbol)
            return None

        item = JibenItem()
        item['plat_id'] = self.plat_id
        item['date'] = symbol[1]
        item['turnover_amount'] = internal_content.get('turnover_amount')
        item['unconventional_turnover_amount'] = internal_content.get('unconventional_turnover_amount')
        item['trade_amount'] = internal_content.get('trade_amount')
        item['borrower_amount'] = internal_content.get('borrower_amount')
        item['investor_amount'] = internal_content.get('investor_amount')
        item['different_borrower_amount'] = internal_content.get('different_borrower_amount')
        item['different_investor_amount'] = internal_content.get('different_investor_amount')
        item['loan_balance'] = internal_content.get('loan_balance')
        item['avg_full_time'] = internal_content.get('avg_full_time')
        item['product_overdue_rate'] = internal_content.get('product_overdue_rate')
        item['overdue_loan_amount'] = internal_content.get('overdue_loan_amount')
        item['compensatory_amount'] = internal_content.get('compensatory_amount')
        item['loan_overdue_rate'] = internal_content.get('loan_overdue_rate')

        log_empty_fields(item, self.logger)
        return item
