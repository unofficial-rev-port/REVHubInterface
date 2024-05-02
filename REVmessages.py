PAYLOAD_MAX_SIZE = 128

class LEDColor:
    Red = 0
    Yellow = 1
    Green = 2


class ADCChannel:
    ADC_0 = 0
    ADC_1 = 1
    ADC_2 = 2
    ADC_3 = 3
    ADC_GPIO = 4
    ADC_I2C = 5
    ADC_Servo = 6
    ADC_Battery = 7
    ADC_Motor0 = 8
    ADC_Motor1 = 9
    ADC_Motor2 = 10
    ADC_Motor3 = 11
    ADC_5VMonitor = 12
    ADC_BatteryMonitor = 13
    ADC_CPUTemp = 14


class REVBytes:
    creationCounter = 0

    def __init__(self, NumBytes):
        self.numBytes = NumBytes
        self.data = 0
        self.memberOrder = REVBytes.creationCounter
        REVBytes.creationCounter += 1

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return self.numBytes

    def __setattr__(self, name, value):
        if isinstance(value, str):
            try:
                value = int(value, 16)
            except ValueError:
                value = int(ord(value), 16)

        if isinstance(value, REVBytes):
            value = value.data
        self.__dict__[name] = value

    def __lt__(self, other):
        if self.data < other:
            return True
        return False

    def __le__(self, other):
        if self.data <= other:
            return True
        return False

    def __eq__(self, other):
        if self.data == other:
            return True
        return False

    def __ne__(self, other):
        if self.data != other:
            return True
        return False

    def __ge__(self, other):
        if self.data >= other:
            return True
        return False

    def __gt__(self, other):
        if self.data > other:
            return True
        return False

    def __sub__(self, other):
        return self.data - other

    def __rsub__(self, other):
        return other - self.data

    def __add__(self, other):
        return self.data + other

    def __float__(self):
        return float(self.data)

    def __int__(self):
        return int(self.data)

    def __add__(self, other):
        if isinstance(other, str):
            myBytes = self.getHexString()
            if len(myBytes) > 2:
                swappedText = ''
                for i in range(len(myBytes), 0, -2):
                    swappedText += myBytes[i - 2:i]

                myBytes = swappedText
            return myBytes + other
        else:
            return self.data + other

    def __radd__(self, other):
        if isinstance(other, str):
            myBytes = self.getHexString()
            if len(myBytes) > 2:
                swappedText = ''
                for i in range(len(myBytes), 0, -2):
                    swappedText += myBytes[i - 2:i]

                myBytes = swappedText
            return other + myBytes
        else:
            return other + self.data
        
    def getHexString(self):
        hexString = '%0' + str(self.numBytes * 2) + 'X'
        hexString = hexString % int(self.data) 
        return hexString


class LEDPattern:

    def __init__(self):
        self.patt = []
        for _ in range(15):
            self.patt.append(REVBytes(4))

    def set_step(self, step_num, r, g, b, t):
        r &= 255
        g &= 255
        b &= 255
        t &= 255
        self.patt[step_num] = r << 24 | g << 16 | b << 8 | t


class REVHeader:

    def __init__(self, Cmd=''):
        self.length = REVBytes(2)
        self.destination = REVBytes(1)
        self.source = REVBytes(1)
        self.msgNum = REVBytes(1)
        self.refNum = REVBytes(1)
        self.packetType = REVBytes(2)
        self.packetType = Cmd >> 8 | Cmd % 256 << 8

    def __len__(self):
        length = 0
        for classMemberName in dir(self):
            classMember = getattr(self, classMemberName)
            if isinstance(classMember, REVBytes):
                length += len(classMember)

        return length

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name].data = value
        elif isinstance(value, REVBytes):
            self.__dict__[name] = value
        else:
            exit('\n\n\n!!!Attempting to add something other than REVBytes to payload structure!!!\n\n\n')

    def __add__(self, TextToAppend):
        return self.__str__() + TextToAppend

    def __radd__(self, TextToPrepend):
        return TextToPrepend + self.__str__()

    def __str__(self):
        return self.length.getHexString() + self.destination.getHexString() + self.source.getHexString() + self.msgNum.getHexString() + self.refNum.getHexString() + self.packetType.getHexString()


class REVPayload:

    def __len__(self):
        length = 0
        for classMemberName in dir(self):
            classMember = getattr(self, classMemberName)
            if isinstance(classMember, REVBytes):
                length += len(classMember)

        return length

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name].data = value
        elif isinstance(value, REVBytes):
            self.__dict__[name] = value
        else:
            print('Value is not an instance of REVBytes: ', value)
            exit('\n\n\n!!!Attempting to add something other than REVBytes to payload structure!!!\n\n\n')

    def __add__(self, TextToAppend):
        return self.__str__() + TextToAppend

    def __radd__(self, TextToPrepend):
        return TextToPrepend + self.__str__()

    def __str__(self):
        payloadDict = {}
        payloadStr = ''
        for objectStr in dir(self):
            memberObject = getattr(self, objectStr)
            if isinstance(memberObject, REVBytes):
                payloadDict[memberObject.memberOrder] = memberObject

        for payloadKey in sorted(payloadDict):
            if payloadDict[payloadKey].data < 0:
                comp = 'FF' * len(payloadDict[payloadKey])
                comp = int('0x' + comp, 16) - abs(int(payloadDict[payloadKey])) + 1
                strComp = ''
                strComp = hex(int(comp))[2:]
                if strComp.endswith('L'):
                    strComp = strComp[:-1]
                if len(strComp) > 2:
                    swappedText = ''
                    for i in range(len(strComp), 0, -2):
                        swappedText += strComp[i - 2:i]

                    strComp = swappedText
                payloadStr += strComp
            else:
                payloadStr += payloadDict[payloadKey]

        return payloadStr

    def getOrderedMembers(self):
        payloadMembers = []
        payloadDict = {}
        for objectStr in dir(self):
            memberObject = getattr(self, objectStr)
            if isinstance(memberObject, REVBytes):
                payloadDict[memberObject.memberOrder] = memberObject

        for payloadKey in sorted(payloadDict):
            payloadMembers.append(payloadDict[payloadKey])

        return payloadMembers


class REVPacket:
    """
   |DEKAPlSaSaDsDsMnCmPa------>Ck|
    0 1 2 3 4 5 6 7 8 9 A B C D E F
   """
    FrameIndex_Start = 0
    FrameIndex_End = FrameIndex_Start + 4
    HeaderIndex_Start = FrameIndex_End
    LengthIndex_Start = FrameIndex_End
    LengthIndex_End = LengthIndex_Start + 4
    DestinationIndex_Start = LengthIndex_End
    DestinationIndex_End = DestinationIndex_Start + 2
    SourceIndex_Start = DestinationIndex_End
    SourceIndex_End = SourceIndex_Start + 2
    MsgNumIndex_Start = SourceIndex_End
    MsgNumIndex_End = MsgNumIndex_Start + 2
    RefNumIndex_Start = MsgNumIndex_End
    RefNumIndex_End = RefNumIndex_Start + 2
    PacketTypeIndex_Start = RefNumIndex_End
    PacketTypeIndex_End = PacketTypeIndex_Start + 4
    HeaderIndex_End = PacketTypeIndex_End

    def __init__(self, Header, Payload):
        self.frame = '444B'
        self.header = Header
        self.payload = Payload
        self.chkSum = '00'
        self.calcLength()

    def calcLength(self):
        self.header.length = len(self.header) + len(self.payload) + 3
        self.header.length = int(self.header.length) >> 8 | int(self.header.length) % 256 << 8

    def getPacketData(self):
        chkSummableBytes = self.frame + self.header + self.payload
        chkSum = 0
        for i in range(0, len(chkSummableBytes), 2):
            chkSum += int(chkSummableBytes[i:i + 2], 16)
            chkSum %= 256

        self.chkSum = '%02X' % chkSum
        return (self.frame + self.header + self.payload + self.chkSum).upper()

    def assignRawBytes(self, rawBytes_nibble):
        frameBytes = rawBytes_nibble[REVPacket.FrameIndex_Start:REVPacket.FrameIndex_End]
        lengthByte = rawBytes_nibble[REVPacket.LengthIndex_Start:REVPacket.LengthIndex_End]
        destinationBytes = rawBytes_nibble[REVPacket.DestinationIndex_Start:REVPacket.DestinationIndex_End]
        sourceBytes = rawBytes_nibble[REVPacket.SourceIndex_Start:REVPacket.SourceIndex_End]
        msgNumByte = rawBytes_nibble[REVPacket.MsgNumIndex_Start:REVPacket.MsgNumIndex_End]
        refNumByte = rawBytes_nibble[REVPacket.RefNumIndex_Start:REVPacket.RefNumIndex_End]
        packetBytes = rawBytes_nibble[REVPacket.HeaderIndex_End:-2]
        checkSumByte = rawBytes_nibble[-2:]
        self.header.length = lengthByte
        self.header.destination = destinationBytes
        self.header.source = sourceBytes
        self.header.msgNum = msgNumByte
        self.header.refNum = refNumByte
        self.header.packetType = packetBytes
        payloadDict = {}
        for payloadMemberName in dir(self.payload):
            payloadMember = getattr(self.payload, payloadMemberName)
            if isinstance(payloadMember, REVBytes):
                payloadDict[payloadMember.memberOrder] = {'Name': payloadMemberName, 'Length': (payloadMember.numBytes)}

        byteCounter = 0
        for payloadKey in sorted(payloadDict):
            name = payloadDict[payloadKey]['Name']
            length = payloadDict[payloadKey]['Length']
            value = packetBytes[byteCounter:byteCounter + length * 2]
            byteCounter += length * 2
            if length > 1:
                swappedText = ''
                for i in range(len(value), 0, -2):
                    swappedText += value[i - 2:i]

                value = swappedText
            setattr(self.payload, name, value)


