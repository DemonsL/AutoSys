# coding: utf-8
from scrapy.crawler import CrawlerProcess
from .Crawls.spiders import amz_tops




if __name__ == '__main__':

    process = CrawlerProcess()
    process.crawl(amz_tops)
    process.start()