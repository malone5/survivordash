from survivordash import wiki_extract, boxscore_extract, db_load

def run():
    wiki_extract.run()
    boxscore_extract.run()
    db_load.run()

if __name__ == '__main__':
    run()
