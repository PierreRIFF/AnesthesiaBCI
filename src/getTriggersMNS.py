# -*- coding: utf-8 -*-
"""
Get triggers from USB device
"""

import usb.core
import usb.util
import sys


# Hexadecimal vendor and product values (remove '0x' if decimal)
device = usb.core.find(idVendor=0x0403, idProduct=0xf601)
print(device)

endpoint = device[0][(0,0)][0] # first endpoint
# device[configIndex][(interfaceIndex,interfaceAlt)][endpointIndex]

# ## Device configuration
# print('********************')
# print('Configuration ...')
# c = 1
# for config in device:
#     print('Config # ', c)
#     print('Interfaces : ', config.bNumInterfaces)
#     for i in range(config.bNumInterfaces):
#         if device.is_kernel_driver_active(i):
#             try:
#                 device.detach_kernel_driver(i)
#             except usb.core.USBError as e:
#                 sys.exit("Could not detatch kernel driver: %s" % str(e))
#         print('Interface # ', i)
#     c+=1

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
attempts = 10
data = None
while collected < attempts :
    try:
        data = device.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        collected += 1
        print(data)
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue

# ## Release device
# print('********************')
# print('Releasing device ...')
# c = 1
# for config in device:
#     print('Config # ', c)
#     print('Interfaces : ', config.bNumInterfaces)
#     for i in range(config.bNumInterfaces):
#         # Release the device
#         usb.util.release_interface(device, i)
#         # Reattach the device to the OS kernel
#         device.attach_kernel_driver(i)
#         print('Interface # ', i)
#     c+=1
# print('Done !')
# print('********************')


"""
Notes
"""
# DEVICE ID 0403:f601 on Bus 001 Address 012 =================
#  bLength                :   0x12 (18 bytes)
#  bDescriptorType        :    0x1 Device
#  bcdUSB                 :  0x110 USB 1.1
#  bDeviceClass           :    0x0 Specified at interface
#  bDeviceSubClass        :    0x0
#  bDeviceProtocol        :    0x0
#  bMaxPacketSize0        :    0x8 (8 bytes)
#  idVendor               : 0x0403
#  idProduct              : 0xf601
#  bcdDevice              :  0x200 Device 2.0
#  iManufacturer          :    0x1 micromed
#  iProduct               :    0x2 micromed usb interface
#  iSerialNumber          :    0x0
#  bNumConfigurations     :    0x1
#   CONFIGURATION 1: 44 mA ===================================
#    bLength              :    0x9 (9 bytes)
#    bDescriptorType      :    0x2 Configuration
#    wTotalLength         :   0x20 (32 bytes)
#    bNumInterfaces       :    0x1
#    bConfigurationValue  :    0x1
#    iConfiguration       :    0x0
#    bmAttributes         :   0xa0 Bus Powered, Remote Wakeup
#    bMaxPower            :   0x16 (44 mA)
#     INTERFACE 0: Vendor Specific ===========================
#      bLength            :    0x9 (9 bytes)
#      bDescriptorType    :    0x4 Interface
#      bInterfaceNumber   :    0x0
#      bAlternateSetting  :    0x0
#      bNumEndpoints      :    0x2
#      bInterfaceClass    :   0xff Vendor Specific
#      bInterfaceSubClass :   0xff
#      bInterfaceProtocol :   0xff
#      iInterface         :    0x2 micromed usb interface
#       ENDPOINT 0x81: Bulk IN ===============================
#        bLength          :    0x7 (7 bytes)
#        bDescriptorType  :    0x5 Endpoint
#        bEndpointAddress :   0x81 IN
#        bmAttributes     :    0x2 Bulk
#        wMaxPacketSize   :   0x40 (64 bytes)
#        bInterval        :    0x0
#       ENDPOINT 0x2: Bulk OUT ===============================
#        bLength          :    0x7 (7 bytes)
#        bDescriptorType  :    0x5 Endpoint
#        bEndpointAddress :    0x2 OUT
#        bmAttributes     :    0x2 Bulk
#        wMaxPacketSize   :   0x40 (64 bytes)
#        bInterval        :    0x0
# return array('B', [49, 96])
