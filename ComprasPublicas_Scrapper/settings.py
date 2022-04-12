# Scrapy settings for ComprasPublicas_Scrapper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from ComprasPublicas_Scrapper import params
from ComprasPublicas_Scrapper.proxy_rotation import get_proxies

BOT_NAME = 'ComprasPublicas_Scrapper'

SPIDER_MODULES = ['ComprasPublicas_Scrapper.spiders']
NEWSPIDER_MODULE = 'ComprasPublicas_Scrapper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ComprasPublicas_Scrapper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs


# set the delay in scrapy
DOWNLOAD_DELAY = 0
if params.is_stealthy:
        DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

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
    #'ComprasPublicas_Scrapper.middlewares.CompraspublicasScrapperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'ComprasPublicas_Scrapper.middlewares.CompraspublicasScrapperDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810, 
}

if params.is_proxy_mode: 
    number_of_proxies = params.proxy_count 
    ROTATING_PROXY_LIST = get_proxies(number_of_proxies)
    # if proxy mode is enable, add middleware
    DOWNLOADER_MIDDLEWARES['rotating_proxies.middlewares.RotatingProxyMiddleware'] = 610
    DOWNLOADER_MIDDLEWARES['rotating_proxies.middlewares.BanDetectionMiddleware'] = 620

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# set where the files will be download to 
if params.dest_folder is not None:
    FILES_STORE = os.path.join( params.dest_folder, params.domain )
else:
    FILES_STORE = params.domain

ITEM_PIPELINES = {
    'ComprasPublicas_Scrapper.pipelines.CompraspublicasScrapperPipeline': 300,
}

if params.is_downloading_files:
    # if downloading file such pdf is enable, add middleware for it
    ITEM_PIPELINES['ComprasPublicas_Scrapper.pipelines.CompraspublicasFilePipeline'] = 1

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
