from dotenv import load_dotenv
from dotenv import dotenv_values


handle = dotenv_values('.env')

user = handle["USER"]
password = handle["PASS"]
ruc = handle["RUC"]

