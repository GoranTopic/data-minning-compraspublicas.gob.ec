import scrapy
import time
import json
from bs4 import BeautifulSoup
from lxml import etree
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By

login_handle = dotenv_values('.env')  
  
    def start_requests(self):
        login_url = self.login_handle['LOGIN_URL']
        baseurl = self.login_handle['DOMAIN'] + "/ProcesoContratacion/compras/ProcesoContratacion/" 

    def is_redirect_to_home_page(self, driver):
        # Check whether the current url is the homepage
        url = driver.current_url
        if "home.cpe" in url:
            return True
        return False
        
def popup_handler(popup_element):
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
 
def handle_home_page(driver):
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


def authentication_handler(driver):
    # function which handles the pupup which apears after login
    #wait until popup it apprears 
    loading_page = True
    loading_popup = True
    while(loading_popup):
        time.sleep(3)
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
        for i in range(0, 16):
            try: # get the values in the selenium session, from the form data
                name = driver.execute_script(f'return $("paginaActual").form[{i}].name')
                value = driver.execute_script(f'return $("paginaActual").form[{i}].value')
                user_data[name] = value
            except: 
                print("could not get data")
        return (cookies, user_data)

    def organize_cookies(self, cookies):
        cookie_string = ""
        cookie_order = ['WRTCorrelator', 'NSC_IUUQT_wTfswfs_TPDF_DOU', 'incop_fw_.compraspublicas.gob.ec_%2F_wlf', 'incop_fw_.compraspublicas.gob.ec_%2F_wat', 'mySESSIONID', 'incop_fw_www.compraspublicas.gob.ec_%2F_wat', 'vssck', '_ga', '_gid']
        for order in cookie_order:
            for cookie in cookies:
                if order == cookie['name']:
                    cookie_string += cookie['name'] + "=" + cookie['value'] + "; "
                    break
            print(f"could not loacte {order}")
        return cookie_string

    def organize_body(self, request):
        body_string = ''
        body_order = ['__class', '__action', 'csrf_token', 'idus', 'UsuarioID', 'captccc2', 'txtPalabrasClaves', 'Entidadbuscar', 'txtEntidadContratante', 'cmbEntidad', 'txtCodigoTipoCompra', 'txtCodigoProceso', 'f_inicio f_fin', 'count', 'paginaActual20', 'estado', 'trx']
        for order in body_order:
            try:
                body_string += order + "=" + request[order] + '&' 
            except:
                print(f"could not get value: {order}")
        return body_string[:-1]

    def get_projects(self, driver, offset):
        # loads the next 20 'procesos'
        driver.execute_script(f"presentarProcesos({offset})")
        # get the inner tables data
        innerHTML = driver.execute_script('return $("frmDatos").innerHTML')
        # parse the html string
        soup = BeautifulSoup(innerHTML, "html.parser")
        # create dom from parsed html 
        dom = etree.HTML(str(soup))
        # get urls with xpath there are only 20 links per page
        relative_urls = dom.xpath('//a/@href')[4:24]
        codes = [ e.text for e in dom.xpath('//a')[4:24] ]
        # make absolute urls
        IDs = list(map(lambda l : l.split('=')[1], relative_urls))
        return list(map(lambda ID, code  : { 'ID': ID, 'code': code }, IDs, codes))

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
        driver.execute_script('botonBuscar()')
        # get user data from the selenium driver
        (cookies, user_data) = self.get_driver_user_data(driver)
        request_body = self.organize_body(user_data)

        current_count = 0
        total_count = 100
        offset = 20

        filepath = "/ProcesoContratacion/compras/ProcesoContratacion/" 
        baseurl = self.login_handle['DOMAIN'] + filepath
        
        #os.chdir(project.code)
        #cwd = os.getcwd()
        #os.mkdir(project.code)
        #os.chdir(project.code)

        while( current_count <= total_count ):
            # search for procesos
            # get the ID's for every procesos in the page
            projects = self.get_projects(driver, current_count)
            print(f"\n\n{projects}")
            print(f"RESPONSE from {current_count}/{current_count + offset}:\n\n")
            for project in projects: # for every id run scrapy requests
                for i in range(1,6): # total of six tabs
                    url=baseurl + f"tab.php?tab={i}&id={project['ID']}"
                    yield scrapy.Request(url=url, 
                            callback=self.parse_project, 
                            meta={'project': project, 'tab_num': i})
            current_count += offset
        
            
    def parse_project(self, response):
        project = response.meta.get('project')
        tab_num = response.meta.get('tab_num')
        #if(tab_type == 6) 
        #   get for files 
        #   for url in urls:
        #       add data to meta
        #       yield scrapy.Request(url=url, 
        #               callback=parse_project, 
        #               meta={'project': project, "type": i})
        return {'response': response, 
                'body': response.body,
                'project': project, 
                'tab_num': tab_num }


            
