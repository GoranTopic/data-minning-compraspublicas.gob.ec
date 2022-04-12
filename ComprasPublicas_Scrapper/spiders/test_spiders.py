import scrapy
import json
from ComprasPublicas_Scrapper import params 
from ComprasPublicas_Scrapper.test_data import test_projects
from ComprasPublicas_Scrapper.spiders.compras_spider import ComprasSpider
from ComprasPublicas_Scrapper.selenium_scripts.scrap_ids import scrap_project_ids

class TestScrapySpider(ComprasSpider):
    name = 'test_scrapy'
    # overwirte scrapy
    def compras_parser(self, response):
        """ test the scrapy frame worky my downloading projects with the test 
            data id project """
        # get the test data project ids 
        projects = test_projects 
        # parse each project
        for project in projects: # for every id run scrapy requests
            # request the resumen contractuales
            resumen_url = params.resumen_contractual_url + project['ID']
            yield scrapy.Request(url=resumen_url, 
                    callback=self.parse_project, 
                    meta={'project': project, 'isResume': True, })
            # get request
            for i in range(1,7): # total of six tabs, but the 5th is hidden?
                url = self.baseurl + f"tab.php?tab={i}&id={project['ID']}"
                yield scrapy.Request(url=url, 
                        callback=self.parse_project, 
                        meta={'project': project, 'tab_num': i})


class TestSeleniumSpider(ComprasSpider):
    """ this spider only tests if the slenium functions is working correcly"""
    name = 'test_selenium'
    
    def start_requests(self):
        # test the login in 
        login_url = params.login_url
        yield scrapy.Request( url=login_url, 
                # which the parser to test difrent parts of the selenim code 
                callback=self.procesos_especiales_parser
                )

    def selenium_test_parser(self, response):
        # get the test data project ids 
        ( user_data, projects ) = scrap_project_ids()

    def regimenes_especiales_parser(self, response):
        url = params.regimenes_especiales_url
        # get the test data project ids 
        ( user_data, projects ) = scrap_project_ids(login=False, url=url)

    def procesos_especiales_parser(self, response):
        url = params.procesos_especiales_url
        # get the test data project ids 
        ( user_data, projects ) = scrap_project_ids(login=False, url=url)

class ProxyTestSpider(ComprasSpider):
    """ this spidet test where the proxies are working correctly,
    most have proxies enabled in setting """
    name = 'test_proxy'
    ips = {}
    
    def start_requests(self):
        # test the login in 
        public_ip_url = "https://api.myip.com/"
        for i in range(100):
            yield scrapy.Request( url=public_ip_url,
                    callback=self.public_ip_parser,
                    dont_filter = True)
        print('\n\n')
        print(self.ips)
        print('\n\n')

    def public_ip_parser(self, response):
        res = json.loads(response.body.decode())
        try:
            self.ips[res['ip']] += 1
        except KeyError:
            self.ips[res['ip']]  = 1


