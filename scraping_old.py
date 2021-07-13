from typing import Optional

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime


def create_file(file_name: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('Id produktu;Nazwa produktu;Pozycja na liscie;Sklep;Cena\n')
    return None


def write_to_file(file_name: str, line: str) -> None:
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(line)
    return None


def find_last_page(url: str) -> int:
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')
    return int(soup.find('input', id='page-counter').get('data-pagecount'))


def scraping(url: str) -> None:
    category = urlparse(url).path[1:]
    file_name = f"Ceneo {category} {datetime.now().strftime('%d.%m.%Y %H.%M')}.csv"
    date = datetime.now().strftime('%d.%m.%Y')
    create_file(file_name)
    last_page = find_last_page(url)
    for page in range(last_page):
        print(f'Page {page + 1} of {last_page}')
        link = url + ';0020-30-0-0-' + str(page) + '.htm'
        get_products_list(link, file_name)
    return None


def get_products_list(url: str, file_name: str) -> None:
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_containers = soup.find_all('div', class_='cat-prod-row')
    for product in product_containers:
        scope = product.find('strong', class_='cat-prod-row__name')
        product_name = scope.text.strip()
        id = re.search('([0-9]+).?', scope.find('a').get('href')[1:]).groups()[0]
        link = f"https://www.ceneo.pl/{id}"
        go_to_shop = product.find_all('a', class_='go-to-shop')
        if len(go_to_shop):
            get_one_product(file_name, product, product_name)
        else:
            get_product_from_list(file_name, product_name, link, id)
    return None


def get_list(file: str) -> None:
    file_name = f"Ceneo {datetime.now().strftime('%d.%m.%Y %H.%M')}.csv"
    date = datetime.now().strftime('%d.%m.%Y')
    create_file(file_name)
    with open(file, 'r', encoding='utf-8') as f:
        ids = [i.strip() for i in f.readlines()]
        print(ids)
        i = 1
        for id in ids:
            link = f"https://www.ceneo.pl/{id}"
            print(i)
            i += 1
            get_product_from_list(file_name, None, link, id)
    return None


def get_product_from_list(file_name: str, product_name: Optional[str], link: str, id: str) -> None:
    product_page = requests.get(link, timeout=10)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    if product_name is None:
        product_name = product_soup.find('h1', class_='product-top-2020__product-info__name').text.strip()
    product_containers = product_soup.find_all('li', class_='product-offers-2020__list__item')
    for product in product_containers:
        div = product.find('div', class_='product-offer-2020__container')
        position = div.get('data-position')
        if position is not None:
            price = div.get('data-price').replace('.', ',')
        else:
            button = div.find('button')
            position = button.get('data-position')
            price = button.get('data-price').replace('.', ',')
        details = product.find('div', class_='product-offer-2020__details')
        offer = details.find('a', class_='link js_product-offer-link').text.strip()
        shop_name = re.search('Opinie o ([a-zA-Z0-9 -]+)', offer).groups()[0]
        line = ';'.join([id, product_name, position, shop_name, price]) + '\n'
        write_to_file(file_name, line)
    return None


def get_one_product(file_name: str, product: BeautifulSoup, product_name: str) -> None:
    price = product.find('span', class_='price').text.replace(' ', '')
    shop_url = product.get('data-shopurl')
    shop_name = get_shop_name(shop_url) if shop_url is not None else ''
    line = ';'.join(['', product_name, '', shop_name, price]) + '\n'
    write_to_file(file_name, line)
    return None


def get_shop_name(link: str) -> str:
    pattern = '(https?://)?(www.)?([0-9a-zA-Z]+)\..'
    return re.search(pattern, link).groups()[2]


if __name__ == '__main__':
    print(datetime.now())
    # url = 'https://www.ceneo.pl/Telewizory'
    # url = 'https://www.ceneo.pl/AGD_wolnostojace'
    # url = 'https://www.ceneo.pl/AGD_do_zabudowy'
    # url = 'https://www.ceneo.pl/Male_AGD_do_kuchni'
    # url = 'https://www.ceneo.pl/Depilatory_i_golarki_damskie'
    # url = 'https://www.ceneo.pl/Odkurzacze'
    # url = 'https://www.ceneo.pl/Smartfony'
    # url = 'https://www.ceneo.pl/Laptopy'
    # url = 'https://www.ceneo.pl/Tablety_PC'
    # scraping(url)
    get_list('list.txt')
    print(datetime.now())
