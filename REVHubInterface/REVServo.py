from . import REVmessages as REVMsg


def setServoConfiguration(commObj, destination, servoChannel, framePeriod):
    setServoConfigurationMsg = REVMsg.SetServoConfiguration()
    setServoConfigurationMsg.payload.servoChannel = servoChannel
    setServoConfigurationMsg.payload.framePeriod = framePeriod
    return commObj.sendAndReceive(setServoConfigurationMsg, destination)


def getServoConfiguration(commObj, destination, servoChannel):
    getServoConfigurationMsg = REVMsg.GetServoConfiguration()
    getServoConfigurationMsg.payload.servoChannel = servoChannel
    packet = commObj.sendAndReceive(getServoConfigurationMsg, destination)
    return packet.payload.framePeriod


def setServoPulseWidth(commObj, destination, servoChannel, pulseWidth):
    setServoPulseWidthMsg = REVMsg.SetServoPulseWidth()
    setServoPulseWidthMsg.payload.servoChannel = servoChannel
    setServoPulseWidthMsg.payload.pulseWidth = pulseWidth
    return commObj.sendAndReceive(setServoPulseWidthMsg, destination)


def getServoPulseWidth(commObj, destination, servoChannel):
    getServoPulseWidthMsg = REVMsg.GetServoPulseWidth()
    getServoPulseWidthMsg.payload.servoChannel = servoChannel
    packet = commObj.sendAndReceive(getServoPulseWidthMsg, destination)
    return packet.payload.pulseWidth


def setServoEnable(commObj, destination, servoChannel, enable):
    setServoEnableMsg = REVMsg.SetServoEnable()
    setServoEnableMsg.payload.servoChannel = servoChannel
    setServoEnableMsg.payload.enable = enable
    return commObj.sendAndReceive(setServoEnableMsg, destination)


def getServoEnable(commObj, destination, servoChannel):
    getServoEnableMsg = REVMsg.GetServoEnable()
    getServoEnableMsg.payload.servoChannel = servoChannel
    packet = commObj.sendAndReceive(getServoEnableMsg, destination)
    return packet.payload.enabled


class Servo:

    def __init__(self, commObj, channel, destinationModule):
        self.commObj = commObj
        self.destinationModule = destinationModule
        self.channel = channel

    def setDestination(self, destinationModule):
        self.destinationModule = destinationModule

    def getDestination(self):
        return self.destinationModule

    def setChannel(self, channel):
        self.channel = channel

    def getChannel(self):
        return self.channel

    def setPeriod(self, period):
        setServoConfiguration(self.commObj, self.destinationModule, self.channel, period)

    def getPeriod(self):
        return getServoConfiguration(self.commObj, self.destinationModule, self.channel)

    def setPulseWidth(self, pulseWidth):
        setServoPulseWidth(self.commObj, self.destinationModule, self.channel, pulseWidth)

    def getPulseWidth(self):
        return getServoPulseWidth(self.commObj, self.destinationModule, self.channel)

    def enable(self):
        errorCode = setServoEnable(self.commObj, self.destinationModule, self.channel, 1)

    def disable(self):
        setServoEnable(self.commObj, self.destinationModule, self.channel, 0)

    def isEnabled(self):
        return getServoEnable(self.commObj, self.destinationModule, self.channel)

    def init(self):
        self.setPeriod(20000)