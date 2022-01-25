import scrapy
from dotenv import dotenv_values
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger

    
class LoginSpider(scrapy.Spider):
    name = 'login'
    login_url = self.login_handle['DOMAIN']
    login_handle = dotenv_values('../.env')  

    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.login)

    def login_parser(self, response):
        # define options for firefox
        firefoxOptions = webdriver.FirefoxOptions()
        # firefox set headless option
        firefoxOptions.set_headless()
        # open firefox driver with options
        driver = webdriver.Firefox(firefox_options=firefoxOptions)
        # get webpage 
        driver.get(self.login_url)
        # get elements for login
        RUC_element = driver.find_element(By.ID, "txtRUCRecordatorio")
        username_element = driver.find_element(By.ID, "txtLogin")
        pass_element = driver.find_element(By.ID, "txtPassword") 
        # send keys to elements
        RUC_element.send_keys(self.login_handle['RUC'])
        username_element.send_keys(self.login_handle['USER'])
        pass_element.send_keys(self.login_handle['PASS'])
        # press the submit button
        submit_button = driver.find_element(By.ID, "btnEntrar")
        submit_button.click()
        driver.save_screenshot("test1.png")
        # driver get Url

        #home_url = driver.current url

        # send to scrapy 
        request = Request(
                home_url,
                cookies=driver.get_cookies(),
                callback=self.parse_landing_page)
        # get the home landing url
        driver.quit()

    def parse_landing_page(self, response):
        #print(f"\n{response}\n")
        #return response
        # go to page with 
        # for project in project
            # for request( url, callback=pares_project)

    def parse_project(self, response):
        return None

