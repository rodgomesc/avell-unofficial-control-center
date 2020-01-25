"""
Copyright (c) 2019, Rodrigo Gomes.
Distributed under the terms of the MIT License.
The full license is in the file LICENSE, distributed with this software.
Created on May 22, 2019
@author: @rodgomesc
"""
import argparse
import textwrap
import sys
import os
from aucc.core.handler import DeviceHandler
import time
from aucc.core.colors import (get_mono_color_vector,
                              get_h_alt_color_vector,
                              get_v_alt_color_vector,
                              _colors_available)


# Keyboard brightness has 4 variations 0x08,0x16,0x24,0x32
brightness_map = {
    1: 0x08,
    2: 0x16,
    3: 0x24,
    4: 0x32
}

programs = {
    "breathing":          0x02,
    "wave":               0x03,
    "random":             0x04,
    "reactive":           0x04,
    "rainbow":            0x05,
    "ripple":             0x06,
    "reactiveripple":     0x07,
    "marquee":            0x09,
    "fireworks":          0x11,
    "raindrop":           0x0A,
    "aurora":             0x0E,
}

colours = {
    "r": 0x01, # red
    "o": 0x02, # orange
    "y": 0x03, # yellow
    "g": 0x04, # green
    "b": 0x05, # blue
    "t": 0x06, # teal
    "p": 0x07, # purple
}

import re
light_style_pattern = "^({})({})?$".format(
                            '|'.join(programs.keys()),
                            '|'.join([ c[0] for c in colours.keys() ])
                        )
def get_light_style_code( style, brightness=3 ) :
    kwargs = {}
    match = re.match( light_style_pattern, style ).groups()
    
    if not match[0] :
        raise Exception( "Error: Style {} not found".format(program) )

    program = match[0]
    program_code =      programs[program]

    kwargs["colour"] =  colours[match[1]]  if match[1] else 0x08 # Default rainbow colour
    kwargs["brightness"] =  brightness_map[brightness]

    if program == "rainbow" :
        kwargs["colour"] = 0x00
        kwargs["program2"] = 0x00
    elif program == "marquee" :
        kwargs["colour"] = 0x08
        kwargs["program2"] = 0x00
    elif program == "wave" :
        kwargs["colour"] = 0x00
        kwargs["program2"] = 0x01
    elif program in ["reactive", "reactiveaurora", "fireworks"] :
        kwargs["program2"] = 0x01

    return get_code( program_code, **kwargs )


def get_code( program, speed=0x05, brightness=0x24, colour=0x08, program2=0x00, save_changes=0x00 ):
    # Byte  Purpose     Notes
    # 0     ???         0x08 to issue commands?
    # 1     ???         0x02 to issue commands? Other values seem to cause failure. 0x01 appears to switch off lights
    # 2     Program     The 'effect' in use
    # 3     Speed       0x0?: 1,2,3,4,5,6,7,8,9,a (fastest to slowest)
    # 4     Brightness  0x08, 0x16, 0x24, 0x32
    # 5     Colour      0x0?: 1 red, 2 orange, 3 yellow, 4 green, 5 blue, 6 teal, 7 purple, 8 rainbow
    # 6     Program?    Required to be changed for some effects
    # 7     save changes (00 for no, 01 for yes)
    return ( 0x08, 0x02, program, speed, brightness, colour, program2, save_changes )


class ControlCenter(DeviceHandler):
    def __init__(self, vendor_id, product_id):
        super(ControlCenter, self).__init__(vendor_id, product_id)
        self.brightness = None

    def disable_keyboard(self):
        self.ctrl_write(0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)

    def keyboard_style(self, style, brightness=3):
        self.ctrl_write(*get_light_style_code(style, brightness))

    def adjust_brightness(self, brightness=None):
        if brightness:
            self.brightness = brightness
            self.ctrl_write(0x08, 0x02, 0x33, 0x00,
                            brightness_map[self.brightness], 0x00, 0x00, 0x00)
        else:
            self.adjust_brightness(4)

    def color_scheme_setup(self, save_changes=0x01):
        '''
        options available: (0x00 for no, 0x01 for yes)
        purpose: write changes on chip to keep current color on reboot
        '''
        self.ctrl_write(0x12, 0x00, 0x00, 0x08, save_changes, 0x00, 0x00, 0x00)

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
    from elevate import elevate

    if not os.geteuid() == 0:
        elevate()

    control = ControlCenter(vendor_id=0x048d, product_id=0xce00)

    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
            Supply at least one of the options [-c|-H|-V|-s|-d].
                
            Colors available:
            [red|green|blue|teal|pink|purple|white|yellow|orange|olive|maroon|brown|gray|skyblue|navy|crimson|darkgreen|lightgreen|gold|violet] '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-c', '--color', help='Select a single color for all keys.')
    parser.add_argument(
        '-b', '--brightness', help='Set brightness, 1 is minimum, 4 is maximum.', type=int, choices=range(1, 5))
    parser.add_argument('-H', '--h-alt', nargs=2,
                        help='Horizontal alternating colors')
    parser.add_argument('-V', '--v-alt', nargs=2,
                        help='Vertical alternating colors')
    parser.add_argument('-s', '--style',
                        help='One of (rainbow, marquee, wave, raindrop, aurora, random, reactive, breathing, ripple, reactiveripple, reactiveaurora, fireworks). Additional single colors are available for the following styles: raindrop, aurora, random, reactive, breathing, ripple, reactiveripple, reactiveaurora and fireworks. These colors are: Red (r), Orange (o), Yellow (y), Green (g), Blue (b), Teal (t), Purple (p). Append those styles with the start letter of the color you would like (e.g. rippler = Ripple Red')
    parser.add_argument('-d', '--disable', action='store_true',
                        help='Turn keyboard backlight off'),

    parsed = parser.parse_args()
    if parsed.disable:
        control.disable_keyboard()
    else :
        if parsed.style:
            if parsed.brightness :
                control.keyboard_style(parsed.style, parsed.brightness)
            else :
                control.keyboard_style(parsed.style)
        else :
            if parsed.brightness:
                control.adjust_brightness(int(parsed.brightness))
            if parsed.color:
                control.mono_color_setup(parsed.color)
            elif parsed.h_alt:
                control.h_alt_color_setup(*parsed.h_alt)
            elif parsed.v_alt:
                control.v_alt_color_setup(*parsed.v_alt)
            else :
                print("Invalid or absent command")


if __name__ == "__main__":
    main()
