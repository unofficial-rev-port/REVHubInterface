"""REV ControlHub Interface for the REV Color Sensor"""
import logging
from .REVI2C import I2CDevice

def getDominantColor(r, g, b):
    """ return dominant color as a string """
    m = max(r, g, b)
    if m == r:
        return 'red'
    if m == g:
        return 'green'
    if m == b:
        return 'blue'
    return 'none'


def rgbi2c(r, g, b, ir):
    """ convert red, green, blue and ir value to clear """
    return r + g + b - 2 * ir


class REVColorSensorV3(I2CDevice):
    """For use with the REV Color Sensor V3"""

    def __init__(self, commObj, channel, destinationModule):
        I2CDevice.__init__(self, commObj, channel, destinationModule, self._REV_COLOR_SENSOR_ADDRESS)
        self.logger = logging.getLogger(__name__)
        self.setType('REVColorSensorV3')

    def initSensor(self):
        try:
            ident = self.readRegister(self._PART_ID)
        except TypeError:
            self.logger.debug('Error reading device ID')
            return False

        self.logger.debug('Device ID: 0x%0X', ident)
        if ident != self._REV_COLOR_SENSOR_ID:
            return False
        self.writeRegister(self._MAIN_CTRL, self._RGB_MODE | self._LS_EN | self._PS_EN)
        self.printRegister(self._MAIN_CTRL)
        self.writeRegister(self._PS_PULSES, 32)
        self.printRegister(self._PS_PULSES)
        self.writeRegister(self._PS_MEAS_RATE, self._PS_RES_11_BIT | self._PS_MEAS_RATE_100ms)
        self.printRegister(self._PS_MEAS_RATE)
        self.writeRegister(self._LS_GAIN, self._LS_GAIN_9)
        self.printRegister(self._LS_GAIN)
        return True

    def getAll(self):
        """ Returns raw proximity, red, green, blue and ir values. This is read as
        a block which is more efficient than getting each value individually. """
        self.writeByte(self._PS_DATA)
        tmp = self.readMultipleBytes(14)
        d = tmp & 2047
        ir = tmp >> 16 & 16777215
        g = tmp >> 40 & 16777215
        b = tmp >> 64 & 16777215
        r = tmp >> 88 & 16777215
        self.logger.debug('R: %d, G: %d, B: %d, I: %d, Prox: %d', r, g, b, ir, d)
        return (
         r, g, b, ir, d)

    def getProxValue(self):
        """ Returns raw proximity value """
        tmp = self.readWord(self._PS_DATA)
        ovf = (tmp & 2048) >> 11
        prox = tmp & 2047
        self.logger.debug('Prox: %d, Ovf: %d', prox, ovf)
        return prox

    def getRGBC(self):
        """ Returns red, green, blue and (calculated) clear value """
        self.writeByte(self._LS_DATA_IR)
        tmp = self.readMultipleBytes(12)
        ir = tmp & 16777215
        g = tmp >> 24 & 16777215
        b = tmp >> 48 & 16777215
        r = tmp >> 72 & 16777215
        c = rgbi2c(r, g, b, ir)
        self.logger.debug('R: %d, G: %d, B: %d, C: %d', r, g, b, c)
        return (
         r, g, b, c)

    def getIrValue(self):
        self.writeByte(self._LS_DATA_IR)
        ir = self.readMultipleBytes(3)
        self.logger.debug('IR: %d', ir)
        return ir

    def getGreenValue(self):
        self.writeByte(self._LS_DATA_GREEN)
        green = self.readMultipleBytes(3)
        self.logger.debug('G: %d', green)
        return green

    def getRedValue(self):
        self.writeByte(self._LS_DATA_RED)
        red = self.readMultipleBytes(3)
        self.logger.debug('R: %d', red)
        return red

    def getBlueValue(self):
        self.writeByte(self._LS_DATA_BLUE)
        blue = self.readMultipleBytes(3)
        self.logger.debug('B: %d', blue)
        return blue

    def readRegister(self, addr):
        self.writeByte(addr)
        tmp = self.readByte()
        self.logger.debug('Reading 0x%02X 0x%02X', addr, tmp)
        return tmp

    def printRegister(self, addr):
        tmp = self.readRegister(addr)
        self.logger.debug('Register 0x%02X: 0x%02X', addr, tmp)

    def readWord(self, addr):
        self.writeByte(addr)
        tmp = self.readMultipleBytes(2)
        self.logger.debug('Reading 0x%02X 0x%04X', addr, tmp)
        return tmp

    def writeRegister(self, register, value):
        self.logger.debug('Writing 0x%02X 0x%02X', register, value)
        self.writeMultipleBytes(2, register & 255 | value << 8)

    _REV_COLOR_SENSOR_ADDRESS = 82
    _REV_COLOR_SENSOR_ID = 194
    _MAIN_CTRL = 0
    _PS_LED = 1
    _PS_PULSES = 2
    _PS_MEAS_RATE = 3
    _LS_MEAS_RATE = 4
    _LS_GAIN = 5
    _PART_ID = 6
    _MAIN_STATUS = 7
    _PS_DATA = 8
    _LS_DATA_IR = 10
    _LS_DATA_GREEN = 13
    _LS_DATA_BLUE = 16
    _LS_DATA_RED = 19
    _INT_CFG = 25
    _INT_PST = 26
    _PS_THRES_UP = 27
    _PS_THRES_LOW = 29
    _PS_CAN = 31
    _LS_THRES_UP = 33
    _LS_THRES_LOW = 36
    _LS_THRES_VAR = 39
    _PS_EN = 1
    _LS_EN = 2
    _RGB_MODE = 4
    _PS_MEAS_RATE_6_25ms = 1
    _PS_MEAS_RATE_12_5ms = 2
    _PS_MEAS_RATE_25ms = 3
    _PS_MEAS_RATE_50ms = 4
    _PS_MEAS_RATE_100ms = 5
    _PS_MEAS_RATE_200ms = 6
    _PS_MEAS_RATE_400ms = 7
    _PS_RES_8_BIT = 0
    _PS_RES_9_BIT = 8
    _PS_RES_10_BIT = 16
    _PS_RES_11_BIT = 24
    _LS_GAIN_1 = 0
    _LS_GAIN_3 = 1
    _LS_GAIN_6 = 2
    _LS_GAIN_9 = 3
    _LS_GAIN_18 = 4

# okay decompiling REVColorSensorV3.pyc
