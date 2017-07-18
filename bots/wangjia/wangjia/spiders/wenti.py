import scrapy
import json
from wangjia.items import WentiItem

#################################################################################################
#                                                                                               #
# USAGE: nohup scrapy crawl wenti -a from_id=2016 -a to_id=2016 --loglevel=INFO --logfile=log & #
#                                                                                               #
#################################################################################################

class WentiSpider(scrapy.Spider):
    name = 'wenti'
    allowed_domains = ['wdzj.com']
    start_formated_url = 'http://shuju.wdzj.com/problem-list-all.html?year={year_id}'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=2016, to_id=2016, *args, **kwargs):
        self.logger.debug(locals())
        self.shortlist = xrange(int(from_id), int(to_id) + 1)
        super(WentiSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for year in self.shortlist:
            url = self.start_formated_url.format(year_id=year)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        self.logger.info('Parsing Wangjia Problem Platform From <%s>.' % response.url)
        # print response.body

        item_list = []
        data = json.loads(response.body)
        problems = data.get('problemList')
        for each in problems:
            item = WentiItem()
            item['name'] = each.get('platName')
            item['problem_time'] = each.get('problemTime').split(' ')[0]
            item['event_category'] = each.get('type')
            item_list.append(item)
        return item_list
