#!/usr/bin/env python3
import subprocess
import sys

required = [ 'scrapy', 'python-dotenv', 'beautifulsoup4', 'selenium', "scrapy-rotating-proxies"  ]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

for package in required:
    if package not in installed_packages:
        install(package)

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('compras')
process.start() # the script will block here until the crawling is finished
