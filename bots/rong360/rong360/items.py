# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import rong360


class ProductItem(BaseItem):
    django_model = rong360.FinancialProduct
    update_fields_list = ['rate', 'link', 'issuer', 'fund_scale', 'min_amount', 'w_income', 'ceiling',
                          'ceiling_comment',
                          'speed', 'speed_comment', 'cooperation', 'company']

    unique_key = ('code', 'name', 'date')
