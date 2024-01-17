# Remix of streaks.py to pull from TeamRankings
# From teamrankings.com/ncb/trends/ats_trends :
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import datetime as dt

# Assuming this gets working--possible to generalize to sport?
# BIG TODO: If not, write specific funcs for each sport on TR

# TODO: Extract + add 'Next Game' column
# team rankings home page
tr_url = "https://www.teamrankings.com/ncb/trends/ats_trends/"

# Define lists for streak frequencies
# TODO: Add 'maxAtsStrk', 'maxOvrStrk' and 'maxUndStrk'
ats_freqs=[0]*20
ovr_freqs=[0]*20
undr_freqs=[0]*20
atsStrk=0
ovrStrk=0
# TODO: change this to some 'today' variable from dt library
date = dt.date(2023,1,4)

page = requests.get(tr_url)
if page.status_code != 200:
    print(f"Failed to fetch data: {page.status_code}")
    sys.exit(1)


# use SoupStrainer to just grab the teams table?
# Get full page from TeamRankings
soup = BeautifulSoup(page.content, 'lxml')

# find_all returns set of PageElements ... this is (I assume) of size 1
teams_table = soup.find_all('table',id_='DataTables_Table_0')
print(type(teams_table))

links = list()
for link in teams_table.find_all('a'):
    links.append(link.get('href'))
    #print(link.get('href'))
print(len(links))
# Question: faster to import all team schedules as DFs (and flagging bold values somehow) before 
    # doing streak analysis, or analyze as we import?

# TODO: Add some output / logging messages
# TODO: include some time/space logging as well? 'Took this long:'
# For each D1 team:
    # Grab its team page (w BeautifulSoup?)
    # Grab its Betting View table (HTML element)
    # For each <tr> in table <tbody> (each <tr> is a game), or ... while <tr>[0].date < TODAY (?):
        # look at the 7,8,9th (1-indexed) <td> elements (<td class="betting text-right" ... /td>)
        # if 7th <td> elem is bold (style="font-weight: bold;"):
            # if atsStrk < 0:
                # ats_freqs[abs(atsStrk)] += 1
                # atsStrk = 1
            # Else incremement ATS Streak
        # else (if team did not cover):
            # check if team was on ATS win streak
            # if atsStrk > 0:
                # ats_freqs[abs(atsStrk)] += 1
                # set atsStreak = -1
            # else decrement ATS_Streak

        # if 8th <td> elem is bold (style="font-weight: bold;"):
            # check if team was on under streak
            # if ovrStrk < 0:
                # under_freqs[abs(ovrStrk)] += 1
                # set ovrStrk = 1
            # else increment ovrStrk
        # else:
            # check if team was on over streak
            # if ovrStrk > 0:
                # ovr_freqs[ovrStrk] += 1
                # set OvrStrk = -1
            # else decrement ovrStrk




# dataframe headers : Date,Opponent,Result,Spread,Total,Money
# <table class="tr-table datatable scrollable dataTable no-footer" id="DataTables_Table_0" role="grid">