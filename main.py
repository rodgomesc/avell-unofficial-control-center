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
import colors


# 21 09 00 03 01 00 08 00 # setup packet

# 0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00    #disabled
# 0x08, 0x02, 0x05, 0x05, 0x24, 0x00, 0x00, 0x00    #rainbow
# 0x08, 0x02, 0x04, 0x05, 0x24, 0x08, 0x01, 0x00    #reactive
# 0x08, 0x02, 0x0A, 0x05, 0x24, 0x08, 0x00, 0x00    #rainDrop
# 0x08, 0x02, 0x09, 0x05, 0x24, 0x08, 0x00, 0x00    #Marquee
# 0x08, 0x02, 0x0E, 0x05, 0x24, 0x08, 0x00, 0x00    #Aurora
# 0x08, 0x02, 0x33, 0x00, 0x24, 0x00, 0x00, 0x00    # reset any color scheme before apply a new one, this is needed

def mono_color_setup(color_scheme):

    dev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x300, wIndex=1, data_or_wLength=(
        0x08, 0x02, 0x33, 0x00, 0x24, 0x00, 0x00, 0x00))  # reset color scheme

    dev.ctrl_transfer(bmRequestType=0x21, bRequest=9, wValue=0x300, wIndex=1, data_or_wLength=(
        0x12, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00))  # setup a mono_color scheme

    # i don't know whats happens behind the hoods, but control center send
    # this sequence of bytes 8 times, other wise don't will work
    for _ in range(8):
        dev.write(0x2, getattr(colors, color_scheme))


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
        description='color options are: red, green, blue, teal and pink')
    parser.add_argument('-c', '--color', type=mono_color_setup,
                        action='store', required=True)

    parsed = parser.parse_args()

    #print('Result:',  vars(parsed))
    #print('parsed.reqd:', parsed.reqd)
