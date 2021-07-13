from manage_files import change_status, delete_date

import requests
import re
import os.path
from bs4 import BeautifulSoup
from typing import Optional
from datetime import datetime
import shutil


def get_list(file: str) -> None:
    file_name = f"Raport Ceneo.csv"
    date = datetime.now().strftime('%d.%m.%Y')
    create_file(file_name)
    with open(file, 'r', encoding='utf-8') as f:
        ids = [i.strip() for i in f.readlines()]
        count = 1
        for id in ids:
            link = f"https://www.ceneo.pl/{id}"
            print(f'{count} na {len(ids)}')
            count += 1
            get_product_from_list(file_name, None, link, id, date)
    return None


def create_file(file_name: str) -> None:
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Aktualny;Data;Id produktu;Nazwa produktu;Sklep;Cena\n')
    return None


def write_to_file(file_name: str, line: str) -> None:
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(line)
    return None


def get_product_from_list(file_name: str, product_name: Optional[str], link: str, id: str, date: str,
                          remaining_offers: bool = False) -> None:
    product_page = requests.get(link, timeout=50)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    if product_name is None:
        product_name = product_soup.find('h1', class_='product-top__product-info__name').text.strip()
    product_containers = product_soup.find_all('li', class_='product-offers__list__item')
    for product in product_containers:
        div = product.find('div', class_='product-offer__container')
        price = div.get('data-price')
        if price is not None:
            price = price.replace('.', ',')
        else:
            button = div.find('button')
            price = button.get('data-price').replace('.', ',')
        details = product.find('div', class_='product-offer__details')
        offer = details.find('a', class_='link js_product-offer-link').text.strip()
        shop_name = re.search('Opinie o ([a-zA-Z0-9 -]+)', offer).groups()[0]
        line = ';'.join(['', date, id, product_name, shop_name, price]) + '\n'
        write_to_file(file_name, line)

    if not remaining_offers:
        remaining_divs = product_soup.find_all('div', class_='show-remaining-offers')
        if len(remaining_divs):
            remaining_id = re.search('([0-9]+clr).?', remaining_divs[0].find('a').get('href')[1:]).groups()[0]
            remaining_link = f"https://www.ceneo.pl/{remaining_id}"
            # print(remaining_link)
            get_product_from_list(file_name, product_name, remaining_link, id, date, True)

    return None


if __name__ == '__main__':
    filename = 'Raport Ceneo.csv'

    print(datetime.now())
    get_list('list.txt')
    print(datetime.now())
    change_status(filename)
    shutil.copy(filename, r'\\fssrv4new\Ekonomiczny\DZIAŁ KONTROLINGU\Marcin\CENEO')

    # delete_date(filename, '12.07.2021')
