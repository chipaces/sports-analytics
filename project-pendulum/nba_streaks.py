from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# Specify URL to teams table and request permission from servers
# FUCKKKKKK ODDSSHARK HAS BOGUS ASS ATS RECORDS
nba_url = "https://www.oddsshark.com/nba/ats-standings"
page = requests.get(nba_url)
print(page.status_code)

# pass page object into BS
soup = BeautifulSoup(page.content, 'lxml')
#print(soup.prettify())

tables = soup.find_all('table', class_='table table--striped table--fixed-column caption--plain')
#print(table)

headers = []
print(tables[0])
for col in tables[1].find_all('th'):
    title = col.text.replace('\t',"").replace('\n',"")
    headers.append(title)
print (headers)

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
