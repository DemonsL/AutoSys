# -*- coding: utf-8 -*-
import logging
import scrapy
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from ..items import CrawlsItem
from ..settings import ABS_SITE
from ..db_models import DBSession, PubCategory

logger = logging.getLogger(__name__)

class AmzTopSpider(scrapy.Spider):
    name = 'amz_tops'
    allowed_domains = ['amazon.com']
    start_urls = []

    def start_requests(self):
        if not self.start_urls:
            self.start_urls = self.get_urls()
        for url in self.start_urls:
            headers = {
                'user_agent': UserAgent().random,
                'referer': 'https://www.amazon.com/gp/bestsellers'
            }
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        for li in soup.find(attrs={'id': 'zg-ordered-list'}):
            try:
                a = li.find('a').attrs.get('href')
                cate_id = response.url.split('?')[0].split('bestsellers/')[1]
                p_country = self.get_country_for_category(cate_id)
                item = CrawlsItem()
                item['Country'] = p_country
                item['CategoryID'] = cate_id
                item['Asin'] = a.split('dp/')[1].split('?')[0]
                item['Keywords'] = a.split('/dp')[0].strip('/')
                item['Pic'] = li.find('img').attrs.get('src').split('I/')[1]
                item['Rank'] = li.find('span', attrs={'class': 'zg-badge-text'}).text.strip('#')
                item['Title'] = li.find('div', attrs={'aria-hidden': 'true'}).text.strip()
                item['Star'] = self.parse_star(p_country, li.find('span', attrs={'class': 'a-icon-alt'}).text)
                item['Review'] = li.find('a', attrs={'class': 'a-size-small a-link-normal'}).text.replace(',', '').replace('.', '')
                item['Price'] = self.parse_price(p_country, li.find('span', attrs={'class': 'p13n-sc-price'}))
                yield item
            except Exception as e:
                logger.info('ParseError: %s' % e)

    def parse_star(self, country, p_star):
        if country in ['US', 'CA', 'UK']:
            return p_star.split(' out')[0]
        if country == 'DE':
            return p_star.split(' von')[0].replace(',', '.')
        if country == 'JP':
            return p_star.split(' ')[1]

    def parse_price(self, country, p_price):
        r_price = 0.0
        try:
            if country == 'US':
                r_price = p_price.text.strip('$').split(' -')[0].replace(',', '')
            if country == 'CA':
                r_price = p_price.text.strip('CDN$').split(' -')[0].replace(',', '').strip()
            if country == 'UK':
                r_price = p_price.text.strip('£').split(' -')[0].replace(',', '')
            if country == 'DE':
                r_price = p_price.text.strip('\u00a0€').strip('EUR ').split(' -')[0].strip('€').strip().replace(',', '.')
            if country == 'JP':
                r_price = p_price.text.strip('￥').split(' -')[0].replace(',', '')
            return float(r_price)
        except:
            return 0.0

    def get_urls(self):
        urls = []
        for country, cate in self.get_categories():
            url_host = ABS_SITE.get(country)
            for n in range(1, 3):
                url = url_host + '{cate}?pg={num}'.format(cate=cate, num=n)
                urls.append(url)
        return urls

    def get_categories(self):
        session = DBSession()
        try:
            cates = session.query(PubCategory, PubCategory.Country, PubCategory.SubCategoryID)\
                           .filter_by(Level=1).all()
            return [(cate[1], cate[2]) for cate in cates]
        except Exception as e:
            logger.info('GetCategoryError: %s' % e)
        finally:
            session.close()

    def get_country_for_category(self, cate_id):
        session = DBSession()
        try:
            country = session.query(PubCategory, PubCategory.Country).filter_by(SubCategoryID=cate_id).one()
            return country[1]
        except Exception as e:
            logger.info('GetCategoryError: %s' % e)
        finally:
            session.close()
