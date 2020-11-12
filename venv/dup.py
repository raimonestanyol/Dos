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
        database="new"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor

i=0
async def getData(i, conn):
    URL = 'http://147.83.75.6/services/user/values.xml?id=Trinum?'
    cursor = conn.cursor()
    variables = ["AMB_T", "BOILER_T", "COOL_FLOW", "COOL_T_IN", "COOL_T_OUT", "CURRENT", "E_ENERGY", "E_POWER",
                 "HEAD_T_SET", "HEAT_T_CON", "HRAT_T_LIM", "STATUS", "VDTTM", "VOLTAGE", "DATETIME"]

    while True:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        values = [value.text for value in soup.findAll('value', text=True)]
        # print(len(values))
        # # print(values)
        # print (i)
        #cursor.execute("INSERT INTO polls_question (question_text,pub_date) VALUES (?, ?);", (str(values[0]), dt.datetime.now()))
        print(variables)
        command_string = "INSERT INTO tables_registry (" + ",".join(
            variables) + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        list_values=[float(values[i]) for i in range(len(values))]+[dt.datetime.now()]
        list_values[11],list_values[12]=int(list_values[11]),int(list_values[12])
        print(list_values)
        cursor.execute(command_string, tuple(list_values))
        # try:
        #     command_string="INSERT INTO tables_registry (" + ",".join(variables) + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        #     # "INSERT INTO tables_registry (AMB_T,pub_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        #     cursor.execute(command_string, (str(values[i]) for i in range(len(values))))
        # except mariadb.Error as e:
        #     print(f"Error: {e}")
        conn.commit()

        i+=1
        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.create_task(getData(i,conn))
loop.run_forever()


# variables = ["AMB_T", "BOILER_T", "COOL_FLOW", "COOL_T_IN", "COOL_T_OUT", "CURRENT", "E_ENERGY", "E_POWER", "HEAD_T_SET", "HEAT_T_CON", "HRAT_T_LIM", "STATUS", "VDTTM" , "VOLTAGE", "DATETIME"]
# ['14.600000', '16.400000', '0.000000', '12.700000', '12.900000', '0.000000', '1043.300000', '0.000000', '525.000000', '17.000000', '17.000000', '1.000000', '12112020013506', '0.000000']
