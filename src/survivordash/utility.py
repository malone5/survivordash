import requests
import hashlib
import pandas as pd
from bs4 import BeautifulSoup

def get_html_tables(url):
    html_ctx = requests.get(url).text
    html_tables = pd.read_html(html_ctx)
    return html_tables

def get_df_tables(url):
    html_ctx = requests.get(url).text
    soup = BeautifulSoup(html_ctx, features="html.parser")
    tables = soup.find_all('table')
    df_tables = pd.read_html(str(tables)) 
    return df_tables


def _hash_player_name(name):
    MAX_LENGTH = 5
    return hashlib.md5(name.encode()).hexdigest()[:MAX_LENGTH]