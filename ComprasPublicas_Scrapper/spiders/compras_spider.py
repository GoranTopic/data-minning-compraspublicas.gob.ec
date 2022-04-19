import scrapy
from ComprasPublicas_Scrapper import params 
from ComprasPublicas_Scrapper.test_data import test_projects
from ComprasPublicas_Scrapper.selenium_scripts.scrap_ids import scrap_project_ids

class ComprasSpider(scrapy.Spider):
    name = 'compras'
    start_url = params.login_url
    baseurl = params.project_url
    resumen_contractual_url= params.resumen_contractual_url 
    # if you are setting nologin to true one must provide 
    # the target url in start_ulr at start_requests
    nologin = False
  
    def start_requests(self):
        start_url = self.start_url
        yield scrapy.Request( url=start_url, callback=self.compras_parser)

    def compras_parser(self, response):
        """ this function call the selenium login script to get al the IDs from each 
            project to scrap it when passed those projects to the scrapy """
        # get data form slenuim scraper 
        # if a starget has been set
        (user_data, projects) = scrap_project_ids(login=False, url=response.url) if self.nologin else scrap_project_ids()

            #print(f"\n\n{projects}")
        for project in projects: # for every id run scrapy requests
            # request the resumen contractuales
            resumen_url = self.resumen_contractual_url + project['ID']
            yield scrapy.Request(url=resumen_url, 
                    cookies=user_data['cookies'],
                    callback=self.parse_project, 
                    meta={'project': project, 'isResume': True, })
            # get request
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
        if(item['tab_num'] == 6): 
            # get the rows of every file
            table_rows = response.xpath('//a[@href]/ancestor::tr[1]')
            item['files_meta'] = [ {
                'url': self.baseurl + row.xpath('.//a/@href').get(), 
                'title': row.xpath('.//div[@align="left"]/text()').get().strip() 
                } for row in table_rows ]
            item['file_urls'] = [ meta['url'] for meta in item['files_meta'] ]
        return item 


