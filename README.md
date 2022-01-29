Скрейпинг исторической динамики валютного курса заданной валюты

Локальное развёртывание:

Клонируем репозиторий на локальную машину:
$ git clone https://github.com/A-Kuklin/yatube.git

Создаем виртуальное окружение:
$ python3 -m venv venv

Запускаем виртуальное окружение
$ source venv/bin/activate

Устанавливаем зависимости:
$ pip install -r requirements.txt

Команды:
$ python run.py -h - вывод всех команд
$ python run.py scrap - запус скрапинга
$ python run.py read - вывод на экран из БД сохраненных валют
$ python run.py read-data 'названиие валюты' - вывод на экран из БД данные по запрашиваемой валюте
