import requests

headers = {
    'Api-Key': 'DlG6xeD3ni5z1aGYq3HCDuYDkb200sPp',
    'Content-Type': 'application/json',
}

data = '{"username":"azizbek","password":"@xQ6$ZEVb*$iccZ"}'

response = requests.post('https://www.opensubtitles.com/api/v1/login', headers=headers, data=data)
print(response)
