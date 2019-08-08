# brew install hidapi
# pip install hidapi

"""
Copyright (c) 2019, Rodrigo Gomes.
Distributed under the terms of the MIT License.
The full license is in the file LICENSE, distributed with this software.
Created on Aug, 6, 2019

@author: rodgomesc
"""

import hid
from time import sleep

vendor_id = 0x048d
product_id = 0xce00


print("Opening the device")

h = hid.device()
h.open(vendor_id, product_id) 

print("Manufacturer: %s" % h.get_manufacturer_string())
print("Product: %s" % h.get_product_string())
print("Serial No: %s" % h.get_serial_number_string())

# enable non-blocking mode
h.set_nonblocking(1)

#first char must be the length of the buffer starting at 1
h.send_feature_report([0x08, 0x08, 0x02, 0x33, 0x00, 0x24, 0x00, 0x00, 0x00]) #reset a color scheme
h.send_feature_report([0x08, 0x12, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00]) #setup mono_color

green = [0x00, 0x00, 0x00, 0xFF]*16 + [0x00] #green
red = [0x00, 0x00, 0xFF, 0x00]*16 + [0x00] #red

for _ in range(8):
    h.write(green)

h.close()
