from config import Apartment, headers, PAGES, FLATS, unique_flat_links, flat_links, flat_dataset, root_url
import csv
import os
from time import sleep
import pandas as pd
import time

import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor


# получение количества страниц
def get_page_count(url):
    html_text = get_html_text(url)
    soup = bs(html_text, 'html.parser')
    page_count = soup.find_all('span', class_='base-module__text___3Z3Vp')[-2].text.strip()
    return page_count


# получение html кода по url
def get_html_text(url):
    print("try to ger html by url " + url)
    response = requests.get(url, headers=headers, timeout=10)
    while response.status_code != 200:
        if response.status_code == 403:
            print("Сайт тебя заблокировал")
        sleep(5)
        response = requests.get(url, headers=headers, timeout=10)

    return response.text


# получение всех ссылок со страницы
def get_flat_links(html_text):
    soup = bs(html_text, 'html.parser')
    items = soup.find_all('li', class_='OffersSearchList__item')

    links = []
    for item in items:
        # название и ссылке на объявление
        title_element = item.find('div', class_='LayoutSnippet__title')
        if title_element:
            link = title_element.find('a', class_='LinkSnippet')['href']
            links.append(link.strip())

    return links


# сохранение общей страницы
def download_page(url):
    html_text = get_html_text(url)
    url = url.replace("/", "").replace(":", "").replace("*", "").replace(".", "").replace("?", "")
    with open(f'{PAGES}\\{url}.html', "w", encoding="utf-8") as file_with_flat_page:
        file_with_flat_page.write(html_text)


# сохранение страницы квартиры
def download_flat_page(url):
    flat_html_text = get_html_text(url)
    url = url.replace("/", "").replace(":", "").replace("*", "").replace(".", "").replace("?", "")
    with open(f'{FLATS}\\{url}.html', "w", encoding="utf-8") as file_with_flat_page:
        file_with_flat_page.write(flat_html_text)


# парсинг страницы объявления
def get_flat_data(flat_data_file):
    with open(f"{FLATS}\\{flat_data_file}", 'r', encoding="utf-8") as flat_data:
        data = flat_data.read()

    soap = bs(data, 'html.parser')

    new_flat = Apartment()
    parse_flat(new_flat, soap)
    return new_flat


# получение значений во всех полезных тегах
def parse_flat(flat, soap):
    set_flat_title(flat, soap)
    set_flat_address(flat, soap)
    set_flat_metro(flat, soap)
    set_flat_prise(flat, soap)
    set_flat_description(flat, soap)
    set_flat_specifications(flat, soap)


# название объявления
def set_flat_title(flat, soap):
    title_element = soap.find('h1', class_='fonts-module__h1___2QWY_')
    if title_element:
        flat.title = title_element.text.strip()


# адрес
def set_flat_address(flat, soap):
    address_elements = soap.find_all('a', class_='ClClickableAddress__link')
    if address_elements:
        flat.address = ", ".join([element.text.strip() for element in address_elements])


# метро
def set_flat_metro(flat, soap):
    metro_link = soap.find('a', class_='SubwayStation__link')
    if metro_link:
        flat.metro = metro_link.text.strip()


# описание объявления
def set_flat_description(flat, soap):
    description_element = soap.find('div', class_='fonts-module__primary___2PNSt OfferCard__description')
    if description_element:
        flat.description = description_element.text.strip()


# цена квартиры
def set_flat_prise(flat, soap):
    price = soap.find('span', itemprop='price')
    if price:
        flat.price = int(price['content'])


# параметры квартиры и дома
def set_flat_specifications(flat, soap):
    specifications = soap.find_all('div', class_='grid-module__container___39oIv grid-module__gap___2HbMS')

    for specification in specifications:
        specification_elements = specification.find_all('div', class_='DescriptionCell__body')
        for element in specification_elements:
            name = element.find('div',
                                class_='colors-named-module__secondary___2WPH_ fonts-module__secondary-alone___3wVR-') \
                .text.strip()
            value = element.find(class_='fonts-module__primary___2PNSt DescriptionCell__value')
            if value:
                value = value.text.strip()
                if name == "Ремонт":
                    flat.repair_type = value
                elif name == "Площадь квартиры":
                    value = value.split()[0]
                    value = value.replace(',', '.')
                    flat.area = float(value)
                elif name == "Жилая площадь":
                    value = value.split()[0]
                    value = value.replace(',', '.')
                    flat.living_area = float(value)
                elif name == "Этаж":
                    value = value.split()[0]
                    flat.floor = int(value)
                elif name == "Комнат":
                    flat.room_count = int(value)
                elif name == "Год постройки":
                    flat.year = int(value)
                elif name == "Высота потолков":
                    value = value.split()[0]
                    value = value.replace(',', '.')
                    flat.height = float(value)
                elif name == "Отопление":
                    flat.heating = value
                elif name == "Лифт":
                    if value == "есть":
                        flat.elevator = 1
                elif name == "Материал стен":
                    flat.materials = value


# сохранение данных в файл
def save_csv(data, csv_file):
    with open(csv_file, "a", newline="", encoding="utf-8") as file_new:
        new_writer = csv.writer(file_new, delimiter=",")
        new_writer.writerow([data.price, data.title, data.address, data.room_count,
                             data.area, data.living_area, data.floor, data.metro,
                             data.repair_type, data.year, data.materials, data.heating,
                             data.height, data.elevator, data.description])
        print("flat added " + str(data.price))


# многопоточная обработка страниц
def pages_async(all_page_urls, page_count):
    with ThreadPoolExecutor(16) as p:
        p.map(download_page, all_page_urls)

    # создание массива ссылок на квартиры
    all_links = []
    for open_file_name in os.listdir(PAGES):
        with open(f"{PAGES}\\{open_file_name}", 'r', encoding="utf-8") as file_with_page_data:
            data = file_with_page_data.read()
            links = get_flat_links(data)
            all_links.extend(links)
            print("getting links from page " + open_file_name)

    # запись ссылок в файл для последующего краулинга
    with open('flat_links.csv', 'w') as output_file:
        for link in all_links:
            output_file.write(link + '\n')

    df = pd.read_csv(flat_links, header=None)
    df.drop_duplicates(inplace=True)
    df.to_csv(unique_flat_links, index=False, header=False)

    print(f"Ссылки записаны в файл ", output_file)


# многопоточная обработка страниц объявлений
def flat_data_async():
    # достаем ссылки
    links = []
    with open(unique_flat_links, "r") as file_with_links:
        for line in file_with_links:
            links.append(line.strip())
    links.pop()

    # скачиваем страницы всех объявлений
    with ThreadPoolExecutor(16) as p:
        p.map(download_flat_page, links)

    # парсим все объявления и записываем в датасет
    for open_file_name in os.listdir(FLATS):
        new_flat = get_flat_data(open_file_name)
        save_csv(new_flat, flat_dataset)


if __name__ == '__main__':
    start_time = time.time()

    count = int(get_page_count(root_url + "1"))

    page_urls = [root_url + str(page_number) for page_number in range(1, count)]

    with open(flat_dataset, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(['цена', 'название', 'адрес', 'количество комнат', 'площадь',
                         'жилая площадь', 'этаж', 'метро', 'ремонт', 'год постройки',
                         'материалы', 'отопление', 'высота потолков', 'лифт', 'описание'])

    pages_async(page_urls, count)
    sleep(10)
    flat_data_async()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Программа выполнена за {execution_time} секунд")
