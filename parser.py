import csv

import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/newauto/marka-hyundai/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в $'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price']])


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')
    cars = []
    for items in items:
        cars.append({
            'title': items.find('div', class_='proposition_title').get_text(strip=True),
            'link': HOST + items.find('h3', class_='proposition_name').find('a').get('href'),
            'usd_price': items.find('span', class_='green bold size18').get_text(strip=True)
        })
    return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
    else:
        print('Error')


parse()
