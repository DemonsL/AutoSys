# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlsItem(scrapy.Item):
    Country = scrapy.Field()
    CategoryID = scrapy.Field()
    Rank = scrapy.Field()
    Asin = scrapy.Field()
    Title = scrapy.Field()
    Keywords = scrapy.Field()
    Pic = scrapy.Field()
    Review = scrapy.Field()
    Star = scrapy.Field()
    Price = scrapy.Field()


class SdUsersItem(scrapy.Item):
    UserId = scrapy.Field()
    Name = scrapy.Field()
    Level = scrapy.Field()
    JoinTime = scrapy.Field()
    SpentTime = scrapy.Field()
    LastTime = scrapy.Field()
    Reputation = scrapy.Field()
    Deals = scrapy.Field()
    Votes = scrapy.Field()
    Comments = scrapy.Field()