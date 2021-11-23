import sys
import os
import requests
import csv

import pandas as pd
from bs4 import BeautifulSoup
import re

from survivordash import utility
from survivordash.wiki_etl import SEASON_PLAYERS_FILE


""" Boxscore data pulled from https://www.truedorktimes.com/survivor/boxscores/data.htm"""

FILEPATH = os.path.dirname(os.path.abspath(__file__)) # directory of this file
RESOURCE_PATH = FILEPATH + '/resources/'

# Output files
GAME_STATS_FILE = RESOURCE_PATH + 'player_game_stats.csv'
CHALLENGE_STATS_FILE = RESOURCE_PATH + 'challenge_game_stats.csv'


def _extract_player_names(elements):
        # Expects a list of html elements
        # <a href="../cast/first_last.htm">Nickname</a>
        player_names = {}
        for link in elements:
            nickname = link.text
            fullname = link.get('href').split('/')[-1].replace('.htm', '').replace('_', ' ')
            player_names[nickname] = fullname
        return player_names

def _rename_complete_data_columns(df):
    complete_field_map = {
        "Contestant": "name", #s33 doesnt have this mapping.
        "SurvSc": "srv_score", # (Win% + Tribal Council Appear% + Jurty Vote%)  
        "SurvAv": "srv_avg", 
        "ChW": "ch_wins",
        "ChA": "ch_appear",
        "ChW%" : "ch_win_pct",
        "SO": "ch_sat_out",
        "VFB": "votes_for_bootee",
        "VAP": "votes_against_self",
        "TotV": "total_votes_cast",
        "TCA": "tc_appear",
        "TC%": "tc_success_pct",
        "wTCR": "weighted_tc_ratio",
        "JVF": "jury_votes_for",
        "TotJ": "total_jurors",
        "JV%": "jury_vote_pct"
    }


    df.rename(columns=complete_field_map, inplace=True)

    # mainly to fix issue with season33 missing the label
    if df.columns[1] != 'name':
        df.rename(columns={ df.columns[0]: "name" }, inplace=True)

    return df

def _rename_challenge_data_columns(df):
    df.columns = df.columns.str.replace("*", "")
    df.columns = df.columns.str.replace(".", "")

    challenge_field_map = {
        "Contestant": "name",
        "MPF ChA": "ch_score", # ch_finish_avg * ch_appear
        "MPF  ChA": "ch_score", # we have found anomolies with double spaces
        "MPF": "ch_finish_avg", # Mean of all percent finishes
        "ChA": "ch_appear",
    }
    df.rename(columns=challenge_field_map, inplace=True)

    for col in df.columns[4:]:
        new_col = col.replace(' ', '_')
        new_col = new_col.replace('E', 'ep_')
        new_col = new_col.replace('F', 'final_')
        # new_col = new_col.replace('IC', 'immunity')
        # new_col = new_col.replace('RC', 'reward')
        df.rename(columns={col: new_col}, inplace=True)


def _extract_first_name_last_initial(input_name):
    tokens = input_name.split()
    fname = tokens[0][:3]
    if len(tokens) > 1:
        lname_initial = tokens [1][:1]
        return ' '.join([fname, lname_initial])
    else:
        return fname

def _extract_initials(input_name):
    # initials = ''.join([word[0] for word in input_name])
    words = input_name.split()
    if len(words) > 1:
        initials = ''.join([ word[0] for word in input_name.split() if word])
        return initials
    return None