class ACK_Payload(REVPayload):

    def __init__(self):
        self.attnReq = REVBytes(1)


class NACK_Payload(REVPayload):

    def __init__(self):
        self.nackCode = REVBytes(1)


class GetModuleStatus_Payload(REVPayload):

    def __init__(self):
        self.clearStatus = REVBytes(1)


class KeepAlive_Payload(REVPayload):

    def __init__(self):
        pass


class FailSafe_Payload(REVPayload):

    def __init__(self):
        pass


class SetNewModuleAddress_Payload(REVPayload):

    def __init__(self):
        self.moduleAddress = REVBytes(1)


class QueryInterface_Payload(REVPayload):

    def __init__(self):
        self.interfaceName = REVBytes(PAYLOAD_MAX_SIZE - 7)


class StartProgramDownload_Payload(REVPayload):

    def __init__(self):
        pass


class ProgramDownloadChunk_Payload(REVPayload):

    def __init__(self):
        pass


class SetModuleLEDColor_Payload(REVPayload):

    def __init__(self):
        self.redPower = REVBytes(1)
        self.greenPower = REVBytes(1)
        self.bluePower = REVBytes(1)


class GetModuleLEDColor_Payload(REVPayload):

    def __init__(self):
        pass


class SetModuleLEDPattern_Payload(REVPayload):

    def __init__(self):
        self.rgbtStep0 = REVBytes(4)
        self.rgbtStep1 = REVBytes(4)
        self.rgbtStep2 = REVBytes(4)
        self.rgbtStep3 = REVBytes(4)
        self.rgbtStep4 = REVBytes(4)
        self.rgbtStep5 = REVBytes(4)
        self.rgbtStep6 = REVBytes(4)
        self.rgbtStep7 = REVBytes(4)
        self.rgbtStep8 = REVBytes(4)
        self.rgbtStep9 = REVBytes(4)
        self.rgbtStep10 = REVBytes(4)
        self.rgbtStep11 = REVBytes(4)
        self.rgbtStep12 = REVBytes(4)
        self.rgbtStep13 = REVBytes(4)
        self.rgbtStep14 = REVBytes(4)
        self.rgbtStep15 = REVBytes(4)


class GetModuleLEDPattern_Payload(REVPayload):

    def __init__(self):
        pass


class DebugLogLevel_Payload(REVPayload):

    def __init__(self):
        self.groupNumber = REVBytes(1)
        self.verbosityLevel = REVBytes(1)


class Discovery_Payload(REVPayload):

    def __init__(self):
        pass


class GetBulkInputData_Payload(REVPayload):

    def __init__(self):
        pass


class SetSingleDIOOutput_Payload(REVPayload):

    def __init__(self):
        self.dioPin = REVBytes(1)
        self.value = REVBytes(1)


class SetAllDIOOutputs_Payload(REVPayload):

    def __init__(self):
        self.values = REVBytes(1)


class SetDIODirection_Payload(REVPayload):

    def __init__(self):
        self.dioPin = REVBytes(1)
        self.directionOutput = REVBytes(1)


class GetDIODirection_Payload(REVPayload):

    def __init__(self):
        self.dioPin = REVBytes(1)


class GetSingleDIOInput_Payload(REVPayload):

    def __init__(self):
        self.dioPin = REVBytes(1)


class GetAllDIOInputs_Payload(REVPayload):

    def __init__(self):
        pass


class GetADC_Payload(REVPayload):
    def __init__(self):
        self.adcChannel = REVBytes(1)
        self.rawMode = REVBytes(1)


class SetMotorChannelMode_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.motorMode = REVBytes(1)
        self.floatAtZero = REVBytes(1)


class GetMotorChannelMode_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)


class SetMotorChannelEnable_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.enabled = REVBytes(1)


class GetMotorChannelEnable_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)


class SetMotorChannelCurrentAlertLevel_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.currentLimit = REVBytes(2)


class GetMotorChannelCurrentAlertLevel_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)


class ResetMotorEncoder_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)


class SetMotorConstantPower_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.powerLevel = REVBytes(2)


class GetMotorConstantPower_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)


class SetMotorTargetVelocity_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.velocity = REVBytes(2)


class GetMotorTargetVelocity_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)


class SetMotorTargetPosition_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.position = REVBytes(4)
        self.atTargetTolerance = REVBytes(2)


class GetMotorTargetPosition_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)


class GetMotorAtTarget_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)


class GetMotorEncoderPosition_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)


class SetMotorPIDCoefficients_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.mode = REVBytes(1)
        self.p = REVBytes(4)
        self.i = REVBytes(4)
        self.d = REVBytes(4)


class GetMotorPIDCoefficients_Payload(REVPayload):
    def __init__(self):
        self.motorChannel = REVBytes(1)
        self.mode = REVBytes(1)


class SetPWMConfiguration_Payload(REVPayload):
    def __init__(self):
        self.pwmChannel = REVBytes(1)
        self.framePeriod = REVBytes(2)


class GetPWMConfiguration_Payload(REVPayload):
    def __init__(self):
        self.pwmChannel = REVBytes(1)


class SetPWMPulseWidth_Payload(REVPayload):
    def __init__(self):
        self.pwmChannel = REVBytes(1)
        self.pulseWidth = REVBytes(2)


class GetPWNPulseWidth_Payload(REVPayload):
    def __init__(self):
        self.pwmChannel = REVBytes(1)


class SetPWMEnable_Payload(REVPayload):
    def __init__(self):
        self.pwmChannel = REVBytes(1)
        self.enable = REVBytes(1)


class GetPWMEnable_Payload(REVPayload):
    def __init__(self):
        self.pwmChannel = REVBytes(1)


class SetServoConfiguration_Payload(REVPayload):
    def __init__(self):
        self.servoChannel = REVBytes(1)
        self.framePeriod = REVBytes(2)


class GetServoConfiguration_Payload(REVPayload):
    def __init__(self):
        self.servoChannel = REVBytes(1)


class SetServoPulseWidth_Payload(REVPayload):
    def __init__(self):
        self.servoChannel = REVBytes(1)
        self.pulseWidth = REVBytes(2)


class GetServoPulseWidth_Payload(REVPayload):
    def __init__(self):
        self.servoChannel = REVBytes(1)


class SetServoEnable_Payload(REVPayload):
    def __init__(self):
        self.servoChannel = REVBytes(1)
        self.enable = REVBytes(1)


class GetServoEnable_Payload(REVPayload):
    def __init__(self):
        self.servoChannel = REVBytes(1)


class I2CWriteSingleByte_Payload(REVPayload):
    def __init__(self):
        self.i2cChannel = REVBytes(1)
        self.slaveAddress = REVBytes(1)
        self.byteToWrite = REVBytes(1)


class I2CWriteMultipleBytes_Payload(REVPayload):

    def __init__(self):
        self.i2cChannel = REVBytes(1)
        self.slaveAddress = REVBytes(1)
        self.numBytes = REVBytes(1)
        self.bytesToWrite = REVBytes(PAYLOAD_MAX_SIZE - 7)


class I2CWriteStatusQuery_Payload(REVPayload):
    def __init__(self):
        self.i2cChannel = REVBytes(1)


class I2CReadSingleByte_Payload(REVPayload):

    def __init__(self):
        self.i2cChannel = REVBytes(1)
        self.slaveAddress = REVBytes(1)


class I2CReadMultipleBytes_Payload(REVPayload):

    def __init__(self):
        self.i2cChannel = REVBytes(1)
        self.slaveAddress = REVBytes(1)
        self.numBytes = REVBytes(1)


class I2CReadStatusQuery_Payload(REVPayload):

    def __init__(self):
        self.i2cChannel = REVBytes(1)


class I2CConfigureChannel_Payload(REVPayload):

    def __init__(self):
        self.i2cChannel = REVBytes(1)
        self.speedCode = REVBytes(1)


class PhoneChargeControl_Payload(REVPayload):

    def __init__(self):
        self.enable = REVBytes(1)


class PhoneChargeQuery_Payload(REVPayload):

    def __init__(self):
        pass


class InjectDataLogHint_Payload(REVPayload):

    def __init__(self):
        self.length = REVBytes(1)
        self.hintText = REVBytes(PAYLOAD_MAX_SIZE - 7)


class I2CConfigureQuery_Payload(REVPayload):

    def __init__(self):
        self.i2cChannel = REVBytes(1)


class ReadVersionString_Payload(REVPayload):

    def __init__(self):
        pass


