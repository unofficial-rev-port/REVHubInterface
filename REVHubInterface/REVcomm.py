import tkinter as tk
from tkinter import *
import tkinter.ttk
import multiprocessing as mp, time
from . import REVComPorts, REVmessages as REVMsg
from .REVModule import Module
import binascii, serial, time, queue

class REVcomm:

    def __init__(self):
        self.serialReceive_Thread = False
        self.FunctionReturnTime = 0
        self.msgNum = 1
        self.totalTime = 0
        self.rxQueue = mp.Queue(256)
        self.txQueue = mp.Queue(256)
        self.roundTripAverage = 0
        self.numMsgs = 0
        self.enablePrinting = False
        self.msgSendTime = 0
        self.msgRcvTime = 0
        self.discoveryTimeout = 0.5
        self.averageMsgTime = 0
        self.REVProcessor = serial.Serial(baudrate=460800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

    def listPorts(self):
        REVComPorts.populateSerialPorts()
        return REVComPorts.REVPorts

    def setActivePortBySN(self, sn):
        REVComPorts.populateSerialPorts()
        for port in REVComPorts.serialPorts:
            if port.getSN() == sn:
                setActivePort(port)

    def openActivePort(self):
        numSerialErrors = 2
        while not self.REVProcessor.isOpen():
            self.REVProcessor.port = self.listPorts()[0].getName()
            try:
                self.REVProcessor.open()
            except serial.SerialException as e:
                print('Serial port error: ' + str(e) + ' retrying...')
                numSerialErrors -= 1
                if numSerialErrors == 0:
                    break
                time.sleep(1)

    def closeActivePort(self):
        self.REVProcessor.close()

    def getTime_ms(self):
        return int(round(time.time() * 1000))

    def sendAndReceive(self, PacketToWrite, destination):
        numSerialErrors = 5
        self.WaitForFrameByte1 = 1
        self.WaitForFrameByte2 = 2
        self.WaitForPacketLengthByte1 = 3
        self.WaitForPacketLengthByte2 = 4
        self.WaitForDestByte = 5
        self.WaitForSourceByte = 6
        self.WaitForMsgNumByte = 7
        self.WaitForRefNumByte = 8
        self.WaitForPacketTypeByte = 9
        self.WaitForPayloadBytes = 10
        parseState = 1
        self.parseState = self.WaitForFrameByte1
        incomingPacket = ''
        packetLength = 0
        msgNum = 0
        retry = True
        readingBytesStart = 0
        readingBytesEnd = 0
        discoveryTimeout = 1000
        rcvStarted = False
        startReceiveTime = self.getTime_ms()
        receivedMessageNums = []
        inWaitingQueue = queue.Queue()
        beenInLoop = False
        try:
            retryAttempt = 0
            while retry:
                sendAndReceiveStart = time.time()
                PacketToWrite.header.destination = destination
                if isinstance(PacketToWrite, REVMsg.REVPacket):
                    MaxRetries = 3
                    RetryTimeout_s = 1
                    PacketToWrite.header.msgNum = msgNum
                    msgNum = (msgNum + 1) % 256
                    if msgNum == 0:
                        msgNum = 1
                    printData = PacketToWrite.header.packetType.data >> 8 | PacketToWrite.header.packetType.data % 256 << 8
                    discoveryMode = False
                    if printData == REVMsg.MsgNum.Discovery:
                        discoveryMode = True
                    if self.enablePrinting:
                        print('-->', REVMsg.printDict[printData]['Name'], '::', PacketToWrite.getPacketData())
                    self.REVProcessor.write(binascii.unhexlify(PacketToWrite.getPacketData()))
                    waitTimeStart = time.time()
                    timeout = False
                    while self.REVProcessor.inWaiting() == 0:
                        if time.time() - waitTimeStart > 1:
                            timeout = True
                            retryAttempt += 1
                            if retryAttempt > MaxRetries:
                                retry = False
                            break
                    if timeout:
                        continue
                    if discoveryMode:
                        packet = []
                    if self.REVProcessor.inWaiting() > 0:
                        while self.REVProcessor.inWaiting() > 0:
                            retry = False
                            newByte = binascii.hexlify(self.REVProcessor.read(1)).upper()
                            newByte = str(newByte)
                            newByte = newByte[2:]
                            newByte = newByte[:-1]
                            if parseState == self.WaitForFrameByte1:
                                rcvStarted = True
                                startReceiveTime = time.time()
                                if newByte == '44':
                                    parseState = self.WaitForFrameByte2
                            elif parseState == self.WaitForFrameByte2:
                                if newByte == '44':
                                    None
                                elif newByte == '4B':
                                    parseState = self.WaitForPacketLengthByte1
                                else:
                                    parseState = self.WaitForFrameByte1
                            elif parseState == self.WaitForPacketLengthByte1:
                                incomingPacket = '444B' + newByte
                                lengthBytes = newByte
                                parseState = self.WaitForPacketLengthByte2
                            elif parseState == self.WaitForPacketLengthByte2:
                                incomingPacket += newByte
                                lengthBytes += newByte
                                lengthBytes = int(int(lengthBytes, 16) >> 8 | int(lengthBytes, 16) % 256 << 8)
                                if lengthBytes <= REVMsg.PAYLOAD_MAX_SIZE:
                                    packetLength = lengthBytes
                                    parseState = self.WaitForPayloadBytes
                                elif newByte == '44':
                                    parseState = self.WaitForFrameByte2
                                else:
                                    parseState = self.WaitForFrameByte1
                            elif parseState == self.WaitForPayloadBytes:
                                incomingPacket += newByte
                                if len(incomingPacket) / 2 == packetLength:
                                    msgRcvTime = time.time()
                                    receivedChkSum = int(incomingPacket[-2:], 16)
                                    chksumdata = self.checkPacket(incomingPacket, receivedChkSum)
                                    if chksumdata[0]:
                                        newPacket = self.processPacket(incomingPacket)
                                        if self.enablePrinting:
                                            print('<--', REVMsg.printDict[int(newPacket.header.packetType)]['Name'], '::', newPacket.getPacketData())
                                        if discoveryMode:
                                            packet.append(newPacket)
                                            time.sleep(2)
                                            if self.REVProcessor.inWaiting() > 0:
                                                pass
                                            else:
                                                return packet
                                        else:
                                            return newPacket
                                    else:
                                        print('Invalid ChkSum: ', chksumdata[1], '==', chksumdata[2])
                                    rcvStarted = False
                                    parseState = self.WaitForFrameByte1

                else:
                    exit('\n\n\n!!!Attempting to send something other than a REVPacket!!!\n\n\n')

        except serial.SerialException:
            self.REVProcessor.close()
            return False

        return True

    def checkResponse(self, receivedPacket, PacketToWrite):
        packetType = int(receivedPacket.header.packetType)
        data = PacketToWrite.header.packetType.data >> 8 | PacketToWrite.header.packetType.data % 256 << 8
        responseExpected = REVMsg.printDict[data]['Response']
        if packetType == responseExpected:
            if receivedPacket.header.refNum == PacketToWrite.header.msgNum:
                return True
            else:
                if packetType == REVMsg.RespNum.Discovery_RSP:
                    return True
                print('This response is for a different message. Sent: %d, Received: %d.' % (receivedPacket.header.refNum, PacketToWrite.header.msgNum))
                return False

        else:
            if packetType == REVMsg.MsgNum.NACK:
                printData = PacketToWrite.header.packetType.data >> 8 | PacketToWrite.header.packetType.data % 256 << 8
                print('NACK Code: ', receivedPacket.payload.nackCode)
                print("NACK'd Packet: ", REVMsg.printDict[printData]['Name'], '::', PacketToWrite.getPacketData())
                return False
            else:
                print('Incorrect Response Type. Response Expected: ', binascii.hexlify(str(data)), ', Response Received: ', binascii.hexlify(str(packetType)))
                return False

    def checkPacket(self, incomingPacket, receivedChkSum):
        calcChkSum = 0
        for bytePointer in range(0, len(incomingPacket) - 2, 2):
            calcChkSum += int(incomingPacket[bytePointer:bytePointer + 2], 16)
            calcChkSum %= 256

        return (receivedChkSum == calcChkSum, receivedChkSum, calcChkSum)

    def processPacket(self, incomingPacket):
        packetFrameBytes = int(incomingPacket[REVMsg.REVPacket.FrameIndex_Start:REVMsg.REVPacket.FrameIndex_End], 16)
        packetLength = int(self.swapEndianess(incomingPacket[REVMsg.REVPacket.LengthIndex_Start:REVMsg.REVPacket.LengthIndex_End]), 16)
        packetDest = int(incomingPacket[REVMsg.REVPacket.DestinationIndex_Start:REVMsg.REVPacket.DestinationIndex_End], 16)
        packetSrc = int(incomingPacket[REVMsg.REVPacket.SourceIndex_Start:REVMsg.REVPacket.SourceIndex_End], 16)
        packetMsgNum = int(incomingPacket[REVMsg.REVPacket.MsgNumIndex_Start:REVMsg.REVPacket.MsgNumIndex_End], 16)
        packetRefNum = int(incomingPacket[REVMsg.REVPacket.RefNumIndex_Start:REVMsg.REVPacket.RefNumIndex_End], 16)
        packetCommandNum = int(self.swapEndianess(incomingPacket[REVMsg.REVPacket.PacketTypeIndex_Start:REVMsg.REVPacket.PacketTypeIndex_End]), 16)
        packetPayload = incomingPacket[REVMsg.REVPacket.HeaderIndex_End:-2]
        packetChkSum = int(incomingPacket[-2:], 16)
        newPacket = REVMsg.printDict[packetCommandNum]['Packet']()
        newPacket.assignRawBytes(incomingPacket)
        newPacket.header.length = packetLength
        newPacket.header.destination = packetDest
        newPacket.header.source = packetSrc
        newPacket.header.msgNum = packetMsgNum
        newPacket.header.refNum = packetRefNum
        newPacket.header.packetType = packetCommandNum
        bytePointer = 0
        for payloadMember in newPacket.payload.getOrderedMembers():
            valueToAdd = REVMsg.REVBytes(len(payloadMember))
            valueToAdd.data = int(self.swapEndianess(packetPayload[bytePointer:bytePointer + len(payloadMember) * 2]), 16)
            newPacket.payload.payloadMember = valueToAdd
            bytePointer = bytePointer + len(payloadMember) * 2

        return newPacket

    def swapEndianess(self, bytes):
        swappedBytes = ''
        for bytePointer in range(0, len(bytes), 2):
            thisByte = bytes[bytePointer:bytePointer + 2]
            swappedBytes = thisByte + swappedBytes

        return swappedBytes

    def getModuleStatus(self, destination):
        getModuleStatusMsg = REVMsg.GetModuleStatus()
        getModuleStatusMsg.payload.clearStatus = 1
        packet = self.sendAndReceive(getModuleStatusMsg, destination)
        return packet.payload.motorAlerts

    def keepAlive(self, destination):
        keepAliveMsg = REVMsg.KeepAlive()
        return self.sendAndReceive(keepAliveMsg, destination)

    def failSafe(self, destination):
        failSafeMsg = REVMsg.FailSafe()
        self.sendAndReceive(failSafeMsg, destination)

    def setNewModuleAddress(self, destination, moduleAddress):
        setNewModuleAddressMsg = REVMsg.SetNewModuleAddress()
        setNewModuleAddressMsg.payload.moduleAddress = moduleAddress
        self.sendAndReceive(setNewModuleAddressMsg, destination)

    def queryInterface(self, destination, interfaceName):
        queryInterfaceMsg = REVMsg.QueryInterface()
        queryInterfaceMsg.payload.interfaceName = interfaceName
        packet = self.sendAndReceive(queryInterfaceMsg, destination)
        return (
         packet.payload.packetID, packet.numValues)

    def setModuleLEDColor(self, destination, redPower, greenPower, bluePower):
        setModuleLEDColorMsg = REVMsg.SetModuleLEDColor()
        setModuleLEDColorMsg.payload.redPower = redPower
        setModuleLEDColorMsg.payload.greenPower = greenPower
        setModuleLEDColorMsg.payload.bluePower = bluePower
        self.sendAndReceive(setModuleLEDColorMsg, destination)

    def getModuleLEDColor(self, destination):
        getModuleLEDColorMsg = REVMsg.GetModuleLEDColor()
        packet = self.sendAndReceive(getModuleLEDColorMsg, destination)
        return (
         packet.payload.redPower, packet.payload.greenPower, packet.payload.bluePower)

    def setModuleLEDPattern(self, destination, stepArray):
        setModuleLEDPatternMsg = REVMsg.SetModuleLEDPattern()
        for i, step in enumerate(stepArray.patt):
            setattr(setModuleLEDPatternMsg.payload, ('rgbtStep{}').format(i), step)  
        self.sendAndReceive(setModuleLEDPatternMsg, destination)

    def getModuleLEDPattern(self, destination):
        getModuleLEDPatternMsg = REVMsg.GetModuleLEDPattern()
        packet = self.sendAndReceive(getModuleLEDPatternMsg, destination)
        return packet

    def debugLogLevel(self, destination, groupNumber, verbosityLevel):
        debugLogLevelMsg = REVMsg.DebugLogLevel()
        debugLogLevelMsg.payload.groupNumber = groupNumber
        debugLogLevelMsg.payload.verbosityLevel = verbosityLevel
        self.sendAndReceive(debugLogLevelMsg, destination)

    def discovery(self):
        self.discovered = REVMsg.Discovery()
        packets = self.sendAndReceive(self.discovered, 255)
        REVModules = []
        for packet in packets:
            module = Module(self, packet.header.source, packet.payload.parent)
            module.init_periphs()
            REVModules.append(module)
        return REVModules

    def getBulkInputData(self, destination):
        getBulkInputDataMsg = REVMsg.GetBulkInputData()
        packet = self.sendAndReceive(getBulkInputDataMsg, destination)
        return packet

    def phoneChargeControl(self, destination, enable):
        phoneChargeControlMsg = REVMsg.PhoneChargeControl()
        phoneChargeControlMsg.payload.enable = enable
        self.sendAndReceive(phoneChargeControlMsg, destination)

    def phoneChargeQuery(self, destination):
        phoneChargeQueryMsg = REVMsg.PhoneChargeQuery()
        packet = self.sendAndReceive(phoneChargeQueryMsg, destination)
        return packet.payload.enable

    def injectDataLogHint(self, destination, length, hintText):
        injectDataLogHintMsg = REVMsg.InjectDataLogHint()
        injectDataLogHintMsg.payload.length = length
        injectDataLogHintMsg.payload.hintText = hintText
        self.sendAndReceive(injectDataLogHintMsg, destination)

    def readVersionString(self, destination):
        readVersionStringMsg = REVMsg.ReadVersionString()
        packet = self.sendAndReceive(readVersionStringMsg, destination)
        return packet.payload.versionString

    def getBulkMotorData(self, destination):
        getBulkMotorDataMsg = REVMsg.GetBulkMotorData()
        packet = self.sendAndReceive(getBulkMotorDataMsg, destination)
        return packet

    def getBulkADCData(self, destination):
        getBulkADCDataMsg = REVMsg.GetBulkADCData()
        packet = self.sendAndReceive(getBulkADCDataMsg, destination)
        return packet

    def getBulkI2CData(self, destination):
        getBulkI2CDataMsg = REVMsg.GetBulkI2CData()
        packet = self.sendAndReceive(getBulkI2CDataMsg, destination)
        return packet

    def getBulkServoData(self, destination):
        getBulkServoDataMsg = REVMsg.GetBulkServoData()
        packet = self.sendAndReceive(getBulkServoDataMsg, destination)
        return packet