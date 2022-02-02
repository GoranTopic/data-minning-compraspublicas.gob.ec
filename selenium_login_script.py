import time
from bs4 import BeautifulSoup
from lxml import etree
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    except:
        return None


def authentication_handler(driver):
    # function which handles the pupup which apears after login
    #wait until popup it apprears 
    loading_page = True
    loading_popup = True
    while(loading_popup):
        time.sleep(5)
        try:
            popup_el = driver.find_element(By.ID, "mensaje")
            state = popup_handler(popup_el)
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
            if(is_redirect_to_home_page(driver)):
                return True
        except NoSuchElementException: 
            loading_popup = True
            print("popup Still loading")
        except: 
            print("something when worng, popup did not appear")
            return False

def parse_procesos_urls(driver, offset):
    domain= 'https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/'
    # loads the next 20 'procesos'
    driver.execute_script(f"presentarProcesos({offset})")
    # get the inner tables data
    innerHTML = driver.execute_script('return $("frmDatos").innerHTML')
    # parse the html string
    soup = BeautifulSoup(innerHTML, "html.parser")
    # create dom from parsed html 
    dom = etree.HTML(str(soup))
    # get urls with xpath there are only 20 links per page
    relative_urls =  dom.xpath('//a/@href')[4:24]
    # make absolute urls
    urls = list(map(lambda l : domain + l, relative_urls))
    return urls



login_handle = dotenv_values('.env')  
login_url = login_handle['LOGIN_URL']

# define options for firefox
firefoxOptions = webdriver.FirefoxOptions()
# set to headless driver
firefoxOptions.headless = False
# open firefox driver with options
driver = webdriver.Firefox(
        executable_path='./geckodriver', 
        options=firefoxOptions)
# get webpage 
driver.get(login_url)
# get elements for login
RUC_element = driver.find_element(By.ID, "txtRUCRecordatorio")
username_element = driver.find_element(By.ID, "txtLogin")
pass_element = driver.find_element(By.ID, "txtPassword") 
# send keys to elements
RUC_element.send_keys(login_handle['RUC'])
username_element.send_keys(login_handle['USER'])
pass_element.send_keys(login_handle['PASS'])
# find sumbit button
submit_button = driver.find_element(By.ID, "btnEntrar")
# press the submit button
submit_button.click()
# handle the authetication
authentication_handler(driver)

# got to the look up process page
driver.get('https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/buscarProceso.cpe#') 

# run a empty search to get initial values and the total 
driver.execute_script('botonBuscar()')

not_reached_end = False
current_count = 0
total_count = 200
offset = 20


while( current_count <= total_count ):
    # search for procesos
    #run empty seach
    urls = parse_procesos_urls(driver, current_count)
    print(f"RESPONSE for {current_count} - {current_count + offset}:")
    print(urls)
    current_count += offset


