import scrapy
import time
from selenium_scripts.scrap_ids_without_login import scrap_project_ids
from dotenv import dotenv_values
from test_data import test_projects

class ProcesosSpider(scrapy.Spider):
    name = 'procesos_especiales'
    env = dotenv_values('.env')  
    urls = dotenv_values('.urls')  
    baseurl = urls['PROJECT_URL'] 
  
    def start_requests(self):
        login_url = self.urls['PROCESOS_ESPECIALES']
        yield scrapy.Request( url=login_url, callback=self.selenium_login_parser)

    def selenium_login_parser(self, response):
        """ this function call the selenium login script to get al the IDs from each 
            project to scrap it when passed those projects to the scrapy """
        # get data form selenium scraper 
        ( user_data, projects ) = scrap_project_ids(response.url)
            #print(f"\n\n{projects}")
        for project in projects: # for every id run scrapy requests
            for i in range(1,7): # total of six tabs, but the 5th is hidden?
                url = self.baseurl + f"tab.php?tab={i}&id={project['ID']}"
                yield scrapy.Request(url=url, 
                        cookies=user_data['cookies'],
                        callback=self.parse_project, 
                        meta={'project': project, 'tab_num': i})
            
    def parse_project(self, response):
        item = {
                'project': response.meta.get('project'),
                'tab_num': response.meta.get('tab_num'),
                'response': response,
                }
        if(item['tab_num'] == 6): 
            # get the rows of every file
            table_rows = response.xpath('//a[@href]/ancestor::tr[1]')
            item['files_meta'] = [ {
                'url': self.baseurl + row.xpath('.//a/@href').get(), 
                'title': row.xpath('.//div[@align="left"]/text()').get().strip() 
                } for row in table_rows ]
            item['file_urls'] = [ meta['url'] for meta in item['files_meta'] ]
        return item 


