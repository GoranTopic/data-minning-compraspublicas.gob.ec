import scrapy
from scrapy_selenium import SeleniumRequest


def authentication_failed(response):
    print("\nPRINTING RESPONSE")
    print(response)
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class LoginSpider(scrapy.Spider):
    name = 'login'

    def start_requests(self):
        #urls = ['http://www.example.com/users/login.php']
        urls = ['http://www.compraspublicas.gob.ec/ProcesoContratacion/compras/index.php']
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse_result)
            #yield scrapy.Request(url=url, callback=self.parse)


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
