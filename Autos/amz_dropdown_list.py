# coding: utf-8
import sys
sys.path.append('../')
import time
import json
import random
import requests
import logging
import datetime
import fake_useragent
from Common.common import RedisClient
from Models import dropdown_words
from sqlalchemy import and_, distinct
from Config.api_config import amz_dropdown_host, amz_dropdown_interface, amz_marketplace


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/amz_dropdown_list/{}.log'.format(datetime.date.today())
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
            'http': 'http://{}'.format(RedisClient().random())
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
                self.add_dropdown_words(ct, cate, snap_date, g_words)

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

    def get_search_words(self):
        session = dropdown_words.DBSession()
        try:
            search_words = session.query(dropdown_words.ApbSpKeyword.Country,
                                         dropdown_words.ApbSpKeyword.Category,
                                         dropdown_words.ApbSpKeyword.Keyword) \
                                  .order_by(dropdown_words.ApbSpKeyword.Country).all()
            return search_words
        except Exception as e:
            log.error('Get search word error: %s' % e)

    def add_words_to_sql(self, ct, cate, words):
        session = dropdown_words.DBSession()
        try:
            for word in words:
                word_db = dropdown_words.ApbSpKeyword(ct, cate, word)
                session.add(word_db)
            session.commit()
        except Exception as e:
            log.error('Add search words error: %s' % e)






if __name__ == '__main__':

    snap_date = datetime.datetime.now().date()

    log.info('Amz dropdown words crawls starting... ')
    amz_dropdown = AmzDropdownList()
    search_word_list = amz_dropdown.get_search_words()
    for search_word in search_word_list:
        log.info('Country: %s, Category: %s, Count_words: %s' % (search_word[0], search_word[1], len(search_word_list)))
        log.info('---------%s---------' % str(search_word))
        try:
            amz_dropdown.get_words_loop(search_word[0], search_word[1], snap_date, search_word[2])
        except Exception as e:
            log.error('Error: %s' % e)
    log.info('Amz dropdown words crawls end! ')