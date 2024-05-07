from . import REVmessages as REVMsg
import time


def i2cWriteSingleByte(commObj, destination, i2cChannel, slaveAddress, byteToWrite):
    i2cWriteSingleByteMsg = REVMsg.I2CWriteSingleByte()
    i2cWriteSingleByteMsg.payload.i2cChannel = i2cChannel
    i2cWriteSingleByteMsg.payload.slaveAddress = slaveAddress
    i2cWriteSingleByteMsg.payload.byteToWrite = byteToWrite
    commObj.sendAndReceive(i2cWriteSingleByteMsg, destination)


def i2cWriteMultipleBytes(commObj, destination, i2cChannel, slaveAddress, numBytes, bytesToWrite):
    i2cWriteMultipleBytesMsg = REVMsg.I2CWriteMultipleBytes()
    i2cWriteMultipleBytesMsg.payload.i2cChannel = i2cChannel
    i2cWriteMultipleBytesMsg.payload.slaveAddress = slaveAddress
    i2cWriteMultipleBytesMsg.payload.numBytes = numBytes
    i2cWriteMultipleBytesMsg.payload.bytesToWrite = bytesToWrite
    commObj.sendAndReceive(i2cWriteMultipleBytesMsg, destination)


def i2cWriteStatusQuery(commObj, destination, i2cChannel):
    i2cWriteStatusQueryMsg = REVMsg.I2CWriteStatusQuery()
    i2cWriteStatusQueryMsg.payload.i2cChannel = i2cChannel
    packet = commObj.sendAndReceive(i2cWriteStatusQueryMsg, destination)
    return (
     packet.payload.i2cStatus, packet.payload.numBytes)


def i2cReadSingleByte(commObj, destination, i2cChannel, slaveAddress):
    i2cReadSingleByteMsg = REVMsg.I2CReadSingleByte()
    i2cReadSingleByteMsg.payload.i2cChannel = i2cChannel
    i2cReadSingleByteMsg.payload.slaveAddress = slaveAddress
    commObj.sendAndReceive(i2cReadSingleByteMsg, destination)


def i2cReadMultipleBytes(commObj, destination, i2cChannel, slaveAddress, numBytes):
    i2cReadMultipleBytesMsg = REVMsg.I2CReadMultipleBytes()
    i2cReadMultipleBytesMsg.payload.i2cChannel = i2cChannel
    i2cReadMultipleBytesMsg.payload.slaveAddress = slaveAddress
    i2cReadMultipleBytesMsg.payload.numBytes = numBytes
    commObj.sendAndReceive(i2cReadMultipleBytesMsg, destination)


def i2cReadStatusQuery(commObj, destination, i2cChannel):
    i2cReadStatusQueryMsg = REVMsg.I2CReadStatusQuery()
    i2cReadStatusQueryMsg.payload.i2cChannel = i2cChannel
    packet = commObj.sendAndReceive(i2cReadStatusQueryMsg, destination)
    return (
     packet.payload.i2cStatus, packet.payload.byteRead, packet.payload.payloadBytes)


def i2cConfigureChannel(commObj, destination, i2cChannel, speedCode):
    i2cConfigureChannelMsg = REVMsg.I2CConfigureChannel()
    i2cConfigureChannelMsg.payload.i2cChannel = i2cChannel
    i2cConfigureChannelMsg.payload.speedCode = speedCode
    commObj.sendAndReceive(i2cConfigureChannelMsg, destination)


def i2cConfigureQuery(commObj, destination, i2cChannel):
    i2cConfigureQueryMsg = REVMsg.I2CConfigureQuery()
    i2cConfigureQueryMsg.payload.i2cChannel = i2cChannel
    packet = commObj.sendAndReceive(i2cConfigureQueryMsg, destination)
    return packet.payload.speedCode


def i2cBlockReadConfig(commObj, destination, i2cChannel, address, startRegister, numberOfBytes, readInterval_ms):
    i2cBlockReadConfigMsg = REVMsg.I2CBlockReadConfig()
    i2cBlockReadConfigMsg.channel = i2cChannel
    i2cBlockReadConfigMsg.address = address
    i2cBlockReadConfigMsg.startRegister = startRegister
    i2cBlockReadConfigMsg.numberOfBytes = numberOfBytes
    i2cBlockReadConfigMsg.readInterval_ms = readInterval_ms
    commObj.sendAndReceive(i2cBlockReadConfigMsg, destination)


