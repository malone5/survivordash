import os
from sqlalchemy import create_engine

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