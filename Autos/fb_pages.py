# coding: utf-8
import sys
sys.path.append('../')
import time
import datetime
import logging
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


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
        return so.find('div', attrs={'class': '_4bl9 _5m_o'}).text







if __name__ == '__main__':

    url = 'https://www.facebook.com/pages/category/topic-shopping-retail/?page={}'
    headers = {
        'referer': 'https://www.facebook.com/pages/category/topic-shopping-retail/',
        'accept-language': 'en-us'
    }
    ip_ports = [
        '121.40.199.105:80', '139.186.13.209:54808', '174.120.70.232:80', '145.239.120.150:3128',
        '121.42.163.161:80', '123.206.227.91:46376', '210.242.179.118:80', '115.42.35.18:4220',
        '116.199.2.196:80', '106.53.169.125:46554', '139.199.207.26:3128', '139.5.71.80:23500',
        '114.116.75.60:60562', '129.28.109.202:46350', '221.180.170.8:8080', '157.52.208.86:3129',
        '119.3.37.101:36194', '129.28.40.119:50607', '125.118.149.224:808', '170.210.80.241:3128',
        '106.52.68.116:25417', '39.105.24.57:51857', '114.219.26.77:8998', '118.175.207.180:40017',
        '1.20.97.96:54205', '85.234.126.107:55555', '202.179.7.158:23500', '36.81.252.104:8080',
        '84.241.44.182:8080', '218.94.153.150:8008', '103.216.82.146:6666', '93.78.205.197:57437'
    ]

    ua = UserAgent()
    fp = FbPages()
    for i in range(79, 3000):
        log.info(url.format(i + 1))
        with open('../fp_csv.csv', 'a', encoding='utf-8') as f:
            f.write(url.format(i + 1) + '\n')
        user_agent = {
            'user_agent': ua.random
        }
        proxies = {
            'http': 'http://{}'.format(random.choice(ip_ports))
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
            pgab_resp = requests.get(pg_link + 'about/?ref=page_internal', headers=headers, proxies=proxies)
            pgab_soup = BeautifulSoup(pgab_resp.text, 'lxml')
            pgab_terms = fp.get_terms(pgab_soup)
            pgab_site = fp.get_site(pgab_soup)
            pg_re = (pg_link, pg_name, pg_likes, pgab_terms, pgab_site)
            log.info(pg_re)
            # 写入文件
            with open('../fp_csv.csv', 'a', encoding='utf-8') as f:
                f.write(str(pg_re) + '\n')

