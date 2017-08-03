# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import nifa


class BaseInfoItem(BaseItem):
    django_model = nifa.CompanyBaseInfo
    update_fields_list = ['link', 'short_name', 'full_name', 'registered_capital', 'zc_country', 'zc_province',
                          'zc_city', 'zc_address', 'zc_zip', 'estab_date', 'legal_person', 'scope', 'fax', 'phone',
                          'email', 'jy_country', 'jy_province', 'jy_city', 'jy_address', 'paidin_capital', 'fund_bank',
                          'fund_info', 'agreement_pdf', 'partner_list']
    unique_key = ('code',)


class GovernInfoItem(BaseItem):
    django_model = nifa.CompanyGovernInfo

    update_fields_list = ['link', 'name', 'structure', 'relation', 'controller', 'shareholder_list',
                          'manager_list']
    unique_key = ('code',)


class SiteInfoItem(BaseItem):
    django_model = nifa.CompanySiteInfo
    update_fields_list = ['link', 'website', 'short_name', 'online_time', 'license',
                          'app', 'wechat', 'certification']
    unique_key = ('code',)


class FinanceInfoItem(BaseItem):
    django_model = nifa.CompanyFinanceInfo
    update_fields_list = ['link', 'name', 'finance_list']
    unique_key = ('code',)


class TradeLogItem(BaseItem):
    django_model = nifa.CompanyTradeLog
    update_fields_list = ['link', 'name', 'log']
    unique_key = ('code', 'date')
