import scrapy
from ComprasPublicas_Scrapper import params 
from ComprasPublicas_Scrapper.spiders.compras_spider import ComprasSpider
from ComprasPublicas_Scrapper.selenium_scripts.scrap_ids import scrap_project_ids

class ProcesosSpider(ComprasSpider):
    name = 'procesos_especiales'
    nologin = True
    start_url = params.procesos_especiales_url

    def start_requests(self):
        start_url = self.start_url
        yield scrapy.Request( url=start_url, callback=self.compras_parser)