class GetBulkPIDData_Payload(REVPayload):

    def __init__(self):
        self.motorChannel = REVBytes(1)


class I2CBlockReadConfig_Payload(REVPayload):

    def __init__(self):
        self.channel = REVBytes(1)
        self.address = REVBytes(1)
        self.startRegister = REVBytes(1)
        self.numberOfBytes = REVBytes(1)
        self.readInterval_ms = REVBytes(1)


class I2CBlockReadQuery_Payload(REVPayload):

    def __init__(self):
        self.channel = REVBytes(1)


class I2CWriteReadMultipleBytes_Payload(REVPayload):

    def __init__(self):
        self.channel = REVBytes(1)
        self.address = REVBytes(1)
        self.startRegister = REVBytes(1)
        self.numberOfBytes = REVBytes(1)


class IMUBlockReadConfig_Payload(REVPayload):

    def __init__(self):
        self.startRegister = REVBytes(1)
        self.numberOfBytes = REVBytes(1)
        self.readInterval_ms = REVBytes(1)


class IMUBlockReadQuery_Payload(REVPayload):

    def __init__(self):
        self.channel = REVBytes(1)


class GetBulkMotorData_Payload(REVPayload):

    def __init__(self):
        pass


class GetBulkADCData_Payload(REVPayload):

    def __init__(self):
        pass


class GetBulkI2CData_Payload(REVPayload):

    def __init__(self):
        pass


class GetBulkServoData_Payload(REVPayload):

    def __init__(self):
        pass


class GetModuleStatus_RSP_Payload(REVPayload):

    def __init__(self):
        self.statusWord = REVBytes(1)
        self.motorAlerts = REVBytes(1)


class QueryInterface_RSP_Payload(REVPayload):

    def __init__(self):
        self.packetID = REVBytes(2)
        self.numValues = REVBytes(2)


class GetModuleLEDColor_RSP_Payload(REVPayload):

    def __init__(self):
        self.redPower = REVBytes(1)
        self.greenPower = REVBytes(1)
        self.bluePower = REVBytes(1)


class GetModuleLEDPattern_RSP_Payload(REVPayload):

    def __init__(self):
        self.rgbtStep0 = REVBytes(4)
        self.rgbtStep1 = REVBytes(4)
        self.rgbtStep2 = REVBytes(4)
        self.rgbtStep3 = REVBytes(4)
        self.rgbtStep4 = REVBytes(4)
        self.rgbtStep5 = REVBytes(4)
        self.rgbtStep6 = REVBytes(4)
        self.rgbtStep7 = REVBytes(4)
        self.rgbtStep8 = REVBytes(4)
        self.rgbtStep9 = REVBytes(4)
        self.rgbtStep10 = REVBytes(4)
        self.rgbtStep11 = REVBytes(4)
        self.rgbtStep12 = REVBytes(4)
        self.rgbtStep13 = REVBytes(4)
        self.rgbtStep14 = REVBytes(4)
        self.rgbtStep15 = REVBytes(4)


class Discovery_RSP_Payload(REVPayload):

    def __init__(self):
        self.parent = REVBytes(1)


class TunnelReadDebugPort_RSP_Payload(REVPayload):

    def __init__(self):
        self.numBytes = REVBytes(1)
        self.bytesRead = REVBytes(PAYLOAD_MAX_SIZE - 7)


class GetBulkInputData_RSP_Payload(REVPayload):

    def __init__(self):
        self.digitalInputs = REVBytes(1)
        self.motor0Encoder = REVBytes(4)
        self.motor1Encoder = REVBytes(4)
        self.motor2Encoder = REVBytes(4)
        self.motor3Encoder = REVBytes(4)
        self.motorStatus = REVBytes(1)
        self.motor0Velocity = REVBytes(2)
        self.motor1Velocity = REVBytes(2)
        self.motor2Velocity = REVBytes(2)
        self.motor3Velocity = REVBytes(2)
        self.motor0mode = REVBytes(1)
        self.motor1mode = REVBytes(1)
        self.motor2mode = REVBytes(1)
        self.motor3mode = REVBytes(1)
        self.analogInput0 = REVBytes(2)
        self.analogInput1 = REVBytes(2)
        self.analogInput2 = REVBytes(2)
        self.analogInput3 = REVBytes(2)
        self.gpioCurrent_mA = REVBytes(2)
        self.i2cCurrent_mA = REVBytes(2)
        self.servoCurrent_mA = REVBytes(2)
        self.batteryCurrent_mA = REVBytes(2)
        self.motor0current_mA = REVBytes(2)
        self.motor1current_mA = REVBytes(2)
        self.motor2current_mA = REVBytes(2)
        self.motor3current_mA = REVBytes(2)
        self.mon5v_mV = REVBytes(2)
        self.batteryVoltage_mV = REVBytes(2)
        self.servo0cmd = REVBytes(2)
        self.servo1cmd = REVBytes(2)
        self.servo2cmd = REVBytes(2)
        self.servo3cmd = REVBytes(2)
        self.servo4cmd = REVBytes(2)
        self.servo5cmd = REVBytes(2)
        self.servo0framePeriod_us = REVBytes(2)
        self.servo1framePeriod_us = REVBytes(2)
        self.servo2framePeriod_us = REVBytes(2)
        self.servo3framePeriod_us = REVBytes(2)
        self.servo4framePeriod_us = REVBytes(2)
        self.servo5framePeriod_us = REVBytes(2)
        self.i2c0data = REVBytes(10)
        self.i2c1data = REVBytes(10)
        self.i2c2data = REVBytes(10)
        self.i2c3data = REVBytes(10)
        self.imuBlock = REVBytes(10)
        self.i2c0Status = REVBytes(1)
        self.i2c1Status = REVBytes(1)
        self.i2c2Status = REVBytes(1)
        self.i2c3Status = REVBytes(1)
        self.imuStatus = REVBytes(1)
        self.mototonicTime = REVBytes(4)


class GetDIODirection_RSP_Payload(REVPayload):

    def __init__(self):
        self.directionOutput = REVBytes(1)


class GetSingleDIOInput_RSP_Payload(REVPayload):

    def __init__(self):
        self.inputValue = REVBytes(1)


class GetAllDIOInputs_RSP_Payload(REVPayload):

    def __init__(self):
        self.inputValues = REVBytes(1)


class GetADC_RSP_Payload(REVPayload):

    def __init__(self):
        self.adcValue = REVBytes(2)


class GetMotorChannelMode_RSP_Payload(REVPayload):

    def __init__(self):
        self.motorChannelMode = REVBytes(1)
        self.floatAtZero = REVBytes(1)


class GetMotorChannelEnable_RSP_Payload(REVPayload):

    def __init__(self):
        self.enabled = REVBytes(1)


class GetMotorChannelCurrentAlertLevel_RSP_Payload(REVPayload):

    def __init__(self):
        self.currentLimit = REVBytes(2)


class GetMotorConstantPower_RSP_Payload(REVPayload):

    def __init__(self):
        self.powerLevel = REVBytes(2)


class GetMotorTargetVelocity_RSP_Payload(REVPayload):

    def __init__(self):
        self.velocity = REVBytes(2)


class GetMotorTargetPosition_RSP_Payload(REVPayload):

    def __init__(self):
        self.targetPosition = REVBytes(4)
        self.atTargetTolerance = REVBytes(2)


class GetMotorAtTarget_RSP_Payload(REVPayload):

    def __init__(self):
        self.atTarget = REVBytes(1)


class GetMotorEncoderPosition_RSP_Payload(REVPayload):

    def __init__(self):
        self.currentPosition = REVBytes(4)


class GetMotorPIDCoefficients_RSP_Payload(REVPayload):

    def __init__(self):
        self.p = REVBytes(4)
        self.i = REVBytes(4)
        self.d = REVBytes(4)


class GetPWMConfiguration_RSP_Payload(REVPayload):

    def __init__(self):
        self.framePeriod = REVBytes(2)


class GetPWNPulseWidth_RSP_Payload(REVPayload):

    def __init__(self):
        self.pulseWidth = REVBytes(1)


class GetPWMEnable_RSP_Payload(REVPayload):

    def __init__(self):
        self.enabled = REVBytes(1)


class GetServoConfiguration_RSP_Payload(REVPayload):

    def __init__(self):
        self.framePeriod = REVBytes(2)


class GetServoPulseWidth_RSP_Payload(REVPayload):

    def __init__(self):
        self.pulseWidth = REVBytes(2)


class GetServoEnable_RSP_Payload(REVPayload):

    def __init__(self):
        self.enabled = REVBytes(1)


class I2CWriteStatusQuery_RSP_Payload(REVPayload):

    def __init__(self):
        self.i2cStatus = REVBytes(1)
        self.numBytes = REVBytes(1)


class I2CReadStatusQuery_RSP_Payload(REVPayload):

    def __init__(self):
        self.i2cStatus = REVBytes(1)
        self.byteRead = REVBytes(1)
        self.payloadBytes = REVBytes(PAYLOAD_MAX_SIZE - 7)


class PhoneChargeQuery_RSP_Payload(REVPayload):

    def __init__(self):
        self.enable = REVBytes(1)


class I2CConfigureQuery_RSP_Payload(REVPayload):

    def __init__(self):
        self.speedCode = REVBytes(1)


