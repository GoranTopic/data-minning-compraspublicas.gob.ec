import os
import time
from lxml import etree
from functions import *
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.by import By

def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def login_script(): 
    """ This Script handles the Selenium login script """
    # define constants for website
    offset = 20 # number of projects we get from a page
    current_project_count = 0 # start at zero
    total_project_count = None # must define late on
    projects_ids = [] # list to store ids in memory
    
    # read from config files
    env = dotenv_values('.env')  
    urls = dotenv_values('.urls')  

    # get the baseurl make abosulte links
    baseurl = urls['PROJECT_URL'] 

    # read headless option
    is_headless = env['HEADLESS']
    print(f"Headless mode is set to: {is_headless}")
    if(is_headless == "true"):
        headless = True
    else:
        headless = False

    # read dest folder from .env file
    if env['DEST_FOLDER'] is not None:
        dest = env['DEST_FOLDER']
    else: 
        print('could not get destination folder from .env file')
        exit()

    # make destination folder
    # if it does not exits
    make_folder(dest)

    # create file where to store all the donwloaded project ids
    # filename for the writing the project ids
    filename = os.path.join(dest, 'project_found.txt')
    # open ids
    projects_file = open(filename, 'w')
    projects_file.write(f"projects_ids = [\n")

    """ ---- start script process ----"""

    # create driver   
    driver = create_driver(headless=headless)

    # load login page
    driver.get(urls['LOGIN_URL'])

    # handle the login 
    submit_login_handler(driver)

    # handle authentication result
    authentication_handler(driver)

    # For some reason the server only gives us user_data,
    # after we load the 'Procesos' page
    driver.get(urls['QUERY_PROJ_URL']) 
    
    # run search function 
    driver.execute_script('botonBuscar()')

    # get user data from the selenium driver
    (cookies, data) = get_driver_user_data(driver)

    # clean the reuqest body
    request_body = organize_body(data)
    
    # request body 
    user_data = { 'cookies': cookies, 'request_body': request_body }

    # get the total number of projects
    total_project_count = get_total_project_count(driver)
    
  #   # base url for the 
    # while(current_project_count <= total_project_count):
        # # search for procesos
        # # get the ID's for every procesos in the page
        # current_projects = get_projects(driver, current_project_count)
        # # print(f"\n\n{projects}")
        # for project in current_projects: # for every id run scrapy requests
            # # save project to memory list
            # projects_ids.append(project)
            # # write project to disk
            # projects_file.write(f"{project},\n ")
        # # add offset to get new projects
            # current_project_count += offset
        # print(f"\nproject: {current_project_count} out of {total_project_count}")
    # projects_file.write(f"]")
    # # exit session
    # driver.quit()

    # return bothe the usre data and the projects_ids, in memory
    return (user_data, projects_ids)

login_script()
