# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import lingyi


class NewsItem(BaseItem):
    django_model = lingyi.LingyiNews
    update_fields_list = ['source', 'title', 'created', 'author', 'summary', 'content', 'raw_content', 'image_url',
                          'keywords']
    unique_key = ('thread', 'category')


class PlatformItem(BaseItem):
    django_model = lingyi.LingyiPlatform
    update_fields_list = ['platname', 'website', 'online_time', 'borrow_amount', 'borrow_cnt', 'interest', 'period',
                          'borrower_cnt',
                          'borrower_avg', 'investor_cnt', 'investor_avg', 'repay', 'stay']
    unique_key = ('code', 'name', 'date')
