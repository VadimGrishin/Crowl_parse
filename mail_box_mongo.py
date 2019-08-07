from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys    #Клавиши клавиатуры

from pymongo import MongoClient

import time

client = MongoClient('mongodb://127.0.0.1:27017')

db = client['mailbox_db']
lesson6 = db.my_box
lesson6.drop()

driver = webdriver.Chrome()

driver.get('https://mail.ru/')
# assert "GeekBrains" in driver.title

#Заполняем поля для ввода
elem = driver.find_element_by_id("mailbox:login")
elem.send_keys('svadimvadimych@inbox.ru')  # логин

elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('tobeornot1')  # пароль
elem.send_keys(Keys.RETURN)
time.sleep(40)

elems = driver.find_elements_by_xpath('//div[@class="llc__content"]')
print(len(elems))

for i in range(len(elems)):

    it = elems[i]

    x_from = it.find_element_by_xpath('//span[contains(@class,"ll-crpt")]').text
    x_subj = it.find_element_by_xpath('//span[contains(@class,"llc__subject")]').text
    x_time = it.find_element_by_xpath('//div[@class="llc__item llc__item_date"]').text

    it.click()

    time.sleep(4)
    body_elem = driver.find_element_by_xpath('//div[@class="letter__body"]')
    x_body = body_elem.text

    letter_data = {
        'from': x_from,
        'subj': x_subj,
        'date_time': x_time,
        'body': x_body
    }

    lesson6.insert_one(letter_data)

    driver.back()
    time.sleep(4)
    elems = driver.find_elements_by_xpath('//div[@class="llc__content"]')


driver.close()
