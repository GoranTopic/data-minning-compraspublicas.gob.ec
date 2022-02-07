import scrapy
import time
from dotenv import dotenv_values
from selenium_functions import *
from test_data import test_projects

class LoginSpider(scrapy.Spider):
    name = 'compras'
    env = dotenv_values('.env')  
    urls = dotenv_values('.urls')  
  
    def start_requests(self):
        login_url = self.urls['LOGIN_URL']
        yield scrapy.Request( url=login_url, callback=self.selenium_login)


    def selenium_login(self, response):
        # handles the login with selenium and gets a list of projects ID's
        # passing it along to Scrapy of asyncronous download

        offset = 20 # number of projects we get from a page
        current_count = 0 # start at zero
        total_count = None # must define late on

        headless = True if self.env['HEADLESS'] == 1 else False
        # create driver   
        driver = create_driver(headless=True)

        # load login page
        driver.get(self.urls['LOGIN_URL'])

        # handle the login 
        submit_login_handler(driver)

        # handle authentication result
        authentication_handler(driver)

        # for some reason the server only gives us a user id
        # after we load the 'Procesos' page
        driver.get(self.urls['QUERY_PROJ_URL']) 
        # run empty seach
        driver.execute_script('botonBuscar()')

        # get user data from the selenium driver
        (cookies, user_data) = get_driver_user_data(driver)
        request_body = organize_body(user_data)

        # get the total number of projects
        total_count = get_total_project_count(driver)

        # base url for the 
        baseurl = self.urls['PROJECT_URL'] 
        projects_file = open('projects.py', 'w')
        projects_file.write(f"projects = [\n")
        while( current_count <= total_count ):
            # search for procesos
            # get the ID's for every procesos in the page
            projects = get_projects(driver, current_count)
            #print(f"\n\n{projects}")
            for project in projects: # for every id run scrapy requests
                for i in range(1,7): # total of six tabs, but the 5th is hidden?
                    url = baseurl + f"tab.php?tab={i}&id={project['ID']}"
                    yield scrapy.Request(url=url, 
                            cookies=cookies,
                            callback=self.parse_project, 
                            meta={'project': project, 'tab_num': i})
                    projects_file.write(f"{project},\n ")
                current_count += offset
                print(f"\nproject: {current_count} out of {total_count}\n")
        projects_file.write(f"]")
        #exit session
        driver.quit()
        
            
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


            
