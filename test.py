import requests
from bs4 import BeautifulSoup

url_for_date = requests.get('http://oblenergo.cv.ua/shutdowns')

soup = BeautifulSoup(url_for_date.content, "html.parser")

current_date = soup.find("div", {"data-id": "14"}).text

print(current_date)


list = []
for num, i in enumerate(current_date):
    if i == 'в':
        list.append(num)
    else:
        list.append('|')

print(list)

list_test = []
list_res = []
for num, j in enumerate(list):
    if num == 0:
        if type(j) is int:
            list_res.append([j])
    else:
        if len(list_res) == 0:
            if type(j) is int:
                list_res.append([j])
        else:
            len_list = len(list_res)
            if type(list_test[-1]) is int:
                if j == '|':
                    if not list_test[-1] == list_res[-1][-1]:
                        list_res.append([list_test[-1]])

            if list_test[-1] == '|':
                if type(j) is int:
                    list_res.append([j])
            else:
                if type(j) is int:
                    list_res[len_list - 1].append(j)
    list_test.append(j)

print(list_res)

list_out = []
for count, k in enumerate(list_res):
    list_count = len(list_res)
    if count + 1 == list_count:
        list_out.append(f'{k[0]}-{k[-1] + 1}')
        continue
    list_out.append(f'{k[0]}-{k[-1] + 1}')

print(list_out)
# for num ,i in enumerate(current_date):
#     if i == "в":
#         print(num)

# list_test = []
# list_res = []
# for num, j in enumerate(current_date):
#     if num == 0:
#         if j == "з":
#             list_res.append([j])
#     else:
#         if len(list_res) == 0:
#             if j == "з":
#                 list_res.append([j])
#         else:
#             len_list = len(list_res)
#             if list_test[-1] == "з":
#                 if j == 'в':
#                     if not list_test[-1] == list_res[-1][-1]:
#                         list_res.append([list_test[-1]])
#
#             if list_test[-1] == 'в':
#                 if j == "в":
#                     list_res.append([j])
#             else:
#                 if j == "з":
#                     list_res[len_list - 1].append(j)
#     list_test.append(j)
#
# print(list_res, list_test)