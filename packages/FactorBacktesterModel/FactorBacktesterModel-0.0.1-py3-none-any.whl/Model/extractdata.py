from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import psycopg2

def add(a,b):
    return a+b

def GetUniverse(universe, cashfut, sector, start_date, end_date):
    pass

################################################ BigQuery #######################################################

project = 'tb-sandbox-338012'
credentials = service_account.Credentials.from_service_account_file('./Factor-Backtester/source/file.json')
client = bigquery.Client(credentials= credentials,project=project)
query = """

SELECT Date,avg(LTP) FROM `tb-sandbox-338012.prod_ticks.NSE_Index_Historical` WHERE DATE(Date) = "2022-04-28" and TIME(Date) >= "15:00:00" and Index = "NIFTY BANK"  AND EXTRACT(second FROM Date) in (0,5)
group by Date order by Date

"""
query_job = client.query(query).result().to_dataframe() 

##################################### PostGres ################################################
conn = psycopg2.connect(
   database="postgres", user='postgres', password='Akshit@123', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''SELECT * from contractspecs''')
#result = cursor.fetchone();
#print(result)

result = cursor.fetchall();
print(result)
conn.commit()
conn.close()