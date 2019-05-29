"""
Copyright (c) 2019, Rodrigo Gomes.
Distributed under the terms of the MIT License.
The full license is in the file LICENSE, distributed with this software.
Created on May 22, 2019
@author: @rodgomesc
"""
import argparse
import sys
import os
from core.handler import DeviceHandler
import time
from core.colors import (get_mono_color_vector,
                         get_h_alt_color_vector,
                         get_v_alt_color_vector,
                         _colors_available)


light_style = {
    'rainbow': (0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    'reactive': (0x08, 0x02, 0x04, 0x05, 0x24, 0x08, 0x01, 0x00),
    'raindrop': (0x08, 0x02, 0x0A, 0x05, 0x24, 0x08, 0x00, 0x00),
    'marquee': (0x08, 0x02, 0x09, 0x05, 0x24, 0x08, 0x00, 0x00),
    'aurora': (0x08, 0x02, 0x0E, 0x05, 0x24, 0x08, 0x00, 0x00)
}

# keybpoard brightness have 4 variations 0x08,0x16,0x24,0x32
brightness_map = {
    1: 0x08,
    2: 0x16,
    3: 0x24,
    4: 0x32
}


class ControlCenter(DeviceHandler):
    def __init__(self, vendor_id, product_id):
        super(ControlCenter, self).__init__(vendor_id, product_id)
        self.brightness = None

    def disable_keyboard(self):
        self.ctrl_write(0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)

    def keyboard_style(self, style):
        self.ctrl_write(*light_style[style])

    def adjust_brightness(self, brightness=None):
        if brightness:
            self.brightness = brightness
            self.ctrl_write(0x08, 0x02, 0x33, 0x00,
                            brightness_map[self.brightness], 0x00, 0x00, 0x00)
        else:
            self.adjust_brightness(4)

    def color_scheme_setup(self):
        self.ctrl_write(0x12, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00)

    def mono_color_setup(self, color_scheme):

        if self.brightness:
            self.color_scheme_setup()
            color_vector = get_mono_color_vector(color_scheme)
            self.bulk_write(times=8, payload=color_vector)
        else:
            self.adjust_brightness()
            self.mono_color_setup(color_scheme)

    def h_alt_color_setup(self, color_scheme_a, color_scheme_b):

        self.color_scheme_setup()
        color_vector = get_h_alt_color_vector(color_scheme_a, color_scheme_b)
        self.bulk_write(times=8, payload=color_vector)

    def v_alt_color_setup(self, color_scheme_a, color_scheme_b):

        self.color_scheme_setup()
        color_vector = get_v_alt_color_vector(color_scheme_a, color_scheme_b)
        self.bulk_write(times=8, payload=color_vector)


def main():
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root!')

    control = ControlCenter(vendor_id=0x048d, product_id=0xce00)

    parser = argparse.ArgumentParser(
        description="Supply at least one of the options [-c|-H|-V|-s|-d]. "
        "Colors available: "
        "[red|green|blue|teal|pink|purple|white|yellow|orange]")
    parser.add_argument('-c', '--color', help='Single color')
    parser.add_argument('-b', '--brightness', help='1, 2, 3 or 4')
    parser.add_argument('-H', '--h-alt', nargs=2,
                        help='Horizontal alternating colors')
    parser.add_argument('-V', '--v-alt', nargs=2,
                        help='Vertical alternating colors')
    parser.add_argument('-s', '--style',
                        help='one of (rainbow, reactive, raindrop, marquee, aurora)')
    parser.add_argument('-d', '--disable', action='store_true',
                        help='turn keyboard backlight off'),

    parsed = parser.parse_args()
    if parsed.disable:
        control.disable_keyboard()
    if parsed.brightness:
        control.adjust_brightness(int(parsed.brightness))
    if parsed.color:
        control.mono_color_setup(parsed.color)
    elif parsed.h_alt:
        control.h_alt_color_setup(*parsed.h_alt)
    elif parsed.v_alt:
        control.v_alt_color_setup(*parsed.v_alt)
    elif parsed.style:
        control.keyboard_style(parsed.style)
    else:
        print("Invalid or absent command")


if __name__ == "__main__":
    main()
