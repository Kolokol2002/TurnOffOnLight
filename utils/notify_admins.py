import logging

import requests

from PIL import Image, ImageChops
from aiogram import Dispatcher

from data.config import admins


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            #open oblenergo
            img = requests.get('http://oblenergo.cv.ua/shutdowns/GPV.png')

            #give date from image
            # headers_date = img.headers['Date'].split()[-2][:-3]

            #download image
            img_file = open('./gvp.png', 'wb')
            img_file.write(img.content)
            img_file.close()

            image = Image.open('./gvp.png')
            w, h = image.size

            #colors of pixel
            green_pix = [(1, (119, 136, 66, 255))]
            silver_pix = [(1, (217, 217, 217, 255))]
            white_pix = [(1, (255, 255, 255, 255))]

            #coordinate to cut image
            left = int()
            top = int()
            rigth = int()
            bottom = int()

            #deffind coordinate on image
            # top
            for num_top, i in enumerate(range(0, 300)):
                im_top = image.crop((10, 0 + i, 10+1, 1+i))
                im_top_col = Image.Image.getcolors(im_top)
                if im_top_col == green_pix:
                    # print(True)
                    top = num_top
                    bottom = top + 1
                    break
            # left
            for num_left, i in enumerate(range(0, 300)):
                im_left = image.crop((0 + i, top + 1, 1 + i, bottom + 1))

                imm_left_col = Image.Image.getcolors(im_left)
                if imm_left_col == green_pix:
                    # print(True)
                    left = num_left
                    bottom = int()
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
                    top += 62
                    break

            #cut image of deffind coordinate
            crop_res = image.crop((left, top, w - rigth, h - bottom))
            image.close()
            w_size, h_size = crop_res.size

            #formula for cut group section
            number_group = 14
            section_size = 28
            group_size = number_group * 28

            #cut group section
            group = crop_res.crop((0, group_size - section_size, w_size, group_size))

            #check if equal image
            group_diff = Image.open('./group.png').convert('RGB')
            diff = ImageChops.difference(group.convert('RGB'), group_diff)
            group_diff.close()
            if diff.getbbox():
                group.save('./group.png')

                #colors for for group off or on
                red = [(27, (255, 255, 255, 255)), (5, (222, 99, 57, 255)), (1, (50, 66, 87, 255)),
                       (1, (125, 99, 101, 255)), (1, (89, 83, 101, 255)), (787, (222, 116, 101, 255)),
                       (1, (191, 66, 23, 255)), (2, (158, 116, 101, 255)), (2, (89, 66, 87, 255)), (1, (222, 83, 40, 255)),
                       (3, (50, 0, 0, 255)), (1, (0, 0, 23, 255)), (2, (0, 0, 40, 255)), (3, (0, 0, 0, 255))]
                #list with clock off or on light
                list = []

                #cycle for deffind while will turn off ro on light
                image_groups = Image.open('./group.png')
                for i in range(0, 24):
                    start_img_group = (190) + (i * 31)
                    end_img_group = 27
                    image_group = image_groups.crop((start_img_group, 0, start_img_group + 31, end_img_group))
                    im1 = Image.Image.getcolors(image_group)
                    if im1 == red:
                        list.append(i)
                    else:
                        list.append('|')
                image_groups.close()

                #parse clock list
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

                #parse list with result in normal view
                list_out = []
                for count, k in enumerate(list_res):
                    list_count = len(list_res)
                    if count + 1 == list_count:
                        list_out.append(f'{k[0]}-{k[-1] + 1}')
                        continue
                    list_out.append(f'{k[0]}-{k[-1] + 1}\n')

                #parse list out for send in telegram
                data = ''
                for p in list_out:
                    data += p
                #send list in  telegram message (only admins)
                await dp.bot.send_message(admin, data)

        except Exception as err:
            logging.exception(err)
