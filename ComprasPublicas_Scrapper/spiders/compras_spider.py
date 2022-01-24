import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger


def authentication_failed(response):
    print("\nPRINTING RESPONSE")
    print(response)
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger

class CountriesSpiderSpider(scrapy.Spider):
    # Initializing log file
    allowed_domains = ["toscrape.com"]# Using a dummy website to start scrapy request
    name = 'login'

    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_countries)

    def parse_countries(self, response):
        driver = webdriver.Chrome()  
        # To open a new browser window and navigate it
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        # Getting list of Countries
        driver.get("https://openaq.org/#/countries")
        # Implicit wait
        driver.implicitly_wait(10)# Explicit wait
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card__title")))
        countries = driver.find_elements_by_class_name("card__title")
        countries_count = 0
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file
        for country in countries:
            yield {
                "country": country.text,
            }
            countries_count += 1
        driver.quit()
        logger.info(f"Total number of Countries in openaq.org: {countries_count}")

class LoginSpider(scrapy.Spider):
    name = 'someSpider'
    driver = webdriver.Chrome()

    def start_requests(self):
        #urls = ['http://www.compraspublicas.gob.ec/ProcesoContratacion/compras/index.php']
        urls = ['https://openaq.org/#/countries']
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.login_parser)

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
