from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

def main(sport):
    # Specify URL to teams table and request permission from servers
    urls = {
        "nba": ["https://www.oddsshark.com/nba/ats-standings", 4],
        "cbb": ["https://www.oddsshark.com/ncaab/ats-standings", 6]
        # TODO: look for nhl_url (not on OddShark)
    }
    if sport not in urls.keys():
        print("Invalid arg!")
        sys.exit(1)
    
    page = requests.get(urls[sport][0])
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

    df['Streak-Length'] = df['ATS-Streak'].str.extract('(\d+)').astype(int)
    df.sort_values('Streak-Length',ascending=False,inplace=True)

    # TODO: add parameter for 'streak_length', 'cumul'
        # streak_len (int, Default=6): int value corres
        # cumul (bool, Default=True): true->shows all streaks >= streak_len. false->shows only streaks==streak_len
    # TODO: add feature for no sport given -> show both/all sport tables side-by-side
        # (combine dataframes of both/all sports)
    # Can't help but feel like I'm using a Python script to do a database's job

    print(df[df['Streak-Length'] >= urls[sport][1]][['Team', 'ATS-Streak']])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing arguments!")
        sys.exit(1)
    main(sys.argv[1].lower())
        