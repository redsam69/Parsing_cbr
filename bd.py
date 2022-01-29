import sqlite3


def connect():
    """Подключение к базе данных."""
    conn = sqlite3.connect("mydatabase.db")
    conn.execute("PRAGMA foreign_keys = on")
    cursor = conn.cursor()
    return conn, cursor


def create():
    """Создание базы данных."""
    conn, cursor = connect()
    cursor.execute("""CREATE TABLE IF NOT EXISTS currency_table
                  (
                    currency_id TEXT PRIMARY KEY,
                    currency_name TEXT NOT NULL
                    )
               """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS currency_item_table
                  (
                    date DATETIME ,
                    unit INTEGER,
                    curs REAL,
                    currency_id TEXT NOT NULL,
                    FOREIGN KEY (currency_id) REFERENCES
                    currency_table(currency_id),
                    PRIMARY KEY (date, currency_id)
                    )
               """)


def write_db(currencies, currency_name, date):
    """Запись данных в базу данных."""
    conn, cursor = connect()
    value = currencies.get(currency_name)
    currency_table = [(value, currency_name)]
    cursor.executemany("INSERT OR IGNORE INTO currency_table VALUES (?,?)",
                       currency_table)
    cursor.executemany("INSERT OR IGNORE INTO currency_item_table "
                       "VALUES (?,?,?,?)", date)
    conn.commit()


def read_currency_table():
    """Чтение из базы данных название валют."""
    conn, cursor = connect()
    sql = "SELECT * FROM currency_table"
    try:
        cursor.execute(sql)
    except Exception as ex:
        raise ex('Таблица еще не создана, выполните scrap!!!')
    print(cursor.fetchall())


def read_currency_data(currency_name):
    """Чтение из базы данных данных по названию валюты."""
    conn, cursor = connect()
    sql = ("SELECT currency_item_table.date, "
           "currency_item_table.unit, "
           "currency_item_table.curs "
           "FROM currency_table "
           "JOIN currency_item_table "
           "ON currency_table.currency_id = currency_item_table.currency_id "
           "WHERE currency_name= ?")
    try:
        cursor.execute(sql, (currency_name,))
    except Exception as ex:
        raise ex('Таблица еще не создана, выполните scrap!!!')
    print(cursor.fetchall())
