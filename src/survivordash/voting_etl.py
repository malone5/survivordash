import sys
import os
import requests
import csv
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re

from survivordash import utility
from survivordash.wiki_etl import SEASON_PLAYERS_FILE
import requests


""" Boxscore data pulled from https://www.truedorktimes.com/survivor/boxscores/data.htm"""

FILEPATH = os.path.dirname(os.path.abspath(__file__)) # directory of this file
RESOURCE_PATH = FILEPATH + '/resources/'

def get_season_wiki_url(season_number):
    all_seasons_wiki = 'https://en.wikipedia.org/wiki/Survivor_(American_TV_series)'
    tables = utility.get_html_tables(all_seasons_wiki)
    target_row = season_number-1
    season = tables[1].iloc[target_row]['Season title']
    season_wiki_url = "https://en.wikipedia.org/wiki/" + season.replace(" ", "_")
    return season_wiki_url


def get_voting_table(season_number):
    season_wiki_url = get_season_wiki_url(season_number)
    tables = utility.get_df_tables(season_wiki_url)
    voting_table = tables[4]
    voting_table = voting_table.reset_index(drop=True)
    return voting_table


def elimination_results(df, season_number):
    # set dimensions
    ROW_START, ROW_END = 2, 6
    df.set_index(df.columns[0], drop=True, inplace=True)
    df = df.iloc[ROW_START:ROW_END] # slice sub-table

    # pivot
    pivot = df.T
    pivot.columns = ['Episode', 'Day', 'Eliminated', 'Vote']
    pivot.reset_index(drop=True, inplace=True)
    pivot.to_csv('test.csv', index=False)
    pattern = r"\[.+\]" # between brackets []
    endash = "\u2013"
    pivot['Vote'] = pivot['Vote'].apply(lambda x: re.sub(pattern, '',  x).replace(endash, "-"))
    pivot['VoteId'] = pivot.apply(lambda row: ('S' + str(season_number) + 'E' + row['Episode']), axis=1)

    def _extract_majority_votecount(vote_string):
        if '-' not in vote_string:
            return 0
        return vote_string.split('-')[0]

    pivot['MajorityVoteCount'] = pivot['Vote'].apply(lambda x: _extract_majority_votecount(x))

    def _extract_total_votes(vote_string):
        if '-' not in vote_string:
            return 0
        return sum(int(votes) for votes in vote_string.split('-'))

    pivot['TotalVotesCast'] = pivot['Vote'].apply(lambda x: _extract_total_votes(x))
    print(pivot)
    return pivot

def vote_history(df, season_number):
    # structure: Voter, VoteID, VoteTarger
    # set dimensions
    ROW_START, ROW_END = 8, 24
    df = df.iloc[ROW_START:ROW_END] # slice sub-table

    df_dict = df.replace({np.nan:None}).to_dict()

    data = []
    for episode in df_dict:
        for voter, target in df_dict[episode].items():
            if not target:
                continue

            #print(f'In Episode {episode}, {voter} voted for {target}')
            data.append((season_number, episode, voter, target))


    votes_df = pd.DataFrame(data, columns=['Season', 'Episode', 'Voter', 'VotedFor'])
    votes_df['VoteID'] = votes_df.apply(lambda row: ("S" + str(season_number) + 'E' + row['Episode']), axis=1)
    print(votes_df)
    return votes_df


def extract_all_vote_results(season_number):
    vote_table = get_voting_table(season_number)
    EPISODE_NUMBER_ROW = 2
    vote_table.columns = vote_table.iloc[EPISODE_NUMBER_ROW] # Episode numbers as our header row
    vote_table = vote_table.loc[:,~vote_table.columns.duplicated(keep='last')] # Condense special outcomes formatting

    elimination_df = elimination_results(vote_table, season_number)
    votes_df = vote_history(vote_table, season_number)
    


def run():
    season_cap = 3

    for season in range(2, season_cap):
        extract_all_vote_results(season)


if __name__ == '__main__':
    run()