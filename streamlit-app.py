#!/usr/bin/env python
# coding: utf-8

# import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

# Add CSS for the background image

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://c4.wallpaperflare.com/wallpaper/56/162/480/text-wall-typography-change-nba-basketball-michael-jordan-chicago-bulls-black-background-sports-basketball-hd-art-wallpaper-preview.jpg");
background-size: 100%;
background-position: center;
background-repeat: no-repeat;
background-attachment: local;
background-size: cover;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)



tm_to_team =  {
 'TOR': 'Toronto Raptors',         'MEM': 'Memphis Grizzlies',
 'MIA': 'Miami Heat',              'BRK': 'Brooklyn Nets',
 'NOP': 'New Orleans Pelicans',    'MIL': 'Milwaukee Bucks',
 'CLE': 'Cleveland Cavaliers' ,    'LAL': 'Los Angeles Lakers',
 'ORL': 'Orlando Magic',           'HOU': 'Houston Rockets' ,
 'WAS': 'Washington Wizards' ,     'PHO': 'Phoenix Suns',
 'UTA': 'Utah Jazz',               'SAC': 'Sacramento Kings',
 'CHO': 'Charlotte Hornets',       'CHI': 'Chicago Bulls' ,
 'NYK': 'New York Knicks',         'DEN': 'Denver Nuggets' ,
 'PHI': 'Philadephia 76ers' ,      'SAS': 'San Antonio Spurs' ,
 'LAC': 'Los Angeles Clippers',    'OKC': 'Oklahoma City Thunder' ,
 'MIN': 'Minnesota Timberwolves',  'DET': 'Detroit Pistons' ,
 'IND': 'Indiana Pacers',          'GSW': 'Golden State Warriors' ,
 'POR': 'Portland Trailblazers',   'ATL': 'Atlanta Hawks',
 'BOS': 'Boston Celtics',          'DAL':'Dallas Mavericks',
 }
team_to_tm =  {v: k for k, v in tm_to_team.items()}


st.title("SlamDunk Prognosticator")
st.markdown('''
####  <span style="color:white"> Market value of NBA players </span> 
''', unsafe_allow_html=True)
st.write('---')


data = pd.read_csv('data/df_marketvalues.csv')
data = data.set_index('Player', drop=False)
datanice = data.copy()
# datanice = datanice.set_index('Player', drop=False)
datanice = datanice[['Tm','Age','Pos','Current_Sal','Market_Val','G','GS','MP','FG%','PTS','AST', 'TRB']]
my_dict = {'Market_Val':'Value ($M)', 'Current_Sal':'Salary ($M)', 'MP':'MPG'}
datanice = datanice.rename(columns=my_dict)


st.sidebar.markdown(" # Your Favorite Player from Team: (Mine is Forever Mamba)")
image_url = "https://c4.wallpaperflare.com/wallpaper/402/588/984/kobe-bryant-nba-los-angeles-lakers-basketball-hd-wallpaper-preview.jpg"  # Replace with the URL of your image


st.sidebar.image(image_url)
team = st.sidebar.selectbox("Team (your Clan):",
                                   sorted(team_to_tm.keys()))
tm = team_to_tm[team]

player = st.sidebar.selectbox("Player (Your Hero):",
                                      (data[data['Tm'] == tm].Player.unique()))

salary = data.loc[player].Current_Sal.round(1)
market_value = data.loc[player].Market_Val.round(1)

st.write(f'''
         ##### This year, <span style="color:orange">{player}</span> is earning a salary of <span style="color:orange"> ${salary}M </span>
          ##### The model result, his market value is <span style="color:orange">${market_value}M</span>
         ''', unsafe_allow_html=True)

st.write('---')
st.write(f'''
         
         #### {team}:
         ''')



my_data = datanice[datanice['Tm'] == tm]
my_format =  {'MPG': '{:.1f}', 'FG%': '{:.3f}','PTS': '{:.1f}', 'AST': '{:.1f}',
                                    'TRB': '{:.1f}', 'Value ($M)':'{:.1f}', 'Salary ($M)':'{:.1f}',
                                   }
st.dataframe(my_data.style.format(my_format))

