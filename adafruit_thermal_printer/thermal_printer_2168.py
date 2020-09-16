# The MIT License (MIT)
#
# Copyright (c) 2020 Tony DiCola, Grzegorz Nowicki
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_thermal_printer.thermal_printer_2168.ThermalPrinter`
==============================================================

Thermal printer control module built to work with small serial thermal
receipt printers.  Note that these printers have many different firmware
versions and care must be taken to select the appropriate module inside this
package for your firmware printer:

* thermal_printer_2164 = Printers with firmware version 2.168+.
* thermal_printer = The latest printers with firmware version 2.68 up to 2.168
* thermal_printer_264 = Printers with firmware version 2.64 up to 2.68.
* thermal_printer_legacy = Printers with firmware version before 2.64.

* Author(s): Tony DiCola, Grzegorz Nowicki
"""


import adafruit_thermal_printer.thermal_printer as thermal_printer
import imageio
import numpy as np
from PIL import Image


# pylint: disable=too-many-arguments
class ThermalPrinter(thermal_printer.ThermalPrinter):
    """Thermal printer for printers with firmware version from 2.168"""

    # Barcode types.  These vary based on the firmware version so are made
    # as class-level variables that users can reference (i.e.
    # ThermalPrinter.UPC_A, etc) and write code that is independent of the
    # printer firmware version.
    UPC_A = 65
    UPC_E = 66
    EAN13 = 67
    EAN8 = 68
    CODE39 = 69
    ITF = 70
    CODABAR = 71
    CODE93 = 72
    CODE128 = 73

    def __init__(
        self,
        uart,
        byte_delay_s=0.00057346,
        dot_feed_s=0.0021,
        dot_print_s=0.03,
        auto_warm_up=True,
    ):
        """Thermal printer class.  Requires a serial UART connection with at
        least the TX pin connected.  Take care connecting RX as the printer
        will output a 5V signal which can damage boards!  If RX is unconnected
        the only loss in functionality is the has_paper function, all other
        printer functions will continue to work.  The byte_delay_s, dot_feed_s,
        and dot_print_s values are delays which are used to prevent overloading
        the printer with data.  Use the default delays unless you fully
        understand the workings of the printer and how delays, baud rate,
        number of dots, heat time, etc. relate to each other.
        """
        super().__init__(
            uart,
            byte_delay_s=byte_delay_s,
            dot_feed_s=dot_feed_s,
            dot_print_s=dot_print_s,
            auto_warm_up=auto_warm_up,
        )

    def warm_up(self, heat_time=120):
        """Apparently there are no parameters for setting darkness in 2.168
        (at least commands from 2.68 dont work), So it is little
        compatibility method to reuse older code.
        """
        self._set_timeout(0.5)  # Half second delay for printer to initialize.
        self.reset()


    def print_bitmap(self, file):
        img = imageio.imread(file)
        if img.shape[2] == 4:
            r, g, b, a = np.split(img, 4, axis=2)
        else:
            r, g, b = np.split(img, 3, axis=2)

        r = r.reshape(-1)
        g = r.reshape(-1)
        b = r.reshape(-1)

        bitmap = list(map(lambda x: 0.333*x[0]+0.333*x[1]+0.333*x[2], zip(r, g, b)))
        bitmap = np.array(bitmap).reshape([img.shape[0], img.shape[1]])
        bitmap = np.multiply((bitmap > 208).astype(float), 255)

        im = Image.fromarray(bitmap.astype(np.uint8))
        f = np.array(im)

        #TODO add size assertions and add printing long pictures as many pictures
        
        

    def fill_vertical(self, m, nH, nL, d):
        self._uart.write(b"\x1B*%s%s%s" % (nH, nL, d))
        self.print("\x1D\x2F\x00\x0A")
        pass

    def print_horizontal(self, m, xL, xH, yL, yH):
        data = bytearray()
        for _ in range(int.from_bytes(xL, byteorder='big')):
            for _ in range(int.from_bytes(yL, byteorder='big')):
                data.append(int("0xFF",16))
        self._uart.write(b"\x1D\x76\x30%s%s%s%s%s%s" % (m, xL, xH, yL, yH, data))
        for d in data:
            self._uart.write(d)
        pass

    def print_horizontal2(self, m, xL, xH, yL, yH, data):
        
        self._uart.write(b"\x1D\x76\x30%s%s%s%s%s%s" % (m, xL, xH, yL, yH, data))
        for d in data:
            self._uart.write(d)
        pass

    def _write_to_byte(self, pos, byte):
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

    def convert_data_horizontally(self, x_size, y_size, file_array):
        datas = bytearray()
        for y in range(y_size):
            for x in range(0, x_size, 8):
                data = 0
                for bit in range(8):
                    try:
                        if file_array[y][x+bit]==0:
                            data = self._write_to_byte(bit,data)

                    except IndexError:
                        pass
                    finally:
                        pass
                datas.append(data)
        return datas