def i2cBlockReadQuery(commObj, destination):
    i2cBlockReadQueryMsg = REVMsg.I2CBlockReadQuery()
    packet = commObj.sendAndReceive(i2cBlockReadQueryMsg, destination)
    return packet


def imuBlockReadConfig(commObj, destination, startRegister, numberOfBytes, readInterval_ms):
    imuBlockReadConfigMsg = REVMsg.IMUBlockReadConfig()
    imuBlockReadConfigMsg.startRegister = startRegister
    imuBlockReadConfigMsg.numberOfBytes = numberOfBytes
    imuBlockReadConfigMsg.readInterval_ms = readInterval_ms
    commObj.sendAndReceive(imuBlockReadConfigMsg, destination)


def imuBlockReadQuery(commObj, destination):
    imuBlockReadQueryMsg = REVMsg.IMUBlockReadQuery()
    packet = commObj.sendAndReceive(imuBlockReadQueryMsg, destination)
    return packet


class I2CChannel:

    def __init__(self, commObj, channel, destinationModule):
        self.commObj = commObj
        self.channel = channel
        self.destinationModule = destinationModule
        self.devices = {}

    def setChannel(self, channel):
        self.channel = channel

    def getChannel(self):
        return self.channel

    def setDestination(self, destinationModule):
        self.destinationModule = destinationModule

    def getDestination(self):
        return self.destinationModule

    def addDevice(self, address, name):
        self.devices[name] = I2CDevice(self.commObj, self.channel, self.destinationModule, address)

    def addColorSensor(self, name):
        self.devices[name] = ColorSensor(self.commObj, self.channel, self.destinationModule)

    def addIMU(self, name):
        self.devices[name] = IMU(self.commObj, self.channel, self.destinationModule)

    def addI2CDevice(self, name, device):
        self.devices[name] = device

    def getDevices(self):
        return self.devices

    def setSpeed(self, speedCode):
        i2cConfigureChannel(self.destinationModule, self.channel, speedCode)
        return i2cConfigureQuery(self.destinationModule, self.channel)


class I2CDevice:

    def __init__(self, commObj, channel, destinationModule, address):
        self.commObj = commObj
        self.channel = channel
        self.destinationModule = destinationModule
        self.address = address
        self.type = 'Generic'

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setChannel(self, channel):
        self.channel = channel

    def getChannel(self):
        return self.channel

    def setDestination(self, destinationModule):
        self.destinationModule = destinationModule

    def getDestination(self):
        return self.destinationModule

    def setAddress(self, address):
        self.address = address

    def getAddress(self):
        return self.address

    def writeByte(self, byteToWrite):
        i2cWriteSingleByte(self.commObj, self.destinationModule, self.channel, self.address, byteToWrite)

    def writeMultipleBytes(self, numBytes, bytesToWrite):
        i2cWriteMultipleBytes(self.commObj, self.destinationModule, self.channel, self.address, numBytes, bytesToWrite)

    def readByte(self):
        i2cReadSingleByte(self.commObj, self.destinationModule, self.channel, self.address)
        return int(i2cReadStatusQuery(self.commObj, self.destinationModule, self.channel)[2]) & 255

    def readMultipleBytes(self, numBytes):
        i2cReadMultipleBytes(self.commObj, self.destinationModule, self.channel, self.address, numBytes)
        byteMask = '0x'
        for i in range(0, numBytes):
            byteMask += 'FF'

        return int(i2cReadStatusQuery(self.commObj, self.destinationModule, self.channel)[2]) & int(byteMask, 16)

    def setBlockReadConfig(self, startRegister, numberOfBytes, readInterval_ms):
        i2cBlockReadConfig(self.commObj, self.destinationModule, self.channel, self.address, startRegister, numberOfBytes, readInterval_ms)

    def getBlockReadConfig(self):
        return i2cBlockReadQuery(self.commObj, self.destinationModule)


