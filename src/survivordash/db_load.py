import os, sys
import psycopg2
from boxscore_extract import CHALLENGE_STATS_FILE, GAME_STATS_FILE
from wiki_extract import SEASON_PLAYERS_FILE
import csv
from db import get_db_conn


def load_file(conn, file, tablename):
    cur = conn.cursor()
    with open(file) as f:
        csv_reader = csv.reader(f, delimiter = '|', quotechar='"')
        for row in csv_reader:
            columns = row
            break

        create_fields = ['"{}" varchar(255)'.format(x) for x in columns]
        create_fields = ", ".join(create_fields)

        # create tables
        cur.execute(f"DROP TABLE IF EXISTS {tablename}")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {tablename} ({create_fields})")
        conn.commit()

        cur.copy_from(f, tablename, sep='|')
        conn.commit()
        
        print(f'loaded {tablename}')



def run():
    try:
        options="-c search_path=lake"
        conn = get_db_conn(options=options)
        cur = conn.cursor()
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS lake")
    except:
        raise Exception("I am unable to connet to the database")

    load_file(conn, CHALLENGE_STATS_FILE, 'challenge_game_stats')
    load_file(conn, GAME_STATS_FILE, 'game_stats')
    load_file(conn, SEASON_PLAYERS_FILE, 'season_players')

if __name__ == '__main__':
    run()



