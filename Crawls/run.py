# coding: utf-8
from scrapy.crawler import CrawlerProcess
from .Crawls.spiders import amz_tops



def main():
    process = CrawlerProcess()
    process.crawl(amz_tops)
    process.start()


main()