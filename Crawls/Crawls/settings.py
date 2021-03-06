# -*- coding: utf-8 -*-
import datetime
# Scrapy settings for Crawls project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Crawls'

SPIDER_MODULES = ['Crawls.spiders']
NEWSPIDER_MODULE = 'Crawls.spiders'

# 日志设置
LOG_LEVEL = 'INFO'
LOG_FILE = '/home/develop/logs/amz_best_seller/{}.log'.format(datetime.datetime.today().date())

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Crawls (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# 对单个IP进行并发请求的最大值。如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定， 使用该设定。 也就是说，并发限制将针对IP，而不是网站。
# 该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0，下载延迟应用在IP而不是网站上。
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# 失败重试设置
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [503]
# 下载超时设置
DOWNLOAD_TIMEOUT = 15

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Crawls.middlewares.CrawlsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Crawls.middlewares.CrawlsDownloaderMiddleware': 543,
#}

PROXY_MIDDLEWARES = {
   'Crawls.middlewares.CrawlsProxyMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Crawls.pipelines.CrawlsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# redis 配置
REDIS_HOST = '47.251.1.157'
REDIS_PORT = 6379
REDIS_PASS = 'discover_1'
# REDIS_DB_INDEX = 0

# mysql 配置
Host='47.88.50.243'
Port=3306
User='develep'
Passwd='xcentz_1'
DB='xcentz'
CharSet = 'utf8'

# Amz_Best_Seller
ABS_SITE = {
   'US': 'https://www.amazon.com/bestsellers/',
   'CA': 'https://www.amazon.ca/bestsellers/',
   'UK': 'https://www.amazon.co.uk/bestsellers/',
   'DE': 'https://www.amazon.de/bestsellers/',
   'JP': 'https://www.amazon.co.jp/bestsellers/'
}
