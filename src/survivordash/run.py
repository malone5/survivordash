from survivordash import wiki_extract, boxscore_extract, db_load, transform, datamarts, metabase_setup

def run():
    wiki_extract.run()
    boxscore_extract.run()
    db_load.run()
    transform.run()
    datamarts.run()
    metabase_setup.run()
    print("Full ETL Complete. Explore data at localhost:3000")

if __name__ == '__main__':
    run()
 