class ReadVersionString_RSP_Payload(REVPayload):

    def __init__(self):
        self.length = REVBytes(1)
        self.versionString = REVBytes(40)


class GetBulkPIDData_RSP_Payload(REVPayload):

    def __init__(self):
        self.motorCurPterm = REVBytes(4)
        self.motorCurIterm = REVBytes(4)
        self.motorCurDterm = REVBytes(4)
        self.motorCurOutput = REVBytes(4)
        self.motorCurCmd = REVBytes(4)
        self.motorCurError = REVBytes(4)
        self.motorVelPterm = REVBytes(4)
        self.motorVelIterm = REVBytes(4)
        self.motorVelDterm = REVBytes(4)
        self.motorVelOutput = REVBytes(4)
        self.motorVelCmd = REVBytes(4)
        self.motorVelError = REVBytes(4)
        self.motorPosPterm = REVBytes(4)
        self.motorPosIterm = REVBytes(4)
        self.motorPosDterm = REVBytes(4)
        self.motorPosOutput = REVBytes(4)
        self.motorPosCmd = REVBytes(4)
        self.motorPosError = REVBytes(4)
        self.monotonicTime = REVBytes(4)


class I2CBlockReadQuery_RSP_Payload(REVPayload):

    def __init__(self):
        self.address = REVBytes(1)
        self.startRegister = REVBytes(1)
        self.numberOfBytes = REVBytes(1)
        self.readInterval_ms = REVBytes(1)


class IMUBlockReadQuery_RSP_Payload(REVPayload):

    def __init__(self):
        self.startRegister = REVBytes(1)
        self.numberOfBytes = REVBytes(1)
        self.readInterval_ms = REVBytes(1)


class GetBulkMotorData_RSP_Payload(REVPayload):

    def __init__(self):
        self.motor0Encoder = REVBytes(4)
        self.motor1Encoder = REVBytes(4)
        self.motor2Encoder = REVBytes(4)
        self.motor3Encoder = REVBytes(4)
        self.motorStatus = REVBytes(1)
        self.motor0Velocity = REVBytes(2)
        self.motor1Velocity = REVBytes(2)
        self.motor2Velocity = REVBytes(2)
        self.motor3Velocity = REVBytes(2)
        self.motor0mode = REVBytes(1)
        self.motor1mode = REVBytes(1)
        self.motor2mode = REVBytes(1)
        self.motor3mode = REVBytes(1)
        self.monotonicTime = REVBytes(4)


class GetBulkADCData_RSP_Payload(REVPayload):

    def __init__(self):
        self.analogInput0 = REVBytes(2)
        self.analogInput1 = REVBytes(2)
        self.analogInput2 = REVBytes(2)
        self.analogInput3 = REVBytes(2)
        self.gpioCurrent_mA = REVBytes(2)
        self.i2cCurrent_mA = REVBytes(2)
        self.servoCurrent_mA = REVBytes(2)
        self.batteryCurrent_mA = REVBytes(2)
        self.motor0current_mA = REVBytes(2)
        self.motor1current_mA = REVBytes(2)
        self.motor2current_mA = REVBytes(2)
        self.motor3current_mA = REVBytes(2)
        self.mon5v_mV = REVBytes(2)
        self.batteryVoltage_mV = REVBytes(2)
        self.monotonicTime = REVBytes(4)


class GetBulkI2CData_RSP_Payload(REVPayload):

    def __init__(self):
        self.i2c0data = REVBytes(10)
        self.i2c1data = REVBytes(10)
        self.i2c2data = REVBytes(10)
        self.i2c3data = REVBytes(10)
        self.imuBlock = REVBytes(10)
        self.i2c0Status = REVBytes(1)
        self.i2c1Status = REVBytes(1)
        self.i2c2Status = REVBytes(1)
        self.i2c3Status = REVBytes(1)
        self.imuStatus = REVBytes(1)
        self.monotonicTime = REVBytes(4)


class GetBulkServoData_RSP_Payload(REVPayload):

    def __init__(self):
        self.servo0cmd = REVBytes(2)
        self.servo1cmd = REVBytes(2)
        self.servo2cmd = REVBytes(2)
        self.servo3cmd = REVBytes(2)
        self.servo4cmd = REVBytes(2)
        self.servo5cmd = REVBytes(2)
        self.servo0framePeriod_us = REVBytes(2)
        self.servo1framePeriod_us = REVBytes(2)
        self.servo2framePeriod_us = REVBytes(2)
        self.servo3framePeriod_us = REVBytes(2)
        self.servo4framePeriod_us = REVBytes(2)
        self.servo5framePeriod_us = REVBytes(2)
        self.monotonicTime = REVBytes(4)


class MsgNum:
    ACK = 32513
    NACK = 32514
    GetModuleStatus = 32515
    KeepAlive = 32516
    FailSafe = 32517
    SetNewModuleAddress = 32518
    QueryInterface = 32519
    StartProgramDownload = 32520
    ProgramDownloadChunk = 32521
    SetModuleLEDColor = 32522
    GetModuleLEDColor = 32523
    SetModuleLEDPattern = 32524
    GetModuleLEDPattern = 32525
    DebugLogLevel = 32526
    Discovery = 32527
    DekaInterfacePrefix = 4096
    GetBulkInputData = DekaInterfacePrefix + 0
    SetSingleDIOOutput = DekaInterfacePrefix + 1
    SetAllDIOOutputs = DekaInterfacePrefix + 2
    SetDIODirection = DekaInterfacePrefix + 3
    GetDIODirection = DekaInterfacePrefix + 4
    GetSingleDIOInput = DekaInterfacePrefix + 5
    GetAllDIOInputs = DekaInterfacePrefix + 6
    GetADC = DekaInterfacePrefix + 7
    SetMotorChannelMode = DekaInterfacePrefix + 8
    GetMotorChannelMode = DekaInterfacePrefix + 9
    SetMotorChannelEnable = DekaInterfacePrefix + 10
    GetMotorChannelEnable = DekaInterfacePrefix + 11
    SetMotorChannelCurrentAlertLevel = DekaInterfacePrefix + 12
    GetMotorChannelCurrentAlertLevel = DekaInterfacePrefix + 13
    ResetMotorEncoder = DekaInterfacePrefix + 14
    SetMotorConstantPower = DekaInterfacePrefix + 15
    GetMotorConstantPower = DekaInterfacePrefix + 16
    SetMotorTargetVelocity = DekaInterfacePrefix + 17
    GetMotorTargetVelocity = DekaInterfacePrefix + 18
    SetMotorTargetPosition = DekaInterfacePrefix + 19
    GetMotorTargetPosition = DekaInterfacePrefix + 20
    GetMotorAtTarget = DekaInterfacePrefix + 21
    GetMotorEncoderPosition = DekaInterfacePrefix + 22
    SetMotorPIDCoefficients = DekaInterfacePrefix + 23
    GetMotorPIDCoefficients = DekaInterfacePrefix + 24
    SetPWMConfiguration = DekaInterfacePrefix + 25
    GetPWMConfiguration = DekaInterfacePrefix + 26
    SetPWMPulseWidth = DekaInterfacePrefix + 27
    GetPWNPulseWidth = DekaInterfacePrefix + 28
    SetPWMEnable = DekaInterfacePrefix + 29
    GetPWMEnable = DekaInterfacePrefix + 30
    SetServoConfiguration = DekaInterfacePrefix + 31
    GetServoConfiguration = DekaInterfacePrefix + 32
    SetServoPulseWidth = DekaInterfacePrefix + 33
    GetServoPulseWidth = DekaInterfacePrefix + 34
    SetServoEnable = DekaInterfacePrefix + 35
    GetServoEnable = DekaInterfacePrefix + 36
    I2CWriteSingleByte = DekaInterfacePrefix + 37
    I2CWriteMultipleBytes = DekaInterfacePrefix + 38
    I2CReadSingleByte = DekaInterfacePrefix + 39
    I2CReadMultipleBytes = DekaInterfacePrefix + 40
    I2CReadStatusQuery = DekaInterfacePrefix + 41
    I2CWriteStatusQuery = DekaInterfacePrefix + 42
    I2CConfigureChannel = DekaInterfacePrefix + 43
    PhoneChargeControl = DekaInterfacePrefix + 44
    PhoneChargeQuery = DekaInterfacePrefix + 45
    InjectDataLogHint = DekaInterfacePrefix + 46
    I2CConfigureQuery = DekaInterfacePrefix + 47
    ReadVersionString = DekaInterfacePrefix + 48
    GetBulkPIDData = DekaInterfacePrefix + 49
    I2CBlockReadConfig = DekaInterfacePrefix + 50
    I2CBlockReadQuery = DekaInterfacePrefix + 51
    I2CWriteReadMultipleBytes = DekaInterfacePrefix + 52
    IMUBlockReadConfig = DekaInterfacePrefix + 53
    IMUBlockReadQuery = DekaInterfacePrefix + 54
    GetBulkMotorData = DekaInterfacePrefix + 55
    GetBulkADCData = DekaInterfacePrefix + 56
    GetBulkI2CData = DekaInterfacePrefix + 57
    GetBulkServoData = DekaInterfacePrefix + 64


