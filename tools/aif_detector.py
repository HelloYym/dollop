from bots import setup_django_env
setup_django_env()

from stalk.models.aif import Basic, Daily
from utils.my_datetime import get_date_list
import datetime
import requests
import json
import time


class AIFDetector(object):
    def __init__(self, cur_date=None, model=Daily, gap=0):
        self.cur_date = cur_date if cur_date else datetime.date.today() - datetime.timedelta(days=2)
        self.model = model
        self.gap = gap
        self.scrapyd_server, self.login, self.daily, self.basic = self.get_aif_config()
        self.distinct_plat_id = self.get_distinct_plat_id()

    @staticmethod
    def load_aif_config():
        with open('aif_config.json') as json_file:
            data = json.load(json_file)
            return data

    def get_aif_config(self):
        conf = self.load_aif_config()
        scrapyd_server = conf['post_url']
        login = {}
        for ele in conf['login']:
            login[ele['plat_id']] = ele['post_data']
        daily = {}
        for ele in conf['daily']:
            daily[ele['plat_id']] = ele['post_data']
        basic = {}
        for ele in conf['basic']:
            basic[ele['plat_id']] = ele['post_data']
        return scrapyd_server, login, daily, basic

    def get_distinct_plat_id(self):
        plat_ids = self.model.objects.values_list('plat_id').distinct()
        return [pid[0] for pid in plat_ids]

    def detect_missing_data(self):
        from_date = self.cur_date - datetime.timedelta(days=self.gap)
        from_date = from_date.strftime("%Y-%m-%d")
        to_date = self.cur_date.strftime("%Y-%m-%d")
        missing_data = []
        for date in get_date_list(from_date, to_date, delimiter='-'):
            for pid in self.distinct_plat_id:
                result = self.model.objects.filter(plat_id=pid).filter(date=date)
                if not result:
                    missing_data.append((pid, date))

        return missing_data

    def get_all_missing_data(self):
        missing_data = self.detect_missing_data()
        missing_plat = set([ele[0] for ele in missing_data])

        for plat_id in missing_plat:
            if plat_id in self.login.keys():
                requests.post(self.scrapyd_server, self.login[plat_id])
                time.sleep(10)
            from_date = self.cur_date - datetime.timedelta(days=self.gap)
            from_date = from_date.strftime("%Y%m%d")
            to_date = self.cur_date.strftime("%Y%m%d")
            if self.model == Daily:
                post_data = self.daily[plat_id]
                post_data['from_date'] = from_date
                post_data['to_date'] = to_date
                requests.post(self.scrapyd_server, post_data)
                time.sleep(20)
            if self.model == Basic:
                post_data = self.basic[plat_id]
                post_data['from_date'] = from_date
                post_data['to_date'] = to_date
                requests.post(self.scrapyd_server, post_data)
                time.sleep(120)

    def get_missing_data(self):
        missing_data = self.detect_missing_data()

        already_login = set()
        for ele in missing_data:
            plat_id = ele[0]
            if plat_id in self.login.keys() and plat_id not in already_login:
                requests.post(self.scrapyd_server, self.login[plat_id])
                already_login.add(plat_id)

        for ele in missing_data:
            plat_id = ele[0]
            missing_date = ele[1].replace('-', '')
            if self.model == Daily:
                post_data = self.daily[plat_id]
            else:
                post_data = self.basic[plat_id]
            post_data['from_date'] = missing_date
            post_data['to_date'] = missing_date
            requests.post(self.scrapyd_server, post_data)

if __name__ == '__main__':
    aif_daily_detector = AIFDetector(gap=10)
    aif_daily_detector.get_all_missing_data()
    time.sleep(60)
    aif_daily_detector = AIFDetector(model=Basic, gap=10)
    aif_daily_detector.get_all_missing_data()
    '''
    aif_daily_detector.get_missing_data()
    time.sleep(120)
    aif_basic_detector = AIFDetector(model=Basic, gap=10)
    aif_basic_detector.get_missing_data()
    '''


