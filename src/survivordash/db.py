import os
from sqlalchemy import create_engine
import psycopg2

def get_db_engine():
    user = os.environ['WAREHOUSE_USER']
    password = os.environ['WAREHOUSE_PASSWORD']
    host = os.environ['WAREHOUSE_HOST']
    port = os.environ['WAREHOUSE_PORT']
    db = os.environ['WAREHOUSE_DB']

    sqluri = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    print("connected:", sqluri)
    engine = create_engine(sqluri)
    return engine


def get_db_conn(options=""):
    user = os.environ['WAREHOUSE_USER']
    password = os.environ['WAREHOUSE_PASSWORD']
    host = os.environ['WAREHOUSE_HOST']
    port = os.environ['WAREHOUSE_PORT']
    db = os.environ['WAREHOUSE_DB']

    sqluri = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    #cxnstr = "dbname='warehouse' user='devuser' host='db' password='welyketoparti'"
    conn = psycopg2.connect(sqluri, options=options)
    return conn