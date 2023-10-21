from PIL import Image, ImageOps

im = Image.open('./images/P9AWD.png')

# Invert image 
# im = ImageOps.invert(im)

# Crop image
#im1 = im.crop()
#newsize = (30, 30)
#im1 = im1.resize(newsize)

# Color convert image 
im1 = im.convert('1')
h, w = im1.size
print(h, w)
# im1.show()
data = list (im1.getdata())
#set color resolution to 1 bit from 8
bin_data = [ 1 if x == 0 else 0 for x in data]
print(len(data))


k = 0
data_2d = []
for x in range(w):
    line = []
    for y in range(h):
        line.append(bin_data[k])
        k = k + 1
        
    data_2d.append(line)

#print data 
for e in data_2d:
    print(e,',' )

#iterate 6x time to get 5 bit line data for each display 
# led_display_data = []
# for x in range(0, 30, 5):
#     # start from first line to the end 
#     print('\n')
#     char = []
#     for line in pikachu:               
#         char_line = line[:-x] if x > 0 else line
#         char_line = char_line[25-x:]
#         print(char_line)
#         char.append(char_line)
#     led_display_data.append(char)

# print(len(led_display_data))
im1.save('bluetooth.bmp')