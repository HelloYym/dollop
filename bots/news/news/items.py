# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from bots.base.items import BaseItem, ProvinceItem
from stalk.models import wqmodels


class ExporterItem(scrapy.Item):

    count = scrapy.Field()

    def __init__(self):
        #NOTE: (zacky, 2016.MAY.5th) DEFINED AS LIST HERE FOR EXPORTER PIPELINE.
        self._record = []
        super(ExporterItem, self).__init__()

    def set_record(self, rc):
        self._record.append(rc)
        self['count'] = len(self._record)

    def get_record(self):
        for rc in self._record:
            yield str(rc)


class WeiyangNewsItem(BaseItem):
    django_model = wqmodels.weiyang_news
    update_fields_list = []
    unique_key = ('thread_id',)

class PaycircleNewsItem(BaseItem):
    django_model = wqmodels.paycircle_news
    update_fields_list = []
    unique_key = ('thread_id',)

class JrzjNewsItem(BaseItem):
    django_model = wqmodels.jrzj_news
    update_fields_list = []
    unique_key = ('thread_id',)

class WeiyangReportItem(BaseItem):
    django_model = wqmodels.weiyang_report
    update_fields_list = []
    unique_key = ('thread_id',)


class WDZJArchiveItem(BaseItem):
    django_model = wqmodels.wdzj_archive
    update_fields_list = ["name","launched_time","location","official_website","enterprise_name","registered_capital","yinhangcunguan","assembly_record","administration","ICP","stockmarket_status","auto_bid","debt_transfer","bid_guarantee","guarantee_mode","guarantee_institute","risk_guarantee","introduction","account_fee","cash_fee","fueling_fee","transfer_fee","vip_fee"]
    unique_key = ('platPin',)

class WDZJFeaturesItem(BaseItem):
    django_model = wqmodels.wdzj_features
    update_fields_list = ["name","company_tag","trouble_tag","overall_rating","cashing_rating","cashing_desc","guarding_rating","guarding_desc","service_rating","service_desc","experience_rating","experience_desc","impression"]
    unique_key = ('platPin',)

class WDZJNavigationItem(BaseItem):
    django_model = wqmodels.wdzj_navigation
    update_fields_list = [ "name","allPin","link","province","launched_time","icon_url"]
    unique_key = ('platPin',)

class P2peyePlatdataItem(BaseItem):
    django_model = wqmodels.p2peye_platdata
    update_fields_list = []
    unique_key = ()

class HujinzhentanExposureItem(BaseItem):
    django_model = wqmodels.hujinzhentan_exposure
    update_fields_list = []
    unique_key = ('thread_id',)
