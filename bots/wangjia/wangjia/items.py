# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem, ProvinceItem
from stalk.models import wangjia

class DaohangItem(BaseItem):
    django_model = wangjia.Navigation
    update_fields_list = ['allPin', 'name', 'link', 'province_id', 'launch_time', 'icon_url', 'plat_id']
    unique_key = ('pin',)

class WentiItem(BaseItem):
    django_model = wangjia.Problem
    update_fields_list = ['problem_time', 'event_category']
    unique_key = ('name',)

class PingjiItem(BaseItem):
    django_model = wangjia.Rating
    update_fields_list = ['name', 'timestamp', 'exponent', 'launch_time', 'location', 'deal', 'popularity',  \
                          'lever', 'dispersity','mobility','transparency']
    unique_key = ('name', 'timestamp')

class ShujuItem(BaseItem):
    django_model = wangjia.Data
    #  0 成交量
    #  1 投资人数
    #  2 借款人数
    #  3 平均利率
    #  4 平均借款期限
    #  5 借款标数
    #  6 注册资金
    #  7 满标用时
    #  8 累计待还金额
    #  9 近30日资金净流入
    # 10 时间加权成交量
    # 11 未来60日待还
    # 12 前十大土豪待收金额占比
    # 13 人均投资金额
    # 14 前十大借款人待还金额占比
    # 15 人均借款金额
    # 16 资金杠杆
    # 17 运营时间
    update_fields_list = ['name', 'timestamp', 'volume', 'investment_passenger', 'loan_passenger',           \
                          'average_interest_rate', 'average_loan_period', 'loan_bid', 'registered_capital',  \
                          'time_for_full_bid', 'accounted_revenue', 'capital_inflow_in_30_days',             \
                          'volumn_weighted_time', 'accounted_revenue_in_60_days',                            \
                          'proportion_of_top_10_tuhao_accounted_revenue', 'average_investment_amount',       \
                          'proportion_of_top_10_borrower_accounted_revenue', 'average_loan_amount',          \
                          'capital_lever', 'operation_time']
    unique_key = ('name', 'timestamp')

class BaoguangItem(BaseItem):
    django_model = wangjia.Exposure
    update_fields_list = ['source', 'title', 'created', 'name', 'link', 'reason', 'content', 'raw_content',  \
                          'image_url']
    unique_key = ('thread',)

class XinwenItem(BaseItem):
    django_model = wangjia.News
    update_field_list = ['thread', 'category', 'source', 'title', 'created', 'author', 'summary',         \
                         'content', 'raw_content', 'image_url']
    unique_key = ('thread', 'category')

class DanganItem(BaseItem):
    django_model = wangjia.Archive
    update_fields_list = ['product_name', 'product_state', 'launch_time', 'province', 'city',
                          'introduction', 'web_url', 'logo_url', 'company_name', 'artificial_person',
                          'company_type', 'registered_capital', 'contributed_capital', 'registered_address', 'opening_date',
                          'approved_date', 'registration_authority', 'business_licence', 'institutional_framework', 'tax_registration_num',
                          'domain_name', 'domain_date', 'domain_company_type', 'domain_company_name', 'ICP_number',
                          'ICP_approval_number', 'account_fee', 'cash_fee', 'fueling_fee', 'transfer_fee',
                          'vip_fee', 'contact_address', 'phone_400', 'phone', 'email',
                          'fax', 'trust_funds', 'financing_record', 'regulatory_association', 'automatic_bid',
                          'equitable_assignment', 'tender_security', 'security_mode', 'emergency_funds', 'stock_market_status',
                          'guarantee_institutions', 'ownership_structure', 'business_scope',]
    unique_key = ('pin',)

class BusinessmanItem(BaseItem):
    django_model = wangjia.Businessman
    update_fields_list = ['product_name', 'image_url', 'introduction']
    unique_key = ('pin', 'name', 'post')