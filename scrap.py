import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
total_page = 20

d = {"URL": [], "Name": [], "Price": [], "Rating": [], "review": [],
     "Description": [], "ASIN": [], "Product_Description": [], "Manufacturer": []}


def get_url(url):
    while (True):
        delay = 0.01
        page = requests.get(url)
        if page.status_code == 200:
            break
        else:
            time.sleep(delay)
            continue

    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


for page in range(1, total_page + 1):
    page_url = url + str(page)
    soup = get_url(page_url)
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    print(len(products))

    for product in products:
        product_url = "https://www.amazon.in" + str(product.find('a', {
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href'])
        product_name = product.find(
            'span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()

        if product.find('span', {'class': 'a-price-whole'}):
            product_price = product.find(
                'span', {'class': 'a-price-whole'}).text.replace(',', '')
        else:
            product_price = 'null'

        if product.find('span', {'class': 'a-icon-alt'}):
            rating = product.find(
                'span', {'class': 'a-icon-alt'}).text.split()[0]
        else:
            rating = 'null'

        if product.find('span', {'class': 'a-size-base'}):
            review = product.find(
                'span', {'class': 'a-size-base'}).text.replace(',', '')
        else:
            review = '0'

        # new_response = requests.get(product_url)
        # new_soup = BeautifulSoup(new_response.text, 'html.parser')

        print(product_url)
        new_soup = get_url(product_url)

        if new_soup.find('span', {'class': 'a-list-item'}):
            description = new_soup.find(
                'span', {'class': 'a-list-item'}).text.strip()
        else:
            description = 'null'

        if new_soup.find('th', string='ASIN'):
            value = new_soup.find('th', string='ASIN').find_next('td')
            asin = value.text.strip()
        else:
            asin = 'null'

        if new_soup.find('span', {'id': 'productTitle'}):
            product_description = new_soup.find(
                'span', {'id': 'productTitle'}).text.strip()
        else:
            product_description = 'null'

        if new_soup.find('a', {'id': 'bylineInfo'}):
            manufacturer = new_soup.find(
                'a', {'id': 'bylineInfo'}).text.strip()

        else:
            manufacturer = 'null'

        d['URL'].append(product_url)
        d['Name'].append(product_name)
        d['Price'].append(product_price)
        d['Rating'].append(rating)
        d['review'].append(review)
        d['Description'].append(description)
        d['ASIN'].append(asin)
        d['Product_Description'].append(product_description)
        d['Manufacturer'].append(manufacturer)


amazon_df = pd.DataFrame.from_dict(d)
amazon_df.to_csv("amazon_data.csv", header=True, index=False)
