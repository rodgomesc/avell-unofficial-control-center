"""
Copyright (c) 2019, Rodrigo Gomes.
Distributed under the terms of the MIT License.
The full license is in the file LICENSE, distributed with this software.
Created on May 27, 2019
@author: @rodgomesc
"""
import usb.core
import usb.util
import sys


class Device(object):
    def __init__(self, vendor_id, product_id):

        self._device = self._get_device(vendor_id, product_id)
        self.interface_id = self._get_interface()
        cfg = self._device.get_active_configuration()

        self.in_ep = self._get_endpoint(cfg[(1, 0)], usb.util.ENDPOINT_IN)
        self.out_ep = self._get_endpoint(cfg[(1, 0)], usb.util.ENDPOINT_OUT)

    def _get_device(self, vendor, product):
        device = usb.core.find(idVendor=vendor, idProduct=product)
        # in linux interface is 1, in windows 0
        if not sys.platform.startswith('win'):
            if device.is_kernel_driver_active(1):
                device.detach_kernel_driver(1)
        if device is None:
            raise ValueError('Device not found')
        else:
            return device

    def _get_interface(self):
        pass

    def _get_endpoint(self, intf, ep_type):

        ep = usb.util.find_descriptor(
            intf,
            custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) ==
            ep_type)

        return ep


class DeviceHandler(Device):
    def __init__(self, vendor_id, product_id):
        super(DeviceHandler, self).__init__(vendor_id, product_id)
        self.bmRequestType = 0x21
        self.bRequest = 0x09
        self.wValue = 0x300
        self.wIndex = 1

    def ctrl_write(self, *payload):
        self._device.ctrl_transfer(
            self.bmRequestType, self.bRequest, self.wValue, self.wIndex, payload)

    def bulk_write(self, times=1, payload=None):
        for _ in range(times):
            self._device.write(self.out_ep, payload)