RESPONSE_BIT = 32768

class RespNum:
    GetModuleStatus_RSP = RESPONSE_BIT | MsgNum.GetModuleStatus
    QueryInterface_RSP = RESPONSE_BIT | MsgNum.QueryInterface
    GetModuleLEDColor_RSP = RESPONSE_BIT | MsgNum.GetModuleLEDColor
    GetModuleLEDPattern_RSP = RESPONSE_BIT | MsgNum.GetModuleLEDPattern
    Discovery_RSP = RESPONSE_BIT | MsgNum.Discovery
    GetBulkInputData_RSP = RESPONSE_BIT | MsgNum.GetBulkInputData
    GetDIODirection_RSP = RESPONSE_BIT | MsgNum.GetDIODirection
    GetSingleDIOInput_RSP = RESPONSE_BIT | MsgNum.GetSingleDIOInput
    GetAllDIOInputs_RSP = RESPONSE_BIT | MsgNum.GetAllDIOInputs
    GetADC_RSP = RESPONSE_BIT | MsgNum.GetADC
    GetMotorChannelMode_RSP = RESPONSE_BIT | MsgNum.GetMotorChannelMode
    GetMotorChannelEnable_RSP = RESPONSE_BIT | MsgNum.GetMotorChannelEnable
    GetMotorChannelCurrentAlertLevel_RSP = RESPONSE_BIT | MsgNum.GetMotorChannelCurrentAlertLevel
    GetMotorConstantPower_RSP = RESPONSE_BIT | MsgNum.GetMotorConstantPower
    GetMotorTargetVelocity_RSP = RESPONSE_BIT | MsgNum.GetMotorTargetVelocity
    GetMotorTargetPosition_RSP = RESPONSE_BIT | MsgNum.GetMotorTargetPosition
    GetMotorAtTarget_RSP = RESPONSE_BIT | MsgNum.GetMotorAtTarget
    GetMotorEncoderPosition_RSP = RESPONSE_BIT | MsgNum.GetMotorEncoderPosition
    GetMotorPIDCoefficients_RSP = RESPONSE_BIT | MsgNum.GetMotorPIDCoefficients
    GetPWMConfiguration_RSP = RESPONSE_BIT | MsgNum.GetPWMConfiguration
    GetPWNPulseWidth_RSP = RESPONSE_BIT | MsgNum.GetPWNPulseWidth
    GetPWMEnable_RSP = RESPONSE_BIT | MsgNum.GetPWMEnable
    GetServoConfiguration_RSP = RESPONSE_BIT | MsgNum.GetServoConfiguration
    GetServoPulseWidth_RSP = RESPONSE_BIT | MsgNum.GetServoPulseWidth
    GetServoEnable_RSP = RESPONSE_BIT | MsgNum.GetServoEnable
    I2CReadStatusQuery_RSP = RESPONSE_BIT | MsgNum.I2CReadStatusQuery
    I2CWriteStatusQuery_RSP = RESPONSE_BIT | MsgNum.I2CWriteStatusQuery
    PhoneChargeQuery_RSP = RESPONSE_BIT | MsgNum.PhoneChargeQuery
    I2CConfigureQuery_RSP = RESPONSE_BIT | MsgNum.I2CConfigureQuery
    ReadVersionString_RSP = RESPONSE_BIT | MsgNum.ReadVersionString
    GetBulkPIDData_RSP = RESPONSE_BIT | MsgNum.GetBulkPIDData
    I2CBlockReadQuery_RSP = RESPONSE_BIT | MsgNum.I2CBlockReadQuery
    IMUBlockReadQuery_RSP = RESPONSE_BIT | MsgNum.IMUBlockReadQuery
    GetBulkMotorData_RSP = RESPONSE_BIT | MsgNum.GetBulkMotorData
    GetBulkADCData_RSP = RESPONSE_BIT | MsgNum.GetBulkADCData
    GetBulkI2CData_RSP = RESPONSE_BIT | MsgNum.GetBulkI2CData
    GetBulkServoData_RSP = RESPONSE_BIT | MsgNum.GetBulkServoData


class ACK(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.ACK), ACK_Payload())


class NACK(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.NACK), NACK_Payload())


class GetModuleStatus(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetModuleStatus), GetModuleStatus_Payload())


class KeepAlive(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.KeepAlive), KeepAlive_Payload())


class FailSafe(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.FailSafe), FailSafe_Payload())


class SetNewModuleAddress(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetNewModuleAddress), SetNewModuleAddress_Payload())


class QueryInterface(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.QueryInterface), QueryInterface_Payload())


class StartProgramDownload(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.StartProgramDownload), StartProgramDownload_Payload())


class ProgramDownloadChunk(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.ProgramDownloadChunk), ProgramDownloadChunk_Payload())


class SetModuleLEDColor(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetModuleLEDColor), SetModuleLEDColor_Payload())


class GetModuleLEDColor(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetModuleLEDColor), GetModuleLEDColor_Payload())


class SetModuleLEDPattern(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetModuleLEDPattern), SetModuleLEDPattern_Payload())


class GetModuleLEDPattern(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetModuleLEDPattern), GetModuleLEDPattern_Payload())


class DebugLogLevel(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.DebugLogLevel), DebugLogLevel_Payload())


class Discovery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.Discovery), Discovery_Payload())


class GetBulkInputData(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetBulkInputData), GetBulkInputData_Payload())


class SetSingleDIOOutput(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetSingleDIOOutput), SetSingleDIOOutput_Payload())


class SetAllDIOOutputs(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetAllDIOOutputs), SetAllDIOOutputs_Payload())


class SetDIODirection(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetDIODirection), SetDIODirection_Payload())


class GetDIODirection(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetDIODirection), GetDIODirection_Payload())


class GetSingleDIOInput(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetSingleDIOInput), GetSingleDIOInput_Payload())


class GetAllDIOInputs(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetAllDIOInputs), GetAllDIOInputs_Payload())


class GetADC(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetADC), GetADC_Payload())


class SetMotorChannelMode(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorChannelMode), SetMotorChannelMode_Payload())


class GetMotorChannelMode(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorChannelMode), GetMotorChannelMode_Payload())


class SetMotorChannelEnable(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorChannelEnable), SetMotorChannelEnable_Payload())


class GetMotorChannelEnable(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorChannelEnable), GetMotorChannelEnable_Payload())


class SetMotorChannelCurrentAlertLevel(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorChannelCurrentAlertLevel), SetMotorChannelCurrentAlertLevel_Payload())


class GetMotorChannelCurrentAlertLevel(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorChannelCurrentAlertLevel), GetMotorChannelCurrentAlertLevel_Payload())


class ResetMotorEncoder(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.ResetMotorEncoder), ResetMotorEncoder_Payload())


class SetMotorConstantPower(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorConstantPower), SetMotorConstantPower_Payload())


class GetMotorConstantPower(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorConstantPower), GetMotorConstantPower_Payload())


class SetMotorTargetVelocity(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorTargetVelocity), SetMotorTargetVelocity_Payload())


class GetMotorTargetVelocity(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorTargetVelocity), GetMotorTargetVelocity_Payload())


class SetMotorTargetPosition(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorTargetPosition), SetMotorTargetPosition_Payload())


class GetMotorTargetPosition(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorTargetPosition), GetMotorTargetPosition_Payload())


class GetMotorAtTarget(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorAtTarget), GetMotorAtTarget_Payload())


class GetMotorEncoderPosition(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorEncoderPosition), GetMotorEncoderPosition_Payload())


class SetMotorPIDCoefficients(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetMotorPIDCoefficients), SetMotorPIDCoefficients_Payload())


class GetMotorPIDCoefficients(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetMotorPIDCoefficients), GetMotorPIDCoefficients_Payload())


class SetPWMConfiguration(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetPWMConfiguration), SetPWMConfiguration_Payload())


class GetPWMConfiguration(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetPWMConfiguration), GetPWMConfiguration_Payload())


class SetPWMPulseWidth(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetPWMPulseWidth), SetPWMPulseWidth_Payload())


class GetPWNPulseWidth(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetPWNPulseWidth), GetPWNPulseWidth_Payload())


class SetPWMEnable(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetPWMEnable), SetPWMEnable_Payload())


class GetPWMEnable(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetPWMEnable), GetPWMEnable_Payload())


class SetServoConfiguration(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetServoConfiguration), SetServoConfiguration_Payload())


class GetServoConfiguration(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetServoConfiguration), GetServoConfiguration_Payload())


class SetServoPulseWidth(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetServoPulseWidth), SetServoPulseWidth_Payload())


class GetServoPulseWidth(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetServoPulseWidth), GetServoPulseWidth_Payload())


class SetServoEnable(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.SetServoEnable), SetServoEnable_Payload())


class GetServoEnable(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetServoEnable), GetServoEnable_Payload())


class I2CWriteSingleByte(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CWriteSingleByte), I2CWriteSingleByte_Payload())


class I2CWriteMultipleBytes(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CWriteMultipleBytes), I2CWriteMultipleBytes_Payload())


class I2CReadSingleByte(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CReadSingleByte), I2CReadSingleByte_Payload())


class I2CReadMultipleBytes(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CReadMultipleBytes), I2CReadMultipleBytes_Payload())