COMMAND_REGISTER_BIT = 128
SINGLE_BYTE_BIT = 0
MULTI_BYTE_BIT = 32
COLOR_SENSOR_ADDRESS = 57
COLOR_SENSOR_ID = 96
ENABLE_REGISTER = 0
ATIME_REGISTER = 1
WTIME_REGISTER = 3
AILTL_REGISTER = 4
AILTH_REGISTER = 5
AIHTL_REGISTER = 6
AIHTH_REGISTER = 7
PILTL_REGISTER = 8
PILTH_REGISTER = 9
PIHTL_REGISTER = 10
PIHTH_REGISTER = 11
PERS_REGISTER = 12
CONFIG_REGISTER = 13
PPULSE_REGISTER = 14
CONTROL_REGISTER = 15
REVISION_REGISTER = 17
ID_REGISTER = 18
STATUS_REGISTER = 19
CDATA_REGISTER = 20
CDATAH_REGISTER = 21
RDATA_REGISTER = 22
RDATAH_REGISTER = 23
GDATA_REGISTER = 24
GDATAH_REGISTER = 25
BDATA_REGISTER = 26
BDATAH_REGISTER = 27
PDATA_REGISTER = 28
PDATAH_REGISTER = 29

class ColorSensor(I2CDevice):

    def __init__(self, commObj, channel, destinationModule):
        I2CDevice.__init__(self, commObj, channel, destinationModule, COLOR_SENSOR_ADDRESS)

    def initSensor(self):
        self.writeByte(COMMAND_REGISTER_BIT | ENABLE_REGISTER)
        self.writeByte(7)
        self.writeByte(COMMAND_REGISTER_BIT | ATIME_REGISTER)
        self.writeByte(255)
        self.writeByte(COMMAND_REGISTER_BIT | PPULSE_REGISTER)
        self.writeByte(8)
        try:
            ident = self.getDeviceID()
        except TypeError:
            ident = 255

        return ident == COLOR_SENSOR_ID

    def getEnable(self):
        self.writeByte(COMMAND_REGISTER_BIT | ENABLE_REGISTER)
        byte1 = self.readByte()
        return byte1

    def getDominantColor(self):
        time.sleep(0.05)
        clear = self.getClearValue()
        red = self.getRedValue()
        green = self.getGreenValue()
        blue = self.getBlueValue()
        RED = 0
        GREEN = 2
        BLUE = 1
        if red > blue and red > green:
            print('RED')
            return RED
        else:
            if blue > red and blue > green:
                print('BLUE')
                return BLUE
            if green > red and green > blue:
                print('GREEN')
                return GREEN
            return -1

    def getDeviceID(self):
        self.writeByte(COMMAND_REGISTER_BIT | MULTI_BYTE_BIT | ID_REGISTER)
        return self.readByte()

    def getGreenValue(self):
        return self.getRegisterValue(GDATA_REGISTER)

    def getRedValue(self):
        return self.getRegisterValue(RDATA_REGISTER)

    def getBlueValue(self):
        return self.getRegisterValue(BDATA_REGISTER)

    def getClearValue(self):
        return self.getRegisterValue(CDATA_REGISTER)

    def getProxValue(self):
        return self.getRegisterValue(PDATA_REGISTER)

    def getRegisterValue(self, register):
        self.writeByte(COMMAND_REGISTER_BIT | MULTI_BYTE_BIT | register)
        return self.readMultipleBytes(2)


