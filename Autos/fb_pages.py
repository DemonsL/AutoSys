# coding: utf-8
import sys
sys.path.append('../')
import time
import datetime
import logging
import random
import requests
from bs4 import BeautifulSoup


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
        return so.find('span', attrs={'id': 'PagesLikesCountDOMID'}).text.split(' ')[0].replace(',', '')


    def get_terms(self, so):
        return so.find('div', attrs={'class': '_4bl9 _5m_o'}).text







if __name__ == '__main__':

    url = 'https://www.facebook.com/pages/category/topic-shopping-retail/?page={}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'referer': 'https://www.facebook.com/pages/category/topic-shopping-retail/',
        'accept-language': 'en-us'
    }
    ip_ports = [
        '121.40.199.105:80',
        '121.42.163.161:80',
        '116.199.2.196:80',
        '114.116.75.60:60562',
        '119.3.37.101:36194',
        '106.52.68.116:25417'
    ]

    fp = FbPages()
    for i in range(7, 3000):
        log.info(url.format(i + 1))
        proxies = {
            'http': 'http://{}'.format(random.choice(ip_ports))
        }
        resp = requests.get(url.format(i + 1), headers=headers, proxies=proxies)
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
            time.sleep(10)
            # 解析About页面
            pgab_resp = requests.get(pg_link + 'about/?ref=page_internal', headers=headers, proxies=proxies)
            pgab_soup = BeautifulSoup(pgab_resp.text, 'lxml')
            pgab_terms = fp.get_terms(pgab_soup)
            pg_re = (pg_link, pg_name, pg_likes, pgab_terms)
            log.info(pg_re)
            # 写入文件
            with open('../fp_csv.csv', 'a', encoding='utf-8') as f:
                f.write(str(pg_re) + '\n')
            time.sleep(10)
