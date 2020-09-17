
import sys
sys.path.append("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer")

import adafruit_thermal_printer
import serial

uart = serial.Serial("COM3", baudrate=19200, timeout=3000)


ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.168)
printer = ThermalPrinter(uart, auto_warm_up=False)
printer.warm_up()


if printer.has_paper():
    print("Printer has paper!")

printer.reset()

printer.print_bitmap("D:\\PyCharm-worksapce\\Adafruit_CircuitPython_Thermal_Printer\\adafruit_thermal_printer\\elmi2.bmp")