IMU_ADDRESS = 40
PAGE_ID = 7
CHIP_ID = 0
ACC_ID = 1
MAG_ID = 2
GYR_ID = 3
SW_REV_ID_LSB = 4
SW_REV_ID_MSB = 5
BL_REV_ID = 6
ACC_DATA_X_LSB = 8
ACC_DATA_X_MSB = 9
ACC_DATA_Y_LSB = 10
ACC_DATA_Y_MSB = 11
ACC_DATA_Z_LSB = 12
ACC_DATA_Z_MSB = 13
MAG_DATA_X_LSB = 14
MAG_DATA_X_MSB = 15
MAG_DATA_Y_LSB = 16
MAG_DATA_Y_MSB = 17
MAG_DATA_Z_LSB = 18
MAG_DATA_Z_MSB = 19
GYR_DATA_X_LSB = 20
GYR_DATA_X_MSB = 21
GYR_DATA_Y_LSB = 22
GYR_DATA_Y_MSB = 23
GYR_DATA_Z_LSB = 24
GYR_DATA_Z_MSB = 25
EUL_H_LSB = 26
EUL_H_MSB = 27
EUL_R_LSB = 28
EUL_R_MSB = 29
EUL_P_LSB = 30
EUL_P_MSB = 31
QUA_DATA_W_LSB = 32
QUA_DATA_W_MSB = 33
QUA_DATA_X_LSB = 34
QUA_DATA_X_MSB = 35
QUA_DATA_Y_LSB = 36
QUA_DATA_Y_MSB = 37
QUA_DATA_Z_LSB = 38
QUA_DATA_Z_MSB = 39
LIA_DATA_X_LSB = 40
LIA_DATA_X_MSB = 41
LIA_DATA_Y_LSB = 42
LIA_DATA_Y_MSB = 43
LIA_DATA_Z_LSB = 44
LIA_DATA_Z_MSB = 45
GRV_DATA_X_LSB = 46
GRV_DATA_X_MSB = 47
GRV_DATA_Y_LSB = 48
GRV_DATA_Y_MSB = 49
GRV_DATA_Z_LSB = 50
GRV_DATA_Z_MSB = 51
TEMP = 52
CALIB_STAT = 53
SELFTEST_RESULT = 54
INTR_STAT = 55
SYS_CLK_STAT = 56
SYS_STAT = 57
SYS_ERR = 58
UNIT_SEL = 59
DATA_SELECT = 60
OPR_MODE = 61
PWR_MODE = 62
SYS_TRIGGER = 63
TEMP_SOURCE = 64
CONFIGMODE = 0
ACCONLY = 1
MAGONLY = 2
GYROONLY = 3
ACCMAG = 4
ACCGYRO = 5
MAGGYRO = 6
AMG = 7
IMUMODE = 8
COMPASS = 9
M4G = 10
NDOF_FMC_OFF = 11
NDOF = 12
NORMAL = 0
LOW_POWER = 1
SUSPEND = 2
AXIS_MAP_CONFIG = 65
AXIS_MAP_SIGN = 66
SIC_MATRIX_0_LSB = 67
SIC_MATRIX_0_MSB = 68
SIC_MATRIX_1_LSB = 69
SIC_MATRIX_1_MSB = 70
SIC_MATRIX_2_LSB = 71
SIC_MATRIX_2_MSB = 72
SIC_MATRIX_3_LSB = 73
SIC_MATRIX_3_MSB = 74
SIC_MATRIX_4_LSB = 75
SIC_MATRIX_4_MSB = 76
SIC_MATRIX_5_LSB = 77
SIC_MATRIX_5_MSB = 78
SIC_MATRIX_6_LSB = 79
SIC_MATRIX_6_MSB = 80
SIC_MATRIX_7_LSB = 81
SIC_MATRIX_7_MSB = 82
SIC_MATRIX_8_LSB = 83
SIC_MATRIX_8_MSB = 84
ACC_OFFSET_X_LSB = 85
ACC_OFFSET_X_MSB = 86
ACC_OFFSET_Y_LSB = 87
ACC_OFFSET_Y_MSB = 88
ACC_OFFSET_Z_LSB = 89
ACC_OFFSET_Z_MSB = 90
MAG_OFFSET_X_LSB = 91
MAG_OFFSET_X_MSB = 92
MAG_OFFSET_Y_LSB = 93
MAG_OFFSET_Y_MSB = 94
MAG_OFFSET_Z_LSB = 95
MAG_OFFSET_Z_MSB = 96
GYR_OFFSET_X_LSB = 97
GYR_OFFSET_X_MSB = 98
GYR_OFFSET_Y_LSB = 99
GYR_OFFSET_Y_MSB = 100
GYR_OFFSET_Z_LSB = 101
GYR_OFFSET_Z_MSB = 102
ACC_RADIUS_LSB = 103
ACC_RADIUS_MSB = 104
MAG_RADIUS_LSB = 105
MAG_RADIUS_MSB = 106
EUL_UNIT_DEG = 0
EUL_UNIT_RAD = 4
GYR_UNIT_DPS = 0
GYR_UNIT_RPS = 2
ACC_UNIT_MSS = 0
ACC_UNIT_MG = 1
ACC_CONFIG = 8
MAG_CONFIG = 9
GYR_CONFIG_0 = 10
GYR_CONFIG_1 = 11
ACC_SLEEP_CONFIG = 12
GYR_SLEEP_CONFIG = 13
INT_MSK = 15
INT_EN = 16
ACC_AM_THRES = 17
ACC_INT_SETTINGS = 18
ACC_HG_DURATION = 19
ACC_HG_THRES = 20
ACC_NM_THRES = 21
ACC_NM_SET = 22
GRYO_INT_SETTING = 23
GRYO_HR_X_SET = 24
GRYO_DUR_ = 25
GRYO_HR_Y_SET = 26
GRYO_DUR_Y = 27
GRYO_HR_Z_SET = 28
GRYO_DUR_Z = 29
GRYO_AM_THRES = 30
GRYO_AM_SET = 31
UNIQUE_ID_FIRST = 80
UNIQUE_ID_LAST = 95

