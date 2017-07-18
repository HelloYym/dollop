# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import aif


class JibenItem(BaseItem):
    django_model = aif.Basic
    update_fields_list = ['plat_id', 'date', 'turnover_amount', 'trade_amount', 'borrower_amount',           \
                          'investor_amount', 'unconventional_turnover_amount', 'different_borrower_amount',  \
                          'different_investor_amount', 'loan_balance', 'product_overdue_rate',               \
                          'overdue_loan_amount', 'avg_full_time', 'compensatory_amount', 'loan_overdue_rate']
    unique_key = ('plat_id', 'date')

class MeiriItem(BaseItem):
    django_model = aif.Daily
    update_fields_list = ['plat_id', 'date', 'daily_turnover', 'daily_trade_cnt', 'daily_invest_cnt',        \
                          'thityday_income', 'service_time']
    unique_key = ('plat_id', 'date')

class MeiyueItem(BaseItem):
    django_model = aif.MonthlyBasic
    update_fields_list = ['plat_id', 'date', 'loan_amount_per_capita', 'avg_loan_per_trade',                 \
                          'invest_amount_per_capita', 'avg_invest_per_trade', 'max_borrower_ratio',          \
                          'topten_borrowers_ratio', 'overdue_project_amount', 'avg_interest_rate',           \
                          'avg_borrow_period']
    unique_key = ('plat_id', 'date')
