# coding: utf-8
import time
import json
import random
import requests
import logging
import datetime
import fake_useragent
from Utils import common
from Models import dropdown_words
from sqlalchemy import and_, distinct
from Config.api_config import amz_dropdown_host, amz_dropdown_interface, amz_marketplace


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/amz_dropdown_words/{}.log'.format(datetime.date.today())
log = logging.getLogger()
log.setLevel(logging.INFO)

fh = logging.FileHandler(file_name, mode='a+')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)


class AmzDropdownList:

    def get_url(self, ct, search_key):
        host = amz_dropdown_host.get(ct)
        mid = amz_marketplace.get(ct)
        api = amz_dropdown_interface.format(marketplace=mid, prefix=search_key)
        url = host + api
        return url

    def get_words(self, ct, url):
        headers = {
            'user_agent': fake_useragent.UserAgent().random,
            'referer': amz_dropdown_host.get(ct)
        }
        proxies = {
            'http': 'http://{}'.format(common.RedisClient().random())
        }
        words_resp = json.loads(requests.get(url, headers=headers, proxies=proxies).text)
        words_list = []
        for words in words_resp.get('suggestions'):
            words_list.append(words.get('value'))
        return words_list

    def get_words_loop(self, ct, cate, s_date, search_key):
        word_url = self.get_url(ct, search_key)
        word_list = self.get_words(ct, word_url)
        if search_key in word_list:
            word_list.remove(search_key)
        db_pwords = self.get_parent_words(ct, cate, s_date)
        if word_list and (len(search_key) < 100) and (search_key not in db_pwords):
            g_words = self.group_words(search_key, word_list)
            if g_words:
                log.info('Add to sql: %s' % g_words)
                self.add_dropdown_words(ct, category, snap_date, g_words)

            for word in word_list:
                if (word.upper() == search_key.upper()) or not self.get_words_loop(ct, cate, s_date, word):
                    continue
                time.sleep(random.choice(range(3, 6)))

    def group_words(self, search_key, words):
        words_list = []
        words_count = len(words)
        for i in range(words_count):
            if (len(words[i]) < 100) and (search_key.upper() != words[i].upper()):
                words_list.append({
                    'PKeyword': search_key,
                    'CKeyword': words[i],
                    'CKeywordRank': i + 1
                })
        return words_list


    # 数据库方法
    def get_parent_words(self, ct, cate, s_date):
        session = dropdown_words.DBSession()
        try:
            parent_words = session.query(distinct(dropdown_words.ApbSpKeywordsRelation.PKeyword)).filter(
                                         and_(and_(dropdown_words.ApbSpKeywordsRelation.Country == ct,
                                                   dropdown_words.ApbSpKeywordsRelation.Category == cate),
                                                   dropdown_words.ApbSpKeywordsRelation.SnapDate == s_date)).all()
            return [word[0] for word in parent_words]
        except Exception as e:
            log.error('Get parent words error: %s' % e)

    def add_dropdown_words(self, ct, cate, s_date, datas):
        session = dropdown_words.DBSession()
        try:
            for data in datas:
                keywords_db = dropdown_words.ApbSpKeywordsRelation(ct, cate, s_date, data)
                session.add(keywords_db)
            session.commit()
        except Exception as e:
            log.error('Add dropdown words to sql error: %s' % e)






if __name__ == '__main__':

    cts = ['DE', 'JP']
    search_word_dict = {
        'UK': ['Cable', ['iphone charger', 'iphone cable', 'ipad charger', 'ipad cable', 'lightning cable', 'lightning charger', 'apple charger', 'charger apple', 'iphone cord', '6ft iphone charger', 'braided lightning cable', 'iphone charging cable', 'iphone charging cord', 'apple charging cord', 'long iphone charger', 'iphone power cord', 'ipad charge cord', 'usb apple cable', 'apple iphone charger', 'ipad charging cable', 'apple charging cable', 'ipad charger cable', 'apple cable', 'lightning cord', 'apple cord']],
        'DE': ['Kabel', ['iphone Kabel', 'iphone Ladekabel', 'iphone ladegerät', 'Lightning Ladekabel', 'Lightning Kabel', 'lightning ladegerät', 'apple ladekabel', 'apple ladegerät', 'apple kabel', 'iphone Kabel 3m', 'iphone Ladekabel 3m', 'iphone Kabel 1.8m', 'iphone Ladekabel 1.8m', 'mfi lightning kabel', 'iphone kabel lang', 'lightning kabel lang', 'iphone Ladekabel lang', 'Lightning Ladekabel lang', 'iphone cable', 'lightning cable', 'apple cable', 'apple lightning kabel', 'apple datenkabel', 'apple usb kabel', 'iphone datenkabel', 'ipad ladekabel', 'ipad ladekabel lang', 'ipad cable', 'ipad kabel']],
        'JP': ['充電ケーブル', ['充電ケーブル', 'ライトニングケーブル', 'iphone 充電ケーブル', 'iphone ライトニングケーブル', 'usbケーブル', 'usbケーブル iphone', 'ライトニングUSBケーブル']]
    }
    snap_date = datetime.datetime.now().date()

    for ct in cts:
        category = search_word_dict.get(ct)[0]
        search_words = search_word_dict.get(ct)[1]

        log.info('Amz dropdown words crawls starting... ')
        log.info('Country: %s, Category: %s, Count_words: %s' % (ct, category, len(search_words)))
        amz_dropdown = AmzDropdownList()
        for search_word in search_words:
            log.info('---------%s---------' % search_word)
            try:
                amz_dropdown.get_words_loop(ct, category, snap_date, search_word)
            except Exception as e:
                log.error('Error: %s' % e)
        log.info('Amz dropdown words crawls end! ')