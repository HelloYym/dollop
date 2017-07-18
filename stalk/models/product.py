# -*- coding: utf-8 -*-
from django.db import models
from .lolly import Lolly


class BankProduct(Lolly):
    # 产品代码
    code = models.CharField(max_length=100, null=False)
    # 产品名称
    name = models.CharField(max_length=100, null=False)
    # 预期年化收益率
    anticipate_rate = models.CharField(max_length=100, null=True)
    # 投资期限
    limit_time = models.CharField(max_length=100, null=True)
    # 起售金额
    min_amount = models.CharField(max_length=100, null=True)
    # 递增金额
    ascend_amount = models.CharField(max_length=100, null=True)
    # 风险等级
    risk = models.CharField(max_length=100, null=True)
    # 产品类型
    product_type = models.CharField(max_length=100, null=True)
    # 理财类型
    finance_type = models.CharField(max_length=100, null=True)
    # 剩余额度
    remaining_quota = models.CharField(max_length=100, null=True)
    # 募集开始日
    ipo_start_date = models.DateField(null=True)
    # 募集结束日
    ipo_end_date = models.DateField(null=True)
    # 收益起算日
    income_start_date = models.DateField(null=True)
    # 产品到期日
    product_end_date = models.DateField(null=True)
    # 所属银行名称
    bank_domain = models.CharField(max_length=100, null=False)
    # 币种
    currency = models.CharField(max_length=20, default='人民币', null=True)
    # 产品详情链接
    link = models.CharField(max_length=200, null=True)
    # 保留字段
    extra = models.CharField(max_length=100, null=True)
    # 投资人列表
    investor_list = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bank_product'
        unique_together = ('code', 'name', 'bank_domain')


    def get_uk_code(self):
        return self.code + '_' + self.name + '_' + self.bank_domain


# class Investor(Lolly):
#     # # 产品代码
#     # prd_code = models.CharField(max_length=100, null=True)
#     # # 产品名称
#     # prd_name = models.CharField(max_length=100, null=False)
#     # # 所属银行名称
#     # bank_domain = models.CharField(max_length=100, null=True)
#
#     # 所属产品
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # 交易号
#     treaty_no = models.CharField(max_length=100)
#     # 投资人姓名
#     investor_name = models.CharField(max_length=100, null=True)
#     # 投资人身份证
#     investor_id = models.CharField(max_length=100, null=True)
#     # 投资人手机
#     investor_phone = models.CharField(max_length=100, null=True)
#     # 投资额
#     invest_amount = models.CharField(max_length=100, null=True)
#     # 投资时间
#     invest_time = models.DateTimeField(null=True)
#
#     extra = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         app_label = 'stalk'
#         db_table = 'bank_product_investor'
#         unique_together = ('product', 'treaty_no')
#
#     def get_uk_code(self):
#         return str(self.id) + '_' + self.treaty_no
