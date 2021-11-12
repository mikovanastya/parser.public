import requests
from bs4 import BeautifulSoup

URL = 'https://www.avito.ru/krasnodar/avtomobili/bmw-ASgBAgICAUTgtg3klyg?cd=1&radius=0'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36',
           'acces': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-content-UnQQ4')#карточки
    cars = []
    for item in items:
        cars.append({
            'price': item.find('span', class_='price-text-E1Y7h text-text-LurtD text-size-s-BxGpL').get_text(strip=True),
            #'city': item.find('div', class_='geo-georeferences-Yd_m5 text-text-LurtD text-size-s-BxGpL').find_next('span').get_text(strip=True),
            #'title': item.find('h3', class_='title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO').get_text()
        })
    return cars

def parse():
    html = get_html(URL)
    #print(html)
    if html.status_code == 200:
        cars = get_content(html.text)
        #print(html.text)
    else:
        print('Error')

parse()

