# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly


class PlatformFeature(Lolly):
    # pin 唯一标示
    # name 平台名
    # link 链接
    # feature 标签
    # online_time 上线时间
    # capital 注册资本
    # address 注册地址
    # company 公司名称
    # legal_representative 法人代表
    # scale 公司规模
    # auto_bid 自动投标
    # debt_assignment 债权转让
    # funds_custody 资金托管
    # assurance_mode 保障模式
    # feature_detail 平台特色
    pin = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=50, null=True)
    link = models.URLField(null=True)
    feature = models.CharField(max_length=500, null=True)
    online_time = models.CharField(max_length=50, null=True)
    capital = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=500, null=True)
    company = models.CharField(max_length=500, null=True)
    legal_representative = models.CharField(max_length=100, null=True)
    scale = models.CharField(max_length=100, null=True)
    auto_bid = models.CharField(max_length=100, null=True)
    debt_assignment = models.CharField(max_length=1000, null=True)
    funds_custody = models.CharField(max_length=500, null=True)
    assurance_mode = models.CharField(max_length=500, null=True)
    feature_detail = models.TextField(null=True)
    state = models.CharField(max_length=100, null=True)
    problem_time = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'p2peye_platform_feature'

    def get_uk_code(self):
        return str(self.id)+'_'+self.pin

class Dangan(Lolly):
    pin = models.CharField(unique=True, max_length=20)
    product_name = models.CharField(max_length=128)
    product_state = models.CharField(max_length=128, null=True)
    p2peye_rating = models.CharField(max_length=20, null=True)
    problem_time = models.CharField(max_length=20, null=True)

    # 公司信息
    launch_time = models.CharField(max_length=20, null=True)
    province = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    introduction = models.TextField(null=True)
    web_url = models.URLField(null=True)
    logo_url = models.URLField(null=True)

    # 工商信息
    company_name = models.CharField(max_length=256, null=True)
    artificial_person = models.CharField(max_length=50, null=True)
    company_type = models.CharField(max_length=50, null=True)
    ownership_structure = models.TextField(null=True)
    registered_capital = models.TextField(null=True)
    contributed_capital = models.TextField(null=True)
    registered_address = models.TextField(null=True)
    opening_date = models.CharField(max_length=20, null=True)
    approved_date = models.CharField(max_length=20, null=True)
    registration_authority = models.TextField(null=True)
    business_licence = models.CharField(max_length=50, null=True)
    institutional_framework = models.CharField(max_length=50, null=True)
    tax_registration_num = models.CharField(max_length=50, null=True)
    business_scope = models.TextField(null=True)

    # 备案信息
    domain_name = models.CharField(max_length=256, null=True)
    domain_date = models.CharField(max_length=20, null=True)
    domain_company_type = models.CharField(max_length=20, null=True)
    domain_company_name = models.CharField(max_length=256, null=True)
    ICP_number = models.CharField(max_length=50, null=True)
    ICP_approval_number = models.CharField(max_length=20, null=True)

    # 平台费用
    account_fee = models.TextField(null=True)
    cash_fee = models.TextField(null=True)
    fueling_fee = models.TextField(null=True)
    #transfer_fee = models.TextField(null=True)
    vip_fee = models.TextField(null=True)

    # 联系方式
    contact_address = models.TextField(null=True)
    phone_400 = models.CharField(max_length=256, null=True)

    # 平台服务
    automatic_bid = models.TextField(null=True)
    equitable_assignment = models.TextField(null=True)
    security_mode = models.TextField(null=True)

    img_grabber_executed = models.BooleanField(default=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'p2peye_archive'

    def get_uk_code(self):
        return 'thread_' + str(self.id)

class GaoGuan(Lolly):
    pin = models.CharField(max_length=20)
    product_name = models.CharField(max_length=128)
    name = models.CharField(max_length=50)
    post = models.CharField(max_length=100)
    image_url = models.URLField(null=True)
    introduction = models.TextField(null=True)

    img_grabber_executed = models.BooleanField(default=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'p2peye_businessman'
        unique_together = ('pin', 'name', 'post')

    def get_uk_code(self):
        return 'thread_'+str(self.id)

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