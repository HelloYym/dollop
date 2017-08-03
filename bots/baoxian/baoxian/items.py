# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from bots.base.items import BaseItem
from stalk.models import baoxian


class ReportItem(BaseItem):
    django_model = baoxian.BaojianhuiReport
    update_fields_list = ['link', 'title', 'created', 'content', 'raw_content', 'image_url']
    unique_key = ('id',)


class JingyingItem(BaseItem):
    django_model = baoxian.BaojianhuiJingying
    update_fields_list = ['link', 'title', 'created', 'data', 'content', 'raw_content', 'image_url', 'year', 'month',
                          'income', 'baohu_xz', 'duli_xz', 'expense', 'manage_fee', 'bank_deposits', 'invest', 'amount',
                          'yanglao_cost',
                          'yanglao_shoutuo', 'yanglao_touzi', 'caichanxian1', 'renshenxian1', 'shouxian1',
                          'jiankangxian1', 'yiwaixian1',
                          'caichanxian2', 'renshenxian2', 'shouxian2', 'jiankangxian2', 'yiwaixian2'
                          ]
    unique_key = ('id',)


class CaichanxianItem(BaseItem):
    django_model = baoxian.BaojianhuiCcxCompany
    update_fields_list = ['link', 'title', 'created', 'income', 'capital_structure', 'content', 'share']
    unique_key = ('year', 'month', 'company_name')


class RenshenxianItem(BaseItem):
    django_model = baoxian.BaojianhuiRsxCompany
    update_fields_list = ['link', 'title', 'created', 'income', 'capital_structure', 'content', 'baohu_xz', 'duli_xz',
                          'share']
    unique_key = ('year', 'month', 'company_name')


class YanglaoxianItem(BaseItem):
    django_model = baoxian.BaojianhuiYlxCompany

    update_fields_list = ['link', 'title', 'created', 'content', 'shoutuo_jf', 'touzi_jf', 'weituo_jf',
                          'shoutuo_zc', 'touzi_zc', 'weituo_zc']
    unique_key = ('year', 'month', 'company_name')


class RegionItem(BaseItem):
    django_model = baoxian.BaojianhuiRegionIncome
    update_fields_list = ['link', 'title', 'created', 'content', 'amount', 'caichanxian', 'shouxian', 'yiwaixian', 'jiankangxian']
    unique_key = ('year', 'month', 'region')


class RecordProductItem(BaseItem):
    django_model = baoxian.BaojianhuiRecordProduct
    update_fields_list = ['company_name', 'company_link', 'record_date', 'type']
    unique_key = ('product_type', 'company_code', 'product_name')


class CompanyItem(BaseItem):
    django_model = baoxian.BaojianhuiCompany
    update_fields_list = ['name', 'link', 'type', 'estab_date', 'address', 'phone', 'principal', 'sw',
                          'register_address', 'state']
    unique_key = ('code',)


class ExposureCompanyItem(BaseItem):
    django_model = baoxian.BaohangxieExposureCompany
    update_fields_list = ['name', 'detail_info', 'type', 'sub_company_list', 'cur_product_list', 'his_product_list']
    unique_key = ('column_id', 'company_code', 'info_no', 'zj')

    @classmethod
    def get_company(cls, column_id, company_code, info_no):
        try:
            obj = cls.django_model.objects.get(column_id=column_id, company_code=company_code, info_no=info_no)
        except:
            return None
        return obj


class CooperationItem(BaseItem):
    django_model = baoxian.BaohangxieCooperation
    update_fields_list = ['full_name', 'short_name', 'website', 'records', 'scope', 'start_date', 'end_date',
                          'cur_product_list', 'his_product_list']
    unique_key = ('terrace_no', 'old_terrace_no', 'flag', 'type')


class MemberItem(BaseItem):
    django_model = baoxian.BaohangxieMember
    update_fields_list = ['link', 'website', 'phone', 'address', 'zip', 'position', 'represent',
                          'type', 'date']
    unique_key = ('name',)

    @classmethod
    def get_member(cls, name):
        try:
            obj = cls.django_model.objects.get(name=name)
        except:
            return None
        return obj


class ProductItem(BaseItem):
    django_model = baoxian.BaohangxieProduct
    update_fields_list = ['link', 'company_name', 'product_name', 'product_type', 'design_type', 'feature', 'insured',
                          'period_type', 'pay_type', 'clause', 'state', 'end_date', 'pdf']
    unique_key = ('code',)
