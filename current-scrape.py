#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
import random

import pickle

from bs4 import BeautifulSoup
import requests
import lxml
import unicodedata


## Scrape current-season NBA stats
## This should be done daily

def scrape_current_season_stats(url):
    '''Get current season stats for all players from basketball-reference.com'''
    d = {}
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    df = pd.read_html(str(soup.find(id='all_per_game_stats')))[0]
    return df


def clean(df_raw):
    df = df_raw.copy()
    #Remove spurious rows
    df = df[df['Rk'].astype(str).str.isdigit()]
    df = df.set_index('Rk')
    #Normalize names
    df['Player'] = df['Player'].apply(strip_accents_and_periods)
    df['FG%'].fillna(df['FG%'].median(), inplace=True)  # no FG: assume median
    df['FT%'].fillna(df['FT%'].median(), inplace=True)  # no FT: assume median
    df['3P%'].fillna(0, inplace=True)                   # no threes: assume the worst
    cols = ['PTS','AST','Age','G','GS','MP','3P','3PA','FT','FTA','ORB', 'TRB', 'AST', 'STL', 'BLK',
            'TOV', 'PTS','3P%','FT%','FG%']
    for col in cols:
        df[col] = df[col].apply(lambda s: pd.to_numeric(s, errors='coerce'))
    return df


def strip_accents_and_periods(text):
    '''Normalize player name spellings'''
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)           .encode('ascii', 'ignore')           .decode("utf-8")
    return str(text).replace('.','')


url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html'
dfcurrent = scrape_current_season_stats(url)
dfcurrent = clean(dfcurrent)
dfcurrent.to_csv(r"C:\Users\Jerrick\Downloads\DataEngineering_project-main\DataEngineering_project-main\data\df_current_clean.csv")
