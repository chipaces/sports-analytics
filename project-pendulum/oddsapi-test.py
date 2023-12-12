import requests
import sys

api_key='632f34156395fe9b6d29b1fdca78ad52'
url='https://api.the-odds-api.com/v4/sports/?apiKey='

response=requests.get(url+api_key)
if response.status_code != 200:
    print(f"Failed to fetch data: {response.status_code}")
    sys.exit(1)
data=response.json()

print(data[0])