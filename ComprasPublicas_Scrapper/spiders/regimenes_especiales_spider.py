import scrapy
import time
from selenium_scripts.scrap_ids_without_login import scrap_project_ids
from ComprasPublicas_Scrapper.spiders.compras_spider import LoginSpider
from dotenv import dotenv_values
from test_data import test_projects

class RegimenesSpider(scrapy.Spider):
    name = 'regimenes_especiales'
    env = dotenv_values('.env')  
    urls = dotenv_values('.urls')  
    options = dotenv_values('options.txt')  
    baseurl = urls['PROJECT_URL'] 
    resumen_contractual_url= urls['RESUMEN_CONTRACTUAL']

    is_downloading_files = options['DOWNLOAD_FILES'] 
    if is_downloading_files is not None:
        is_downloading_files = is_downloading_files == "true" or is_downloading_files == "True"


    def start_requests(self):
        login_url = self.urls['REGIMEN_ESPECIALES']
        yield scrapy.Request( url=login_url, callback=self.compras_parser)

    def compras_parser(self, response):
        """ this function call the selenium login script to get al the IDs from each 
            project to scrap it when passed those projects to the scrapy """
        # get data form slenuim scraper 
        ( user_data, projects ) = scrap_project_ids(response.url)
            #print(f"\n\n{projects}")
        for project in projects: # for every id run scrapy requests
            # request the resumen conttractuales
            yield scrapy.Request(url=self.resumen_contractual_url + project['ID'],
                    cookies=user_data['cookies'],
                    callback=self.parse_project, 
                    meta={'project': project, 'isResume': True, })
            # this handle all the tabs of the project
            for i in range(1,7): # total of six tabs, but the 5th is hidden?
                url = self.baseurl + f"tab.php?tab={i}&id={project['ID']}"
                yield scrapy.Request(url=url, 
                        cookies=user_data['cookies'],
                        callback=self.parse_project, 
                        meta={'project': project, 'tab_num': i})

    def parse_project(self, response):
        item = { # unpack meta data
                'project': response.meta.get('project'),
                'tab_num': response.meta.get('tab_num'),
                'isResume': response.meta.get('isResume'),
                'response': response,
                }
        if(item['isResume']):
            print("--------- Got item resumen ---------")
            print(response)
        elif(item['tab_num'] == 6 and self.is_downloading_files): 
            # get the rows of every file
            table_rows = response.xpath('//a[@href]/ancestor::tr[1]')
            item['files_meta'] = [ {
                'url': self.baseurl + row.xpath('.//a/@href').get(), 
                'title': row.xpath('.//div[@align="left"]/text()').get().strip() 
                } for row in table_rows ]
            item['file_urls'] = [ meta['url'] for meta in item['files_meta'] ]
        return item 
