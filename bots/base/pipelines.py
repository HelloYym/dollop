from scrapy_djangoitem import ValidationError
from functools import wraps

def check_spider_internal(internal_method):

    @wraps(internal_method)
    def wrapper(self, spider):

        if self.__class__.__name__ in spider.pipeline:
            return internal_method(self, spider)

    return wrapper

def check_spider_pipeline(process_item_method):

    @wraps(process_item_method)
    def wrapper(self, item, spider):
        msg = '%%s %s pipline step.' % (self.__class__.__name__,)
        if self.__class__.__name__ in spider.pipeline:
            spider.logger.debug(msg % 'Executing')
            return process_item_method(self, item, spider)
        else:
            spider.logger.debug(msg % 'Skipping')
            return item

    return wrapper

class BaseUniqueItemPersistencePipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):

        if item.unique_key and not item.get_uk():
            return None

        klass = item.__class__
        try:
            # If item doesn't exist, create it.
            item.instance.validate_unique()
            item.save()
        except ValidationError as e:
            # If item exists, update it.
            uk_params = item.get_uk_params()
            spider.logger.info('Duplicate Item From ' + str(uk_params) + '.')
            obj = klass.get_object_by_uk(uk_params)
            update_fields = item.get_update_fields(obj)
            merge_fields = item.get_merge_fields(obj)
            if update_fields:
                obj.update_attr(update_fields, merge_fields, item)
                obj.save()

        return item

class BaseRelatedItemPersistencePipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        klass = item.__class__
        try:
            # If spider.object has existed related item, update it.
            obj = getattr(spider.object, item.related_field)
            update_fields = item.get_update_fields(obj)
            merge_fields = item.get_merge_fields(obj)
            if update_fields:
                obj.update_attr(update_fields, merge_fields, item)
                obj.save()
        except klass.django_model.DoesNotExist as e:
            # If spider.object has no related item, create it.
            setattr(spider.object, item.related_field, item.instance)
            item.save()
            spider.object.save()

        return item

class BaseCacheExporterPersistencePipeline(object):

    def get_type(self):
        raise NotImplementedError

    def get_filepath(self):
        import os
        fpath = os.path.join('items', self.get_type())
        if not os.path.isdir(fpath): os.makedirs(fpath, 0o777)

        return fpath

    def get_filename(self, spider):
        return getattr(spider, 'filename', 'test')

    def log_successful_info(self, item, spider):
        pass

    def log_failure_info(self, spider):
        pass

    @check_spider_internal
    def open_spider(self, spider):
        import os
        fname = os.path.join(self.get_filepath(), self.get_filename(spider))
        self.file = open(fname, 'wb')
        self.first_item = True
        #from scrapy.exporters import JsonItemExporter
        #NOTE: (zacky, 2016.APR.27th) WE CAN SELECT PROPER OUTPUT FORMAT EXPORTERS.
        #self.exporter = PprintItemExporter(self.file)
        #self.exporter.start_exporting()

    @check_spider_internal
    def close_spider(self, spider):
        self.file.close()
        #self.exporter.finish_exporting()

    @check_spider_pipeline
    def process_item(self, item, spider):
        if item and item['count']>0:
            for rc in item.get_record():
                if self.first_item:
                    self.first_item = False
                else:
                    self.file.write('\n')
                #self.exporter.export_item(item)
                self.file.write(rc)
            self.log_successful_info(item, spider)
        else:
            self.log_failure_info(spider)

        return item
