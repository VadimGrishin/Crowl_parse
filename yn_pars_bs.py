import requests
from bs4 import BeautifulSoup

# параметры для эмуляции браузера
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3866.0 Safari/537.36'}

base_url = "https://news.yandex.ru/Moscow_and_Moscow_Oblast/index.html"

def request_to_yn():
    """ Вывод новостей региона с yandex.ru """

    try:
        request = requests.get(base_url)
        html_doc = request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)

    soup = BeautifulSoup(html_doc, 'html.parser')

    sps = soup.findAll('div', {'class': "story story_view_normal story_noimage"})  # все блоки новостей

    res = []
    for sp in sps:

        a = []
        txt = sp.find('div', {'class': 'story__text'}).string  # аннтотация
        dt = sp.find('div', {'class': 'story__date'}).string[-5::]  # время

        sp = sp.find('h2', {'class': 'story__title'})  # заголовок со ссылкой
        a.append(sp.find('a').string)
        a.append(txt)
        a.append(sp.find('a')['href'])
        a.append(dt)

        res.append(a)

    res.sort(key=lambda i: i[3])  # сортировка по времени

    for a in res:
        for it in a:
            print(it)
        print('-'*50)

    print(len(sps))


request_to_yn()




