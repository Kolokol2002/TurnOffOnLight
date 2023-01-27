import requests
url = 'https://api.jsonbin.io/v3/b/63d42f19ace6f33a22c94f26'
headers = {
  'Content-Type': 'application/json',
  'X-Master-Key': '$2b$10$TWMYDoj4.wAMi7q.1XwiieeX.NwIRU68gFC9.ILWiivN2vsPtB0DO',
}

group = input('Введіть номер групи\n'
              'Зарожани - 1\n'
              'Млинки - 2\n'
              'Чернівці - 14\n'
              ':')

data = {"group": int(group)}

req = requests.put(url, json=data, headers=headers)
