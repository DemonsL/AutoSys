# coding: utf-8
import sys
sys.path.append('../')
import time
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from Utils.common import RedisClient


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/fb_logs/{}.log'.format(datetime.date.today())
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

class FbPages:

    def get_link(self, so):
        link_list = so.find_all('a', attrs={'class', '_6x0d'})
        for link in link_list:
            yield link.attrs.get('href'), link.text

    def get_likes(self, so):
        likes = ''
        try:
            likes = so.find('span', attrs={'id': 'PagesLikesCountDOMID'}).text.split(' ')[0].replace(',', '')
        except Exception as e:
            log.error('GetLikesError: %s' % e)
        return likes

    def get_site(self, so):
        site = ''
        try:
            site = so.find('img', attrs={'src': 'https://static.xx.fbcdn.net/rsrc.php/v3/yV/r/EaDvTjOwxIV.png'}) \
                     .parent.parent.text
        except Exception as e:
            log.error('GetSiteError: %s' % e)
        return site

    def get_terms(self, so):
        terms = ''
        try:
            terms = so.find('div', attrs={'class': '_4bl9 _5m_o'}).text
        except Exception as e:
            log.error('GetTermsError: %s' % e)
        return terms







if __name__ == '__main__':

    url = 'https://www.facebook.com/pages/category/topic-shopping-retail/?page={}'
    headers = {
        'referer': 'https://www.facebook.com/pages/category/topic-shopping-retail/',
        'accept-language': 'en-us'
    }

    ua = UserAgent()
    fp = FbPages()
    rc = RedisClient()
    for i in range(477, 3000):
        log.info(url.format(i + 1))
        with open('../fp_csv.csv', 'a', encoding='utf-8') as f:
            f.write(url.format(i + 1) + '\n')
        user_agent = {
            'user_agent': ua.random
        }
        proxies = {
            'http': 'http://{}'.format(rc.random())
        }
        resp = requests.get(url.format(i + 1), headers=headers.update(user_agent), proxies=proxies)
        soup = BeautifulSoup(resp.text, 'lxml')
        hidden_elem = soup.find('div', attrs={'class': 'hidden_elem'}).string
        # fb网页被注释，需要再次解析
        sub_soup = BeautifulSoup(hidden_elem, 'lxml')
        pg_links = list(fp.get_link(sub_soup))
        # 解析详情页面
        for pg_link, pg_name in pg_links:
            pg_resp = requests.get(pg_link, headers=headers, proxies=proxies)
            pg_soup = BeautifulSoup(pg_resp.text, 'lxml')
            pg_likes = fp.get_likes(pg_soup)
            # 解析About页面
            time.sleep(5)
            pgab_resp = requests.get(pg_link + 'about/?ref=page_internal', headers=headers, proxies=proxies)
            pgab_soup = BeautifulSoup(pgab_resp.text, 'lxml')
            pgab_terms = fp.get_terms(pgab_soup)
            pgab_site = fp.get_site(pgab_soup)
            pg_re = (pg_link, pg_name, pg_likes, pgab_terms, pgab_site)
            log.info(pg_re)
            # 写入文件
            with open('../fp_csv.csv', 'a', encoding='utf-8') as f:
                f.write(str(pg_re) + '\n')
            time.sleep(5)

