import sys
import os
import time
import random
import traceback
import numpy as np
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from ComprasPublicas_Scrapper import params 
from ComprasPublicas_Scrapper.selenium_scripts.functions import *

def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def scrap_project_ids(login=True, url=None): 
    """ This Script handles the Selenium login script """
    # define constants for website
    offset = 20 # number of projects we get from a page
    current_project_count = 0 # start at zero
    total_project_count = None # must define late on
    projects_ids = [] # list to store ids in memory
    # read from config files

    # make destination folder
    # if it does not exits
    make_folder(params.dest_folder)

    # create file where to store all the donwloaded project ids
    # filename for the writing the project ids

    filename = os.path.join(params.dest_folder, 
            'extracted_poject_ids')
    npy_file = filename + '.npy'

    does_projects_ids_exists = os.path.isfile(npy_file)

    # check if the projects_id file exist  
    if(does_projects_ids_exists): 
            loaded_array = np.load(npy_file, allow_pickle=True)
            # Converting the Numpy array to a normal Python list
            projects_ids = loaded_array.tolist()
            print('loaded_array legnth')
            print(len(projects_ids))


    """ ---- start script process ---- """

    # create driver   
    driver = create_driver(headless=params.is_headless) 

    """ Here we don't handle the authentification, 
    but go straight to the passed url  """

    if login is True:
        # load login page, it is set to login
        driver.get(params.login_url)

        # handle the login 
        submit_login_handler(driver)

        # handle authentication result
        authentication_handler(driver)

    # remove the readonly atribute to be able to write date
    try: 
        start_date = params.fecha_desde 
        end_date = params.fecha_hasta
    except:
        print(f"Could not get FECHA_DESDE or FECHA_HASTA in the options file\n Quiting")
        traceback.print_exc()
        exit()

    # divide the given date into batches of 200 days
    date_batches = divide_dates(start_date, end_date)
    print(f"date_batches: {date_batches}")
    print(date_batches)

    for date_batch in date_batches:
        try:
            print(f'starting with date: {date_batch}')
            # For some reason the server only gives us user_data,
            # after we load the 'Procesos' page
            if url is not None: 
                # if url is passed
                driver.get(url) 
            else:
                driver.get(params.query_project_url) 

            # input parameter into search 
            input_seach_parameters(date_batch, driver)
            
            # run search function 
            driver.execute_script('botonBuscar()')

            # get the total number of projects
            total_project_count = get_total_project_count(driver)
            
            # base url for the 
            current_project_count = 0
            while(current_project_count <= total_project_count):
                if(params.is_stealthy): 
                    # wait for a range of 0 to 3 second before any query
                    time.sleep(random.randrange(0, 3))
                # search for procesos
                # get the ID's for every procesos in the page
                current_projects = get_projects(driver, current_project_count)
                # print(f"\n\n{projects}")
                for project in current_projects: # for every id run scrapy requests
                    # save project to memory list
                    if any(p for p in projects_ids if p['code'] == project['code']):
                    #if project in projects_ids:
                        # check if it is not already in array
                        print('project already in list')
                    else:
                        projects_ids.append(project)
                # add offset to get new projects
                current_project_count += offset
                #current_project_count += 5000 # debug pourpouse
                print(f"\nExtracted project id: {current_project_count} out of {total_project_count}")
        except Exception as e:
            print("ERROR : "+str(e))
            traceback.print_exc()

    # save file array
    np.save(filename, np.array(projects_ids));

    #save as plain text file
    projects_file = open(filename + '.py', 'w')
    projects_file.write(f"projects_ids = [\n")
    print(len(projects_ids))
    for project in projects_ids: # for every id run scrapy requests
        # write project to disk
        projects_file.write(f"{project},\n ")
    #end array           
    projects_file.write(f"]")

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
   
# don't run script, for debugging only
#url = params.resgimenes_especiales_url
#scrap_project_ids(nologin=True, url)

