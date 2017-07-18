# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import chinawealth

class ChanpinItem(BaseItem):
    django_model = chinawealth.Product
    update_fields_list = ['min_profit', 'pro_end_date', 'state', 'days', 'end_date', 'profit_type',          \
                          'limit_type', 'start_date', 'currency', 'name', 'pro_start_date', 'risk_rank',     \
                          'asset_type', 'bus_start_date', 'init_worth', 'regis_code', 'area', 'max_profit',  \
                          'customer', 'act_profit', 'oprate_mode', 'bus_end_date', 'disbank', 'pro_worth',   \
                          'start_money', 'institution_code', 'bqjz', 'cpdm', 'cpfxdj', 'cplx', 'cpxsqy',     \
                          'cpsylx']
    unique_key = ('pid',)