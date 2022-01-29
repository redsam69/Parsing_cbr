import requests
from bs4 import BeautifulSoup

import bd

URL = 'https://cbr.ru/currency_base/dynamics/'
URL_DATA = ('?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.'
            'mode=1&UniDbQuery.'
            'date_req1=&UniDbQuery.date_req2=&UniDbQuery.'
            'VAL_NM_RQ={}&UniDbQuery.From={}&UniDbQuery.To={}')
date_intervals = {}


def get_answer(url, *args):
    """"Запрс к серверу."""
    main_url = url if not args else url.format(*args)
    try:
        response = requests.get(main_url)
    except requests.exceptions.RequestException as exc:
        raise exc('Ошибка запроса от сервера')
    if response.status_code != 200:
        raise Exception('Сервер не доступен')
    return response


def pars_currency_name_date_intervals(response):
    """Извлекаем название валют, даты."""
    bs = BeautifulSoup(response.text, features="html.parser")
    sel_box = bs.find('label', {"class": "input_label"})
    currencies = {opt.getText().strip(): opt['value']
                  for opt in sel_box.findAll('option')}
    dp_box = bs.find('div', {"class": "datepicker-filter"})
    global date_intervals
    date_intervals = {'data-min-date': dp_box['data-min-date'],
                      'data-max-date': dp_box['data-max-date']}
    return currencies


def input_currency_name(currencies):
    """Вводим нужную валюту из предосавленного списка валют."""
    for currency_name in currencies.keys():
        print(currency_name)
    print('Введите нужную валюту >>>>>>>>>>>>')
    currency_name = input()
    if not currencies.get(currency_name):
        raise KeyError(f'данная валюта <<{currency_name}>> '
                       'отсутсвет в запросах')
    return currency_name


def pars_table_date(resp, currencies, currency_name):
    """Извлекаем данные по названию валюты."""
    arr = []
    bs = BeautifulSoup(resp.text, features="html.parser")
    data_table = bs.find('table', {"class": "data"})
    value = currencies.get(currency_name)
    if data_table:
        for tr in data_table.find_all('tr'):
            d = tuple(tr.getText() for tr in tr.findAll('td'))
            if len(d) == 3:
                zz = d + (value,)
                arr.append(zz)
    return arr


def start():
    """Запуск скрпинга."""
    response = get_answer(URL)
    currencies = pars_currency_name_date_intervals(response)
    currency_name = input_currency_name(currencies)

    url_add = URL + URL_DATA
    resp = get_answer(url_add, currencies[currency_name],
                      date_intervals['data-min-date'],
                      date_intervals['data-max-date'])
    date = pars_table_date(resp, currencies, currency_name)

    bd.create()
    bd.write_db(currencies, currency_name, date)
    print('Данные сохранены!!!!!!')
