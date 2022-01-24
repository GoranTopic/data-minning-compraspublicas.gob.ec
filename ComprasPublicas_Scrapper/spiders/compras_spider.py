import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger

    
class LoginSpider(scrapy.Spider):
    name = 'login'

    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_countries)

    def parse_countries(self, response):
        # dfine options for firefox
        firefoxOptions = webdriver.FirefoxOptions()
        # firefox set headless option
        firefoxOptions.set_headless()
        # open firefox driver with options
        brower = webdriver.Firefox(firefox_options=firefoxOptions)
        # get webpage 
        brower.get('https://pythonbasics.org')
        # print source code
        print(brower.page_source)
        brower.quit()


    def login_parser(self, response):
        # use selenium driver to log in to compras
        print(response.body)
        
        

    def parse(self, response):
        #print(f"\n{response}\n")
        #return response
        return scrapy.FormRequest.from_response(
            response,
            #formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login)

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
