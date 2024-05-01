# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 23 2022, 17:18:36) 
# [GCC 11.2.0]
# Embedded file name: REVComPorts.py
import serial, time, binascii, os
from serial.tools import list_ports
import re
defaultComPort = 0
comPortCommand = ''
testFixture = False

class comPort:

    def __init__(self, sn, name):
        self.sn = sn
        self.name = name

    def getSN(self):
        return self.sn

    def getNumber(self):
        num = re.findall('\\d+', self.name)
        return num[-1]

    def getName(self):
        return self.name


def getPorts():
    comPorts = []
    device_list = list_ports.comports()
    numdevs = len(device_list)
    for usbDevice in device_list:
        if 'SER=' in usbDevice.hwid:
            sections = usbDevice.hwid.split(' ')
            for section in sections:
                if 'SER=' in section:
                    serialNumber = section[4:]
                    deviceName = usbDevice.device
                    time.sleep(0.2)
                    comPorts.append(comPort(serialNumber, deviceName))

    return comPorts


def populateSerialPorts():
    global REVPorts
    global serialPorts
    serialPorts = getPorts()
    REVPorts = []
    for port in serialPorts:
        if port.getSN().startswith('D') and len(port.getSN()) > 2:
            REVPorts.append(port)


# global defaultComPort ## Warning: Unused global

# okay decompiling REVComPorts.pyc
