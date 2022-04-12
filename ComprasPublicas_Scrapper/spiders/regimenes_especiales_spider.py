import scrapy
from ComprasPublicas_Scrapper import params 
from ComprasPublicas_Scrapper.spiders.compras_spider import ComprasSpider

class RegimenesSpider(ComprasSpider):
    name = 'regimenes_especiales'
    nologin = True
    
    def start_requests(self):
        start_url = params.regimenes_especiales_url
        yield scrapy.Request( url=start_url, callback=self.compras_parser)


