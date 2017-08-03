# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly


class BaojianhuiReport(Lolly):
    id = models.CharField(max_length=200, null=False, primary_key=True)
    link = models.URLField(null=False)
    title = models.CharField(max_length=200, null=True)
    created = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)
    img_grabber_executed = models.BooleanField(default=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_stat_report'

    def get_uk_code(self):
        return str(self.id)


class BaojianhuiJingying(Lolly):
    id = models.CharField(max_length=200, null=False, primary_key=True)
    link = models.URLField(null=False)
    title = models.CharField(max_length=200, null=True)
    created = models.CharField(max_length=20, null=True)
    data = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)
    img_grabber_executed = models.BooleanField(default=False)
    year = models.CharField(max_length=20, null=True)
    month = models.CharField(max_length=20, null=True)

    income = models.CharField(max_length=50, null=True)
    baohu_xz = models.CharField(max_length=50, null=True)
    duli_xz = models.CharField(max_length=50, null=True)
    expense = models.CharField(max_length=50, null=True)
    manage_fee = models.CharField(max_length=50, null=True)
    bank_deposits = models.CharField(max_length=50, null=True)
    invest = models.CharField(max_length=50, null=True)
    amount = models.CharField(max_length=50, null=True)
    yanglao_cost = models.CharField(max_length=50, null=True)
    yanglao_shoutuo = models.CharField(max_length=50, null=True)
    yanglao_touzi = models.CharField(max_length=50, null=True)

    caichanxian1 = models.CharField(max_length=50, null=True)
    renshenxian1 = models.CharField(max_length=50, null=True)
    shouxian1 = models.CharField(max_length=50, null=True)
    jiankangxian1 = models.CharField(max_length=50, null=True)
    yiwaixian1 = models.CharField(max_length=50, null=True)

    caichanxian2 = models.CharField(max_length=50, null=True)
    renshenxian2 = models.CharField(max_length=50, null=True)
    shouxian2 = models.CharField(max_length=50, null=True)
    jiankangxian2 = models.CharField(max_length=50, null=True)
    yiwaixian2 = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_jingying'

    def get_uk_code(self):
        return str(self.id)


class BaojianhuiCcxCompany(Lolly):
    link = models.URLField(null=False)
    title = models.CharField(max_length=200, null=False)
    year = models.CharField(max_length=20, null=False)
    month = models.CharField(max_length=20, null=False)
    company_name = models.CharField(max_length=100, null=False)
    income = models.CharField(max_length=100, null=True)
    capital_structure = models.CharField(max_length=100, null=True)
    created = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    share = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_ccx_company_income'
        unique_together = ('year', 'month', 'company_name')

    def get_uk_code(self):
        return self.year + self.month + self.company_name


class BaojianhuiRsxCompany(Lolly):
    link = models.URLField(null=False)
    title = models.CharField(max_length=200, null=False)
    year = models.CharField(max_length=20, null=False)
    month = models.CharField(max_length=20, null=False)
    company_name = models.CharField(max_length=100, null=False)
    income = models.CharField(max_length=100, null=True)
    capital_structure = models.CharField(max_length=100, null=True)
    created = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    baohu_xz = models.CharField(max_length=20, null=True)
    duli_xz = models.CharField(max_length=20, null=True)
    share = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_rsx_company_income'
        unique_together = ('year', 'month', 'company_name')

    def get_uk_code(self):
        return self.year + self.month + self.company_name

class BaojianhuiYlxCompany(Lolly):
    link = models.URLField(null=False)
    title = models.CharField(max_length=200, null=False)
    year = models.CharField(max_length=20, null=False)
    month = models.CharField(max_length=20, null=False)
    company_name = models.CharField(max_length=100, null=False)
    created = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)

    shoutuo_jf = models.CharField(max_length=20, null=True)
    touzi_jf = models.CharField(max_length=20, null=True)
    weituo_jf = models.CharField(max_length=20, null=True)

    shoutuo_zc = models.CharField(max_length=20, null=True)
    touzi_zc = models.CharField(max_length=20, null=True)
    weituo_zc = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_ylx_company_annuity'
        unique_together = ('year', 'month', 'company_name')

    def get_uk_code(self):
        return self.year + self.month + self.company_name

