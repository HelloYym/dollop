# -*- coding: utf-8 -*-
from django.db import models
from .lolly import Lolly


class JdqProduct(Lolly):
    '''借点钱产品'''

    # 产品代码
    code = models.CharField(max_length=20, null=False, unique=True)
    # 产品名称
    name = models.CharField(max_length=20, null=False)
    channel_name = models.CharField(max_length=20, null=False)
    # logo
    logo = models.URLField(null=True)
    # 申请成功人数
    apply_count = models.IntegerField(null=True)
    # 申请成功率
    success_rate = models.FloatField(null=True)
    # 标签列表
    tag_list = models.CharField(max_length=200, null=True)
    # 特点
    description = models.CharField(max_length=200, null=True)

    # 额度范围
    min_amount = models.FloatField(null=True)
    max_amount = models.FloatField(null=True)

    # 期限范围
    min_terms = models.IntegerField(null=True)
    max_terms = models.IntegerField(null=True)

    # 利率
    interest = models.FloatField(null=True)
    # 利率单位
    interest_unit = models.CharField(max_length=20, null=True)

    # 最快放款时间
    min_duration = models.FloatField(null=True)
    # 最快放款时间单位
    min_duration_unit = models.CharField(max_length=20, null=True)

    # 申请条件
    conditions = models.CharField(max_length=100, null=True)
    # 所需材料
    materials = models.CharField(max_length=100, null=True)

    # 跳转地址
    apply_url = models.URLField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'xjd_jdq_product'

    def get_uk_code(self):
        return self.code + '_' + self.channel_name + '_' + self.name


class XjdProduct(Lolly):
    '''现金贷产品'''

    # 产品名称
    name = models.CharField(max_length=20, null=False)
    # 类别
    category = models.CharField(max_length=20, null=False)
    # logo
    logo = models.URLField(null=True)
    # 注释
    comment = models.CharField(max_length=200, null=True)
    # 贷款金额
    amount = models.CharField(max_length=100, null=True)
    # 贷款期限
    term = models.CharField(max_length=100, null=True)
    # 贷款利息
    interest = models.CharField(max_length=100, null=True)
    # 还款额
    repay = models.CharField(max_length=100, null=True)
    # 下款速度
    speed = models.CharField(max_length=100, null=True)
    # 跳转地址
    link = models.URLField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'xjd_xjd_product'
        unique_together = ('category', 'name')

    def get_uk_code(self):
        return self.category + '_' + self.name
