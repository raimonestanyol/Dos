import requests, asyncio
from bs4 import BeautifulSoup
# Module Imports
import mariadb, datetime as dt, logging

# Connect to MariaDB Platform
def connect():
    try:
        connection = mariadb.connect(
            user = "root",
            password = "tfg2020",
            host = "localhost",
            port = 3306,
            database = "new",
        )
        connection.auto_reconnect = True
        return connection

    except mariadb.Error as e:
        logging.error(e)


# Get Cursor

async def getData(connection):
    URL = 'http://147.83.75.6/services/user/values.xml?id=Trinum?'
    cursor = connection.cursor()
    variables = ["AMB_T", "BOILER_T", "COOL_FLOW", "COOL_T_IN", "COOL_T_OUT", "CURRENT", "E_ENERGY", "E_POWER",
                 "HEAD_T_SET", "HEAT_T_CON", "HRAT_T_LIM", "STATUS", "VDTTM", "VOLTAGE", "DATETIME"]

    while True:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        values = [value.text for value in soup.findAll('value', text=True)]

        command_string = "INSERT INTO tables_registry (" + ",".join(
            variables) + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        list_values=[float(values[i]) for i in range(len(values))]+[dt.datetime.now().isoformat(' ', 'seconds')]
        list_values[11],list_values[12]=int(list_values[11]),int(list_values[12])

        try:
            cursor.execute(command_string, tuple(list_values))
            connection.commit()

        except mariadb.Error as e:
             logging.error(e)

        print(list_values[14])
        await asyncio.sleep(60)

logging.basicConfig(filename='scraper_log.log', encoding='utf-8', level=logging.ERROR)
connection = connect()
loop = asyncio.get_event_loop()
loop.create_task(getData(connection))
loop.run_forever()