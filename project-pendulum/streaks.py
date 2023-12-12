from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

# Specify URL to teams table and request permission from servers

nba_url = "https://www.oddsshark.com/nba/ats-standings"
cbb_url = "https://www.oddsshark.com/ncaab/ats-standings"
# TODO: look for nhl_url (not on OddShark)
page = requests.get(cbb_url)
if page.status_code != 200:
    print(f"Failed to fetch data: {page.status_code}")
    sys.exit(1)

# pass page object into BS
soup = BeautifulSoup(page.content, 'lxml')

# tables is list of HTML table elements (NBA divs, NCAAB confs)
tables = soup.find_all('table', class_='table--striped table--fixed-column caption--plain table block block-oddsshark-data-blocks block-standings-block')

headers = []
# Use tables[0] to get col names
for col in tables[0].find_all('th'):
    title = col.text.strip().replace(' ','-')
    headers.append(title)

df = pd.DataFrame(columns=headers)

# combine all tables into df
# each <tr class> is a row, with several <td class> col values
for t in tables:
    for i in t.find_all('tr')[1:]:
        row_data = i.find_all('td')
        row = [j.text for j in row_data]
        df.loc[len(df)] = row

df.sort_values('ATS-Streak',ascending=False,inplace=True)
print(df[['Team','ATS-Streak']].head(15))