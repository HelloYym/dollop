# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import p2peye


class ExposureItem(BaseItem):
    django_model = p2peye.P2peyeExposure
    update_fields_list = ['source', 'title', 'created', 'name', 'link', 'reason', 'content', 'raw_content',
                          'image_url']
    unique_key = ('thread',)



class NewsItem(BaseItem):
    django_model = p2peye.P2peyeNews
    update_fields_list = ['source', 'title', 'created', 'author', 'summary', 'content', 'raw_content', 'image_url']
    unique_key = ('thread', 'category')