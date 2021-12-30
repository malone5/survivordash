from db import get_db_conn

def create_data_mart(conn):
    print("creating data mart for survivor winners..")
    cur = conn.cursor()
    with open('/code/src/survivordash/sql/winners_mart.sql', 'r') as sql_file:
        cur.execute(sql_file.read())


def run():
    conn = get_db_conn()
    create_data_mart(conn)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run()