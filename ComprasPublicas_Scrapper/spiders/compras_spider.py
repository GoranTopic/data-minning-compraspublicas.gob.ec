import scrapy
from dotenv import dotenv_values
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logzero import logfile, logger

    
class LoginSpider(scrapy.Spider):
    name = 'login'
    login_handle = dotenv_values('.env')  

    def start_requests(self):
        login_url = self.login_handle['LOGIN_URL']
        yield scrapy.SeleniumRequest(url=login_url, callback=self.login_parser)

    def login_parser(self, response):
        # define options for firefox
        #firefoxOptions = webdriver.FirefoxOptions()
        # set to headless driver
        #firefoxOptions.headless = False
        # open firefox driver with options
        driver = response.request.meta['driver']
        #driver = webdriver.Firefox(
                #executable_path='./geckodriver', 
                #options=firefoxOptions)
        # get webpage 
        driver.get(response.url)
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

        # wait
        el = WebDriverWait(driver, 2000000).until(
                lambda d: d.find_element_by_tag_name("p")
                )
        #wait = WebDriverWait(driver, 1000)
        #element = wait.until(EC.element_to_be_clickable((By.ID, 'mensaje')))
        print("wait ended")
        print("element:")
        print(el)

        # take screen shot
        driver.save_screenshot("screenshot.png")


        #try:
            #element = WebDriverWait(driver, 1000).until(
                    #EC.presence_of_element_located((By.ID, "mensaje")) 
                    #or
                    #EC.url_to_be(self.login_handle['HOME_URL'])
                    #)
            #print("endeed the wait")
        #finally:
            # was not redirected to home page
            # login failed posibly
            #print("could not get home page")
            #driver.quit()

        #print(f"element: {element}")
        # driver get Url

        #home_url = driver.current url

        # send to scrapy 
        #request = Request(
                #home_url,
                #cookies=driver.get_cookies(),
                #callback=self.parse_landing_page)
        # get the home landing url

        #driver.quit()

    def Authentification_response_parser(driver):
        pass

    def parse_landing_page(self, response):
        #print(f"\n{response}\n")
        #return response
        # go to page with 
        # for project in project
            # for request( url, callback=pares_project)
        pass
        return None

    def parse_project(self, response):
        return None

