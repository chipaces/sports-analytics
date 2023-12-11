import requests

api_key='632f34156395fe9b6d29b1fdca78ad52'
url='https://api.the-odds-api.com/v4/sports/?apiKey='

response=requests.get(url+api_key)
if response.status_code == 200:
    data=response.json()
else:
    print(f"Failed to fetch data: {response.status_code}")
print(data[0])