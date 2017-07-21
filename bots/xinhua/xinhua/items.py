# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import xinhua


class NewsItem(BaseItem):

    django_model = xinhua.XinhuaNews
    update_fields_list = ['source', 'title', 'created', 'author', 'summary', 'content', 'raw_content', 'image_url',
                          'keywords']

    unique_key = ('thread', 'category')
