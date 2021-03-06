# -*- coding: utf-8 -*-
"""
Get triggers from USB device
"""

import usb.core
import usb.util
import sys
import array as a


# Hexadecimal vendor and product values (remove '0x' if decimal)
device = usb.core.find(idVendor=0x046d, idProduct=0xc534)
print(device)

endpoint = device[0][(1,0)][0] # first endpoint
# device[configIndex][(interfaceIndex,interfaceAlt)][endpointIndex]

## Device configuration
print('********************')
print('Configuration ...')
c = 1
for config in device:
    print('Config # ', c)
    print('Interfaces : ', config.bNumInterfaces)
    for i in range(config.bNumInterfaces):
        if device.is_kernel_driver_active(i):
            try:
                device.detach_kernel_driver(i)
            except usb.core.USBError as e:
                sys.exit("Could not detatch kernel driver: %s" % str(e))
        print('Interface # ', i)
    c+=1

# Set configuration
try:
    device.reset()
    device.set_configuration()
except usb.core.USBError as e:
    sys.exit("Could not set configuration: %s" % str(e))
print('Done !')
print('********************')

## Read a data packet
print('Triggers :')
collected = 0
attempts = 15
data = None
while collected < attempts :
    try:
        data = device.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        if data[1] != 0 or data[6] != 0:
            collected += 1
            print(data)
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue

## Release device
print('********************')
print('Releasing device ...')
c = 1
for config in device:
    print('Config # ', c)
    print('Interfaces : ', config.bNumInterfaces)
    for i in range(config.bNumInterfaces):
        # Release the device
        usb.util.release_interface(device, i)
        # Reattach the device to the OS kernel
        device.attach_kernel_driver(i)
        print('Interface # ', i)
    c+=1
print('Done !')
print('********************')
