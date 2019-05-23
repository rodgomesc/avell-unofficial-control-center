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
import usb.core
import usb.util
from colors import get_mono_color_vector, get_h_alt_color_vector, get_v_alt_color_vector

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

# 21 09 00 03 01 00 08 00 # setup packet


def disable_keyboard():
    dev.ctrl_transfer(
        bmRequestType=0x21, bRequest=9, wValue=0x300, wIndex=1,
        data_or_wLength=(0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
    )


def keyboard_style(style):
    dev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x300,
                      wIndex=1, data_or_wLength=light_style[style])


def adjust_brightness(value='4'):

    dev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x300, wIndex=1, data_or_wLength=(
        0x08, 0x02, 0x33, 0x00, brightness_map[value], 0x00, 0x00, 0x00))


def color_scheme_setup():

    # setup a mono_color scheme
    dev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x300, wIndex=1,
                      data_or_wLength=(0x12, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00))


def mono_color_setup(color_scheme):
    color_scheme_setup()

    # i don't know whats happens behind the hoods, but control center send
    # this sequence of bytes 8 times, other wise don't will work
    color_vector = get_mono_color_vector(color_scheme)

    for _ in range(8):
        dev.write(0x2, color_vector)


def h_alt_color_setup(color_scheme_a, color_scheme_b):
    color_scheme_setup()
    color_vector = get_h_alt_color_vector(color_scheme_a, color_scheme_b)
    for _ in range(8):
        dev.write(0x2, color_vector)


def v_alt_color_setup(color_scheme_a, color_scheme_b):
    color_scheme_setup()
    color_vector = get_v_alt_color_vector(color_scheme_a, color_scheme_b)
    for _ in range(8):
        dev.write(0x2, color_vector)


if __name__ == "__main__":

    if not os.geteuid() == 0:
        sys.exit('This script must be run as root!')

    dev = usb.core.find(idVendor=0x048d, idProduct=0xce00)

    if dev is None:
        raise ValueError('Device not found')

    # in linux interface is 1, in windows 0
    if not sys.platform.startswith('win'):
        if dev.is_kernel_driver_active(1):
            dev.detach_kernel_driver(1)

    cfg = dev.get_active_configuration()
    intf = cfg[(1, 0)]

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match=lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

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
                        help='turn keyboard backlight off')

    parsed = parser.parse_args()
    if parsed.disable:
        disable_keyboard()
    if parsed.brightness:
        adjust_brightness(int(parsed.brightness))
    if parsed.color:
        mono_color_setup(parsed.color)
    elif parsed.h_alt:
        h_alt_color_setup(*parsed.h_alt)
    elif parsed.v_alt:
        v_alt_color_setup(*parsed.v_alt)
    elif parsed.style:
        keyboard_style(parsed.style)
    else:
        print("Invalid or absent command")
