# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly

class P2peyeExposure(Lolly):
    thread = models.IntegerField(unique=True)
    source = models.URLField(null=True)
    title = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(null=True)
    name = models.CharField(max_length=100, null=True)
    link = models.URLField(null=True)
    reason = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)
    img_grabber_executed = models.BooleanField(default=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'p2peye_exposure'

    def get_uk_code(self):
        return 'thread_'+str(self.id)

class P2peyeNews(Lolly):
    thread = models.IntegerField()
    category = models.CharField(max_length=50, null=True)
    source = models.URLField(null=True)
    title = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(null=True)
    author = models.CharField(max_length=50, null=True)
    summary = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)
    img_grabber_executed = models.BooleanField(default=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'p2peye_news'
        unique_together = ('thread', 'category')

    def get_uk_code(self):
        return 'thread_'+str(self.id)