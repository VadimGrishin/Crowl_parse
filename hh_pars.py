import requests
from lxml import html
from lxml import etree

# параметры для эмуляции браузера
headers = {'accept': '*/*',
          'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3866.0 Safari/537.36'}
base_url = "https://hh.ru/search/vacancy"

# базовые параметры запроса
get_params = {
    'L_is_autosearch': 'false',
    'area': '1',
    'clusters': 'true',
    'enable_snippets': 'true',
    'search_field': 'name'
}


def request_to_hh(text):
    get_params.update({'text': text})
    session = requests.Session()
    res = []
    for i in range(3):
        get_params.update({'page': i})
        req = session.get(base_url, headers=headers, params=get_params)

        blocks = html.fromstring(req.text).xpath('//div[@class="vacancy-serp-item__row vacancy-serp-item__row_header"]')
        xxs = [etree.tostring(block) for block in blocks]

        res_salary = [(html.fromstring(xx).xpath('//div[@class="vacancy-serp-item__compensation"]')) for xx in xxs]
        res_salary = [r[0].text_content() if r else 'Зарплата не указана' for r in res_salary]
        res_salary = [' '.join(b.split()) for b in res_salary]

        res_title = [html.fromstring(xx).xpath('//a[@data-qa="vacancy-serp__vacancy-title" ]')[0].text_content() for xx in xxs]

        res_href = [html.fromstring(etree.tostring(block)).xpath('//@href')[0] for block in blocks]

        res += list(zip(res_title, res_href, res_salary))
    for it in res:
        print(it)
    print(len(res))


search_text = input('Введите название вакансии: ')

request_to_hh(search_text)
