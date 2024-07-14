import json
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

HOST = 'https://spb.hh.ru/search/vacancy?text=python+Django+Flask&area=1&area=2'


def get_headers():
    return Headers(browser='firefox', os='win').generate()


SOURCE = requests.get(HOST, headers=get_headers()).text

bs = BeautifulSoup(SOURCE, features='lxml')

articles_list = bs.find('main', class_="vacancy-serp-content")

articles = articles_list.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter')
vacancy_list = []

for article in articles:
    link = article.find('a')['href']
    company = article.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').text.replace(u'\xa0',
                                                                                                    ' ').replace(
        u'\u2009', '').replace(u'\u202f', '')
    salary = 0
    if article.find('span', class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni "
                                   "compensation-text--kTJ0_rp54B2vNeZ3CTt2 "
                                   "separate-line-on-xs--mtby5gO4J0ixtqzW38wh") is None:
        salary = None
    else:
        salary = article.find('span', class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni "
                                             "compensation-text--kTJ0_rp54B2vNeZ3CTt2 "
                                             "separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text.replace(u'\xa0',
                                                                                                       ' ').replace(
            u'\u2009', '').replace(u'\u202f', '')

    city = article.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text

    vacancy_list.append({

        'Ссылка': link,
        'Зарплата': salary,
        'Компания': company,
        'Город': city,

    })

with open('vacancy.json', 'w', encoding="utf-8") as f:
    json.dump(vacancy_list, f, ensure_ascii=False, indent=4)
