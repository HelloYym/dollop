# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly


class DailuopanDailyData(Lolly):
    thread = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    link = models.URLField(null=False)
    date = models.CharField(max_length=20, null=False)

    amount = models.CharField(max_length=50, null=True)
    inamount = models.CharField(max_length=50, null=True)
    stay_still_day = models.CharField(max_length=50, null=True)
    stay_still_total = models.CharField(max_length=50, null=True)
    invest_amount_avg = models.CharField(max_length=50, null=True)
    borrow_amount_avg = models.CharField(max_length=50, null=True)

    invest_num_day = models.CharField(max_length=50, null=True)
    borrow_num_day = models.CharField(max_length=50, null=True)
    invest_num_stay = models.CharField(max_length=50, null=True)
    borrow_num_stay = models.CharField(max_length=50, null=True)

    top10_investor_prop = models.CharField(max_length=50, null=True)
    top10_borrower_prop = models.CharField(max_length=50, null=True)

    rate = models.CharField(max_length=50, null=True)
    loan_period = models.CharField(max_length=50, null=True)
    full_loan_time = models.CharField(max_length=50, null=True)
    total_loan_num = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'dailuopan_daily_data'
        unique_together = ('thread', 'date')

    def get_uk_code(self):
        return self.thread + self.date


class DailuopanInvestor(Lolly):
    thread = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    link = models.URLField(null=False)
    date = models.CharField(max_length=20, null=False)

    age_distribution = models.CharField(max_length=100, null=True)
    sex_distribution = models.CharField(max_length=100, null=True)
    tag_list = models.CharField(max_length=500, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'dailuopan_investor'
        unique_together = ('thread', 'date')

    def get_uk_code(self):
        return self.thread + self.date


class DailuopanHonor(Lolly):
    thread = models.CharField(max_length=50, null=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    link = models.URLField(null=False)

    honor_list = models.CharField(max_length=500, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'dailuopan_honor'

    def get_uk_code(self):
        return self.thread


class DailuopanRate(Lolly):
    thread = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    link = models.URLField(null=False)
    date = models.CharField(max_length=20, null=False)

    institution = models.CharField(max_length=100, null=False)
    rate = models.CharField(max_length=20, null=False)
    unit = models.CharField(max_length=10, null=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'dailuopan_rate'
        unique_together = ('thread', 'date', 'institution')

    def get_uk_code(self):
        return self.thread + self.date + self.institution


class DailuopanFlow(Lolly):
    thread = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    link = models.URLField(null=False)
    date = models.CharField(max_length=20, null=False)
    institution = models.CharField(max_length=100, null=False)
    flow = models.CharField(max_length=20, null=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'dailuopan_flow'
        unique_together = ('thread', 'date', 'institution')

    def get_uk_code(self):
        return self.thread + self.date + self.institution


class DailuopanReport(Lolly):
    thread = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=100, null=False)
    link = models.URLField(null=False)
    category = models.CharField(max_length=50, null=False)

    created = models.CharField(max_length=50, null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)
    img_grabber_executed = models.BooleanField(default=False)

    class Meta:
        app_label = 'stalk'
        db_table = 'dailuopan_report'
        unique_together = ('thread', 'category')

    def get_uk_code(self):
        return self.thread + self.category
