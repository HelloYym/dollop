# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly


class LingyiNews(Lolly):
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
    keywords = models.CharField(max_length=200, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'lingyi_news'
        unique_together = ('thread', 'category')

    def get_uk_code(self):
        return 'thread_' + str(self.id)


class LingyiPlatform(Lolly):
    # 平台代码
    code = models.CharField(max_length=100, null=False)
    # 平台名称
    name = models.CharField(max_length=100, null=False)
    # 平台名称，英文链接
    platname = models.CharField(max_length=100, null=False)
    # 平台网站
    website = models.URLField(null=True)
    # 上线时间
    online_time = models.CharField(max_length=20, null=False)

    # 日期
    date = models.DateField(null=False)

    # 以下是随时间变化的指标，每天一条记录

    # 借款额
    borrow_amount = models.FloatField(null=True)
    # 借款笔数
    borrow_cnt = models.IntegerField(null=True)
    # 利率
    interest = models.FloatField(null=True)
    # 平均借款期限
    period = models.FloatField(null=True)

    # 借款人数量
    borrower_cnt = models.IntegerField(null=True)
    # 人均借款额
    borrower_avg = models.FloatField(null=True)
    # 投资人数
    investor_cnt = models.IntegerField(null=True)
    # 人均投资额
    investor_avg = models.FloatField(null=True)

    # 还款金额
    repay = models.FloatField(null=True)
    # 待还金额
    stay = models.FloatField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'lingyi_platform'
        unique_together = ('code', 'name', 'date')

    def get_uk_code(self):
        return self.code + '_' + self.name + '_' + str(self.date)
