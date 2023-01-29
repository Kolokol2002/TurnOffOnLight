import logging
import time

import requests
import json
from bs4 import BeautifulSoup

from aiogram import Dispatcher

from builtins import SystemExit

from data.config import admins

from app import number_of_group

async def on_startup_notify(dp: Dispatcher):
    #virtual variable
    url_data_put = 'https://api.jsonbin.io/v3/b/63d521a9c0e7653a0563205b'
    url_data_get = 'https://api.jsonbin.io/v3/b/63d521a9c0e7653a0563205b/latest'
    headers_data_put = {
        'Content-Type': 'application/json',
        'X-Master-Key': '$2b$10$TWMYDoj4.wAMi7q.1XwiieeX.NwIRU68gFC9.ILWiivN2vsPtB0DO',
    }
    headers_data_get = {
        'X-Master-Key': '$2b$10$TWMYDoj4.wAMi7q.1XwiieeX.NwIRU68gFC9.ILWiivN2vsPtB0DO',
    }

    # number group
    number_group = number_of_group

    url_for_date = requests.get('https://oblenergo.cv.ua/shutdowns/?next')
    soup = BeautifulSoup(url_for_date.content, "html.parser")

    current_date_group = soup.find("div", {"data-id": str(number_group)}).text

    list_date = []
    for num, i in enumerate(current_date_group):
        if i == 'в':
            list_date.append(num)
        else:
            list_date.append('|')

    # parse clock list
    list_test = []
    list_res = []
    for num, j in enumerate(list_date):
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

    # parse list with result in normal view
    list_out = []
    for count, k in enumerate(list_res):
        list_count = len(list_res)
        if count + 1 == list_count:
            list_out.append(f'{k[0]}-{k[-1] + 1}')
            continue
        list_out.append(f'{k[0]}-{k[-1] + 1}')

    # parse list out for send in telegram
    soup = BeautifulSoup(url_for_date.content, "html.parser")
    current_date = soup.find("div", {"id": "gsv"}).find('p').text

    def get_data():
        data = ''
        if number_group == 1:
            data += 'Зарожани\n'
        if number_group == 2:
            data += 'Млинки\n'
        if number_group == 14:
            data += 'Че\n'
        for p in list_out:
            data += f'{p}\n'
        data += f'---------------\n{current_date}'
        return data

    # send list in  telegram message (only admins)
    data_out = get_data()

    get = requests.get(url_data_get, json=None, headers=headers_data_get).json()
    y = json.dumps(get)
    x = json.loads(y)['record']['data']

    if data_out == x:
        try:
            id = await dp.bot.send_message(454836837, "False")
            time.sleep(5)
            await dp.bot.delete_message(454836837, id['message_id'])
            raise SystemExit()

        except Exception as err:
            logging.exception(err)

    else:
        data = {"data": data_out}
        put_data = requests.put(url_data_put, json=data, headers=headers_data_put)
        for admin in admins:
            try:
                await dp.bot.send_message(admin, get_data())

            except Exception as err:
                logging.exception(err)

        raise SystemExit()

