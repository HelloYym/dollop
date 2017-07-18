import scrapy, json
from scrapy.http import Request
from utils.webpage import log_empty_fields, get_url_param
from utils.exporter import read_cache
from utils.hmacsha1 import get_unix_time, get_access_signature
from aif.items import MeiyueItem

class MeiyueSpider(scrapy.Spider):
    name = 'meiyue'
    allowed_domains = ['zwgt.com', 'order.ddsoucai.com']
    start_formated_url = None
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, plat_id=None, method='0', need_token='0', formated_url='', password=None, month='201609', is_json=0, is_upper=0, *args, **kwargs):
        self.logger.debug(locals())
        self.plat_id = plat_id
        self.method = bool(int(method))
        self.need_token = bool(int(need_token))
        self.start_formated_url = formated_url
        self.password = password
        self.month = '-'.join(map('{:0>2}'.format, map(int, (month[:4], month[4:6]))))
        self.is_json = int(is_json)
        self.is_upper = int(is_upper)

        super(MeiyueSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.need_token:
            token = ''
            lines = read_cache('tokens', (self.plat_id or 'token')+'.tk')
            if self.need_token and lines:
                token = lines[0]

            timestamp = get_unix_time()
            signature = get_access_signature(token, timestamp, self.password, self.is_upper)
            body = {'token': token, 'timestamp': timestamp, 'signature': signature, 'month': self.month}
            if self.is_json:
                yield Request(self.start_formated_url, body=json.dumps(body), method='POST')
            else:
                yield scrapy.FormRequest(self.start_formated_url, formdata=body, dont_filter=True)
        else:
            if self.method:
                yield scrapy.FormRequest(self.start_formated_url.format(month=self.month), method='GET', dont_filter=True)
            else:
                body = {'month':self.month}
                if self.is_json:
                    yield Request(self.start_formated_url, body=json.dumps(body), method='POST')
                else:
                    yield scrapy.FormRequest(self.start_formated_url, formdata=body, dont_filter=True)

    def parse(self, response):
        if self.method:
            symbol = (self.plat_id, get_url_param(response.url, 'month'), response.url)
        else:
            if self.is_json:
                symbol = (self.plat_id, json.loads(response.request.body)['month'], response.url)
            else:
                symbol = (self.plat_id, get_url_param(response.request.body, 'month'), response.url)
        self.logger.info('Parsing No.%s Plat %s Monthly Data From <%s>.' % symbol)

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
            self.logger.warning('Fail To Receive No.%s Plat %s Monthly Data From <%s>' % symbol)
            return None

        item = MeiyueItem()
        item['plat_id'] = self.plat_id
        item['date'] = symbol[1]
        item['loan_amount_per_capita'] = internal_content.get('loan_amount_per_capita')
        item['avg_loan_per_trade'] = internal_content.get('avg_loan_per_trade')
        item['invest_amount_per_capita'] = internal_content.get('invest_amount_per_capita')
        item['avg_invest_per_trade'] = internal_content.get('avg_invest_per_trade')
        item['max_borrower_ratio'] = internal_content.get('max_borrower_ratio')
        item['topten_borrowers_ratio'] = internal_content.get('topten_borrowers_ratio')
        item['overdue_project_amount'] = internal_content.get('overdue_project_amount')
        item['avg_interest_rate'] = internal_content.get('avg_interest_rate')
        item['avg_borrow_period'] = internal_content.get('avg_borrow_period')

        log_empty_fields(item, self.logger)
        return item
