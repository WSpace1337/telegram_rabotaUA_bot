from bs4 import BeautifulSoup
import requests
import time
import config

workers = []


def parse(city):
    URL = 'https://rabota.ua/ua/' + str(city)
    HEADERS = {
        'User-Agent':config.UserAgent #Вставляем свой user agent в файле config.py
    }

    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    works = soup.findAll('article', class_ = 'card')
    workers.clear()

    for work in works:
        workers.append({
            'title': work.find('a', class_ = 'ga_listing' ).get_text(strip = True),
            'price': work.find('span', class_ = 'salary').get_text(strip = True),
            'location': work.find('span', class_ = 'location').get_text(strip = True),
            'description': work.find('div', class_ = 'card-description').get_text(strip = True),
            'time': work.find('div', class_ = 'publication-time').get_text(strip = True),
            'link': work.find('a', class_ ='ga_listing').get('href')
        })
#    for worker in workers:
#        time.sleep(0.5)
#        print(f'{worker["title"]} \nЗП:{worker["price"]}👛\nГород:{worker["location"]}\nОписание:{worker["description"]} \
#        \nВремя публикации:{worker["time"]}\n\nLink: https://rabota.ua{worker["link"]}\n')
