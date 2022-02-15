import scrapy
import time
import json
from os import path
from bs4 import BeautifulSoup
from lxml import etree
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By

env = dotenv_values('.env')  

def is_redirect_to_home_page(driver):
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
    elif 'Usuario deshabilitado' in text:
        print("Usuario deshabilitado")
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

def authentication_handler(driver):
    # function which handles the pupup which apears after login
    #wait until popup it apprears 
    loading_page = True
    loading_popup = True
    while(loading_popup):
        time.sleep(3)
        try:
            popup_el = driver.find_element(By.ID, "mensaje")
            state = popup_handler(popup_el)
            if(state == 'acepted'): 
                # click button
                print("Acepted")
                popup_el.find_element(By.ID, "btnEntrar").click()
                return True
            elif(state == 'denied'): 
                print("Denied")
                exit()
                return False
            elif(state == 'loading'): 
                print("Loading...")
                loading_popup = True
            # if there are no Popup
            if(is_redirect_to_home_page(driver)):
                return True
        except NoSuchElementException: 
            loading_popup = True
            print("popup Still loading")
        except: 
            print("something when worng, popup did not appear")
            return False

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

def get_driver_user_data(driver):
    # get session Data
    cookies = driver.get_cookies()
    user_data = {} #make empty obj
    user_data['UsuarioID'] = driver.execute_script('return UsuarioID.value')
    for i in range(0, 16):
        try: # get the values in the selenium session, from the form data
            name = driver.execute_script(f'return $("paginaActual").form[{i}].name')
            value = driver.execute_script(f'return $("paginaActual").form[{i}].value')
            user_data[name] = value
        except: 
            print("could not get data")
    return (cookies, user_data)

def organize_cookies(cookies):
    cookie_string = ""
    cookie_order = [
            'WRTCorrelator', 
            'NSC_IUUQT_wTfswfs_TPDF_DOU', 
            'incop_fw_.compraspublicas.gob.ec_%2F_wlf', 
            'incop_fw_.compraspublicas.gob.ec_%2F_wat', 
            'mySESSIONID', 
            'incop_fw_www.compraspublicas.gob.ec_%2F_wat', 
            'vssck', 
            '_ga', 
            '_gid']
    for order in cookie_order:
        for cookie in cookies:
            if order == cookie['name']:
                cookie_string += cookie['name'] + "=" + cookie['value'] + "; "
                break
        print(f"could not loacte {order}")
    return cookie_string

def organize_body(request):
    body_string = ''
    body_order = [
            '__class',
            '__action', 
            'csrf_token', 
            'idus', 
            'UsuarioID', 
            'captccc2', 
            'txtPalabrasClaves', 
            'Entidadbuscar', 
            'txtEntidadContratante', 
            'cmbEntidad', 
            'txtCodigoTipoCompra', 
            'txtCodigoProceso', 
            'f_inicio',
            'f_fin', 
            'count', 
            'paginaActual20', 
            'estado', 
            'trx']
    for order in body_order:
        try:
            body_string += order + "=" + request[order] + '&' 
        except:
            print(f"could not get value: {order}")
    return body_string[:-1]

def get_projects(driver, offset):
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

def create_driver(headless=True):
    if(path.exists('./geckodriver')):
        geckodriver_path = './geckodriver'
    else:
        geckodriver_path = None

    # define options for firefoxa
    firefoxOptions = webdriver.FirefoxOptions()
    # set to headless driver
    firefoxOptions.headless = headless
    # open firefox driver with options
    driver = webdriver.Firefox(
    executable_path=geckodriver_path,  #must be in bin drive
    options=firefoxOptions)
    return driver

def submit_login_handler(driver):
    # write ruc in input
    RUC_element = driver.find_element(By.ID, "txtRUCRecordatorio")
    RUC_element.send_keys(env['RUC'])
    # write username in input
    username_element = driver.find_element(By.ID, "txtLogin")
    username_element.send_keys(env['USER'])
    # write password
    pass_element = driver.find_element(By.ID, "txtPassword") 
    pass_element.send_keys(env['PASS'])
    # press sumbit button
    #submit_button = driver.find_element(By.ID, "btnEntrar")

    # when button is not in view, (headless mode)
    driver.execute_script("_lCominc()")
    #submit_button.click()

def get_total_project_count(driver):
    page_stats = driver.find_element(By.XPATH, 
            '//table/tbody/tr/td[@colspan="4"][@align="left"]').text
    total_projects = page_stats.split(' ')[-1]
    return int(total_projects)


