import logging

import requests

from PIL import Image, ImageChops
from aiogram import Dispatcher

from data.config import admins

from app import number_of_group

async def on_startup_notify(dp: Dispatcher):
    # number group
    number_group = number_of_group

    # open oblenergo
    img = requests.get('http://oblenergo.cv.ua/shutdowns/GPV.png')

    # give date from image
    # headers_date = img.headers['Date'].split()[-2][:-3]

    # download image
    img_file = open('./gvp.png', 'wb')
    img_file.write(img.content)
    img_file.close()

    image = Image.open('./gvp.png')
    w, h = image.size

    # colors of pixel
    green_pix = [(1, (119, 136, 66, 255))]
    silver_pix = [(1, (217, 217, 217, 255))]
    white_pix = [(1, (255, 255, 255, 255))]
    light_green_pix = [(1, (222, 224, 201, 255))]

    # coordinate to cut image
    left = int()
    top = int()
    top_undo_green = int()
    rigth = int()
    bottom = int()
    section_size_h = int()

    # deffind coordinate on image
    # top
    count_top = 0
    count_green = 0
    for num_top, i in enumerate(range(0, 300)):
        im_top = image.crop((10, 0 + i, 10 + 1, 1 + i))
        im_top_col = Image.Image.getcolors(im_top)
        if im_top_col == green_pix:
            if count_green == 0:
                top_undo_green = num_top
                count_green += 1
                continue
        if im_top_col == silver_pix:
            if count_top == 0:
                count_top += 1
                # print(True)
                continue
            else:
                top = num_top + 1
                # print(top)
                continue
        if im_top_col == light_green_pix:
            section_size_h = num_top - top + 1
            # print(section_size_h)
            break
    # left
    for i in range(0, 300):
        im_left = image.crop((0 + i, top_undo_green, 1 + i, top_undo_green + 1))

        imm_left_col = Image.Image.getcolors(im_left)
        if imm_left_col == green_pix:
            # print(True)
            left = i
            # print(left, 'left')
            break
    # bottom
    for num_bottom, i in enumerate(range(0, 300)):
        im_bottom = image.crop((left, h - 1 - i, left + 1, h - i))

        imm_bottom_col = Image.Image.getcolors(im_bottom)
        if imm_bottom_col == silver_pix:
            # print(True)
            bottom = num_bottom
            break
    # rigth
    for num_rigth, i in enumerate(range(0, 300)):
        im_rigth = image.crop(((w - 1) - i, h - bottom, w - i, (h - bottom) + 1))

        im_rigth_col = Image.Image.getcolors(im_rigth)
        if im_rigth_col == white_pix:
            # print(True)
            rigth = num_rigth
            break

    # cut image of deffind coordinate
    crop_res = image.crop((left, top, w - rigth, h - bottom))
    # crop_res.show()
    image.close()
    w_size, h_size = crop_res.size

    # formula for cut group section

    group_size = number_group * section_size_h

    # cut group section
    group = crop_res.crop((0, group_size - section_size_h, w_size, group_size))

    # check if equal image
    group_diff = Image.open('./group.png').convert('RGB')
    diff = ImageChops.difference(group.convert('RGB'), group_diff).getbbox()
    # diff = True
    group_diff.close()
    if diff:
        group.save('./group.png')

        # colors for for group off or on
        red = [(1, (222, 116, 101, 255))]

        # list with clock off or on light
        list = []

        # cycle for deffind while will turn off ro on light
        image_groups = Image.open('./group.png')
        w_section = int()
        left_section = int()
        top_section = 0
        right_section = left_section + w_section
        bottom_section = section_size_h - 1

        for left_sections in range(0, 400):
            img_detect = image_groups.crop((0 + left_sections, 0, 1 + left_sections, 1))
            # img_detect.show()
            img_col = Image.Image.getcolors(img_detect)
            # print(top_sections, img_col)
            if img_col == white_pix:
                continue
            else:
                left_section = left_sections + 1
                # print(left_section, 'dafsd')
                break

        for w_sections in range(0, 400):
            img_detect = image_groups.crop((left_section + w_sections, 0, left_section + 1 + w_sections, 1))
            # img_detect.show()
            img_col = Image.Image.getcolors(img_detect)
            # print(top_sections, img_col)
            if img_col == white_pix:
                w_section = w_sections + 1
                # print(w_section, 'w')
                break

        for i in range(0, 24):

            # start_img_group = (202) + (i * 34)
            # end_img_group = 27
            # print(left_section, top_section, right_section, bottom_section, w_section)
            image_group = image_groups.crop((left_section+(i*w_section), top_section, left_section+(i*w_section)+w_section, bottom_section))
            # image_group.show()
            im_pix = image_group.crop((0, 0, 1, 1))
            im_col = Image.Image.getcolors(im_pix)
            # print(im_col)
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
            list_out.append(f'{k[0]}-{k[-1] + 1}\n')

        # parse list out for send in telegram
        def get_data():
            data = ''
            if number_group == 1:
                data += 'Зарожани\n'
            if number_group == 2:
                data += 'Млинки\n'
            if number_group == 14:
                data += 'Че\n'
            for p in list_out:
                data += p
            return data

        # send list in  telegram message (only admins)
        # print(get_data())
        for admin in admins:
            try:
                await dp.bot.send_message(admin, get_data())

            except Exception as err:
                logging.exception(err)
