import os
import pandas as pd
import requests
import bs4
import lxml
import functions.web_scrapper_functions as scrpr
import mysql.connector
import json
import datetime

import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(filename='Parfum AE Web Scrapper Log.log', level=logging.INFO,
format='%(asctime)s:%(levelname)s:%(message)s')

frag_type_dict = scrpr.get_frag_types()
print("Available fragrance types: \n", frag_type_dict.keys())

prod_list_dict = {}
start_time = datetime.datetime.now()

for key, val in frag_type_dict.items():
    try:
        logging.info('Currently scrapping ', key)
        prod_list_dict[key] = scrpr.prod_list(val)
        logging.info('Number of products: ', len(prod_list_dict[key]))
    except:
        logging.error("Error in ", key)
end_time = datetime.datetime.now()
time_taken = end_time - start_time
logging.info(f"Time taken to retrieve list of all products: {time_taken}")


# Testing using only 5 items per category

# temp_dict = {}
# for key, prod in prod_list_dict.items():
#     for i in range(0, 5):


start_time = datetime.datetime.now()
products = scrpr.prod_info(prod_list_dict)
end_time = datetime.datetime.now()
time_taken = end_time - start_time
logging.info(f"Time taken to retrieve information for each product: {time_taken}")

print(products)