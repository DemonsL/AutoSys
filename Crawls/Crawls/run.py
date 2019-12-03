# coding: utf-8
import sys
sys.path.append('../')
from scrapy.crawler import CrawlerProcess
from Crawls.Crawls.spiders import amz_tops



def main():
    process = CrawlerProcess()
    process.crawl(amz_tops)
    process.start()


main()