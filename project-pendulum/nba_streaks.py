from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# 12/11/23 TODO: Figure out why this is a separate file from pend.py
#   My guess is NBA formatting on OddShark was slightly annoyingly different from CBB
# TODO: add sport-specific functions to pend.py, DELETE THIS

# Specify URL to teams table and request permission from servers
nba_url = "https://www.oddsshark.com/nba/ats-standings"
page = requests.get(nba_url)
print(page.status_code)

# pass page object into BS
soup = BeautifulSoup(page.content, 'lxml')
#print(soup.prettify())

tables = soup.find_all('table', class_='table--striped table--fixed-column caption--plain table block block-oddsshark-data-blocks block-standings-block')
#print(table)

headers = []
print(tables[0])
for col in tables[1].find_all('th'):
    title = col.text.replace('\t',"").replace('\n',"").strip()
    headers.append(title)
print (headers)

df = pd.DataFrame(columns=headers)

# combine all tables dataframe
# each <tr class> is a row, with several <td class> col values
for conf in tables:
    for j in conf.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        df.loc[len(df)] = row

df1 = df.sort_values('ATS Streak',ascending=False).head(15)
print(df1)
