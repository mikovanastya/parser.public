import requests
from bs4 import BeautifulSoup#библтотека для парсинга
import csv
import os #для автоматического открытия файла
import time


URL = 'https://auto.ria.com/legkovie/jeep/' #ссылка на запрашиваемый сайт, категорию того что нужно
# user-agent: передаётся название браузера операционной системы
#headers чтобы не посчитал нас за бота имитируем работу браузера
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36',
           'accept': '*/*'} ##словарь, в который мы отправим заголовки
HOST = 'https://auto.ria.com'#чтобы можно было перейти по ссылки
FILE = 'cars.csv'

#аргументы: url страницы, с которой необходимо получить контент,
#params - опциональный аргумент, нужен чтобы мы могли передавать номера страниц, чтобы спарсить все(дополнительные параметры к адресу URL)
#(когда переходим на страницу URL, то джипов мб больше чем на 1 стр, поэтому к ссылке добавляются нове параметры params)
def get_html(url, params=None):
    r = requests.get(url , headers=HEADERS, params=params)
    return r


#функция для количества страниц ()узнает сколько их)
#если не автомат, то в URL пишем другой адрес
def get_pages_count(html):#количество страниц
    soup = BeautifulSoup(html, 'html.parser')

    pagination = soup.find_all('span', class_='mhide')#Пагина́ция-порядковая нумерация страниц
    #получаем порядок нумерации страниц
    if pagination:#проверяем есть ли пагинация
        return int(pagination[-1].get_text())#последний элемент
    else:
        return 1
    print(pagination)



#html.parser - тип документа с которым мы работаем
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')#cоздаются объекты пайтон с которыми можно работать
    items = soup.find_all('div', class_='content-bar')

    cars = []#пустой словарь.куда будем складывать каждый элемент
    for item in items:
        #проверяем есть ли цена в гривнах
        uah_price = item.find('span', class_='grey size15')
        #если цена есть
        if uah_price:  # если объект есть
            uah_price = uah_price.get_text() #.replace('*','') замена
        else:
            uah_price = 'цены нет(цену уточняйте)'
        cars.append({#добавляем список в словари, у каждого списка свой словарь
            'title': item.find('div', class_='head-ticket').find_next('span').get_text(strip=True),#strip=true убирает пробелы
            'usd_price': item.find('span', class_='bold green').get_text(strip=True),
            'link': HOST + item.find('a', class_ ='').get('href'),
            'uah_price': uah_price,
            'city': item.find('li', class_='item-char view-location js-location').find_next('span').get_text(strip=True),
        }) #добавлять в список словари
    return cars


#функция, которая сохраняет файл
def save_file(items, path): #путь к файлу куда необходимо сохранять
    with open(path, 'w', newline = '') as file: #w - открываем файл для записи, если файла нет, то он будет создан, если есть, то будет очищен и запишутся новые данные
        writer = csv.writer(file, delimiter = ';') #объект writer переменная также записана, указываем указатель открытого файла file, delimiter - разделитель для csv файлов, чтобы нормально открывались в excel
        writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в UAh', 'Город'])
        #проходим по коллекции, те берем конкретный автомобиль и записываем его файл csv
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])
    #закрывать файл не нужно тк с конструкцией with open .. он будет закрыт автоматически

#Метод GET указывает на то, что происходит попытка извлечь данные из определенного ресурса. Для того, чтобы выполнить запрос GET
#HTML - это код, который используется для структурирования и отображения веб-страницы и её контента.
def parse():
    URL = input('Введите URL:')
    URL = URL.strip()  # для обрезания ссылки
    html = get_html(URL)
    #print(html.status_code)
    if html.status_code == 200:
        #cars = get_content(html.text)
        cars = []
        pages_count = get_pages_count(html.text)

        #цикл, чтобы парсить все страницы сразу
        for page in range(1, pages_count + 1):  # метод с первой стрицы до последнего увеличиваем на 1 так как последний элемент не участвует поэтому мы хотим чтобы он участвовал

            print(f'парсинг страниц {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))#расширяем список
        save_file(cars, FILE)  # передаем ей полученные автомобили
        print(f'Получено {len(cars)} автомобилей')
        os.startfile(FILE) #автоматическое открытие файла
        # cars = get_content(html.text)
    else:
        print('Error')

parse()