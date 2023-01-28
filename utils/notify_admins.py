import logging
import time

import requests
import json
from bs4 import BeautifulSoup

from PIL import Image
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

    # open oblenergo
    img = requests.get('http://oblenergo.cv.ua/shutdowns/GPV.png')

    # download image
    img_file = open('./gvp.png', 'wb')
    img_file.write(img.content)
    img_file.close()

    image = Image.open('./gvp.png')
    w, h = image.size

    # colors of pixel
    green_pix = [(1, (196, 208, 157, 255))]
    red_pix = [(1, (222, 116, 101, 255))]
    silver_pix = [(1, (217, 217, 217, 255))]
    white_pix = [(1, (255, 255, 255, 255))]
    light_green_pix = [(1, (222, 224, 201, 255))]
    black_pix = [(1, (0, 0, 0, 255))]

    # coordinate to cut image
    left = int()
    top = int()
    top_undo_green = int()
    rigth = w
    bottom = int()
    section_size_h = int()

    # deffind coordinate on image
    # top
    count_top = 0
    count_green = 0
    for i in range(0, 300):
        im_top = image.crop((10, 0 + i, 10 + 1, 1 + i))
        im_top_col = Image.Image.getcolors(im_top)
        if im_top_col == green_pix:
            if count_green == 0:
                top_undo_green = i
                count_green += 1
                continue
        if im_top_col == silver_pix:
            if count_top == 0:
                count_top += 1
                continue
            else:
                top = i + 1
                continue
        if im_top_col == light_green_pix:
            section_size_h = i - top + 1
            break
    # left
    for i in range(0, 300):
        im_left = image.crop((0 + i, top_undo_green, 1 + i, top_undo_green + 1))

        imm_left_col = Image.Image.getcolors(im_left)
        if imm_left_col == green_pix:
            left = i
            break
    # bottom
    for num_bottom, i in enumerate(range(0, 300)):
        im_bottom = image.crop((left, h - 1 - i, left + 1, h - i))

        imm_bottom_col = Image.Image.getcolors(im_bottom)
        if imm_bottom_col == silver_pix:
            bottom = num_bottom
            break

    # # rigth
    # for num_rigth, i in enumerate(range(0, 300)):
    #     im_rigth = image.crop(((w - 1) - i, h - bottom, w - i, (h - bottom) + 1))
    #
    #     im_rigth_col = Image.Image.getcolors(im_rigth)
    #     if im_rigth_col == white_pix:
    #         rigth = num_rigth
    #         break

    # cut image of deffind coordinate
    crop_res = image.crop((left, top, rigth, h - bottom))
    image.close()
    w_size, h_size = crop_res.size

    # formula for cut group section
    group_size = number_group * section_size_h

    # cut group section
    group = crop_res.crop((0, group_size - section_size_h, w_size, group_size))

    # colors for for group off or on
    red = [(1, (222, 116, 101, 255))]

    # list with clock off or on light
    list = []

    # cycle for deffind while will turn off ro on light
    image_groups = group
    w_section = int()
    left_section = int()
    top_section = 0
    bottom_section = section_size_h - 1
    ect_pix_size = 0

    for left_sections in range(0, 400):
        img_detect = image_groups.crop((0 + left_sections, bottom_section-2, 1 + left_sections, bottom_section-1))
        img_col = Image.Image.getcolors(img_detect)
        # print(top_sections, img_col)
        if img_col == white_pix:
            continue
        if img_col == black_pix:
            # col_counter = img_col
            black_counter = None
            black_pix_size = 0
            for j in range(0, 200):
                black_col_detect = image_groups.crop((left_sections + j, bottom_section-2, left_sections + j + 1, bottom_section-1))
                black_col = Image.Image.getcolors(black_col_detect)
                if black_col == black_pix:
                    if black_counter == red_pix or black_counter == green_pix:
                        ect_pix_size += j
                        break
                    else:
                        black_pix_size += 1
                black_counter = black_col
            left_section = black_pix_size + ect_pix_size + left_sections
            break
        if img_col == red_pix or green_pix:
            left_section = left_sections + 1
            break

    for w_sections in range(0, 400):
        img_detect = image_groups.crop((left_section + w_sections, 0, left_section + 1 + w_sections, 1))
        img_col = Image.Image.getcolors(img_detect)
        if img_col == white_pix:
            w_section = w_sections + 1
            break
    for i in range(0, 24):
        image_group = image_groups.crop((left_section+(i*w_section), top_section, left_section+(i*w_section)+w_section, bottom_section))
        im_pix = image_group.crop((5, 0, 6, 1))
        im_col = Image.Image.getcolors(im_pix)
        # image_group.show()
        if im_col == red:
            list.append(i)
        else:
            list.append('|')
    image_groups.close()

    # parse clock list
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

    # parse list with result in normal view
    list_out = []
    for count, k in enumerate(list_res):
        list_count = len(list_res)
        if count + 1 == list_count:
            list_out.append(f'{k[0]}-{k[-1] + 1}')
            continue
        list_out.append(f'{k[0]}-{k[-1] + 1}')

    # parse list out for send in telegram


    url_for_date = requests.get('http://oblenergo.cv.ua/shutdowns')

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

