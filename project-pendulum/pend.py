from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# Specify URL to teams table and request permission from servers

nba_url = "https://www.oddsshark.com/nba/ats-standings"
#nhl_url = 
cbb_url = "https://www.oddsshark.com/ncaab/ats-standings"
page = requests.get(cbb_url)
#print(page.status_code)

# pass page object into BS
soup = BeautifulSoup(page.content, 'lxml')
#print(soup.prettify())

# Build list of conf tables (OddShark groups by conf)
tables = soup.find_all('table', class_='table--striped table--fixed-column caption--plain table block block-oddsshark-data-blocks block-standings-block')
#print(len(tables)) # number of CBB D1 conferences

headers = []
# Use tables[0] to get col names (tables[0]==America East)
for col in tables[0].find_all('th'):
    title = col.text.strip()
    headers.append(title)
#print (headers)

# build dataframe
df = pd.DataFrame(columns=headers)

# combine all tables into df
# each <tr class> is a row, with several <td class> col values
for conf in tables:
    for j in conf.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        df.loc[len(df)] = row

df1 = df.sort_values('ATS Streak',ascending=False).head(15)
print(df1)