class I2CReadStatusQuery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CReadStatusQuery), I2CReadStatusQuery_Payload())


class I2CWriteStatusQuery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CWriteStatusQuery), I2CWriteStatusQuery_Payload())


class I2CConfigureChannel(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CConfigureChannel), I2CConfigureChannel_Payload())


class PhoneChargeControl(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.PhoneChargeControl), PhoneChargeControl_Payload())


class PhoneChargeQuery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.PhoneChargeQuery), PhoneChargeQuery_Payload())


class InjectDataLogHint(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.InjectDataLogHint), InjectDataLogHint_Payload())


class I2CConfigureQuery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CConfigureQuery), I2CConfigureQuery_Payload())


class ReadVersionString(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.ReadVersionString), ReadVersionString_Payload())


class GetBulkPIDData(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetBulkPIDData), GetBulkPIDData_Payload())


class I2CBlockReadConfig(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CBlockReadConfig), I2CBlockReadConfig_Payload())


class I2CBlockReadQuery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CBlockReadQuery), I2CBlockReadQuery_Payload())


class I2CWriteReadMultipleBytes(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.I2CWriteReadMultipleBytes), I2CWriteReadMultipleBytes_Payload())


class IMUBlockReadConfig(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.IMUBlockReadConfig), IMUBlockReadConfig_Payload())


class IMUBlockReadQuery(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.IMUBlockReadQuery), IMUBlockReadQuery_Payload())


class GetBulkMotorData(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetBulkMotorData), GetBulkMotorData_Payload())


class GetBulkADCData(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetBulkADCData), GetBulkADCData_Payload())


class GetBulkI2CData(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetBulkI2CData), GetBulkI2CData_Payload())


class GetBulkServoData(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=MsgNum.GetBulkServoData), GetBulkServoData_Payload())


class GetModuleStatus_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetModuleStatus_RSP), GetModuleStatus_RSP_Payload())


class QueryInterface_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.QueryInterface_RSP), QueryInterface_RSP_Payload())


class GetModuleLEDColor_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetModuleLEDColor_RSP), GetModuleLEDColor_RSP_Payload())


class GetModuleLEDPattern_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetModuleLEDPattern_RSP), GetModuleLEDPattern_RSP_Payload())


class Discovery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.Discovery_RSP), Discovery_RSP_Payload())


class GetBulkInputData_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetBulkInputData_RSP), GetBulkInputData_RSP_Payload())


class GetDIODirection_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetDIODirection_RSP), GetDIODirection_RSP_Payload())


class GetSingleDIOInput_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetSingleDIOInput_RSP), GetSingleDIOInput_RSP_Payload())


class GetAllDIOInputs_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetAllDIOInputs_RSP), GetAllDIOInputs_RSP_Payload())


class GetADC_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetADC_RSP), GetADC_RSP_Payload())


class GetMotorChannelMode_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorChannelMode_RSP), GetMotorChannelMode_RSP_Payload())


class GetMotorChannelEnable_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorChannelEnable_RSP), GetMotorChannelEnable_RSP_Payload())


class GetMotorChannelCurrentAlertLevel_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorChannelCurrentAlertLevel_RSP), GetMotorChannelCurrentAlertLevel_RSP_Payload())


class GetMotorConstantPower_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorConstantPower_RSP), GetMotorConstantPower_RSP_Payload())


class GetMotorTargetVelocity_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorTargetVelocity_RSP), GetMotorTargetVelocity_RSP_Payload())


class GetMotorTargetPosition_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorTargetPosition_RSP), GetMotorTargetPosition_RSP_Payload())


class GetMotorAtTarget_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorAtTarget_RSP), GetMotorAtTarget_RSP_Payload())


class GetMotorEncoderPosition_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorEncoderPosition_RSP), GetMotorEncoderPosition_RSP_Payload())


class GetMotorPIDCoefficients_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetMotorPIDCoefficients_RSP), GetMotorPIDCoefficients_RSP_Payload())


class GetPWMConfiguration_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetPWMConfiguration_RSP), GetPWMConfiguration_RSP_Payload())


class GetPWNPulseWidth_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetPWNPulseWidth_RSP), GetPWNPulseWidth_RSP_Payload())


class GetPWMEnable_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetPWMEnable_RSP), GetPWMEnable_RSP_Payload())


class GetServoConfiguration_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetServoConfiguration_RSP), GetServoConfiguration_RSP_Payload())


class GetServoPulseWidth_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetServoPulseWidth_RSP), GetServoPulseWidth_RSP_Payload())


class GetServoEnable_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetServoEnable_RSP), GetServoEnable_RSP_Payload())


class I2CWriteStatusQuery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.I2CWriteStatusQuery_RSP), I2CWriteStatusQuery_RSP_Payload())


class I2CReadStatusQuery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.I2CReadStatusQuery_RSP), I2CReadStatusQuery_RSP_Payload())


class PhoneChargeQuery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.PhoneChargeQuery_RSP), PhoneChargeQuery_RSP_Payload())


class I2CConfigureQuery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.I2CConfigureQuery_RSP), I2CConfigureQuery_RSP_Payload())


class ReadVersionString_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.ReadVersionString_RSP), ReadVersionString_RSP_Payload())


class GetBulkPIDData_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetBulkPIDData_RSP), GetBulkPIDData_RSP_Payload())


class I2CBlockReadQuery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.I2CBlockReadQuery_RSP), I2CBlockReadQuery_RSP_Payload())


class IMUBlockReadQuery_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.IMUBlockReadQuery_RSP), IMUBlockReadQuery_RSP_Payload())


class GetBulkMotorData_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetBulkMotorData_RSP), GetBulkMotorData_RSP_Payload())


class GetBulkADCData_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetBulkADCData_RSP), GetBulkADCData_RSP_Payload())


class GetBulkI2CData_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetBulkI2CData_RSP), GetBulkI2CData_RSP_Payload())


class GetBulkServoData_RSP(REVPacket):

    def __init__(self):
        REVPacket.__init__(self, REVHeader(Cmd=RespNum.GetBulkServoData_RSP), GetBulkServoData_RSP_Payload())


