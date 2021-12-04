
import os, sys
import re
import numpy as np
import pandas as pd
from survivordash import utility
from db import get_db_engine


""" Boxscore data pulled from https://www.truedorktimes.com/survivor/boxscores/data.htm"""

FILEPATH = os.path.dirname(os.path.abspath(__file__)) # directory of this file
RESOURCE_PATH = FILEPATH + '/resources/'
ALL_SEASONS_WIKI_URL = 'https://en.wikipedia.org/wiki/Survivor_(American_TV_series)'

def _get_season_wiki_url(season_number):
    tables = utility.get_html_tables(ALL_SEASONS_WIKI_URL)
    target_row = season_number-1
    season = tables[1].iloc[target_row]['Season title']
    season_wiki_url = "https://en.wikipedia.org/wiki/" + season.replace(" ", "_")
    return season_wiki_url


def _get_voting_table(season_number):
    season_wiki_url = _get_season_wiki_url(season_number)
    print(season_wiki_url)
    tables = utility.get_df_tables(season_wiki_url)
    voting_table = tables[4]
    voting_table = voting_table.reset_index(drop=True)
    return voting_table

def _elimination_results(season_number):
    df = _get_voting_table(season_number)

    # set dimensions
    ROW_START, ROW_END = 2, 6
    df.set_index(df.columns[0], drop=True, inplace=True)
    df = df.iloc[ROW_START:ROW_END] # slice sub-table
    df.columns = df.iloc[1] # Episode numbers
    df = df.loc[:,~df.columns.duplicated(keep='last')] # remove duplicats cols

    # pivot
    pivot = df.T
    pivot = pivot.iloc[1: , :] # drop first row, its a duplicated of our header
    pivot.columns = ['Episode', 'Day', 'Eliminated', 'Vote']
    pivot.reset_index(drop=True, inplace=True)
    pattern = r"\[.+\]" # between brackets []
    endash = "\u2013"
    pivot['Vote'] = pivot['Vote'].apply(lambda x: '0' if pd.isnull(x) else re.sub(pattern, '',  x).replace(endash, "-"))
    pivot['VoteId'] = pivot.apply(lambda row: ('S' + str(season_number) + 'E' + str(row['Episode'])), axis=1)

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
    pivot.insert(0, 'Season', season_number, allow_duplicates=True)
    return pivot


def _final_vote_dict(season_number):
    # we take from https://en.wikipedia.org/wiki/Survivor_(American_TV_series)
    table = utility.get_html_tables(ALL_SEASONS_WIKI_URL)[1]
    target_row = season_number-1
    df = table.iloc[target_row]

    runners = " & ".join(set([df['Runner(s)-up'], df['Runner(s)-up.1']]))

    final_vote = {
        "Season": season_number,
        "Winner": df['Winner'],
        "Runners": runners,
        "Vote": df['Final vote']
    }
    return final_vote

    
def extract_final_vote_results(start, end):
    print(f"fetching final votes for seasons {start} - {end-1}...")
    header_row = ['Season', 'Winner', 'Runners', 'Vote']
    rows = []
    for season_num in range(start, end):
        final_vote = _final_vote_dict(season_num)
        row = [final_vote['Season'], final_vote['Winner'], final_vote['Runners'], final_vote['Vote']]
        rows.append(row)

    df = pd.DataFrame(data=rows, columns=header_row)
    # Load to lake
    engine = get_db_engine()
    df.to_sql('final_votes', engine, schema='lake', if_exists='replace', index=False)


def extract_elimination_stats(start, end):

    final_df = None
    for season_num in range(start, end):
        df = _elimination_results(season_num)
        if final_df is not None:
            pd.concat([final_df, df])
        else:
            final_df=df

    engine = get_db_engine()
    final_df.to_sql('votes', engine, schema='lake', if_exists='replace', index=False)



def run():
    season_start = 1
    season_cap = 10
    extract_final_vote_results(season_start, season_cap)
    extract_elimination_stats(season_start, season_cap)
    


if __name__ == '__main__':
    run()