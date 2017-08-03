# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import dailuopan


class DailyDataItem(BaseItem):
    django_model = dailuopan.DailuopanDailyData

    update_fields_list = ['name', 'link', 'turnover', 'inamount', 'stay_still_day', 'stay_still_total',
                          'invest_amount_avg', 'borrow_amount_avg', 'invest_num_day', 'borrow_num_day',
                          'invest_num_stay', 'borrow_num_stay',
                          'top10_investor_prop', 'top10_borrower_prop', 'rate', 'loan_period', 'full_loan_time',
                          'total_loan_num']

    unique_key = ('thread', 'date')


class InvestorItem(BaseItem):
    django_model = dailuopan.DailuopanInvestor
    update_fields_list = ['name', 'link', 'age_distribution', 'sex_distribution', 'tag_list']

    unique_key = ('thread', 'date')


class HonorItem(BaseItem):
    django_model = dailuopan.DailuopanHonor
    update_fields_list = ['name', 'link', 'honor_list']
    unique_key = ('thread',)


class RateItem(BaseItem):
    django_model = dailuopan.DailuopanRate
    update_fields_list = ['name', 'link', 'rate', 'unit']
    unique_key = ('thread', 'date', 'institution')


class FlowItem(BaseItem):
    django_model = dailuopan.DailuopanFlow
    update_fields_list = ['name', 'link', 'flow']
    unique_key = ('thread', 'date', 'institution')


class ReportItem(BaseItem):
    django_model = dailuopan.DailuopanReport
    update_fields_list = ['title', 'link', 'created', 'content', 'raw_content', 'image_url', 'img_grabber_executed']
    unique_key = ('thread', 'category')
