import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import pickle
import numpy as np
from neuro_web import img_to_vec
import os
#This programm convert text on photo by simple text


#function for the search the connected component in photo. Algorinm:
# 1) is this pixel is black. No - end work
# 2) if yes, make this pixel white
# 3) give coordinates to massive
# 4) use function to neighbor pixel
# Функция для поиска компонент связности. при подаче координат пикселя:
# 1) провряет чёрный ли это пиксель. Нет - прекращает работу
# 2) красит соответствующий пиксель в белый
# 3) заносит свои координаты в массив
# 4) передаёт функцию на соседние пиксели
def neighbors(y, x, mass):
    pix_now = im2.getpixel((y, x))
    if pix_now == 1:
        im2.putpixel((y, x), 255)
        im2.save("tst.gif")
        mass.append([x, y])
        a1 = y > 0
        a2 = y < img.size[0] - 1
        b1 = x > 0
        b2 = x < img.size[1] - 1
        if a1:
            neighbors(y - 1, x, mass)
        if b1:
            neighbors(y, x - 1, mass)
        if a2:
            neighbors(y + 1, x, mass)
        if b2:
            neighbors(y, x + 1, mass)
        if a1 and b1:
            neighbors(y - 1, x - 1, mass)
        if a1 and b2:
            neighbors(y - 1, x + 1, mass)
        if a2 and b1:
            neighbors(y + 1, x - 1, mass)
        if a2 and b2:
            neighbors(y + 1, x + 1, mass)


def like_a(x, y):
    return abs(x - y) <= 6


drawed = Image.open("to_text.gif")
print(drawed.histogram())
draw = ImageDraw.Draw(drawed)
group = []

# make image binar (b/w)

img = Image.open("to_text.gif")
img = img.convert("P")
im2 = Image.new("P", img.size, 255)
img = img.convert("P")
for x in range(img.size[1]):
    for y in range(img.size[0]):
        pix = img.getpixel((y, x))
        if pix <50:
            im2.putpixel((y, x), 1)
        else:
            im2.putpixel((y, x), 255)
im2.save("tst.gif")
im2.save("control.gif")
im3 = im2.copy()
# use function to all black pixels
for x in range(im2.size[1]):
    for y in range(im2.size[0]):
        pix = im2.getpixel((y, x))
        if pix == 1:
            mas = []
            try:
                neighbors(y, x, mas)
                group.extend([mas])
            except:
                pass
# array with right, left, top and down coordinates op symbol
# ALARM! max_y - down coord, min_y - top, max_x - right, min_x - left
frames = []
for i in range(len(group)):
    max_x = 0
    min_x = 999999
    max_y = 0
    min_y = 999999
    for ii in range(len(group[i])):
        if group[i][ii][0] < min_y:
            min_y = group[i][ii][0]
        if group[i][ii][1] < min_x:
            min_x = group[i][ii][1]
        if group[i][ii][0] > max_y:
            max_y = group[i][ii][0]
        if group[i][ii][1] > max_x:
            max_x = group[i][ii][1]
    if len(frames) == 0:
        frames.append([(min_x - 1, min_y - 1), (max_x + 2, max_y + 2)])
    else:
        check = True
        for i in range(len(frames)):
            if min_x > frames[i][0][0]:
                check = False
                frames.insert(i, [(min_x - 1, min_y - 1), (max_x + 2, max_y + 2)])
                break
        if check:
            frames.append([(min_x - 1, min_y - 1), (max_x + 2, max_y + 2)])
strings = [[frames[0]]]
used = len(frames)
# parse image to string
for i in range(used):
    check = True
    for ii in range(len(strings)):
        if like_a(frames[i][0][1], strings[ii][0][0][1]) or like_a(frames[i][1][1], strings[ii][0][1][1]):
            strings[ii].append(frames[i])
            check = False
            break
    if check:
        strings.append([frames[i]])

print(len(strings))
print(strings)
to_del = []
# this part make symbols like a "i","j", "й", "ё" as one
for i in range(len(strings)):
    for ii in range(len(strings[i]) - 2, 0, -1):
        try:
            if abs(strings[i][ii][1][1] - strings[i][ii + 1][0][1]) <= 4:
                strings[i][ii + 1][0] = (strings[i][ii + 1][0][0], strings[i][ii][0][1])
                strings[i][ii + 1][1] = (strings[i][ii + 1][1][0], strings[i][ii + 1][1][1])
                to_del.append([i, ii])
                print("Y,s", i, ii + 1)
        except:
            pass

for i in range(len(to_del)):
    strings[to_del[i][0]].pop(to_del[i][1])
# cut the symbols
result = []
names = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхчшщъыьэюя123456789"
names = names[::-1]
for ii in range(len(strings)):
    result.append("")
    for i in range(len(strings[ii])):
        a = (strings[ii][i][0][0], strings[ii][i][0][1], strings[ii][i][1][0], strings[ii][i][1][1])
        try:
            kay = im3.crop(a)
            kay.save("char's/" + str(i) + "." + str(ii + 1) + ".gif")
        except:
            pass
    # all symbols to 15*15 image
    for i in range(len(strings[ii])):
        im = Image.open("char's/" + str(i) + "." + str(ii + 1) + ".gif")
        im = im.resize((15, 15))
        im.save("char's/" + str(i) + "." + str(ii + 1) + ".gif")
    with open('machine.pickle', 'rb') as machine:
        data_new = pickle.load(machine)
    for i in range(len(strings[ii])):
        char = Image.open("char's/" + str(i) + "." + str(ii + 1) + ".gif")
        vec = np.array(img_to_vec(char))
        result[ii] = str(data_new.predict(vec)[0]) + result[ii]

    # symbol delete
    for i in range(len(strings[ii])):
        os.remove("char's/" + str(i)+"."+str(ii+1) + ".gif")
        try:
            os.remove("char's/" + str(i)+".gif")
        except:
            pass
to_buffer = open('buff.txt','w')
for i in range(len(result)):
    to_buffer.write(result[i])
    to_buffer.write("""\n""")