class BaojianhuiRegionIncome(Lolly):
    link = models.URLField(null=False)
    title = models.CharField(max_length=200, null=False)
    year = models.CharField(max_length=20, null=False)
    month = models.CharField(max_length=20, null=False)
    region = models.CharField(max_length=100, null=False)
    created = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)

    amount = models.CharField(max_length=20, null=True)
    caichanxian = models.CharField(max_length=20, null=True)
    shouxian = models.CharField(max_length=20, null=True)
    yiwaixian = models.CharField(max_length=20, null=True)
    jiankangxian = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_ylx_region_income'
        unique_together = ('year', 'month', 'region')

    def get_uk_code(self):
        return self.year + self.month + self.region


class BaojianhuiRecordProduct(Lolly):
    product_type = models.CharField(max_length=20, null=False)
    company_name = models.CharField(max_length=100, null=False)
    company_code = models.CharField(max_length=100, null=False)
    company_link = models.URLField(null=False)
    product_name = models.CharField(max_length=100, null=False)
    record_date = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_record_product'
        unique_together = ('product_type', 'company_code', 'product_name')

    def get_uk_code(self):
        return self.product_type + self.company_code + self.product_name


class BaojianhuiCompany(Lolly):
    code = models.CharField(max_length=100, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    link = models.URLField(null=False)
    type = models.CharField(max_length=100, null=True)
    estab_date = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=100, null=True)
    principal = models.CharField(max_length=100, null=True)
    sw = models.CharField(max_length=100, null=True)
    register_address = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bjh_company'

    def get_uk_code(self):
        return self.company_code + self.company_name


class BaohangxieExposureCompany(Lolly):
    column_id = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=200, null=False)
    company_code = models.CharField(max_length=200, null=False)
    info_no = models.CharField(max_length=200, null=False)
    zj = models.CharField(max_length=200, null=False)
    name = models.CharField(max_length=200, null=False)
    detail_info = models.TextField(null=True)
    sub_company_list = models.TextField(null=True)
    cur_product_list = models.TextField(null=True)
    his_product_list = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bhx_exposure_company'
        unique_together = ('column_id', 'company_code', 'info_no', 'zj')

    def get_uk_code(self):
        return self.column_id + self.company_code + self.info_no


class BaohangxieCooperation(Lolly):
    company = models.ForeignKey(BaohangxieExposureCompany, on_delete=models.CASCADE)
    terrace_no = models.CharField(max_length=200, null=False)
    old_terrace_no = models.CharField(max_length=200, null=False)
    # 01 当前，00 历史
    flag = models.CharField(max_length=200, null=False)
    # 01 中介，02 第三方
    type = models.CharField(max_length=200, null=False)

    full_name = models.CharField(max_length=200, null=True)
    short_name = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=200, null=True)
    # 备案信息
    records = models.CharField(max_length=200, null=True)
    scope = models.CharField(max_length=200, null=True)
    start_date = models.CharField(max_length=200, null=True)
    end_date = models.CharField(max_length=200, null=True)

    cur_product_list = models.TextField(null=True)
    his_product_list = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bhx_cooperation'
        unique_together = ('terrace_no', 'old_terrace_no', 'flag', 'type')

    def get_uk_code(self):
        return self.terrace_no + self.old_terrace_no + self.type + self.com_type


class BaohangxieMember(Lolly):
    name = models.CharField(max_length=200, null=False, primary_key=True)
    link = models.URLField(null=False)
    website = models.URLField(null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)
    position = models.CharField(max_length=200, null=True)
    represent = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)
    date = models.CharField(max_length=200, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'bhx_member'

    def get_uk_code(self):
        return self.name


class BaohangxieProduct(Lolly):
    code = models.CharField(max_length=200, null=False, primary_key=True)
    link = models.URLField(null=False)
    company_name = models.CharField(max_length=200, null=False)
    product_name = models.CharField(max_length=200, null=False)
    product_type = models.CharField(max_length=200, null=True)
    design_type = models.CharField(max_length=200, null=True)
    feature = models.CharField(max_length=200, null=True)
    insured = models.CharField(max_length=200, null=True)
    period_type = models.CharField(max_length=200, null=True)
    pay_type = models.CharField(max_length=200, null=True)
    clause = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    end_date = models.CharField(max_length=200, null=True)
    pdf = models.URLField(null=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'bhx_product'

    def get_uk_code(self):
        return self.code
