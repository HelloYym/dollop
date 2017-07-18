# -*- coding: utf-8 -*-
import scrapy
import json
from chinawealth.items import ChanpinItem

class ChanpinSpider(scrapy.Spider):
    name = "chanpin"
    allowed_domains = ["chinawealth.com.cn"]
    search_url = 'http://www.chinawealth.com.cn/lccpAllProJzyServlet.go'
    pipeline = ['UniqueItemPersistencePipeline']
    cpzt = {1: ('02',), 2: ('04',), 3: ('02', '04')}
    #02 在售， 04 存续

    def __init__(self, state=1, from_page=1, to_page=1, *args, **kwargs):
        self.state_id = int(state)
        self.shortlist = xrange(int(from_page), int(to_page)+1)
        super(ChanpinSpider,self).__init__(*args, **kwargs)

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        for zt in self.cpzt.get(self.state_id):
            for page in self.shortlist:
                body = {'pagenum': str(page), 'tzzlxdm': '03', 'cpzt': zt}
                yield scrapy.FormRequest(self.search_url, headers=headers, formdata=body, dont_filter=True, meta=body)

    def parse(self, response):
        data = json.loads(response.body)
        symbol = (response.meta['pagenum'], response.meta['cpzt'])

        if data.get('code'):
            self.logger.info('Parsing Chinawealth Product List in Page %s is Error' % symbol[0])
            return None

        self.logger.info('Parsing Chinawealth Product List of Type.%s (Count is %d) in Page %s'
                         % (symbol[1],data.get('Count'), symbol[0]))

        item_list = []
        for each in data.get('List', []):
            print(each)
            item = ChanpinItem()
            item['pid'] = each.get('cpid')
            item['min_profit'] = each.get('yjkhzdnsyl')
            item['pro_end_date'] = each.get('cpyjzzrq')
            item['state'] = each.get('cpztms')
            item['days'] = each.get('cpqx')
            item['end_date'] = each.get('mjjsrq')
            item['profit_type'] = each.get('cpsylxms')
            item['limit_type'] = each.get('qxms')
            item['start_date'] = each.get('mjqsrq')
            item['currency'] = each.get('mjbz')
            item['name'] = each.get('cpms')
            item['pro_start_date'] = each.get('cpqsrq')
            item['risk_rank'] = each.get('fxdjms')
            item['asset_type'] = each.get('tzlxms')
            item['bus_start_date'] = each.get('kfzqqsr')
            item['init_worth'] = each.get('csjz')
            item['regis_code'] = each.get('cpdjbm')
            item['area'] = each.get('xsqy')
            item['max_profit'] = each.get('yjkhzgnsyl')
            item['customer'] = each.get('tzzlxms')
            item['act_profit'] = each.get('dqsjsyl')
            item['oprate_mode'] = each.get('cplxms')
            item['bus_end_date'] = each.get('kfzqjsr')
            item['disbank'] = each.get('fxjgms')
            item['pro_worth'] = each.get('cpjz')
            item['start_money'] = each.get('qdxsje')
            item['institution_code'] = each.get('fxjgdm')
            item['bqjz'] = each.get('bqjz')
            item['cpdm'] = each.get('cpdm')
            item['cpfxdj'] = each.get('cpfxdj')
            item['cplx'] = each.get('cplx')
            item['cpxsqy'] = each.get('cpxsqy')
            item['cpsylx'] = each.get('cpsylx')


            item_list.append(item)
        return item_list

