"""aaa
"""
import sys
import serial
import struct
from PIL import Image, ImageOps


sys.path.append("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer")

import adafruit_thermal_printer

SIZE_X = (384, 384)

im = Image.open("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer\\adafruit_thermal_printer\\elmi.bmp")
#im.show()

im = im.convert(mode="1")
print(im)
im.save("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer\\adafruit_thermal_printer\\elmi_converted.bmp")
#uart = serial.Serial("COM5", baudrate=19200, timeout=3000)

#ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.168)
#printer = ThermalPrinter(uart, auto_warm_up=False)
#printer.warm_up()


#if printer.has_paper():
#    print("Printer has paper!")
#else:
#    print("Printer might be out of paper, or RX is disconnected!")

# print(printer.up_down_mode)
# printer.print("Default Mode Hello !")

#printer.up_down_mode = True
# print(printer.up_down_mode)
#printer.print("Upside down hello upDownMode!")

#printer.reset()


# printer.up_down_mode = False
# print(printer.up_down_mode)
#printer.print("Normal hello upDownMode!")


#printer.print_bitmap(b"\x30", b"\x04", b"\xFF")
#printer.fill_vertical(b"\x00", b"\x01", b"\x01",b"\xFF")
#printer.feed(2)
