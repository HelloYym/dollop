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

class Buchong2Spider(scrapy.Spider):
    name = 'buchong2'
    allowed_domains = ['wdzj.com']
    start_url = 'http://shuju.wdzj.com/plat-info-target.html'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=27, to_id=27, target1=2, target2=0, *args, **kwargs):
        self.logger.debug(locals())
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.target1 = str(target1)
        self.target2 = str(target2)
        self.mapping = {}
        super(Buchong2Spider, self).__init__(*args, **kwargs)

    def start_requests(self):
        body = {'type':'1','target1':self.target1,'target2':self.target2}
        for i in self.shortlist:
            obj = DaohangItem.get_object_by_pk(i)
            if obj.plat_id:
                plat_id = obj.plat_id
                self.mapping[plat_id] = obj
                body['wdzjPlatId'] = str(plat_id)

                yield scrapy.FormRequest(self.start_url, formdata=body, meta = body, dont_filter=True)

    def parse(self, response):
        symbol = (response.meta.get('wdzjPlatId'), response.url)
        self.logger.info('Parsing ID.%s Wangjia Data From <%s>.' % symbol)

        obj = self.mapping[symbol[0]]

        try:
            content = json.loads(response.body)
            if not content or not len(content) or not content.get('date'):
                raise ValueError
        except Exception as e:
            self.logger.warning('Empty Response Of %s Wangjia Data From <%s>.' % symbol)
            return None

        data_list = []
        length = len(content.get('date'))

        if response.meta.get('target1') == '2'and response.meta.get('target2') == '0':
            for i in xrange(length):
                timestamp = get_timestamp(content['date'][i], '-')
                if timestamp > '20160601' and timestamp < '20161231':
                    item = ShujuItem()
                    timestamp = timestamp
                    item['name'] = obj.name
                    item['timestamp'] = timestamp
                    item['average_interest_rate'] = content['data1'][i]
                    if item.get_uk(): data_list.append(item)

        elif response.meta.get('target1') == '10' and response.meta.get('target2') == '23':
            for i in xrange(length):
                timestamp = get_timestamp(content['date'][i], '-')
                if timestamp > '20160601' and timestamp < '20161231':
                    item = ShujuItem()
                    timestamp = timestamp
                    item['name'] = obj.name
                    item['timestamp'] = timestamp
                    item['average_loan_period'] = content['data1'][i]
                    if item.get_uk(): data_list.append(item)

        return data_list
