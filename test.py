import requests
from bs4 import BeautifulSoup

url_for_date = requests.get('http://oblenergo.cv.ua/shutdowns')

soup = BeautifulSoup(url_for_date.content, "html.parser")

current_date = soup.find("div", {"id": "gsv"}).find('p').text

print(current_date)