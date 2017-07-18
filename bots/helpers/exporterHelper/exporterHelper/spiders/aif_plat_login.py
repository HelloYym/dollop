import scrapy, json, time
from scrapy.http import Request
from utils.webpage import get_url_host
from utils.hmacsha1 import get_unix_time, get_login_signature
from exporterHelper.items import ExporterItem


############################################################################################
#                                                                                          #
# USAGE: nohup scrapy crawl aif_login -a plat_id=1 -a login_url='http://xxx.com/login?a=b' #
#        --loglevel=INFO --logfile=log &                                                   #
#                                                                                          #
############################################################################################

class AIFPlatLoginSpider(scrapy.Spider):
    name = 'aif_plat_login'
    allowed_domains = []
    start_formated_url = None
    token_field = 'plat_id'
    pipeline = ['TokenFileExporterPersistencePipeline']

    def __init__(self, plat_id=None, login_url=None, username=None, password=None, secret_key=None, is_json=0, is_upper=0, *args, **kwargs):
        self.logger.debug(locals())
        self.plat_id = plat_id
        self.login_url = login_url
        self.username = username
        self.password = password
        self.secret_key = secret_key
        self.is_json = int(is_json)
        self.is_upper = int(is_upper)
        super(AIFPlatLoginSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.login_url:
            timestamp = get_unix_time()
            signature = get_login_signature(self.username, self.password, timestamp, self.secret_key, self.is_upper)
            self.logger.info('timestamp: '+timestamp)
            self.logger.info('signature: '+signature)
            if self.secret_key:
                body = {'username':self.username, 'password':self.password, 'timestamp':timestamp, 'signature':signature.upper()}
            else:
                body = {'username':self.username, 'timestamp':timestamp, 'signature':signature}
            if self.is_json:
                yield Request(self.login_url, body=json.dumps(body), method='POST')
            else:
                yield scrapy.FormRequest(self.login_url, formdata=body)

    def parse(self, response):
        symbol = (self.plat_id, get_url_host(response.url), response.url)
        self.logger.info('Parsing No.%s [%s] Plat Login Info From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            self.logger.info(content)
            if int(content.get('result', 0)) != 1:
                raise ValueError
        except Exception:
            self.logger.warning('Fail To Receive No.%s [%s] Plat Login Info From <%s>.' % symbol)
            return None

        item = ExporterItem()
        item.set_record(content.get('data', {}).get('token'))
        print content.get('data', {}).get('token')
        return item
