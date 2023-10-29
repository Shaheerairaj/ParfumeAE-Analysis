import pandas as pd
import requests
import bs4
import lxml

def get_frag_types():

    '''
    Grabs the fragrance types from the main page of parfum.ae
    '''

    result_main_page = requests.get("https://www.parfum.ae/fragrance/")
    soup_main_page = bs4.BeautifulSoup(result_main_page.text,'lxml')

    # Contains elements for frag types
    elements = soup_main_page.select('.innerlistside')[0].select('a')

    frag_type_dict = {}

    # Get fragrance type names and their URLs
    for element in elements:
        frag_type_dict[element.text] = element['href']

    return frag_type_dict



def prod_list_our_creations(frag_type_dict):

    '''
    Grabs the fragrace type dictionary containing the URLs for each fragrance type
    and searches for all products listed under the Our Creations type
    '''

    result_frag_type = requests.get(frag_type_dict['Our Creations'])
    soup_frag_type = bs4.BeautifulSoup(result_frag_type.text,'lxml')

    last_page = soup_frag_type.select('.pagination')[0].select('li')[-1].select('a')[0]['href'].split('page-')[1][:-1]
    prod_listing_dict = {}

    for page in range(1, int(last_page)+1):
        url = frag_type_dict['Our Creations'] + '/page-' + str(page)

        result_frag_type = requests.get(url)
        soup_frag_type = bs4.BeautifulSoup(result_frag_type.text,'lxml')

        h3_elements = soup_frag_type.select('.product__detail__list.mt-4 h3')
        
        for h3 in h3_elements:
            prod_listing_dict[h3.text[1:]] = h3.find('a')['href']

    return prod_listing_dict


def prod_info_our_creations(prod_listing_dict):

    products = {}

    for key,val in prod_listing_dict.items():
        prod_result = requests.get(val)
        prod_soup = bs4.BeautifulSoup(prod_result.text,'lxml')
        
        prod_dict = {}

        try:
            prod_dict['productTitle'] = prod_soup.select('.product-main__title')[0].text
        except (IndexError, AttributeError):
            prod_dict['productTitle'] = None

        try:
            prod_att_hot = prod_soup.select('.hot__product.product-main__hot')
            prod_dict['hot'] = True if 'hot' in str(prod_att_hot) else False
        except (IndexError, AttributeError):
            prod_dict['hot'] = None

        try:
            prod_dict['imitationOf'] = prod_soup.find('span', style='touch-action: manipulation; font-weight: bolder; font-size: 18px;').text
        except (AttributeError, TypeError):
            prod_dict['imitationOf'] = None

        try:
            prod_dict['partOfFragrance'] = [element.text.replace('\xa0','').replace('This perfume is part of','') for element in prod_soup.select('p') if 'This perfume is part of' in element.text][0]
        except (IndexError, AttributeError):
            prod_dict['partOfFragrance'] = None

        try:
            prod_dict['topNotes'] = [element.text.replace('Top Notes:\xa0', '') for element in prod_soup.select('p') if 'Top Notes:' in element.text][0]
        except (IndexError, AttributeError):
            prod_dict['topNotes'] = None

        try:
            prod_dict['middleNotes'] = [element.text.replace('Middle Notes:\xa0', '') for element in prod_soup.select('p') if 'Middle Notes:' in element.text][0]
        except (IndexError, AttributeError):
            prod_dict['middleNotes'] = None

        try:
            prod_dict['baseNotes'] = [element.text.replace('Base Notes:\xa0', '') for element in prod_soup.select('p') if 'Base Notes:' in element.text][0].split(', ')
        except (IndexError, AttributeError):
            prod_dict['baseNotes'] = None

        try:
            prod_dict['concentration'] = [element.text.replace('Concentration:\xa0', '') for element in prod_soup.select('p') if 'Concentration' in element.text][0]
        except (IndexError, AttributeError):
            prod_dict['concentration'] = None

        try:
            prod_dict['overallRating'] = len(prod_soup.select('.stars__wrap')[0].find_all('i', class_='fas fa-star'))
        except (IndexError, AttributeError):
            prod_dict['overallRating'] = None

        try:
            prod_dict['totalReviews'] = int(prod_soup.select('.stars__wrap')[0].text.replace('\n','').split(' ')[0])
        except (IndexError, AttributeError, ValueError):
            prod_dict['totalReviews'] = None


        products[prod_dict['productTitle']] = prod_dict

    return products