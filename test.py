import datetime

import requests
from bs4 import BeautifulSoup

url_for_date = requests.get('http://oblenergo.cv.ua/shutdowns')

soup = BeautifulSoup(url_for_date.content, "html.parser")

current_date = soup.find("div", {"data-id": "14"}).text

print(list(current_date))
res_list = []
test_list = None
for i in current_date:
    if i == 'м':
        test_list = i
        continue
    if test_list == 'м':
        if i == 'з':
            res_list.append('з')
            test_list = i
            continue
    if i == 'з':
        res_list.append('з')
    if i == 'в':
        res_list.append('в')
    test_list = i

print(current_date)
from datetime import datetime

time = datetime.now().strftime("%H")
print(type(time))

