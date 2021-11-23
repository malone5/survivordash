from survivordash import wiki_etl, boxscores_etl, db_load

def run():
    wiki_etl.run()
    boxscores_etl.run()
    db_load.run()

if __name__ == '__main__':
    run()
