

import sys
import math
import imageio
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import serial


sys.path.append("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer")

import adafruit_thermal_printer




def write_to_byte(pos, byte):
    if pos == 0:
        return byte | 0b10000000
    if pos == 1:
        return byte | 0b01000000
    if pos == 2:
        return byte | 0b00100000
    if pos == 3:
        return byte | 0b00010000
    if pos == 4:
        return byte | 0b00001000
    if pos == 5:
        return byte | 0b00000100
    if pos == 6:
        return byte | 0b00000010
    if pos == 7:
        return byte | 0b00000001

uart = serial.Serial("COM3", baudrate=19200, timeout=3000)



ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.168)
printer = ThermalPrinter(uart, auto_warm_up=False)
printer.warm_up()

if printer.has_paper():
    print("Printer has paper!")

printer.reset()

f= imageio.imread("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer\\adafruit_thermal_printer\\elmi2.bmp")
#im = Image.open("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer\\adafruit_thermal_printer\\elmi.bmp")
#im = im.convert(mode="1")
#f = np.array(im)

if f.shape[2] == 4:
    r, g, b, a = np.split(f, 4, axis=2)
else:
    r, g, b = np.split(f, 3, axis=2)

r = r.reshape(-1)
g = r.reshape(-1)
b = r.reshape(-1)


bitmap = list(map(lambda x: 0.333*x[0]+0.333*x[1]+0.333*x[2], zip(r, g, b)))
bitmap = np.array(bitmap).reshape([f.shape[0], f.shape[1]])
bitmap = np.multiply((bitmap > 208).astype(float), 255)
im = Image.fromarray(bitmap.astype(np.uint8))
f = np.array(im)



subs = list()

if f.shape[1] <= 384:
    if f.shape[0] <= 8:
        #process_data()
        pass
    else:
        i = 0
        while i < f.shape[0]:
            subs.append(f[(i):(i+8), 0:384])
            i += 8



# for img in subs:
#     for x in range(img.shape[1]):
#         data = 0
#         for y in range(img.shape[0]):
#             if img[y][x] == 0:          # Here 0 is our bit on, 255 is bit off
#                 data = write_to_byte(y, data) # Here 1 is bit on , 0 bit off

#         datas.append(data)
#     for x in range(8 - (img.shape[1] % 8)):
#         data = 0
#         datas.append(data)

#f = f[(0):(0+8), 0:384]
print(f.shape, f.dtype)


def convert_data_btm():
    datas = bytearray()
    for x in range(f.shape[1]):
        for y in range(0, f.shape[0], 8):
            data = 0
            for b in range(8):
                
                try:
                    if f[y+b][x] == 0:          # Here 0 is our bit on, 255 is bit off
                        data = write_to_byte(b, data) # Here 1 is bit on , 0 bit off
                        
                except IndexError:
                    pass
                finally:
                    pass
            datas.append(data)  # appending data byte after all bit manipulations
        #printer.print_bitmap(bytes([math.ceil(f.shape[1]/8)]), b"\x01", datas)
        #datas.clear()
    return datas

data = bytearray()
for _ in range(int.from_bytes(b"\x30", byteorder='big')):
    for _ in range(int.from_bytes(b"\x0F", byteorder='big')):
        data.append(int("0x4a",16))
#data = b"\x00"


def convert_data_horizontally():
    datas = bytearray()
    for y in range(f.shape[0]):
        for x in range(0, f.shape[1], 8):
            data = 0
            for bit in range(8):
                try:
                    if f[y][x+bit]==0:
                        data = write_to_byte(bit,data)

                except IndexError:
                    pass
                finally:
                    pass
            datas.append(data)
    return datas
data_hor = convert_data_horizontally()


img_X = math.ceil(f.shape[1]/8)
img_Y = f.shape[0]
img_LX = (img_X & 0xFF).to_bytes(1, byteorder="big")
img_HX = ((img_X & 0xFF00) >> 8).to_bytes(1, byteorder="big")
img_LY = (img_Y & 0xFF).to_bytes(1, byteorder="big")
img_HY = ((img_Y & 0xFF00) >> 8).to_bytes(1, byteorder="big")

mode = b"\x00"

printer.print_horizontal2(mode, img_LX, img_HX, img_LY, img_HY, data_hor)
#printer.print_bitmap(bytes([math.ceil(f.shape[1]/8)]), bytes([math.ceil(f.shape[0]/8)]), datas)
# printer.feed(2)
# printer.feed(2)
# img = subs[0]
# for x in range(img.shape[1]):
#     data = 0
#     for y in range(img.shape[0]):
#         if img[y][x] == 0:          # Here 0 is our bit on, 255 is bit off
#             data = write_to_byte(y, data) # Here 1 is bit on , 0 bit off

#     datas.append(data)



#printer.print_bitmap(bytes([math.ceil(f.shape[1]/8)]), bytes([math.ceil(f.shape[0]/8)]), datas)



