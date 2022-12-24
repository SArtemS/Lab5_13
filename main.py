import matplotlib.pyplot as plt
import numpy as np
import requests
from xml.etree import ElementTree as ET


def get_currencies(currencies_ids_lst=['R01239', 'R01235', 'R01035']):

    cur_res_str = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
    root = ET.fromstring(cur_res_str.content)
    valutes = root.findall('Valute')

    result = {}
    full_names = []

    for el in valutes:
        valute_id = el.get('ID')

        if str(valute_id) in currencies_ids_lst:
            valute_cur_val = el.find('Value').text
            result[el.find('CharCode').text] = valute_cur_val
            full_names.append(el.find('Name').text)

    return result, full_names


def get_year_currency(currency_id = 'R01820'):
    import time
    result = {}
    day_diff = 86400
    day_count = 365
    dt_now = int(time.time())
    dt = dt_now - day_diff * day_count
    while dt != dt_now:
        dt_i = str(time.strftime("%d/%m/%Y", time.gmtime(dt)))
        cur_res_str = requests.get(f"https://cbr.ru/scripts/XML_daily.asp?date_req={dt_i}")
        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall('Valute')
        for el in valutes:
            valute_id = el.get('ID')
            if str(valute_id) in currency_id:
                valute_cur_val = el.find('Value').text
                result[f'{dt_i}'] = valute_cur_val
        dt += day_diff

    return result


if __name__ == '__main__':
    import seaborn as sns
    sns.set()

    # значения x и y для 10 валют
    cur_vals, full_named_cs = get_currencies([
        'R01035', 'R01200', 'R01235', 'R01239', 'R01335', 
        'R01375', 'R01565', 'R01700J', 'R01760', 'R01820'
    ])
    objects = cur_vals.keys()
    print(cur_vals)
    y_pos = np.arange(len(objects))
    performance = [float(x.replace(",", ".")) for x in cur_vals.values()]

    # значения x и y для данных за год
    year_currency = get_year_currency()
    year_x = year_currency.keys()
    year_y = [float(x.replace(",", ".")) for x in year_currency.values()]

    # общая настройка отображения окна
    fig, ax = plt.subplots(1, 2)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    fig.set_facecolor('floralwhite')

    # настройка отображения для 10 валют
    color_rectangle = np.random.rand(10, 3)  # RGB
    bars = ax[0].bar(objects, performance, color=color_rectangle)
    ax[0].set_facecolor('seashell')
    ax[0].legend(bars, full_named_cs, fontsize = 6, loc = 'lower right')
    ax[0].set_title('10 различных валют', fontsize = 24)
    ax[0].set_xlabel('Валюта', fontsize = 16)
    ax[0].set_ylabel('Рубли', fontsize = 16)
    ax[0].tick_params('x', labelsize = 8)
    
    # настройка отображения для данных за год
    ax[1].plot(year_x, year_y)
    ax[1].set_title('График вашей валюты за последний год', fontsize = 24)
    ax[1].set_xlabel('Дата', fontsize = 16)
    ax[1].set_ylabel('Рубли', fontsize = 16)
    # ax[1].tick_params('x', labelrotation=90, labelsize = 5) # настройка тиков 
    ax[1].axes.axes.get_xaxis().set_ticks([]) # прячем тики для оси x

    plt.show()
