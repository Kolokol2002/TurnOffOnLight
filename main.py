import requests
import pyperclip

from PIL import Image
img = requests.get('http://oblenergo.cv.ua/shutdowns/GPV.png')

img_file = open('C:\\Users\\maksk\\Desktop\\project-on-python\\TurnOffOnLight\\gvp.png', 'wb')
img_file.write(img.content)
img_file.close()

image = Image.open('C:\\Users\\maksk\\Desktop\\project-on-python\\TurnOffOnLight\\gvp.png')
w, h = image.size

green_pix = [(1, (119, 136, 66, 255))]
silver_pix = [(1, (217, 217, 217, 255))]
white_pix = [(1, (255, 255, 255, 255))]

left = int()
top = int()
rigth = int()
bottom = int()

# top
for num_top, i in enumerate(range(0, 300)):
    im_top = image.crop((0+i, 0+i, 1+i, 1+i))
    im_top_col = Image.Image.getcolors(im_top)
    if im_top_col == green_pix:
        # print(True)
        top = num_top
        bottom = top + 1
        break

# left
for num_left, i in enumerate(range(0, 300)):
    im_left = image.crop((0+i, top+1, 1+i, bottom+1))

    imm_left_col = Image.Image.getcolors(im_left)
    if imm_left_col == green_pix:
        # print(True)
        left = num_left
        bottom = int()
        break

# bottom
for num_bottom, i in enumerate(range(0, 300)):
    im_bottom = image.crop((left, h-1-i, left+1, h-i))

    imm_bottom_col = Image.Image.getcolors(im_bottom)
    if imm_bottom_col == silver_pix:
        # print(True)
        bottom = num_bottom
        break

# rigth
for num_rigth, i in enumerate(range(0, 300)):
    im_rigth = image.crop(((w-1)-i, h-bottom, w-i, (h-bottom)+1))

    im_rigth_col = Image.Image.getcolors(im_rigth)
    if im_rigth_col == white_pix:
        # print(True)
        rigth = num_rigth
        top +=62
        break
crop_res = image.crop((left, top, w-rigth, h-bottom))
w_size, h_size = crop_res.size
# print(w_size, h_size)
# crop_res.show()

section_size = 28
group_size = 14 * section_size
group = crop_res.crop((0, group_size-section_size, w_size, group_size))
group.save('C:\\Users\\maksk\\Desktop\\project-on-python\\TurnOffOnLight\\group.png')

green = [(3, 0), (1, 4), (1, 7), (1, 23), (1, 75), (1, 91), (1, 97), (1, 123), (1, 128), (1, 153), (1, 156), (1, 174), (1, 182), (1, 193), (824, 199), (28, 255)]
red = [(27, (255, 255, 255, 255)), (5, (222, 99, 57, 255)), (1, (50, 66, 87, 255)), (1, (125, 99, 101, 255)), (1, (89, 83, 101, 255)), (787, (222, 116, 101, 255)), (1, (191, 66, 23, 255)), (2, (158, 116, 101, 255)), (2, (89, 66, 87, 255)), (1, (222, 83, 40, 255)), (3, (50, 0, 0, 255)), (1, (0, 0, 23, 255)), (2, (0, 0, 40, 255)), (3, (0, 0, 0, 255))]

list = []
image_groups = Image.open('C:\\Users\\maksk\\Desktop\\project-on-python\\TurnOffOnLight\\group.png')

end_img_group = 27
for i in range(0, 24):
    start_img_group = (190) + (i * 31)
    image_group = image_groups.crop((start_img_group, 0, start_img_group+31, end_img_group))
    im1 = Image.Image.getcolors(image_group)
    if im1 == red:
        list.append(i)
    else:
        list.append('|')
    # image_group.show()


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

list_out = []
for count, k in enumerate(list_res):
    list_count = len(list_res)
    if count+1 == list_count:
        list_out.append(f'{k[0]}-{k[-1]+1}')
        continue
    list_out.append(f'{k[0]}-{k[-1] + 1}\n')

data = ''
for p in list_out:
    data += p

# print(data)
pyperclip.copy(data)
spam = pyperclip.paste()