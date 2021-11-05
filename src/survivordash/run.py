from survivordash import wiki_etl, boxscores_etl

def run():
    wiki_etl.run()
    boxscores_etl.run()

if __name__ == '__main__':
    run()
