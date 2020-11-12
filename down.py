import requests, asyncio
from bs4 import BeautifulSoup
# Module Imports
import mariadb, sys, datetime as dt

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="tfg2020",
        host="localhost",
        port=3306,
        database="maria"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor

i=0
async def getData(i, conn):
    URL = 'http://147.83.75.6/services/user/values.xml?id=Trinum?'
    cursor = conn.cursor()
    while True:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        values = [value.text for value in soup.findAll('value', text=True)]
        print(values)
        print (i)
        cursor.execute("INSERT INTO polls_question (question_text,pub_date) VALUES (?, ?);", (str(values[0]), dt.datetime.now()))
        # try:
        #     cursor.execute("INSERT INTO polls_question (question_text,pub_date) VALUES (?, NOW())", str(values[0]))
        # except mariadb.Error as e:
        #     print(f"Error: {e}")
        conn.commit()

        i+=1
        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.create_task(getData(i,conn))
loop.run_forever()


# variables = ["AMB_T", "BOILER_T", "COOL_FLOW", "COOL_T_IN", "COOL_T_OUT", "CURRENT", "DESCRIPTION", "E_ENERGY", "HEAD_T_SET", "HEAT_T_CON", "HRAT_T_LIM", "NAME", "STATUS", "VDTTM" , "VOLTAGE"]
# results = [[variable,soup.find('value' , text=True).text] for variable in variables]
# [print(result[1]) for result in results]
# AMB_T = soup.find(id='Trinum.AMB_T').prettyfy(),
# BOILER_T = soup.find(id='Trinum.BOILER_T'),
# COOL_FLOW = soup.find(id='Trinum.COOL_FLOW'),
# COOL_T_IN = soup.find(id='Trinum.COOL_T_IN'),
# COOL_T_OUT = soup.find(id='Trinum.COOL_T_OUT'),
# CURRENT = soup.find(id='Trinum.CURRENT'),
# DESCRIPTION = soup.find(id='Trinum.DESCRIPTION'),
# E_ENERGY = soup.find(id='Trinum.E_ENERGY'),
# E_POWER = soup.find(id='Trinum.E_POWER'),
# HEAD_T_SET = soup.find(id='Trinum.HEAD_T_SET'),
# HEAT_T_CON = soup.find(id='Trinum.HEAT_T_CON'),
# HRAT_T_LIM = soup.find(id='Trinum.HRAT_T_LIM'),
# NAME = soup.find(id='Trinum.NAME'),
# STATUS = soup.find(id='Trinum.STATUS'),
# VDTTM = soup.find(id='Trinum.VDTTM'),
# VOLTAGE = soup.find(id='Trinum.VOLTAGE')]
