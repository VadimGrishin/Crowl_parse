from pymongo import MongoClient
import requests
from lxml import html

import datetime

now = datetime.datetime.now()


# заголовок для эмуляции браузера
headers = {'accept': '*/*',
          'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3866.0 Safari/537.36'}

avito_url = "https://www.avito.ru/moskva"

client = MongoClient('mongodb://127.0.0.1:27017')

db = client['avito_db']
lesson5 = db.lesson
# lesson5.drop()


def request_to_site(url):
    try:
        request = requests.get(url, headers=headers)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def parse_ads_into_mongo():
    """
    Производит обновление базы объявлений по ключу href, если ключ не найден - добавляет новый элемент
    """

    html_page = html.fromstring(request_to_site(avito_url))
    ads = html_page.xpath("//div[@itemprop='price']/../..")  # карточка объявления

    upd_count, ins_count = 0, 0
    for ad in ads:

        href = ad.xpath('.//a[@itemprop="url"]/@href')[0]                         # ссылка для идентификации объявления
        name = ad.xpath('.//span[@itemprop="name"]/text()')[0]                    # название товара
        price = float(ad.xpath('.//div[@itemprop="price"]/@content')[0].replace('...', '-1'))  # цена
        date_time = datetime.datetime.strptime(                                   # дата-время объявления
            ad.xpath('.//span[contains(text(), ":") and contains(@class, "text-size")]/text()')[0].
            replace('Сегодня', now.strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M')

        ad_data = {
            "href": href,
            "name": name,
            "price": price if price >= 0 else None,
            "date_time": date_time,
            "date_timestr": ad.xpath('.//span[contains(text(), ":")]/text()')[0].replace('Сегодня',
                                                                             now.strftime("%Y-%m-%d"))
        }

        if list(lesson5.find({"href": href})):
            lesson5.update_one({"href": href}, {'$set': ad_data})
            upd_count += 1
        else:
            lesson5.insert_one(ad_data)
            ins_count += 1
    print(f'Добавлено новых записей: {ins_count}, обновлено: {upd_count}')


def print_ads(**kwargs):
    """Печать записей БД по условию kwargs"""

    s = lesson5.find(kwargs)
    for i, r in enumerate(list(s)):
        print(f"{i+1:>3}.   {r['price']} {r['name']} {r['date_time']}")


parse_ads_into_mongo()

print('\nПредложения ниже 500 рублей:')
print_ads(price={'$lt': 500})  # вызов с условием price < 500


