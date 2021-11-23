import sys, os
import requests
import pandas as pd
import json
import re
import hashlib
import csv
from survivordash import utility

"""
create files we will use as refrence
"""

FILEPATH = os.path.dirname(os.path.abspath(__file__)) # directory of this file
RESOURCE_PATH = FILEPATH + '/resources/'

# Output files
SEASONS_FILE = RESOURCE_PATH + 'seasons.json'
SEASON_PLAYERS_FILE = RESOURCE_PATH + 'wiki_season_players.csv'


def _season_name_to_number(season_name):
    if not os.path.exists(os.path.join(SEASONS_FILE)):
        create_seasons_file()

    with open(os.path.join(SEASONS_FILE)) as json_file:
        season_map = json.load(json_file)
        season_number = season_map[str(season_name)]

    return season_number

def _name_between_quotes(name):
    nickname = re.findall('"([^"]*)"', name) # string between quotes
    if len(nickname) > 0:
        return nickname[0].replace('"', '').strip()
    return None

def _name_outside_quotes(name):
    name = name.replace(",", "")
    if '"' not in name:
        return name

    open_quote_idx = name.find('"')
    close_quote_idx = name.rfind('"')

    # +2 to delete the quote-and-space that follows a nickname.
    standard_name = ' '.join([name[:open_quote_idx].strip(), name[close_quote_idx+2:].strip()])
    return standard_name

def create_seasons_file():
    html_tables = utility.get_html_tables('https://en.wikipedia.org/wiki/Survivor_(American_TV_series)')

    # The second table on the wiki has the list of seasons
    column_trans = {'Season title': 'season_title', '#': 'season_number'}
    seasons_table = html_tables[1][['#', 'Season title']].rename(columns=column_trans)
    
    season_map = dict(zip(seasons_table['season_title'], seasons_table['season_number']))

    with open(os.path.join(SEASONS_FILE), 'w') as file:
        file.write(json.dumps(season_map))


def create_season_players_file():
    """Create CSV of all players for each season"""
    html_tables = utility.get_html_tables('https://en.wikipedia.org/wiki/List_of_Survivor_(American_TV_series)_contestants')

    # The wiki splits up html_tables into decades. So we union them.
    player_table_union = pd.concat([html_tables[1], html_tables[2]])
    player_table = player_table_union[['Name', 'Age', 'Hometown', 'Profession', 'Season']]

    column_trans = {'Name': 'name', 'Age': 'age', 'Hometown': 'hometown', 'Profession':'profession', 'Season': 'season'}
    player_table = player_table.rename(columns=column_trans)

    # Create fields 
    player_table.insert(0, 'nick_name', player_table['name'].apply(_name_between_quotes), True)
    player_table.insert(0, 'standard_name', player_table['name'].apply(_name_outside_quotes), True)
    player_table.insert(0, 'player_hash', player_table['standard_name'].apply(utility._hash_player_name))
    player_table.insert(0, 'season_number', player_table['season'].apply(_season_name_to_number), True)
    player_table.reset_index(drop=True, inplace=True)

    # Create file
    player_table.to_csv(SEASON_PLAYERS_FILE, index=False, quoting=csv.QUOTE_NONNUMERIC)


def run():
    create_seasons_file()
    create_season_players_file()

if __name__ == '__main__':
    run()
