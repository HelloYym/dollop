# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from bots.base.pipelines import BaseUniqueItemPersistencePipeline

class UniqueItemPersistencePipeline(BaseUniqueItemPersistencePipeline):
    pass


from bots.base.pipelines import BaseCacheExporterPersistencePipeline

class CacheFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'news_cache'

    def get_filename(self, spider):
        filename = 'news_cache'
        return filename+'.ch'