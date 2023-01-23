from PIL import Image, ImageChops

from app import number_of_group

number_group = number_of_group

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
            print(top)
            continue
    if im_top_col == light_green_pix:
        section_size_h = num_top - top + 1
        print(section_size_h)
        break
# left
for i in range(0, 300):
    im_left = image.crop((0 + i, top_undo_green, 1 + i, top_undo_green + 1))

    imm_left_col = Image.Image.getcolors(im_left)
    if imm_left_col == green_pix:
        # print(True)
        left = i
        print(left, 'left')
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
# group.save('./group.png')


image_groups = Image.open('./group.png')
w_section = int()
left_section = int()
top_section = 0
right_section = w_section + w_section
for left_sections in range(0, 400):
    img_detect = image_groups.crop((0 + left_sections, 0, 1 + left_sections, 1))
    # img_detect.show()
    img_col = Image.Image.getcolors(img_detect)
    # print(top_sections, img_col)
    if img_col == white_pix:
        continue
    else:
        left_section = left_sections + 1
        print(left_section, 'dafsd')
        break

for w_sections in range(0, 400):
    img_detect = image_groups.crop((left_section + w_sections, 0, left_section + 1 + w_sections, 1))
    # img_detect.show()
    img_col = Image.Image.getcolors(img_detect)
    # print(top_sections, img_col)
    if img_col == white_pix:
        w_section = w_sections + 1
        print(w_section, 'w')
        break


