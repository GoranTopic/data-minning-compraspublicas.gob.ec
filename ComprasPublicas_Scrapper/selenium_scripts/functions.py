import time
import traceback
import json
import random
import scrapy
from os import path
from lxml import etree
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from ComprasPublicas_Scrapper import params 
from ComprasPublicas_Scrapper import proxy_rotation


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
        print("loading...")
        return None
    return "loading"


def divide_dates(start, end):
    """ this functioins take a range of two date and divindes into batches of 200 days """
    date_batches = [] # batches of data
    batch_size = 150
    start_date = date.fromisoformat(start) # first date of the range
    end_date = date.fromisoformat(end) # last date of the range
    date_range = end_date - start_date
    # if start data is earlier than end date
    if(date_range.days < 0):
        print("start date is earlier end date")
        exit() 
    # get dates
    num_batches = int(date_range.days / batch_size)
    for i in range(num_batches):
        date_batches.append({
            'start': start_date + timedelta(days=(batch_size * (i))),
            'end': start_date + timedelta(days=(batch_size * (i + 1))),
            })
    # get last days in the batch
    last_batch = date_range.days % batch_size
    last = start_date + timedelta(days=(batch_size * num_batches))
    date_batches.append({
        'start': last,
        'end': last + timedelta(days=last_batch),
        })
    return date_batches

def input_seach_parameters(date_batch, driver):
    # get seach parameters inputed 
    fecha_desde = date_batch['start'].strftime("%Y-%m-%d")
    fecha_hasta = date_batch['end'].strftime("%Y-%m-%d")

    if(params.palabras_claves):
        print(f'PALABRAS_CLAVES:      {params.palabras_claves}')
        element = driver.find_element(By.ID, "txtPalabrasClaves")
        element.send_keys(params.palabras_claves)

    if(params.entidad_contratante):
        print(f'ENTIDAD_CONTRATANTE:  {params.entidad_contratante}')
        element = driver.find_element(By.ID, "txtEntidadContratante")
        element.send_keys(params.entidad_contratante)

    if(params.tipo_de_contratacion):
        print(f'TIPO_DE_CONTRATACION: {parmas.tipo_de_contratacion}')
        element = driver.find_element(By.ID, "txtCodigoTipoCompra")
        element.send_keys(params.tipo_de_contratacion)

     # if(params.tipo_de_compra):
        # print(f'TIPO_DE_COMPRA:       {params.tipo_de_compra}')
        # element = driver.find_element(By.ID, "txtCodigoTipoCompra")
        # element.send_keys(params.tipo_de_compra)

    if(params.codigo_de_proceso):
        print(f'CODIGO_DEL_PROCESO:   {params.codigo_de_proceso}')
        element = driver.find_element(By.ID, "txtCodigoProceso")
        element.send_keys(params.codigo_de_proceso)

    # remove the readonly atribute to be able to write date
    driver.execute_script('document.getElementsByName("f_inicio")[0].removeAttribute("readonly")')
    if(params.fecha_desde):
        print(f'FECHA_DESDE:          {params.fecha_desde}')
        element = driver.find_element(By.ID, "f_inicio")
        element.send_keys(fecha_desde)

    # remove the readonly atribute to be able to write date
    driver.execute_script('document.getElementsByName("f_fin")[0].removeAttribute("readonly")')
    if(params.fecha_hasta):
        print(f'FECHA_HASTA:           {params.fecha_hasta}')
        element = driver.find_element(By.ID, "f_fin")
        element.send_keys(fecha_hasta)

def authentication_handler(driver):
    # function which handles the pupup which apears after login
    # wait until popup it apprears 
    loading_popup = True 
    while(loading_popup): 
        time.sleep(3)
        try:
            popup_el = driver.find_element(By.ID, "mensaje")
            state = popup_handler(popup_el)
        except Exception as e: 
            print("Alert Pop up not found")
            state = None
        if(state):
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
        elif(is_redirect_to_home_page(driver)):
            print("Acepted")
            return True

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
    user_data = {} # make empty obj
    #user_data['UsuarioID'] = driver.execute_script('return UsuarioID.value')
    for i in range(0, 16):
        try: # get the values in the selenium session, from the form data
            name = driver.execute_script(f'return $("paginaActual").form[{i}].name')
            value = driver.execute_script(f'return $("paginaActual").form[{i}].value')
            user_data[name] = value
        except: 
            print("could not get data")
            traceback.print_exc()
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
    def if_empty_link(x): # remove any 'javascript:void(0);'
        return False if(x == "javascript:void(0);") else True;
    relative_urls = list(filter(if_empty_link, relative_urls))
    # retrive project id 
    IDs = list(map(lambda l : l.split('=')[1], relative_urls))
    # retun object of ID
    return list(map(lambda ID, code : { 'ID': ID, 'code': code }, IDs, codes))

def create_driver(headless=False):
    # if we have the driver in the project
    if(path.exists('./ComprasPublicas_Scrapper/geckodriver')):
        geckodriver_path = './ComprasPublicas_Scrapper/geckodriver'
    else:
        geckodriver_path = None
    # define options for firefox
    firefoxOptions = webdriver.FirefoxOptions()
    # if proxies are enabled
    if params.is_proxy_mode: # get proxy and add it to options
        firefoxOptions.proxy = get_random_proxy()
    # set to headless driver
    firefoxOptions.headless = headless
    # open firefox driver with options
    if(geckodriver_path):
        driver = webdriver.Firefox(
                executable_path=geckodriver_path,  # must be in bin drive
                options=firefoxOptions)
    else:
        driver = webdriver.Firefox(
                options=firefoxOptions)
    return driver

def submit_login_handler(driver):
    # write ruc in input
    RUC_element = driver.find_element(By.ID, "txtRUCRecordatorio")
    RUC_element.send_keys(params.ruc)
    # write username in input
    username_element = driver.find_element(By.ID, "txtLogin")
    username_element.send_keys(params.username)
    # write password
    pass_element = driver.find_element(By.ID, "txtPassword") 
    pass_element.send_keys(params.password)
    # press sumbit button
    #submit_button = driver.find_element(By.ID, "btnEntrar")

    # when button is not in view, (headless mode)
    driver.execute_script("_lCominc()")
    #submit_button.click()

def get_total_project_count(driver):
    try:
        page_stats = driver.find_element(By.XPATH, 
                '//table/tbody/tr/td[@colspan="4"][@align="left"]').text
        total_projects = page_stats.split(' ')[-1]
        return int(total_projects)
    except Exception as e:
        print("ERROR : "+str(e))
        traceback.print_exc()
        return 0

def get_random_proxy():
    # import proxies
    proxies = proxy_rotation.proxies
    # select one random proxy
    randomProxy = random.choice(list(proxies))
    # set it in a selenium proxy object
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': randomProxy,
        'sslProxy': randomProxy,
        'noProxy': ''})
    return proxy


