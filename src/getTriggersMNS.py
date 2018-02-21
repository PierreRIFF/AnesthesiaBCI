import usb.core
import usb.util


device = usb.core.find(idVendor=0x046d, idProduct=0xc534)
print(device)

# device.set_configuration()
device.get_active_configuration()

endpoint = device[0][(0,0)][0] # first endpoint

# Read a data packet
data = None
while True:
    try:
        data = device.read(endpoint.bEndpointAddress,
                           endpoint.wMaxPacketSize)
        print(data)

    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
