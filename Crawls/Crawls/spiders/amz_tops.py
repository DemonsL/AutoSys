# -*- coding: utf-8 -*-
import logging
import scrapy
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from ..items import CrawlsItem
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
                item = CrawlsItem()
                item['Country'] = 'US'
                item['CategoryID'] = response.url.split('?')[0].split('bestsellers/')[1]
                item['Asin'] = a.split('dp/')[1].split('?')[0]
                item['Keywords'] = a.split('/dp')[0].strip('/')
                item['Pic'] = li.find('img').attrs.get('src').split('I/')[1]
                item['Rank'] = li.find('span', attrs={'class': 'zg-badge-text'}).text.strip('#')
                item['Title'] = li.find('div', attrs={'aria-hidden': 'true'}).text.strip()
                item['Star'] = li.find('span', attrs={'class': 'a-icon-alt'}).text.split(' out')[0]
                item['Review'] = li.find('a', attrs={'class': 'a-size-small a-link-normal'}).text.replace(',', '')
                item['Price'] = li.find('span', attrs={'class': 'p13n-sc-price'}).text.strip('$').split(' -')[0].replace(',', '')
                yield item
            except Exception as e:
                logger.info('ParseError: %s' % e)

    def get_urls(self):
        urls = []
        for cate in self.get_categories():
            for n in range(1, 3):
                url = 'https://www.amazon.com/gp/bestsellers/{cate}?pg={num}'.format(cate=cate, num=n)
                urls.append(url)
        return urls

    def get_categories(self):
        session = DBSession()
        try:
            cates = session.query(PubCategory, PubCategory.SubCategoryID).filter_by(Level=1).all()
            return [cate[1] for cate in cates]
        except Exception as e:
            logger.info('GetCategoryError: %s' % e)
        finally:
            session.close()

