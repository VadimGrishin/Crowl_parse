"""
ТЗ на парсинг регламентной базы энергосистемы РФ (сайт https://www.np-sr.ru/ru)

Постановка задачи.

1. Необходимо найти документы в формате MS Word на сайте НП Совет Рынка, соответствующие:
а) стандартным формам договоров между участниками рынка электроэнергии, инфраструктурными организациями:
https://www.np-sr.ru/ru/regulation/joining/standardcontracts/index.htm (основная страница)
    //a[@class="p_link"]/@href
    https://www.np-sr.ru/ru/regulation/joining/standardcontracts/index.htm/{dddd} (страницы по темам)
        //a[@class="p_link"]/@href
        https://www.np-sr.ru/ru/regulation/joining/standardcontracts/{dddd}  (страницы отдельного договора)
            //a[@class="doc__link"]
б) регламентам оптового рынка электроэнергии и мощности (ОРЭМ).
https://www.np-sr.ru/ru/regulation/joining/reglaments/index.htm (основная страница)
    //a[@class="p_link"]/@href
    https://www.np-sr.ru/ru/regulation/joining/reglaments/{dddd} (страницы отдельного регламента)
        //a[@class="doc__link"]

2. Скачать эти документы в локальную папку, одновременно провести запись в БД названия файла и наименования 
документа из соответствующего тега.

3. Провести парсинг файлов на пункты (включая подпункты). Каждый пункт должен сохраняться в БД. 
Структура данных для хранения пунктов должна предполагать отслеживание версионности каждого пункта в дальнейшем.
При этом надо понимать, что новая версия пункта может иметь другой номер пункта (идентификация будет по содержанию).

4. Для идентификации новых версий пунктов по содержанию будут в дальнейшем использоваться методы ИИ. 
В рамках курсовой должны быть выполнены пп.1-3.
"""

from pymongo import MongoClient
import requests
from lxml import html
import re


def save_doc(href, file_name):
    """Сохранение бинарного файла по ссылке"""

    req1 = requests.get(href)
    with open(file_name, 'wb') as out:
        out.write(req1.content)

    return True


client = MongoClient('mongodb://127.0.0.1:27017')

db = client['np_sr_db']
std_contracts = db.std_contracts

# ---------------------------------------------------------------------------------
# Парсинг договоров
base_url = "https://www.np-sr.ru/ru/regulation/joining/standardcontracts/index.htm"
req = requests.get(base_url)

#  Основная страница
contr_types = html.fromstring(req.text).xpath('//a[@class="p_link"]/@href')
contr_types_titles = html.fromstring(req.text).xpath('//div[@class="border-content-box__text text-c-base"]/text()')

n = 0
i = 0
for contr_type in contr_types:
    # 		тематическая страница
    req = requests.get(contr_type)
    contrs = html.fromstring(req.text).xpath('//div[@class=" border-content-box border-content-box--offset  '
                                             'border-content-box--brown border-content-box--hover flex flex--a-center '
                                             'flex--j-between typography"]//@href')
    contr_titles = html.fromstring(req.text).xpath('//div[@class=" border-content-box border-content-box--offset  '
                                                   'border-content-box--brown border-content-box--hover '
                                                   'flex flex--a-center flex--j-between typography"]'
                                                   '/div[@class="border-content-box__text text-c-base"]/text()')

    ad_data = {
        "contract_type": contr_type,
        "contract_type_title": contr_types_titles[n],
        "docs": []
    }
    if list(std_contracts.find({"contract_type": contr_type})):
        std_contracts.update_one({"contract_type": contr_type}, {'$set': ad_data})
        #  upd_count += 1
    else:
        std_contracts.insert_one(ad_data)
        #  ins_count += 1

    j = 0
    print(contr_types_titles[n])
    for contr in contrs:
        i += 1
        #  договор
        req_contr_doc = requests.get(contr)
        contr_doc = html.fromstring(req_contr_doc.text).xpath('//a[@class="doc__link"]/@href')
        print(f'{i}) {contr} {contr_titles[j]}')

        doc_name = contr_doc[0].replace("https://www.np-sr.ru/sites/default/files/sr_regulation/standcont/",
                                        "").replace("/", "")

        if save_doc(contr_doc[0], doc_name):
            print(f'{doc_name} сохранен на диске')

        std_contracts.update_one({"contract_type": contr_type}, {'$push': {'docs': {
            'contr': contr,
            'doc_name': doc_name
        }}})

        j += 1

    n += 1  
  
# ---------------------------------------------------------------------------------
# Парсинг регламентов

# to be continued...
