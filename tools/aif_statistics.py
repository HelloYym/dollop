# -*- coding: utf-8 -*-
from bots import setup_django_env
setup_django_env()

import numpy as np
import xlwt
from stalk.models.aif import Basic, Daily, MonthlyBasic

map = {
        'thityday_income': True,
        'daily_invest_cnt': True,
        'daily_turnover': True,
        'daily_trade_cnt': True,
        'service_time': True,

        'trade_amount': False,
        'different_borrower_amount': False,
        'loan_overdue_rate': True,
        'borrower_amount': False,
        'different_investor_amount': False,
        'turnover_amount': False,
        'compensatory_amount': False, #
        'overdue_loan_amount': False, #
        'loan_balance': False, #
        'product_overdue_rate': True,
        'investor_amount': False,
        'avg_full_time': True,
        'unconventional_turnover_amount': False,

        'avg_interest_rate': True,
        'avg_loan_per_trade': True,
        'avg_borrow_period': True,
        'topten_borrowers_ratio': True,
        'max_borrower_ratio': True,
        'overdue_project_amount': False, #
        'loan_amount_per_capita': True,
        'avg_invest_per_trade': True,
        'invest_amount_per_capita': True
    }

ratio = ('loan_overdue_rate', 'product_overdue_rate', 'avg_interest_rate',
         'topten_borrowers_ratio', 'max_borrower_ratio')

plat = {'21097': u'微贷网',
        '22456': u'浙金网',
        '23096': u'鑫合汇',
        '89234': u'中网国投',
        '89390': u'点点搜财',
        '89391': u'华赢贷',
        '89393': u'佐助金服',
        '89394': u'铜板街'}


def get_field_list(model, field):
    values = model.objects.values_list(field)
    data = []
    blank_num = 0
    for value in values:
        value = value[0]
        if value is None or value == '0' or value == '':
            blank_num += 1
        else:
            value = float(value)
            if field in ratio:
                if value > 1.0:
                    value /= 100
                    if value > 1.0:
                        blank_num += 1
                        continue
            data.append(value)
    return data, float(len(values)-blank_num)/len(values)


def get_field_difference_value_list(model, field):
    all_data = []
    all_blank_num = 0
    all_num = 0
    except_plat = []
    max_value = 0
    for plat_id in plat.keys():
        values = model.objects.filter(plat_id=plat_id).order_by('date').values_list(field, 'date')
        data = []
        blank_num = 0
        for val in values:
            value = val[0]
            if value is None or value == '0' or value == '':
                blank_num += 1
            else:
                data.append([float(value), val[1]])
        index = len(data)-1
        step = 1
        while index > -1:
            if data[index][0] >= data[index-step][0]:
                if data[index][0]-data[index-step][0] > max_value:
                    platform = plat_id
                    day1 = data[index][1]
                    day2 = data[index-step][1]
                    max_value = data[index][0]-data[index-step][0]
                all_data.append(data[index][0]-data[index-step][0])
                index -= step
                step = 1
            else:
                except_plat.append((plat.get(plat_id), field, data[index][1], data[index][0], data[index-step][1], data[index-step][0], data[index][0]-data[index-step][0]))
                step += 1
        all_blank_num += blank_num
        all_num += len(values)
    return all_data, float(len(all_data))/all_num, except_plat


def calculation(model, field, flag):
    exceptions = []
    if flag:
        data, covarage = get_field_list(model, field)
    else:
        data, covarage, exceptions = get_field_difference_value_list(model, field)
    data = np.array(data)
    max = data.max()
    min = data.min()
    mean = data.mean()
    var = data.var()
    return field, covarage, max, min, mean, var, exceptions


def calculate_all(model):
    attributes = model._meta.get_all_field_names()
    all_exceptions = []
    result = []
    for attr in attributes:
        if map.has_key(attr):
            field, covarage, max, min, mean, var, exceptions = calculation(model, attr, map.get(attr))
            result.append((field, covarage, max, min, mean, var))
            all_exceptions += exceptions
    return result, all_exceptions


def generate_excel(filename, sheetname, data):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(sheetname)

    for i, l in enumerate(data):
        for j, col in enumerate(l):
            ws.write(i, j, col)

    wb.save(filename)

if __name__ == '__main__':
    get_field_difference_value_list(Basic, 'turnover_amount')
