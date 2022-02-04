import time
from bs4 import BeautifulSoup
from lxml import etree
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_functions import *

offset = 20 # number of projects we get from a page
current_project_count = 0 # start at zero
total_project_count = None # must define late on

env = dotenv_values('.env')  

headless = True if env['HEADLESS'] == 1 else False
# create driver   
driver = create_driver(headless)

# load login page
driver.get(env['LOGIN_URL'])

# handle the login 
submit_login_handler(driver)

# handle authentication result
authentication_handler(driver)

# for some reason the server only gives us a user After we load the 'Procesos' page
driver.get(env['QUERY_PROJ_URL']) 
# run empty seach
driver.execute_script('botonBuscar()')

# get user data from the selenium driver
(cookies, user_data) = get_driver_user_data(driver)
request_body = organize_body(user_data)

# get the total number of projects
total_project_count = get_total_project_count(driver)


while( current_count <= total_count ):
    # search for procesos
    print(f"RESPONSE for {current_count} - {current_count + offset}:")
    print(urls)
    current_count += offset

driver.quit()

