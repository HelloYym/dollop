# -*- coding: utf-8 -*-
from django.db import models
from .lolly import Lolly


class FinancialProduct(Lolly):
    # 产品代码
    code = models.CharField(max_length=100, null=False)
    # 产品名称
    name = models.CharField(max_length=100, null=False)
    # 日期
    date = models.DateField(null=False)
    # 七日年化收益率，随日期变化
    rate = models.CharField(max_length=50, null=True)

    # 产品详情链接
    link = models.CharField(max_length=200, null=True)
    # 发行机构
    issuer = models.CharField(max_length=50, null=True)
    # 资金规模
    fund_scale = models.CharField(max_length=50, null=True)
    # 起售金额
    min_amount = models.CharField(max_length=50, null=True)
    # 万份收益
    w_income = models.CharField(max_length=50, null=True)
    # 提取上限及说明
    ceiling = models.CharField(max_length=50, null=True)
    ceiling_comment = models.TextField(null=True)
    # 提现速度及说明
    speed = models.CharField(max_length=50, null=True)
    speed_comment = models.TextField(null=True)

    # 合作机构
    cooperation = models.CharField(max_length=50, null=True)
    # 公司名称
    company = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'rong360_product'
        unique_together = ('code', 'name', 'date')


    def get_uk_code(self):
        return self.code + '_' + self.name + '_' + str(self.date)