printDict = {(MsgNum.ACK): {'Name': 'ACK', 'Packet': ACK, 
                  'Response': None}, 
   (MsgNum.NACK): {'Name': 'NACK', 'Packet': NACK, 
                   'Response': None}, 
   (MsgNum.GetModuleStatus): {'Name': 'GetModuleStatus', 'Packet': GetModuleStatus, 
                              'Response': (RespNum.GetModuleStatus_RSP)}, 
   (MsgNum.KeepAlive): {'Name': 'KeepAlive', 'Packet': KeepAlive, 
                        'Response': (MsgNum.ACK)}, 
   (MsgNum.FailSafe): {'Name': 'FailSafe', 'Packet': FailSafe, 
                       'Response': (MsgNum.ACK)}, 
   (MsgNum.SetNewModuleAddress): {'Name': 'SetNewModuleAddress', 'Packet': SetNewModuleAddress, 
                                  'Response': (MsgNum.ACK)}, 
   (MsgNum.QueryInterface): {'Name': 'QueryInterface', 'Packet': QueryInterface, 
                             'Response': (RespNum.QueryInterface_RSP)}, 
   (MsgNum.StartProgramDownload): {'Name': 'StartProgramDownload', 'Packet': StartProgramDownload, 
                                   'Response': (MsgNum.ACK)}, 
   (MsgNum.ProgramDownloadChunk): {'Name': 'ProgramDownloadChunk', 'Packet': ProgramDownloadChunk, 
                                   'Response': (MsgNum.ACK)}, 
   (MsgNum.SetModuleLEDColor): {'Name': 'SetModuleLEDColor', 'Packet': SetModuleLEDColor, 
                                'Response': (MsgNum.ACK)}, 
   (MsgNum.GetModuleLEDColor): {'Name': 'GetModuleLEDColor', 'Packet': GetModuleLEDColor, 
                                'Response': (RespNum.GetModuleLEDColor_RSP)}, 
   (MsgNum.SetModuleLEDPattern): {'Name': 'SetModuleLEDPattern', 'Packet': SetModuleLEDPattern, 
                                  'Response': (MsgNum.ACK)}, 
   (MsgNum.GetModuleLEDPattern): {'Name': 'GetModuleLEDPattern', 'Packet': GetModuleLEDPattern, 
                                  'Response': (RespNum.GetModuleLEDPattern_RSP)}, 
   (MsgNum.DebugLogLevel): {'Name': 'DebugLogLevel', 'Packet': DebugLogLevel, 
                            'Response': (MsgNum.ACK)}, 
   (MsgNum.Discovery): {'Name': 'Discovery', 'Packet': Discovery, 
                        'Response': (RespNum.Discovery_RSP)}, 
   (MsgNum.GetBulkInputData): {'Name': 'GetBulkInputData', 'Packet': GetBulkInputData, 
                               'Response': (RespNum.GetBulkInputData_RSP)}, 
   (MsgNum.SetSingleDIOOutput): {'Name': 'SetSingleDIOOutput', 'Packet': SetSingleDIOOutput, 
                                 'Response': (MsgNum.ACK)}, 
   (MsgNum.SetAllDIOOutputs): {'Name': 'SetAllDIOOutputs', 'Packet': SetAllDIOOutputs, 
                               'Response': (MsgNum.ACK)}, 
   (MsgNum.SetDIODirection): {'Name': 'SetDIODirection', 'Packet': SetDIODirection, 
                              'Response': (MsgNum.ACK)}, 
   (MsgNum.GetDIODirection): {'Name': 'GetDIODirection', 'Packet': GetDIODirection, 
                              'Response': (RespNum.GetDIODirection_RSP)}, 
   (MsgNum.GetSingleDIOInput): {'Name': 'GetSingleDIOInput', 'Packet': GetSingleDIOInput, 
                                'Response': (RespNum.GetSingleDIOInput_RSP)}, 
   (MsgNum.GetAllDIOInputs): {'Name': 'GetAllDIOInputs', 'Packet': GetAllDIOInputs, 
                              'Response': (RespNum.GetAllDIOInputs_RSP)}, 
   (MsgNum.GetADC): {'Name': 'GetADC', 'Packet': GetADC, 
                     'Response': (RespNum.GetADC_RSP)}, 
   (MsgNum.SetMotorChannelMode): {'Name': 'SetMotorChannelMode', 'Packet': SetMotorChannelMode, 
                                  'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorChannelMode): {'Name': 'GetMotorChannelMode', 'Packet': GetMotorChannelMode, 
                                  'Response': (RespNum.GetMotorChannelMode_RSP)}, 
   (MsgNum.SetMotorChannelEnable): {'Name': 'SetMotorChannelEnable', 'Packet': SetMotorChannelEnable, 
                                    'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorChannelEnable): {'Name': 'GetMotorChannelEnable', 'Packet': GetMotorChannelEnable, 
                                    'Response': (RespNum.GetMotorChannelEnable_RSP)}, 
   (MsgNum.SetMotorChannelCurrentAlertLevel): {'Name': 'SetMotorChannelCurrentAlertLevel', 'Packet': SetMotorChannelCurrentAlertLevel, 
                                               'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorChannelCurrentAlertLevel): {'Name': 'GetMotorChannelCurrentAlertLevel', 'Packet': GetMotorChannelCurrentAlertLevel, 
                                               'Response': (RespNum.GetMotorChannelCurrentAlertLevel_RSP)}, 
   (MsgNum.ResetMotorEncoder): {'Name': 'ResetMotorEncoder', 'Packet': ResetMotorEncoder, 
                                'Response': (MsgNum.ACK)}, 
   (MsgNum.SetMotorConstantPower): {'Name': 'SetMotorConstantPower', 'Packet': SetMotorConstantPower, 
                                    'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorConstantPower): {'Name': 'GetMotorConstantPower', 'Packet': GetMotorConstantPower, 
                                    'Response': (RespNum.GetMotorConstantPower_RSP)}, 
   (MsgNum.SetMotorTargetVelocity): {'Name': 'SetMotorTargetVelocity', 'Packet': SetMotorTargetVelocity, 
                                     'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorTargetVelocity): {'Name': 'GetMotorTargetVelocity', 'Packet': GetMotorTargetVelocity, 
                                     'Response': (RespNum.GetMotorTargetVelocity_RSP)}, 
   (MsgNum.SetMotorTargetPosition): {'Name': 'SetMotorTargetPosition', 'Packet': SetMotorTargetPosition, 
                                     'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorTargetPosition): {'Name': 'GetMotorTargetPosition', 'Packet': GetMotorTargetPosition, 
                                     'Response': (RespNum.GetMotorTargetPosition_RSP)}, 
   (MsgNum.GetMotorAtTarget): {'Name': 'GetMotorAtTarget', 'Packet': GetMotorAtTarget, 
                               'Response': (RespNum.GetMotorAtTarget_RSP)}, 
   (MsgNum.GetMotorEncoderPosition): {'Name': 'GetMotorEncoderPosition', 'Packet': GetMotorEncoderPosition, 
                                      'Response': (RespNum.GetMotorEncoderPosition_RSP)}, 
   (MsgNum.SetMotorPIDCoefficients): {'Name': 'SetMotorPIDCoefficients', 'Packet': SetMotorPIDCoefficients, 
                                      'Response': (MsgNum.ACK)}, 
   (MsgNum.GetMotorPIDCoefficients): {'Name': 'GetMotorPIDCoefficients', 'Packet': GetMotorPIDCoefficients, 
                                      'Response': (RespNum.GetMotorPIDCoefficients_RSP)}, 
   (MsgNum.SetPWMConfiguration): {'Name': 'SetPWMConfiguration', 'Packet': SetPWMConfiguration, 
                                  'Response': (MsgNum.ACK)}, 
   (MsgNum.GetPWMConfiguration): {'Name': 'GetPWMConfiguration', 'Packet': GetPWMConfiguration, 
                                  'Response': (RespNum.GetPWMConfiguration_RSP)}, 
   (MsgNum.SetPWMPulseWidth): {'Name': 'SetPWMPulseWidth', 'Packet': SetPWMPulseWidth, 
                               'Response': (MsgNum.ACK)}, 
   (MsgNum.GetPWNPulseWidth): {'Name': 'GetPWNPulseWidth', 'Packet': GetPWNPulseWidth, 
                               'Response': (RespNum.GetPWNPulseWidth_RSP)}, 
   (MsgNum.SetPWMEnable): {'Name': 'SetPWMEnable', 'Packet': SetPWMEnable, 
                           'Response': (MsgNum.ACK)}, 
   (MsgNum.GetPWMEnable): {'Name': 'GetPWMEnable', 'Packet': GetPWMEnable, 
                           'Response': (RespNum.GetPWMEnable_RSP)}, 
   (MsgNum.SetServoConfiguration): {'Name': 'SetServoConfiguration', 'Packet': SetServoConfiguration, 
                                    'Response': (MsgNum.ACK)}, 
   (MsgNum.GetServoConfiguration): {'Name': 'GetServoConfiguration', 'Packet': GetServoConfiguration, 
                                    'Response': (RespNum.GetServoConfiguration_RSP)}, 
   (MsgNum.SetServoPulseWidth): {'Name': 'SetServoPulseWidth', 'Packet': SetServoPulseWidth, 
                                 'Response': (MsgNum.ACK)}, 
   (MsgNum.GetServoPulseWidth): {'Name': 'GetServoPulseWidth', 'Packet': GetServoPulseWidth, 
                                 'Response': (RespNum.GetServoPulseWidth_RSP)}, 
   (MsgNum.SetServoEnable): {'Name': 'SetServoEnable', 'Packet': SetServoEnable, 
                             'Response': (MsgNum.ACK)}, 
   (MsgNum.GetServoEnable): {'Name': 'GetServoEnable', 'Packet': GetServoEnable, 
                             'Response': (RespNum.GetServoEnable_RSP)}, 
   (MsgNum.I2CWriteSingleByte): {'Name': 'I2CWriteSingleByte', 'Packet': I2CWriteSingleByte, 
                                 'Response': (MsgNum.ACK)}, 
   (MsgNum.I2CWriteMultipleBytes): {'Name': 'I2CWriteMultipleBytes', 'Packet': I2CWriteMultipleBytes, 
                                    'Response': (MsgNum.ACK)}, 
   (MsgNum.I2CWriteStatusQuery): {'Name': 'I2CWriteStatusQuery', 'Packet': I2CWriteStatusQuery, 
                                  'Response': (RespNum.I2CWriteStatusQuery_RSP)}, 
   (MsgNum.I2CReadSingleByte): {'Name': 'I2CReadSingleByte', 'Packet': I2CReadSingleByte, 
                                'Response': (MsgNum.ACK)}, 
   (MsgNum.I2CReadMultipleBytes): {'Name': 'I2CReadMultipleBytes', 'Packet': I2CReadMultipleBytes, 
                                   'Response': (MsgNum.ACK)}, 
   (MsgNum.I2CReadStatusQuery): {'Name': 'I2CReadStatusQuery', 'Packet': I2CReadStatusQuery, 
                                 'Response': (RespNum.I2CReadStatusQuery_RSP)}, 
   (MsgNum.I2CConfigureChannel): {'Name': 'I2CConfigureChannel', 'Packet': I2CConfigureChannel, 
                                  'Response': (MsgNum.ACK)}, 
   (MsgNum.PhoneChargeControl): {'Name': 'PhoneChargeControl', 'Packet': PhoneChargeControl, 
                                 'Response': (MsgNum.ACK)}, 
   (MsgNum.PhoneChargeQuery): {'Name': 'PhoneChargeQuery', 'Packet': PhoneChargeQuery, 
                               'Response': (RespNum.PhoneChargeQuery_RSP)}, 
   (MsgNum.InjectDataLogHint): {'Name': 'InjectDataLogHint', 'Packet': InjectDataLogHint, 
                                'Response': (MsgNum.ACK)}, 
   (MsgNum.I2CConfigureQuery): {'Name': 'I2CConfigureQuery', 'Packet': I2CConfigureQuery, 
                                'Response': (RespNum.I2CConfigureQuery_RSP)}, 
   (MsgNum.ReadVersionString): {'Name': 'ReadVersionString', 'Packet': ReadVersionString, 
                                'Response': (RespNum.ReadVersionString_RSP)}, 
   (MsgNum.GetBulkPIDData): {'Name': 'GetBulkPIDData', 'Packet': GetBulkPIDData, 
                             'Response': (RespNum.GetBulkPIDData_RSP)}, 
   (MsgNum.I2CBlockReadConfig): {'Name': 'I2CBlockReadConfig', 'Packet': I2CBlockReadConfig, 
                                 'Response': (MsgNum.ACK)}, 
   (MsgNum.I2CBlockReadQuery): {'Name': 'I2CBlockReadQuery', 'Packet': I2CBlockReadQuery, 
                                'Response': (RespNum.I2CBlockReadQuery_RSP)}, 
   (MsgNum.I2CWriteReadMultipleBytes): {'Name': 'I2CWriteReadMultipleBytes', 'Packet': I2CWriteReadMultipleBytes, 
                                        'Response': (MsgNum.ACK)}, 
   (MsgNum.IMUBlockReadConfig): {'Name': 'IMUBlockReadConfig', 'Packet': IMUBlockReadConfig, 
                                 'Response': (MsgNum.ACK)}, 
   (MsgNum.IMUBlockReadQuery): {'Name': 'IMUBlockReadQuery', 'Packet': IMUBlockReadQuery, 
                                'Response': (RespNum.IMUBlockReadQuery_RSP)}, 
   (MsgNum.GetBulkMotorData): {'Name': 'GetBulkMotorData', 'Packet': GetBulkMotorData, 
                               'Response': (RespNum.GetBulkMotorData_RSP)}, 
   (MsgNum.GetBulkADCData): {'Name': 'GetBulkADCData', 'Packet': GetBulkADCData, 
                             'Response': (RespNum.GetBulkADCData_RSP)}, 
   (MsgNum.GetBulkI2CData): {'Name': 'GetBulkI2CData', 'Packet': GetBulkI2CData, 
                             'Response': (RespNum.GetBulkI2CData_RSP)}, 
   (MsgNum.GetBulkServoData): {'Name': 'GetBulkServoData', 'Packet': GetBulkServoData, 
                               'Response': (RespNum.GetBulkServoData_RSP)}, 
   (RespNum.GetModuleStatus_RSP): {'Name': 'GetModuleStatus_RSP', 'Packet': GetModuleStatus_RSP, 
                                   'Response': None}, 
   (RespNum.QueryInterface_RSP): {'Name': 'QueryInterface_RSP', 'Packet': QueryInterface_RSP, 
                                  'Response': None}, 
   (RespNum.GetModuleLEDColor_RSP): {'Name': 'GetModuleLEDColor_RSP', 'Packet': GetModuleLEDColor_RSP, 
                                     'Response': None}, 
   (RespNum.GetModuleLEDPattern_RSP): {'Name': 'GetModuleLEDPattern_RSP', 'Packet': GetModuleLEDPattern_RSP, 
                                       'Response': None}, 
   (RespNum.Discovery_RSP): {'Name': 'Discovery_RSP', 'Packet': Discovery_RSP, 
                             'Response': None}, 
   (RespNum.GetBulkInputData_RSP): {'Name': 'GetBulkInputData_RSP', 'Packet': GetBulkInputData_RSP, 
                                    'Response': None}, 
   (RespNum.GetDIODirection_RSP): {'Name': 'GetDIODirection_RSP', 'Packet': GetDIODirection_RSP, 
                                   'Response': None}, 
   (RespNum.GetSingleDIOInput_RSP): {'Name': 'GetSingleDIOInput_RSP', 'Packet': GetSingleDIOInput_RSP, 
                                     'Response': None}, 
   (RespNum.GetAllDIOInputs_RSP): {'Name': 'GetAllDIOInputs_RSP', 'Packet': GetAllDIOInputs_RSP, 
                                   'Response': None}, 
   (RespNum.GetADC_RSP): {'Name': 'GetADC_RSP', 'Packet': GetADC_RSP, 
                          'Response': None}, 
   (RespNum.GetMotorChannelMode_RSP): {'Name': 'GetMotorChannelMode_RSP', 'Packet': GetMotorChannelMode_RSP, 
                                       'Response': None}, 
   (RespNum.GetMotorChannelEnable_RSP): {'Name': 'GetMotorChannelEnable_RSP', 'Packet': GetMotorChannelEnable_RSP, 
                                         'Response': None}, 
   (RespNum.GetMotorChannelCurrentAlertLevel_RSP): {'Name': 'GetMotorChannelCurrentAlertLevel_RSP', 'Packet': GetMotorChannelCurrentAlertLevel_RSP, 
                                                    'Response': None}, 
   (RespNum.GetMotorConstantPower_RSP): {'Name': 'GetMotorConstantPower_RSP', 'Packet': GetMotorConstantPower_RSP, 
                                         'Response': None}, 
   (RespNum.GetMotorTargetVelocity_RSP): {'Name': 'GetMotorTargetVelocity_RSP', 'Packet': GetMotorTargetVelocity_RSP, 
                                          'Response': None}, 
   (RespNum.GetMotorTargetPosition_RSP): {'Name': 'GetMotorTargetPosition_RSP', 'Packet': GetMotorTargetPosition_RSP, 
                                          'Response': None}, 
   (RespNum.GetMotorAtTarget_RSP): {'Name': 'GetMotorAtTarget_RSP', 'Packet': GetMotorAtTarget_RSP, 
                                    'Response': None}, 
   (RespNum.GetMotorEncoderPosition_RSP): {'Name': 'GetMotorEncoderPosition_RSP', 'Packet': GetMotorEncoderPosition_RSP, 
                                           'Response': None}, 
   (RespNum.GetMotorPIDCoefficients_RSP): {'Name': 'GetMotorPIDCoefficients_RSP', 'Packet': GetMotorPIDCoefficients_RSP, 
                                           'Response': None}, 
   (RespNum.GetPWMConfiguration_RSP): {'Name': 'GetPWMConfiguration_RSP', 'Packet': GetPWMConfiguration_RSP, 
                                       'Response': None}, 
   (RespNum.GetPWNPulseWidth_RSP): {'Name': 'GetPWNPulseWidth_RSP', 'Packet': GetPWNPulseWidth_RSP, 
                                    'Response': None}, 
   (RespNum.GetPWMEnable_RSP): {'Name': 'GetPWMEnable_RSP', 'Packet': GetPWMEnable_RSP, 
                                'Response': None}, 
   (RespNum.GetServoConfiguration_RSP): {'Name': 'GetServoConfiguration_RSP', 'Packet': GetServoConfiguration_RSP, 
                                         'Response': None}, 
   (RespNum.GetServoPulseWidth_RSP): {'Name': 'GetServoPulseWidth_RSP', 'Packet': GetServoPulseWidth_RSP, 
                                      'Response': None}, 
   (RespNum.GetServoEnable_RSP): {'Name': 'GetServoEnable_RSP', 'Packet': GetServoEnable_RSP, 
                                  'Response': None}, 
   (RespNum.I2CWriteStatusQuery_RSP): {'Name': 'I2CWriteStatusQuery_RSP', 'Packet': I2CWriteStatusQuery_RSP, 
                                       'Response': None}, 
   (RespNum.I2CReadStatusQuery_RSP): {'Name': 'I2CReadStatusQuery_RSP', 'Packet': I2CReadStatusQuery_RSP, 
                                      'Response': None}, 
   (RespNum.PhoneChargeQuery_RSP): {'Name': 'PhoneChargeQuery_RSP', 'Packet': PhoneChargeQuery_RSP, 
                                    'Response': None}, 
   (RespNum.ReadVersionString_RSP): {'Name': 'ReadVersionString_RSP', 'Packet': ReadVersionString_RSP, 
                                     'Response': None}, 
   (RespNum.GetBulkPIDData_RSP): {'Name': 'GetBulkPIDData_RSP', 'Packet': GetBulkPIDData_RSP, 
                                  'Response': None}, 
   (RespNum.I2CBlockReadQuery_RSP): {'Name': 'I2CBlockReadQuery_RSP', 'Packet': I2CBlockReadQuery_RSP, 
                                     'Response ': None}, 
   (RespNum.IMUBlockReadQuery_RSP): {'Name': 'IMUBlockReadQuery_RSP', 'Packet': IMUBlockReadQuery_RSP, 
                                     'Response ': None}, 
   (RespNum.GetBulkMotorData_RSP): {'Name': 'GetBulkMotorData_RSP', 'Packet': GetBulkMotorData_RSP, 
                                    'Response ': None}, 
   (RespNum.GetBulkADCData_RSP): {'Name': 'GetBulkADCData_RSP', 'Packet': GetBulkADCData_RSP, 
                                  'Response ': None}, 
   (RespNum.GetBulkI2CData_RSP): {'Name': 'GetBulkI2CData_RSP', 'Packet': GetBulkI2CData_RSP, 
                                  'Response ': None}, 
   (RespNum.GetBulkServoData_RSP): {'Name': 'GetBulkServoData_RSP', 'Packet': GetBulkServoData_RSP, 
                                    'Response ': None}}

# okay decompiling REVmessages.pyc
