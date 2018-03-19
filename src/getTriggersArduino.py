# -*- coding: utf-8 -*-
"""
Get triggers from Arduino
"""

import usb.core
import usb.util
import sys
import array as a


# Hexadecimal vendor and product values (remove '0x' if decimal)
device = usb.core.find(idVendor=0x2341, idProduct=0x0043)
print(device)

endpoint = device[0][(1,0)][1] # first endpoint
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

# DEVICE ID 2341:0043 on Bus 001 Address 008 =================
#  bLength                :   0x12 (18 bytes)
#  bDescriptorType        :    0x1 Device
#  bcdUSB                 :  0x110 USB 1.1
#  bDeviceClass           :    0x2 Communications Device
#  bDeviceSubClass        :    0x0
#  bDeviceProtocol        :    0x0
#  bMaxPacketSize0        :    0x8 (8 bytes)
#  idVendor               : 0x2341
#  idProduct              : 0x0043
#  bcdDevice              :    0x1 Device 0.01
#  iManufacturer          :    0x1 Arduino (www.arduino.cc)
#  iProduct               :    0x2 Error Accessing String
#  iSerialNumber          :   0xdc 55736313537351114051
#  bNumConfigurations     :    0x1
#   CONFIGURATION 1: 100 mA ==================================
#    bLength              :    0x9 (9 bytes)
#    bDescriptorType      :    0x2 Configuration
#    wTotalLength         :   0x3e (62 bytes)
#    bNumInterfaces       :    0x2
#    bConfigurationValue  :    0x1
#    iConfiguration       :    0x0
#    bmAttributes         :   0xc0 Self Powered
#    bMaxPower            :   0x32 (100 mA)
#     INTERFACE 0: CDC Communication =========================
#      bLength            :    0x9 (9 bytes)
#      bDescriptorType    :    0x4 Interface
#      bInterfaceNumber   :    0x0
#      bAlternateSetting  :    0x0
#      bNumEndpoints      :    0x1
#      bInterfaceClass    :    0x2 CDC Communication
#      bInterfaceSubClass :    0x2
#      bInterfaceProtocol :    0x1
#      iInterface         :    0x0
#       ENDPOINT 0x82: Interrupt IN ==========================
#        bLength          :    0x7 (7 bytes)
#        bDescriptorType  :    0x5 Endpoint
#        bEndpointAddress :   0x82 IN
#        bmAttributes     :    0x3 Interrupt
#        wMaxPacketSize   :    0x8 (8 bytes)
#        bInterval        :   0xff
#     INTERFACE 1: CDC Data ==================================
#      bLength            :    0x9 (9 bytes)
#      bDescriptorType    :    0x4 Interface
#      bInterfaceNumber   :    0x1
#      bAlternateSetting  :    0x0
#      bNumEndpoints      :    0x2
#      bInterfaceClass    :    0xa CDC Data
#      bInterfaceSubClass :    0x0
#      bInterfaceProtocol :    0x0
#      iInterface         :    0x0
#       ENDPOINT 0x4: Bulk OUT ===============================
#        bLength          :    0x7 (7 bytes)
#        bDescriptorType  :    0x5 Endpoint
#        bEndpointAddress :    0x4 OUT
#        bmAttributes     :    0x2 Bulk
#        wMaxPacketSize   :   0x40 (64 bytes)
#        bInterval        :    0x1
#       ENDPOINT 0x83: Bulk IN ===============================
#        bLength          :    0x7 (7 bytes)
#        bDescriptorType  :    0x5 Endpoint
#        bEndpointAddress :   0x83 IN
#        bmAttributes     :    0x2 Bulk
#        wMaxPacketSize   :   0x40 (64 bytes)
#        bInterval        :    0x1
