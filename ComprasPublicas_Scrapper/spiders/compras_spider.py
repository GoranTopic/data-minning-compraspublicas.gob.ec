import scrapy
import time
import json
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By


    
class LoginSpider(scrapy.Spider):
    name = 'login'
    login_handle = dotenv_values('.env')  
  
    def start_requests(self):
        login_url = self.login_handle['LOGIN_URL']
        yield scrapy.Request(
                url=login_url, 
                callback=self.login_parser)

    def is_redirect_to_home_page(self, driver):
        # Check whether the current url is the homepage
        url = driver.current_url
        if "home.cpe" in url:
            return True
        return False
        
    def popup_handler(self, popup_element):
        # returns the status of the popup element:
        # acepted, denied or loading
        text = popup_element.text
        if "Error de ingreso" in text:
            print("Authetification Error:")
            print(text)
            return "denied"
        elif "Alerta de ingreso" in text:
            print("Authenticated")
            return "acepted"
        #elif # loading function
        #   pass
        #   return "loading"
        else:
            # write catch all function 
            #print("something whent wrong. Could not Identify the popup element")
            #return None
            return "loading"
 
    def handle_home_page(self, driver):
        # if there is a message #finish later
        try: # the the imidiate parent div of the element which is equal to 'AVISO'
            aviso = driver.find_element(By.XPATH, "//*[.='AVISO'/ancestor::div[1]")
            # get the button accept link
            btn = aviso.find_element(By.XPATH, "//*[.='Aceptar']")
            #scroll to view
            driver.execute_script("arguments[0].scrollIntoView(true);", btn);
            # click button
            #btn.click()
        except:
            return None


    def authentication_handler(self, driver):
        # function which handles the pupup which apears after login
        #wait until popup it apprears 
        loading_page = True
        loading_popup = True
        while(loading_popup):
            time.sleep(5)
            try:
                popup_el = driver.find_element(By.ID, "mensaje")
                state = self.popup_handler(popup_el)
                if(state == 'acepted'): 
                    # click button
                    print("ACCEPTED!")
                    popup_el.find_element(By.ID, "btnEntrar").click()
                    return True
                elif(state == 'denied'): 
                    print("DENIED!")
                    return False
                elif(state == 'loading'): 
                    print("LOADING!")
                    loading_popup = True
                # if there are no Popup
                if(self.is_redirect_to_home_page(driver)):
                    return True
            except NoSuchElementException: 
                loading_popup = True
                print("popup Still loading")
            except: 
                print("something when worng, popup did not appear")
                return False

    def get_driver_user_data(self, driver):
        # get session Data
        cookies = driver.get_cookies()
        user_data = {} #m make empty obj
        user_data['UsuarioID'] = driver.execute_script('return UsuarioID.value')
        user_data["__class"] = "SolicitudCompra"
        user_data["__action"] = "buscarProcesoxEntidad"
        for i in range(1, 16):
            try: # get the values in the selenium session, from the form data
                name = driver.execute_script(f'return $("paginaActual").form[{i}].name')
                value = driver.execute_script(f'return $("paginaActual").form[{i}].value')
                user_data[name] = value
            except: 
                print("could not get data")
        return (cookies, user_data)

    def login_parser(self, response):
        # define options for firefox
        firefoxOptions = webdriver.FirefoxOptions()
        # set to headless driver
        firefoxOptions.headless = False
        # open firefox driver with options
        driver = webdriver.Firefox(
                executable_path='./geckodriver', 
                options=firefoxOptions)
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
        # find sumbit button
        submit_button = driver.find_element(By.ID, "btnEntrar")
        # press the submit button
        submit_button.click()
        # handle the authetication
        self.authentication_handler(driver)
        # for some reason the server oly gives us a user After we load the 'Procesos' page
        driver.get('https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/buscarProceso.cpe#') 
        # get user data from the selenium driver
        (cookie_jar, user_data) = self.get_driver_user_data(driver)
        # add page we want to get
        user_data["paginaActual"] = 0
        request_body = json.dumps(user_data)
        print(f"request body:{request_body}")
        
        yield scrapy.Request(
                url="https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/servicio/interfazWeb.php",
                method='POST',
                #body=request_body,
                cookies=cookie_jar,
                headers={
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'
                    },
                callback=self.proceso_parser)

        
    def proceso_parser(self, response):
        print("\n\nPrint reponse from api call: ")
        print(response)
        print("\n\n")



                

        
        #yield scrapy.Request(
                #url="https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/servicio/interfazWeb.php",
                #method='POST',
                #body=request_body,
                #cookies=cookie_jar,
                #headers={
                #    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                #    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'
                #    },
                #callback=self.proceso_parser)


        #wait = WebDriverWait(driver, 1000)
        #Loading = False 
        #while`(True):
        #    print("\nended")
        #    print("element:")

        #    element = WebDriverWait(driver, 100000).until( 
        #            EC.presence_of_element_located((By.ID, 'mensaje'))
        #            )
        #    print(element)
        #    print("\n")
            
        #time.sleep(2000000000)
        # take screen shot
        #driver.save_screenshot("screenshot.png")


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

    def contest_list_parser(self, response):
        #print(f"\n{response}\n")
        #return response
        # go to page with 
        # for project in project
            # for request( url, callback=pares_project)
        pass
        return None

    def parse_project(self, response):
        return None

