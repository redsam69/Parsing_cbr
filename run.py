import argh

import pars
import bd


def read():
    """Чтение сохраненных валют."""
    bd.read_currency_table()


def read_data(name):
    """Выдача данных по требуемой валюте."""
    bd.read_currency_data(name)


def scrap():
    """Запус скрипинга."""
    pars.start()


if __name__ == "__main__":
    argh.dispatch_commands([scrap, read, read_data])
