import requests
from bs4 import BeautifulSoup
# Module Imports
import mariadb, logging
from datetime import datetime as dt, timedelta as td
from threading import Thread
import time, csv


# Connect to MariaDB Platform
def connect():
    try:
        maria_connection = mariadb.connect(
            user="root",
            password="tfg2020",
            host="localhost",
            port=3306,
            database="new",
        )
        maria_connection.auto_reconnect = True
        return maria_connection

    except mariadb.Error as e:
        logging.error(e)


# Get values, make the Sql command and commit it to the database
def get_data(trinum_URL, maria_cursor, table_header):
    page = requests.get(trinum_URL)
    soup = BeautifulSoup(page.content, 'lxml')
    values = [value.text for value in soup.findAll('value', text=True)]

    global last_time, seconds_wait, datetime
    delta = datetime - last_time - td(seconds=seconds_wait)
    # print(str(datetime))
    # print(str(last_time))
    # print(str(delta.microseconds / 1000))
    with open('deltas2.csv', newline='', mode='a') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow([delta.microseconds/1000])
    # logging.error(delta.microseconds/1000)
    last_time = datetime

    command_string = "INSERT INTO tables_registry (" + ",".join(
        table_header) + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    list_values = [float(values[i]) for i in range(len(values))] + [datetime.isoformat(' ', 'seconds')]
    list_values[11], list_values[12] = int(list_values[11]), int(list_values[12])

    try:
        maria_cursor.execute(command_string, tuple(list_values))
        connection.commit()

    except mariadb.Error as e:
        logging.error(e)

    # task1_creator()


logging.basicConfig(filename='scraper_log.log', encoding='utf-8', level=logging.ERROR)
connection = connect()

trinum_URL = 'http://147.83.75.6/services/user/values.xml?id=Trinum?'
maria_cursor = connection.cursor()
table_header = ["AMB_T", "BOILER_T", "COOL_FLOW", "COOL_T_IN", "COOL_T_OUT", "CURRENT", "E_ENERGY", "E_POWER",
             "HEAD_T_SET", "HEAT_T_CON", "HRAT_T_LIM", "STATUS", "VDTTM", "VOLTAGE", "DATETIME"]
seconds_wait = 20
last_time = dt.now()
data_thread = Thread(target=get_data, args=[trinum_URL, maria_cursor, table_header])


def task1_creator():
    global data_thread
    data_thread = Thread(target=get_data, args=[trinum_URL, maria_cursor, table_header])


while True:
    datetime = dt.now()
    # data_thread.start()
    get_data(trinum_URL, maria_cursor, table_header)
    time.sleep(seconds_wait)
