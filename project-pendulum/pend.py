from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# Specify URL to teams table and request permission from servers

#nba_url = "https://www.oddsshark.com/nba/ats-standings"
#nhl_url = 
cbb_url = "https://www.oddsshark.com/ncaab/ats-standings"
page = requests.get(cbb_url)
#print(page.status_code)

# pass page object into BS
soup = BeautifulSoup(page.content, 'lxml')
#print(soup.prettify())

# Create the table of team,ATS_Rec,Cov%,MOV,ATS+/-
tables = soup.find_all('table', class_='table table--striped table--fixed-column caption--plain')
#print(table)

headers = []
for col in tables[0].find_all('th'):
    title = col.text
    headers.append(title)

#print (headers)

# combine all tables in tables into one table/dataframe
df = pd.DataFrame(columns=headers)

# tables[0] == America East
# each <tr class> is a row, with several <td class> col values
for conf in tables:
    for j in conf.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(df)
        df.loc[length] = row

#print(df)

df1 = df.sort_values('ATS Streak').tail(20)
print(df1)
