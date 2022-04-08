# this modeule read the file from the dotenv files and export the for other modeules to read

from dotenv import dotenv_values

secret = dotenv_values('.secret')  

options = dotenv_values('options.txt')  

urls = dotenv_values('.urls')  

if urls:
    baseurl = urls['PROJECT_URL'] 

    resumen_contractual_url= urls['RESUMEN_CONTRACTUAL']

