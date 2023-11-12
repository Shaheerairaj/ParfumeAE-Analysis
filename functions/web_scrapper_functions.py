import pandas as pd
import requests
import bs4
import lxml

import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(filename='Parfum AE Web Scrapper Log.log', level=logging.INFO,
format='%(asctime)s:%(levelname)s:%(message)s')


def get_frag_types():
    '''
    Grabs the fragrance types from the main page of parfum.ae
    '''
    r = requests.get("https://www.parfum.ae/fragrance/")
    s = bs4.BeautifulSoup(r.text, 'lxml')

    # Contains elements for frag types
    elements = s.select('.innerlistside')[0].select('a')

    frag_type_dict = {}

    # Get fragrance type names and their URLs
    for element in elements:
        frag_type_dict[element.text] = element['href']

    return frag_type_dict





def prod_list(url):
    '''
    Grabs the fragrace type dictionary containing the URLs for each fragrance type
    and searches for all products listed under the Our Creations type
    '''

    r = requests.get(url)
    s = bs4.BeautifulSoup(r.text, 'lxml')

    if len(s.select(".pagination")) >= 1:
        last_page = s.select('.pagination')[0].select(
            'li')[-1].select('a')[0]['href'].split('page-')[1][:-1]
        prod_listing_dict = {}

        for page in range(1, int(last_page)+1):
            url = url + '/page-' + str(page)

            r = requests.get(url)
            s = bs4.BeautifulSoup(r.text, 'lxml')

            h3_elements = s.select('.product__detail__list.mt-4 h3')

            for h3 in h3_elements:
                prod_listing_dict[h3.text[1:]] = h3.find('a')['href']

    else:
        prod_listing_dict = {}

        r = requests.get(url)
        s = bs4.BeautifulSoup(r.text, 'lxml')

        h3_elements = s.select('.product__detail__list.mt-4 h3')

        for h3 in h3_elements:
            prod_listing_dict[h3.text[1:]] = h3.find('a')['href']

    return prod_listing_dict





def prod_info(prod_list_dict):
    products = []
    for frag_type, prod_list in prod_list_dict.items():
        for key, val in prod_list.items():
            r = requests.get(val)
            s = bs4.BeautifulSoup(r.content, 'lxml')

            if frag_type in ['Our Creations','Dahn Al Oud']:
                try:
                    id = s.select('[data-product_id]')[0].get('data-product_id')
                except:
                    id = None
                    logging.error(f"Error retrieving id for product: {key} at url: {val}")
                try:
                    name = s.select('.product-main__title')[0].text
                except:
                    name = None
                    logging.error(f"Error retrieving name for product: {key} at url: {val}")
    
                try:
                    stars= 5 - len(s.select('div.stars__wrap')[0].select(".fas.fa-star.graystar"))
                except:
                    stars = None
                    logging.error(f"Error retrieving stars for product: {key} at url: {val}")
    
                try:
                    reviews_total = int(s.select('div.stars__wrap')[0].select('a')[0].text.replace(' reviews',''))
                except:
                    reviews = None
                    logging.error(f"Error retrieving reviews for product: {key} at url: {val}")
    
                try:
                    price = float(s.select('span.product-js-price')[1].text.replace('AED ',''))
                except:
                    price = None
                    logging.error(f"Error retrieving price for product: {key} at url: {val}")
    
                if len(s.select('.hot__product.product-main__hot')) > 0:
                    hot = True
                else:
                    hot = False

                try:
                    reviews = product_reviews(id)
                except:
                    reviews = None
                    logging.error(f"Error retrieving reviews for product: {key} at url: {val}")
    
            else:
                try:
                    id = s.select('[data-product_id]')[0].get('data-product_id')
                except:
                    id = None
                    logging.error(f"Error retrieving id for product: {key} at url: {val}")
                try:
                    name = s.select('.title.page-title')[0].text
                except:
                    name = None
                    logging.error(f"Error retrieving name for product: {key} at url: {val}")
    
                try:
                    stars = 5 - len(s.select('div.stars__wrap')[0].select(".fas.fa-star.graystar"))
                except:
                    stars = None
                    logging.error(f"Error retrieving stars for product: {key} at url: {val}")
    
                try:
                    reviews_total = int(s.select('div.review-links')[0].select('a')[0].text.replace(' reviews',''))
                except:
                    reviews = None
                    logging.error(f"Error retrieving reviews for product: {key} at url: {val}")
    
                try:
                    price = float(s.select('div.product-price')[0].text.replace('AED ',''))
                except:
                    price = None
                    logging.error(f"Error retrieving price for product: {key} at url: {val}")
    
                if len(s.select('.hot__product.product-main__hot')) > 0:
                    hot = True
                else:
                    hot = False
                try:
                    reviews = product_reviews(id)
                except:
                    reviews = None
                    logging.error(f"Error retrieving reviews for product: {key} at url: {val}")
                    
    
            products.append([id,name, stars, price, reviews_total, price, hot, reviews])

    return products





def product_reviews(prod_id):
    # Make request for the initial review page
    url_main = f'https://www.parfum.ae/index.php?route=product/product/review&product_id={prod_id}&page=1'
    r_main = requests.get(url_main)
    s_main = bs4.BeautifulSoup(r_main.content, 'lxml')
    
    # Extract review data
    reviews = []
    page = 1
    
    while True:
        url = f'https://www.parfum.ae/index.php?route=product/product/review&product_id={prod_id}&page={page}'
        r = requests.get(url)
        s = bs4.BeautifulSoup(r.content, 'lxml')
    
        for table in s.select("table"):
            reviewer_name = table.select("strong")[0].text.replace('\xa0',' ')
            reviewer_text = table.select("p")[0].text
            reviewer_rating = len(table.select(".fa.fa-star.fa-stack-2x"))
            reviews.append([reviewer_name, reviewer_text, reviewer_rating])
    
        if len(s.select('table')) == 0:
            break
    
        page += 1

    return reviews
