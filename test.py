import datetime

import requests
from bs4 import BeautifulSoup

url_for_date = requests.get('https://oblenergo.cv.ua/shutdowns')
soup = BeautifulSoup(url_for_date.content, "html.parser")


new_grapfic = soup.find("a", {"href": '/shutdowns/?next'})


print(bool(new_grapfic))

