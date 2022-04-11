# this modeule handle all the paramters th euser can pass to the spider
# this modeule read the file from the dotenv files and export the for other modeules to read 

import os
from dotenv import dotenv_values

# read files 
secret  = dotenv_values('.secret')  
options = dotenv_values('options')  
urls    = dotenv_values('urls')  


# check is a value if has the string none
def is_true_value(value):
    if value is not None:
        if(value == "true" or value == "True"):
            return True
    return False

# load the screate files
if secret is not None:
    ruc = secret['RUC']
    username = secret['USER']
    password = secret['PASS']
else:
    print('could not load .secret file')
    
# load options from options file
if options is not None:
    # add the location/name of the detinations folder
    dest_folder = options['DEST_FOLDER']
    # headless browser
    is_headless = options['HEADLESS']
    # stealth mode
    is_stealthy = options['STEALTH_MODE'] 
    # are we down downloading files
    is_downloading_files = options['DOWNLOAD_FILES'] 
    # proxy mode
    is_proxy_mode = options['PROXY_MODE']
    # check is value are true
    is_headless = is_true_value(is_headless)
    is_stealthy = is_true_value(is_stealthy)
    is_downloading_files = is_true_value(is_downloading_files)
    is_proxy_mode = is_true_value(is_proxy_mode)
    # search paramters
    palabras_claves = options["PALABRAS_CLAVES"]
    entidad_contratante = options["ENTIDAD_CONTRATANTE"]
    tipo_de_contratacion = options["TIPO_DE_CONTRATACION"]
    tipo_de_compra = options["TIPO_DE_COMPRA"]
    codigo_de_proceso = options["CODIGO_DEL_PROCESO"]
    fecha_hasta = options["FECHA_HASTA"]
    fecha_desde = options["FECHA_DESDE"]
else:
    print('could not load options file')
    exit()

# get the url
if urls is not None:
    login_url = urls['LOGIN_URL']
    # this is the base of the project url
    project_url = urls['PROJECT_URL'] 
    # this is the  base of the resumen contractual url
    resumen_contractual_url = urls['RESUMEN_CONTRACTUAL']
    # this is the domain of the website
    domain = urls['DOMAIN']
    # this it the search url for the projectos de regimens especiales
    regimenes_especiales_url = urls['REGIMEN_ESPECIALES']
    # this it the search url for the projectos de procesos especiales
    procesos_especiales_url = urls['PROCESOS_ESPECIALES']
    # this is the homw url of the website
    home_url = urls['HOME_URL']
    # this is the base, for queries about a project`
    query_project_url = urls['QUERY_PROJ_URL']
    # this is the base usrl rof the proces
    procesos_url = urls['PROCESOS_URL']
else:
    print('could not load urls file')
    exit()


