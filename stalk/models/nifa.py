from django.db import models
from lolly import Lolly


class CompanyBaseInfo(Lolly):
    code = models.CharField(max_length=100, null=False, primary_key=True)
    link = models.URLField(null=False)

    short_name = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=100, null=True)

    registered_capital = models.CharField(max_length=100, null=True)
    zc_country = models.CharField(max_length=100, null=True)
    zc_province = models.CharField(max_length=100, null=True)
    zc_city = models.CharField(max_length=100, null=True)
    zc_address = models.CharField(max_length=100, null=True)
    zc_zip = models.CharField(max_length=100, null=True)

    estab_date = models.CharField(max_length=100, null=True)
    legal_person = models.CharField(max_length=100, null=True)
    scope = models.TextField(null=True)
    fax = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    jy_country = models.CharField(max_length=100, null=True)
    jy_province = models.CharField(max_length=100, null=True)
    jy_city = models.CharField(max_length=100, null=True)
    jy_address = models.CharField(max_length=100, null=True)

    paidin_capital = models.CharField(max_length=100, null=True)

    fund_bank = models.CharField(max_length=100, null=True)
    fund_info = models.CharField(max_length=100, null=True)

    agreement_pdf = models.CharField(max_length=200, null=True)

    partner_list = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'nifa_company_base_info'

    def get_uk_code(self):
        return self.company_code + self.short_name


class CompanyGovernInfo(Lolly):
    code = models.CharField(max_length=100, null=False, primary_key=True)
    link = models.URLField(null=False)
    name = models.CharField(max_length=100, null=True)

    structure = models.CharField(max_length=100, null=True)
    relation = models.TextField(null=True)
    controller = models.TextField(null=True)
    shareholder_list = models.TextField(null=True)
    manager_list = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'nifa_company_govern_info'

    def get_uk_code(self):
        return self.company_code + self.name

class CompanySiteInfo(Lolly):
    code = models.CharField(max_length=100, null=False, primary_key=True)
    link = models.URLField(null=False)
    website = models.CharField(max_length=100, null=True)
    short_name = models.CharField(max_length=100, null=True)
    online_time = models.CharField(max_length=100, null=True)
    license = models.TextField(null=True)
    app = models.CharField(max_length=100, null=True)
    wechat = models.CharField(max_length=100, null=True)
    certification = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'nifa_company_site_info'

    def get_uk_code(self):
        return self.company_code + self.name

class CompanyFinanceInfo(Lolly):
    code = models.CharField(max_length=100, null=False, primary_key=True)
    link = models.URLField(null=False)
    name = models.CharField(max_length=100, null=True)
    finance_list = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'nifa_company_finance_info'

    def get_uk_code(self):
        return self.company_code + self.name

class CompanyTradeLog(Lolly):
    code = models.CharField(max_length=100, null=False)
    link = models.URLField(null=False)
    name = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=False)

    # trade_amount = models.CharField(max_length=100, null=False)
    # trade_cnt = models.CharField(max_length=100, null=False)
    # invest_cnt = models.CharField(max_length=100, null=False)
    # financier_cnt = models.CharField(max_length=100, null=False)
    # investor_cnt = models.CharField(max_length=100, null=False)
    # repay_amount = models.CharField(max_length=100, null=False)
    # project_overdue_amount = models.CharField(max_length=100, null=False)
    # amount_overdue_rate = models.CharField(max_length=100, null=False)
    # overdue_cnt = models.CharField(max_length=100, null=False)
    #
    # finance_amount_avg = models.CharField(max_length=100, null=False)
    # invest_amount_avg = models.CharField(max_length=100, null=False)

    log = models.TextField(null=True)


    class Meta:
        app_label = 'stalk'
        db_table = 'nifa_company_trade_log'
        unique_together = ('code', 'date')


    def get_uk_code(self):
        return self.company_code + self.name + self.date

