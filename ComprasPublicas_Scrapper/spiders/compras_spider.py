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

    def login(self, response):
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
        driver.quit()


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
