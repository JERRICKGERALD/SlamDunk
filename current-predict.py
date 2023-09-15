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

from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, ElasticNet
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV


def strip_accents_and_periods(text):
    '''Normalize player name spellings'''
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)           .encode('ascii', 'ignore')           .decode("utf-8")
    return str(text).replace('.','')


def lowercasestrip(string):
    '''Lowercase player names and remove spaces/punctuation'''
    try:
        string = (string.replace('-','').replace('_','').
                  replace(' ','').replace('.','').replace('\'','').lower())
    except:
        pass
    return string

def dollarstoint(string):
    '''Convert hoopshype salary info to integer number of dollas'''
    try:
        string = str(string)
        string = string.replace('$','').replace(',','')
        return int(string)
    except:
        return np.nan


## Generate predictions on saved current season player stats

dfcurrentsal = pd.read_csv(r"C:\Users\Jerrick\Downloads\DataEngineering_project-main\DataEngineering_project-main\data\dfsal2021_bbr.csv")
dfcurrentsal = dfcurrentsal.set_index('Player',drop=True)

dfnba = pd.read_csv(r"C:\Users\Jerrick\Downloads\DataEngineering_project-main\DataEngineering_project-main\data\df_clean.csv")
dfnba = dfnba.set_index('name-year',drop=True)

dfcurrent = pd.read_csv(r"C:\Users\Jerrick\Downloads\DataEngineering_project-main\DataEngineering_project-main\data\df_current_clean.csv")
dfcurrent = dfcurrent.set_index('Player',drop=True)

def add_new_features(df_):
    df = df_.copy()
    maxgames = df.G.max()
    df['GS/G'] = df['GS']/df['G']
    df['G/MaxG'] = df['G']/maxgames
    df['MP_sq'] = df['MP']**2
    df['PTS_sq'] = df['PTS']**2
    return df

dfnba = add_new_features(dfnba)
dfcurrent = add_new_features(dfcurrent)

feats = ['Age', 'G/MaxG','GS/G','MP','MP_sq','3P','3P%','FT','TRB','AST', 'TOV','PTS','PTS_sq']

lr_filename = r"C:\Users\Jerrick\Downloads\DataEngineering_project-main\DataEngineering_project-main\data\lr_model.sav"
loaded_model = pickle.load(open(lr_filename, 'rb'))


market_vals = loaded_model.predict(dfcurrent[feats])
dfcurrent['Market_Val'] = market_vals


dfcurrent =  dfcurrent.reset_index()
dfcurrent['Name'] = dfcurrent['Player'].apply(strip_accents_and_periods).apply(lowercasestrip)
dfcurrent = dfcurrent.set_index('Name',drop=True)
dfcurrent

def addcurrentsal(dfcurrent_, dfcurrentsal_):
    '''create new dataframe with columns for current and previous salary info'''

    dfnew = dfcurrent_.copy()
    for index, row in dfcurrent_.iterrows():
        try:
            dfnew.loc[index, 'Current_Sal'] = dollarstoint(dfcurrentsal_.loc[index, 'Salary'])/1e6
        except:
            dfnew.loc[index, 'Current_Sal'] = np.nan
    return dfnew

dfcurrent = addcurrentsal(dfcurrent, dfcurrentsal)
dfcurrent.to_csv(r"C:\Users\Jerrick\Downloads\DataEngineering_project-main\DataEngineering_project-main\data\df_marketvalues.csv")
