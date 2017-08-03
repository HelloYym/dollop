# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import xianjindai


class JdqProductItem(BaseItem):
    django_model = xianjindai.JdqProduct
    update_fields_list = ['name', 'channel_name', 'logo', 'apply_count', 'success_rate', 'tag_list', 'description',
                          'min_amount', 'max_amount', 'min_terms', 'max_terms', 'interest', 'interest_unit',
                          'min_duration', 'min_duration_unit', 'conditions', 'materials', 'apply_url']

    unique_key = ('code',)


class XjdProductItem(BaseItem):
    django_model = xianjindai.XjdProduct
    update_fields_list = ['logo', 'comment', 'amount', 'term', 'interest',
                          'repay', 'speed', 'link']

    unique_key = ('name', 'category')
