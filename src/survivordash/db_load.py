import os, sys
import psycopg2
from boxscores_etl import CHALLENGE_STATS_FILE


def run():
    try:
        conn = psycopg2.connect("dbname='warehouse' user='devuser' host='db' password='welyketoparti'", options="-c search_path=lake")
        cur = conn.cursor()
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS lake")
    except:
        print("I am unable to connet to the database")

    with open(CHALLENGE_STATS_FILE) as f:
        header = f.readline().rstrip().replace('"', '')
        create_fields = ['"{}" varchar(255)'.format(x) for x in header.split(',')]
        create_fields = ", ".join(create_fields)

        # create tables
        cur.execute(f"DROP TABLE IF EXISTS challenge_game_stats")
        cur.execute(f"CREATE TABLE IF NOT EXISTS challenge_game_stats ({create_fields})")
        conn.commit()

        cur.copy_from(f, 'challenge_game_stats', sep=',')
        conn.commit()
        
        print("success")

if __name__ == '__main__':
    run()



