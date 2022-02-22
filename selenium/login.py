import os
import time
import random
from lxml import etree
from functions import *
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.by import By

def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def scrapy_IDs(): 
    """ This Script handles the Selenium login script """
    # define constants for website
    offset = 20 # number of projects we get from a page
    current_project_count = 0 # start at zero
    total_project_count = None # must define late on
    projects_ids = [] # list to store ids in memory
    
    # read from config files
    env = dotenv_values('.env')  
    urls = dotenv_values('.urls')  
    search_parameters = dotenv_values('search_parameters.txt')

    # get the baseurl make abosulte links
    baseurl = urls['PROJECT_URL'] 

    # read headless option
    is_headless = env['HEADLESS']
    print(f"Headless mode is set to: {is_headless}")
    if(is_headless == "true" or is_headless == "True"):
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

    # remove the readonly atribute to be able to write date
    try: 
        start_date = search_parameters["FECHA_DESDE"]
        end_date = search_parameters["FECHA_HASTA"]
    except:
        print(f"Could not get FECHA_DESDE or FECHA_HASTA\n Quiting")
        exit()

    # divide the given date into batches of 200 days
    date_batches = divide_dates(start_date, end_date)
    print(f"date_batches: {date_batches}")

    for date_batch in date_batches:
        try:
            print(f'starting with date: {date_batch}')
            # For some reason the server only gives us user_data,
            # after we load the 'Procesos' page
            driver.get(urls['QUERY_PROJ_URL']) 

            # input parameter into search 
            input_seach_parameters(date_batch, driver)
            
            # run search function 
            driver.execute_script('botonBuscar()')

            # get the total number of projects
            total_project_count = get_total_project_count(driver)
            
            # base url for the 
            current_project_count = 0
            while(current_project_count <= total_project_count):
                timeDelay = random.randrange(0, 3)
                time.sleep(timeDelay)
                    # search for procesos
                # get the ID's for every procesos in the page
                current_projects = get_projects(driver, current_project_count)
                # print(f"\n\n{projects}")
                for project in current_projects: # for every id run scrapy requests
                    # save project to memory list
                    projects_ids.append(project)
                    # write project to disk
                    projects_file.write(f"{project},\n ")
                # add offset to get new projects
                #current_project_count += offset
                current_project_count += 5000
                print(f"\nprojects: {current_project_count} out of {total_project_count}")
            projects_file.write(f"]")

        except Exception as e:
	        print("ERROR : "+str(e))

    # get user data from the selenium driver
    (cookies, data) = get_driver_user_data(driver)

    # clean the reuqest body
    request_body = organize_body(data)
        
    # request body 
    user_data = { 'cookies': cookies, 'request_body': request_body }

    # exit session
    driver.quit()

    # return bothe the usre data and the projects_ids, in memory
    return (user_data, projects_ids)

def test_script(): 
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

    """-----start script process-----"""

    # create driver   
    driver = create_driver(headless=headless)

    # For some reason the server only gives us user_data,
    # after we load the 'Procesos' page
    driver.get(urls['QUERY_PROJ_URL']) 
    
    # input parameter into search 
    input_seach_parameters(driver)

    # exit session
    #driver.quit()

#test_script()

scrapy_IDs()

