import requests

url = 'https://catfact.ninja/fact'

response = requests.get(url)

print(response.text)