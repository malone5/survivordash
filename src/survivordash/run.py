from survivordash import wiki_extract, boxscore_extract, db_load, transform, datamarts

def run():
    wiki_extract.run()
    boxscore_extract.run()
    db_load.run()
    transform.run()
    datamarts.run()

if __name__ == '__main__':
    run()
