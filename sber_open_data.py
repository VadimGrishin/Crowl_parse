import pandas as pd
from pandas.plotting import register_matplotlib_converters
import datetime

import matplotlib.pyplot as plt
import matplotlib
import pylab

pd.options.display.max_columns = 5

dt = pd.read_csv('opendata.csv', parse_dates=True)
print(dt.info())


def choice_params():
    # Выбор параметров фильтра
    names = list(dt['name'].unique())
    for i, name in enumerate(names):
        print(f'{i} - {name}')

    n = int(input('Выберите номер группы данных: '))

    regions = list(dt['region'].unique())
    for i, reg in enumerate(regions):
        print(f'{i} - {reg}')

    r = int(input('Выберите регион из списка: '))

    try:
        dt_min = datetime.datetime.strptime(input('Введите начальную дату диапазона Y-m-d: '), "%Y-%m-%d")
        dt_max = datetime.datetime.strptime(input('Введите конечную дату диапазона Y-m-d: '), "%Y-%m-%d")
        assert dt_min <= dt_max
    except ValueError or AssertionError:
        dt_min = dt[(dt['name'] == names[n]) & (dt['region'] == regions[r])]['date'].astype(dtype='datetime64').min()
        dt_max = dt[(dt['name'] == names[n]) & (dt['region'] == regions[r])]['date'].astype(dtype='datetime64').max()

    return names[n], regions[r], dt_min, dt_max


def make_report(name, reg):
    # Формирование отфильтрованных данных
    rep = dt[(dt['name'] == name)
             & (dt['date'].astype(dtype='datetime64') >= date_min)
             & (dt['region'] == reg)
             & (dt['date'].astype(dtype='datetime64') <= date_max)][['date', 'value']]

    return rep


def draw_graph():
    # Создание графика:

    #       Преобразуем даты в числовой формат (для дальнейшего форматирования тикеров осей)
    register_matplotlib_converters()
    x_data_float = matplotlib.dates.date2num(report['date'].astype(dtype='datetime64'))

    #       Вызовем subplot явно, чтобы получить экземпляр класса AxesSubplot,
    #       из которого будем иметь доступ к осям
    axes = pylab.subplot(1, 1, 1)

    #       Пусть в качестве меток по оси X выводится только месяц.год
    axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m.%y"))

    #       Изменим локатор, используемый по умолчанию
    locator = matplotlib.dates.AutoDateLocator(minticks=5, maxticks=12)
    axes.xaxis.set_major_locator(locator)

    #       Отобразим данные
    pylab.plot_date(x_data_float, report['value'], fmt="b-")

    plt.title(f'{category_name}\n{region}\nс {date_min} по {date_max}')
    plt.plot(x_data_float, report['value'])

    plt.show()


category_name, region, date_min, date_max = choice_params()

report = make_report(category_name, region)
print()
print('-' * 50)
print(f'Выбрана группа - {category_name}')
print(f'Выбран регион - {region}')
print(f'Выбран диапазон с {date_min} по {date_max}')
print(report)

draw_graph()