def _match_player(input_name, season_number):
    df = pd.read_csv(SEASON_PLAYERS_FILE)
    df = df[['season_number', 'player_hash', 'nick_name', 'name','standard_name']]

    # Clean
    input_name = input_name.replace('*', '')

    # These are one-off names that we must manually adjust
    input_name = input_name.replace('RC', 'R.C.')
    input_name = input_name.replace('Wardog', 'The Wardog')
    input_name = input_name.replace('Flica', 'Flicka')
    
    first_name_last_initial = _extract_first_name_last_initial(input_name)
    initials = _extract_initials(input_name)

    # list of player hash matches returned
    match = df.loc[(df['season_number'] == season_number) & (df['nick_name'].str.contains(input_name))]['standard_name'].values
    if len(match) > 0:
        return match[0]

    # initals match (only if initals are more than 1)
    if len(input_name.split()) > 1:
        match = df[df['standard_name'].apply(_extract_initials).str.contains(initials)]['standard_name'].values
        if len(match) > 0:
            return match[0]

    # Is the firstname in the nickname?
    for token in input_name.split():
        match = df.loc[(df['standard_name'].str.contains(token, na=False))]['standard_name'].values
        if len(match) > 0:
            return match[0]
    
    # list of player hash matches returned
    match = df[df['standard_name'].str.contains(first_name_last_initial)]['standard_name'].values
    if len(match) > 0:
        return match[0]

    # desperation first 2 letter of name
    match = df[df['standard_name'].str.contains(first_name_last_initial[:2])]['standard_name'].values
    if len(match) > 0:
        return match[0]

    return "NOMATCH"


def process_season_data(season_number):

    print(""" 
    ##########\n
    Season {}\n
    ##########
    """.format(season_number))

    # fetch data
    url = f'https://www.truedorktimes.com/survivor/boxscores/s{season_number}.htm'
    print("source: ", url)
    html_tables = utility.get_html_tables(url)
    complete_data = html_tables[0]
    challenge_data = html_tables[1]

    # Procees Complete Data Table 
    # Glossery https://www.truedorktimes.com/survivor/boxscores/glossary.htm
    # We dont need the first header row
    complete_data.columns = complete_data.columns.droplevel(0)  
    _rename_complete_data_columns(complete_data)

    complete_data.insert(0, 'matched_player_name', complete_data['name'].apply(lambda name: _get_player_hash(name, season_number)), True)

    # Individual challenge
    _rename_challenge_data_columns(challenge_data)
    challenge_data.insert(0, 'matched_player_name', challenge_data['name'].apply(lambda name: _get_player_hash(name, season_number)), True)
    
    # Create files
    complete_data.to_csv('resources/season{}_stats.csv'.format(season_number), index=False, quoting=csv.QUOTE_NONNUMERIC)
    challenge_data.to_csv('resources/season{}_stats_indiv.csv'.format(season_number), index=False, quoting=csv.QUOTE_NONNUMERIC)


def complete_boxscore_stats(start=1, end=40):
    final_df = pd.DataFrame()

    for season_number in range(start,end+1):
        # fetch data
        url = f'https://www.truedorktimes.com/survivor/boxscores/s{season_number}.htm'
        print("source: ", url)
        html_tables = utility.get_html_tables(url)
        complete_data = html_tables[0]

        complete_data.columns = complete_data.columns.droplevel(0)
        _rename_complete_data_columns(complete_data)

        complete_data.insert(0, 'matched_name', complete_data['name'].apply(lambda name: _match_player(name, season_number)), True)
        complete_data.insert(0, 'season', season_number, True)

        # append complete data to df
        final_df = pd.concat([final_df, complete_data], ignore_index=True)


    final_df.to_csv(GAME_STATS_FILE, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print("complete!")
    return

def individual_boxscore_stats(start=1, end=40):
    final_df = pd.DataFrame()

    for season_number in range(start,end+1):
        # fetch data
        url = f'https://www.truedorktimes.com/survivor/boxscores/s{season_number}.htm'
        print("source: ", url)
        html_tables = utility.get_html_tables(url)
        challenge_data = html_tables[1]

        # Individual challenge
        _rename_challenge_data_columns(challenge_data)

        challenge_data.insert(0, 'matched_name', challenge_data['name'].apply(lambda name: _match_player(name, season_number)), True)
        challenge_data.insert(0, 'season', season_number, True)

        # append complete data to df
        final_df = pd.concat([final_df, challenge_data], ignore_index=True)


    final_df.to_csv(CHALLENGE_STATS_FILE, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print("complete!")
    return

def process_season_range(start=1, end=39):
    for season in range(start,end+1):
        process_season_data(season)

def run():
    season_cap = 39
    complete_boxscore_stats(end=season_cap)
    individual_boxscore_stats(end=season_cap)
    #process_season_range(27,27)


if __name__ == '__main__':
    run()