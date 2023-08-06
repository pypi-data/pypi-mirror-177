import time
import mysql.connector
import logging
import concurrent.futures
import helper
import requests
import random

logging.basicConfig(filename="logupdate.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.info(f'Logging Enabled: Functions being defiled')
config = helper.read_config()

global start

POOL_SIZE = 100
# from DBUtils.PooledDB import PooledDB, SharedDBConnection
from dbutils.pooled_db import PooledDB, SharedDBConnection

POOL = PooledDB(
    creator=mysql.connector,  # Modules using linked databases
    maxconnections=0,
    # The maximum number of connections allowed in the connection pool, 0 and None indicate unlimited connections
    mincached=20,  # At least idle links created in the link pool during initialization, 0 means not to create
    maxcached=500,  # The most idle links in the link pool, 0 and None are unlimited
    maxshared=0,
    # The maximum number of links shared in the link pool. 0 and None represent all shares. PS: useless, because the
    # threadsafety of pymysql, MySQL dB and other modules is 1. No matter how many values are set, the "maxcached" is
    # always 0, so all links are always shared.
    blocking=True,
    # If there is no connection available in the connection pool, whether to block waiting. True, wait; False,
    # do not wait and report an error
    maxusage=None,  # The maximum number of times a link can be reused, None means unlimited
    setsession=[],
    # List of commands executed before starting a session. For example: ["set datestyle to...", "set time zone..."]
    ping=0,
    # ping MySQL Server, check whether the service is available.# For example: 0 = None = never, 1 = default =
    # whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host=config['DBdetails']['host'],
    user=config['DBdetails']['user'],
    password=config['DBdetails']['password'],
    database=config['DBdetails']['database'],
    charset='utf8'
)


def update(x, y):
    cstart = time.time()
    connection = POOL.connection()
    query1 = "UPDATE msisdn_table SET status= -100 where status=0 AND id BETWEEN " + x + " AND " + y + ""
    query2 = "Select * from msisdn_table where status= -100 AND id BETWEEN " + x + " AND " + y + ""
    newcursor = connection.cursor()
    newcursor.execute(query1)
    connection.commit()
    newcursor.execute(query2)
    results = newcursor.fetchall()
    print('Fetched X:Y = {0} : {1}  Processing...'.format(x, y))
    print(time.time() - cstart)
    for row in results:
        msisdn = row[1]
        jazzcharging(msisdn)
    end = time.time()


def jazzcharging(msisdn):
    tcstart = time.time()
    connection = POOL.connection()
    cursor = connection.cursor()
    response = requests.get('http://127.0.0.1:8080/msisdn.py')
    # responsejazz = response.content.decode('utf-8')
    responsejazz = random.randint(0, 1)
    if responsejazz == 0:
        cursor.execute("UPDATE msisdn_table SET status = -200 where msisdn='" + msisdn + "'")
    elif responsejazz == 1:
        cursor.execute("UPDATE msisdn_table SET status = 100 where msisdn='" + msisdn + "'")
    connection.commit()
    tcend = time.time()
    logging.info(tcend - tcstart)


if __name__ == "__main__":
    start = time.time()
    conn = POOL.connection()
    mycursor = conn.cursor()

    mycursor.execute("SELECT COUNT(*) FROM msisdn_table")
    count = mycursor.fetchall()
    x = list(map(lambda item: item[0], count))
    result = x[0]
    print("Total data: ", result)
    tps = config['TPS']['tps']
    tps = int(tps)
    process = int(result / tps)

    print("Total processes: ", process)
    x = str(1)
    y = str(tps)
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=POOL_SIZE)
    futures = []
    for i in range(process):
        futures.append(executor.submit(update, x, y))
        x = int(x)
        y = int(y)
        x = x + tps
        y = y + tps
        x = str(x)
        y = str(y)
    for future in concurrent.futures.as_completed(futures):
        print('thread completed {}'.format(future.result()))
    end = time.time()
    print("Total Execution time: ", end - start)
