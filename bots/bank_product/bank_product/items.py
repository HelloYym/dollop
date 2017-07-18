# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from bots.base.items import BaseItem
from stalk.models import product


class BankProductItem(BaseItem):
    django_model = product.BankProduct
    update_fields_list = ['anticipate_rate', 'limit_time', 'min_amount', 'ascend_amount', 'risk', 'product_type',
                          'finance_type', 'remaining_quota', 'ipo_start_date', 'ipo_end_date', 'income_start_date',
                          'product_end_date', 'currency', 'extra', 'link', 'investor_list']
    unique_key = ('code', 'name', 'bank_domain')

#
# class BankProductInvestor(BaseItem):
#     django_model = Investor
#     update_fields_list = ['investor_name', 'investor_id', 'investor_phone', 'invest_amount', 'invest_time', 'extra']
#     unique_key = ('treaty_no', 'product')
