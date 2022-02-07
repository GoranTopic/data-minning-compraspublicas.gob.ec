import scrapy
from dotenv import dotenv_values
from test_data import test_projects

class TestSpider(scrapy.Spider):
    name = 'test'
    urls = dotenv_values('.urls')  
  
    def start_requests(self):
        login_url = self.urls['LOGIN_URL']
        baseurl = self.urls['PROJECT_URL'] 

        for project in test_projects: 
            for i in range(1,7): # total of six tabs, but the 5th is hidden?
                url = baseurl + f"tab.php?tab={i}&id={project['ID']}"
                yield scrapy.Request(url=url, 
                        callback=self.parse_project, 
                        meta={'project': project, 'tab_num': i})

            
    def parse_project(self, response):
        item = {
                'project': response.meta.get('project'),
                'tab_num': response.meta.get('tab_num'),
                'response': response,
                }
        if(item['tab_num'] == 6): 
            baseurl = self.urls['PROJECT_URL'] 
            # get the rows of every file
            table_rows = response.xpath('//a[@href]/ancestor::tr[1]')
            item['files_meta'] = [ {
                'url': baseurl + row.xpath('.//a/@href').get(), 
                'title': row.xpath('.//div[@align="left"]/text()').get().strip() 
                } for row in table_rows ]
            item['file_urls'] = [ meta['url'] for meta in item['files_meta'] ]

        return item 


            
