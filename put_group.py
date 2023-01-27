import requests
import json
url_put = 'https://api.jsonbin.io/v3/b/63d42f19ace6f33a22c94f26'
url_get = 'https://api.jsonbin.io/v3/b/63d42f19ace6f33a22c94f26/latest'
headers_put = {
  'Content-Type': 'application/json',
  'X-Master-Key': '$2b$10$TWMYDoj4.wAMi7q.1XwiieeX.NwIRU68gFC9.ILWiivN2vsPtB0DO',
}
headers_get = {
  'X-Master-Key': '$2b$10$TWMYDoj4.wAMi7q.1XwiieeX.NwIRU68gFC9.ILWiivN2vsPtB0DO',
}

get = requests.get(url_get, json=None, headers=headers_get).json()

y = json.dumps(get)
x = json.loads(y)

number_of_group = x['record']['group']

print(f'Зараз встановлений номер - {number_of_group}\n')

group = input('Введіть номер групи\n'
              'Зарожани - 1\n'
              'Млинки - 2\n'
              'Чернівці - 14\n'
              ':')

data = {"group": int(group)}

put = requests.put(url_put, json=data, headers=headers_put)

