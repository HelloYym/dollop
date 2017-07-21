# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly

class XinhuaNews(Lolly):
    thread = models.IntegerField()
    category = models.CharField(max_length=50, null=True)
    source = models.URLField(null=True)
    title = models.CharField(max_length=500, null=True)
    created = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    summary = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)
    img_grabber_executed = models.BooleanField(default=False)
    keywords = models.CharField(max_length=200, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'xinhua_news'
        unique_together = ('thread', 'category')

    def get_uk_code(self):
        return 'thread_'+str(self.id)