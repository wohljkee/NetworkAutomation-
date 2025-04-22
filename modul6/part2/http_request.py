import requests

response  = requests.get('https://www.google.com/index.html')
print(response)

response = requests.post('https://www.google.com/api/')
print(response)