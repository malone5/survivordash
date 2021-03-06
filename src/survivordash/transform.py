from db import get_db_conn


def create_player_table(conn):
    cur = conn.cursor()
    with open('/code/src/survivordash/sql/player_table.sql', 'r') as sql_file:
        cur.execute(sql_file.read())

def create_stats_table(conn):
    cur = conn.cursor()
    with open('/code/src/survivordash/sql/game_stats_table.sql', 'r') as sql_file:
        cur.execute(sql_file.read())

def create_challenge_table(conn):
    cur = conn.cursor()
    with open('/code/src/survivordash/sql/challenge_stats_table.sql', 'r') as sql_file:
        cur.execute(sql_file.read())


def tranform():
    conn = get_db_conn()
    create_player_table(conn)
    create_stats_table(conn)
    create_challenge_table(conn)
    conn.commit()
    conn.close()


def run():
    print("running tranforms...")
    tranform()

if __name__ == '__main__':
    run()