class IMU(I2CDevice):

    def __init__(self, commObj, channel, destinationModule):
        I2CDevice.__init__(self, commObj, channel, destinationModule, IMU_ADDRESS)

    def getDeviceID(self):
        return self.getRegisterValue(CHIP_ID)

    def initSensor(self):
        for _ in range(3):
            self.setRegisterValue(OPR_MODE, CONFIGMODE)
            self.setRegisterValue(PWR_MODE, NORMAL)
            self.setRegisterValue(SYS_TRIGGER, 128)
            self.setRegisterValue(PAGE_ID, 0)
            self.setRegisterValue(UNIT_SEL, ACC_UNIT_MSS)
            self.setRegisterValue(OPR_MODE, IMUMODE)
            try:
                stat = self.getRegisterValue(SYS_STAT)
            except AttributeError:
                stat = -1

            if stat == 5:
                break
            time.sleep(0.1)

    def getTemperature(self):
        return self.getRegisterValue(TEMP)

    def getGyroData_X(self):
        return self.getTwoByteRegisterValue(GYR_DATA_X_LSB)

    def getGyroData_Y(self):
        return self.getTwoByteRegisterValue(GYR_DATA_Y_LSB)

    def getGyroData_Z(self):
        return self.getTwoByteRegisterValue(GYR_DATA_Z_LSB)

    def getAccData_X(self):
        return self.getTwoByteRegisterValue(ACC_DATA_X_LSB)

    def getAccData_Y(self):
        return self.getTwoByteRegisterValue(ACC_DATA_Y_LSB)

    def getAccData_Z(self):
        return self.getTwoByteRegisterValue(ACC_DATA_Z_LSB)

    def getMagData_X(self):
        return self.getTwoByteRegisterValue(MAG_DATA_X_LSB)

    def getMagData_Y(self):
        return self.getTwoByteRegisterValue(MAG_DATA_Y_LSB)

    def getMagData_Z(self):
        return self.getTwoByteRegisterValue(MAG_DATA_Z_LSB)

    def getAllEuler(self):
        values = self.getSixByteRegisterValue(EUL_H_LSB)
        return [360.0 * float(value) / 5760.0 for value in values]

    def getGravity(self):
        values = self.getSixByteRegisterValue(GRV_DATA_X_LSB)
        return [float(value) / 100 for value in values]

    def getAllLinAccel(self):
        values = self.getSixByteRegisterValue(LIA_DATA_X_LSB)
        return [float(value) / 1000 for value in values]

    def setRegisterValue(self, register, value):
        self.writeMultipleBytes(2, register + (value << 8))

    def getRegisterValue(self, register):
        self.writeByte(register)
        return self.readByte()

    def getTwoByteRegisterValue(self, register):
        self.writeByte(register)
        val = int(self.readMultipleBytes(2))
        bits = int(16)
        if val & 1 << bits - 1 != 0:
            val = val - (1 << bits)
        return val

    def getSixByteRegisterValue(self, register):
        self.writeByte(register)
        val = int(self.readMultipleBytes(6))
        bits = int(16)
        values = []
        for i in range(0, 3):
            it_val = val & 65535
            if it_val & 1 << bits - 1 != 0:
                it_val = it_val - (1 << bits)
            values.append(it_val)
            val = val >> 16

        return values