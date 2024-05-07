from . import REVModule, REVADC, REVmessages as REVMsg

Q16 = 65536.0
MODE_CONSTANT_POWER = 0
MODE_CONSTANT_VELOCITY = 1
MODE_POSITION_TARGET = 2
MODE_CONSTANT_CURRENT = 3
BRAKE_AT_ZERO = 0
FLOAT_AT_ZERO = 1
VELOCITY_OFFSET = 6
CURRENT_OFFSET = 8

def setMotorChannelMode(commObj, destination, motorChannel, motorMode, floatAtZero):
    setMotorChannelModeMsg = REVMsg.SetMotorChannelMode()
    setMotorChannelModeMsg.payload.motorChannel = motorChannel
    setMotorChannelModeMsg.payload.motorMode = motorMode
    setMotorChannelModeMsg.payload.floatAtZero = floatAtZero
    commObj.sendAndReceive(setMotorChannelModeMsg, destination)


def getMotorChannelMode(commObj, destination, motorChannel):
    getMotorChannelModeMsg = REVMsg.GetMotorChannelMode()
    getMotorChannelModeMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorChannelModeMsg, destination)
    return (
     packet.payload.motorChannelMode, packet.payload.floatAtZero)


def setMotorChannelEnable(commObj, destination, motorChannel, enabled):
    setMotorChannelEnableMsg = REVMsg.SetMotorChannelEnable()
    setMotorChannelEnableMsg.payload.motorChannel = motorChannel
    setMotorChannelEnableMsg.payload.enabled = enabled
    packet = commObj.sendAndReceive(setMotorChannelEnableMsg, destination)


def getMotorChannelEnable(commObj, destination, motorChannel):
    getMotorChannelEnableMsg = REVMsg.GetMotorChannelEnable()
    getMotorChannelEnableMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorChannelEnableMsg, destination)
    return packet.payload.enabled


def setMotorChannelCurrentAlertLevel(commObj, destination, motorChannel, currentLimit):
    setMotorChannelCurrentAlertLevelMsg = REVMsg.SetMotorChannelCurrentAlertLevel()
    setMotorChannelCurrentAlertLevelMsg.payload.motorChannel = motorChannel
    setMotorChannelCurrentAlertLevelMsg.payload.currentLimit = currentLimit
    commObj.sendAndReceive(setMotorChannelCurrentAlertLevelMsg, destination)


def getMotorChannelCurrentAlertLevel(commObj, destination, motorChannel):
    getMotorChannelCurrentAlertLevelMsg = REVMsg.GetMotorChannelCurrentAlertLevel()
    getMotorChannelCurrentAlertLevelMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorChannelCurrentAlertLevelMsg, destination)
    return packet.payload.currentLimit


def resetMotorEncoder(commObj, destination, motorChannel):
    resetMotorEncoderMsg = REVMsg.ResetMotorEncoder()
    resetMotorEncoderMsg.payload.motorChannel = motorChannel
    commObj.sendAndReceive(resetMotorEncoderMsg, destination)


def setMotorConstantPower(commObj, destination, motorChannel, powerLevel):
    setMotorConstantPowerMsg = REVMsg.SetMotorConstantPower()
    setMotorConstantPowerMsg.payload.motorChannel = motorChannel
    setMotorConstantPowerMsg.payload.powerLevel = powerLevel
    commObj.sendAndReceive(setMotorConstantPowerMsg, destination)


def getMotorConstantPower(commObj, destination, motorChannel):
    getMotorConstantPowerMsg = REVMsg.GetMotorConstantPower()
    getMotorConstantPowerMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorConstantPowerMsg, destination)
    return packet.payload.powerLevel


def setMotorTargetVelocity(commObj, destination, motorChannel, velocity):
    setMotorTargetVelocityMsg = REVMsg.SetMotorTargetVelocity()
    setMotorTargetVelocityMsg.payload.motorChannel = motorChannel
    setMotorTargetVelocityMsg.payload.velocity = velocity
    commObj.sendAndReceive(setMotorTargetVelocityMsg, destination)


def getMotorTargetVelocity(commObj, destination, motorChannel):
    getMotorTargetVelocityMsg = REVMsg.GetMotorTargetVelocity()
    getMotorTargetVelocityMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorTargetVelocityMsg, destination)
    return packet.payload.velocity


def setMotorTargetPosition(commObj, destination, motorChannel, position, atTargetTolerance):
    setMotorTargetPositionMsg = REVMsg.SetMotorTargetPosition()
    setMotorTargetPositionMsg.payload.motorChannel = motorChannel
    setMotorTargetPositionMsg.payload.position = position
    setMotorTargetPositionMsg.payload.atTargetTolerance = atTargetTolerance
    commObj.sendAndReceive(setMotorTargetPositionMsg, destination)


def getMotorTargetPosition(commObj, destination, motorChannel):
    getMotorTargetPositionMsg = REVMsg.GetMotorTargetPosition()
    getMotorTargetPositionMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorTargetPositionMsg, destination)
    return (
     packet.payload.targetPosition, packet.payload.atTargetTolerance)


def getMotorAtTarget(commObj, destination, motorChannel):
    getMotorAtTargetMsg = REVMsg.GetMotorAtTarget()
    getMotorAtTargetMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorAtTargetMsg, destination)
    return packet.payload.atTarget


def getMotorEncoderPosition(commObj, destination, motorChannel):
    getMotorEncoderPositionMsg = REVMsg.GetMotorEncoderPosition()
    getMotorEncoderPositionMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getMotorEncoderPositionMsg, destination)
    val = int(packet.payload.currentPosition)
    bits = int(32)
    if val & 1 << bits - 1 != 0:
        val = val - (1 << bits)
    return val


def setMotorPIDCoefficients(commObj, destination, motorChannel, mode, p, i, d):
    setMotorPIDCoefficientsMsg = REVMsg.SetMotorPIDCoefficients()
    setMotorPIDCoefficientsMsg.payload.motorChannel = motorChannel
    setMotorPIDCoefficientsMsg.payload.mode = mode
    setMotorPIDCoefficientsMsg.payload.p = p * Q16
    setMotorPIDCoefficientsMsg.payload.i = i * Q16
    setMotorPIDCoefficientsMsg.payload.d = d * Q16
    commObj.sendAndReceive(setMotorPIDCoefficientsMsg, destination)


def getMotorPIDCoefficients(commObj, destination, motorChannel, mode):
    getMotorPIDCoefficientsMsg = REVMsg.GetMotorPIDCoefficients()
    getMotorPIDCoefficientsMsg.payload.motorChannel = motorChannel
    getMotorPIDCoefficientsMsg.payload.mode = mode
    packet = commObj.sendAndReceive(getMotorPIDCoefficientsMsg, destination)
    p = int(packet.payload.p) / Q16
    i = int(packet.payload.i) / Q16
    d = int(packet.payload.d) / Q16
    return (
     p, i, d)


def getBulkPIDData(commObj, destination, motorChannel):
    getBulkPIDDataMsg = REVMsg.GetBulkPIDData()
    getBulkPIDDataMsg.payload.motorChannel = motorChannel
    packet = commObj.sendAndReceive(getBulkPIDDataMsg, destination)
    return packet


def setCurrentPIDCoefficients(commObj, destination, motorChannel, p, i, d):
    getMotorPIDCoefficients(commObj, destination, motorChannel, 3, p, i, d)


def setVelocityPIDCoefficients(commObj, destination, motorChannel, p, i, d):
    setMotorPIDCoefficients(commObj, destination, motorChannel, 1, p, i, d)


def setPositionPIDCoefficients(commObj, destination, motorChannel, p, i, d):
    setMotorPIDCoefficients(commObj, destination, motorChannel, 2, p, i, d)


def getCurrentPIDCoefficients(commObj, destination, motorChannel):
    return getMotorPIDCoefficients(commObj, destination, motorChannel, 3)


def getVelocityPIDCoefficients(commObj, destination, motorChannel):
    return getMotorPIDCoefficients(commObj, destination, motorChannel, 1)


def getPositionPIDCoefficients(commObj, destination, motorChannel):
    return getMotorPIDCoefficients(commObj, destination, motorChannel, 2)


class Motor:

    def __init__(self, commObj, channel, destinationModule):
        self.channel = channel
        self.destinationModule = destinationModule
        self.commObj = commObj
        self.motorCurrent = REVADC.ADCPin(self.commObj, 8 + channel, self.destinationModule)

    def setDestination(self, destinationModule):
        self.destinationModule = destinationModule
        self.motorCurrent.setDestination(destinationModule)

    def getDestination(self):
        return self.destinationModule

    def setChannel(self, channel):
        self.channel = channel

    def getChannel(self):
        return self.channel

    def setMode(self, mode, zeroFloat):
        setMotorChannelMode(self.commObj, self.destinationModule, self.channel, mode, zeroFloat)

    def getMode(self):
        return getMotorChannelMode(self.commObj, self.destinationModule, self.channel)

    def enable(self):
        setMotorChannelEnable(self.commObj, self.destinationModule, self.channel, 1)

    def disable(self):
        setMotorChannelEnable(self.commObj, self.destinationModule, self.channel, 0)

    def isEnabled(self):
        return getMotorChannelEnable(self.commObj, self.destinationModule, self.channel)

    def setCurrentLimit(self, limit):
        setMotorChannelCurrentAlertLevel(self.commObj, self.destinationModule, self.channel, limit)

    def getCurrentLimit(self):
        return getMotorChannelCurrentAlertLevel(self.commObj, self.destinationModule, self.channel)

    def resetEncoder(self):
        resetMotorEncoder(self.commObj, self.destinationModule, self.channel)

    def setPower(self, powerLevel):
        setMotorConstantPower(self.commObj, self.destinationModule, self.channel, powerLevel)

    def getPower(self):
        return getMotorConstantPower(self.commObj, self.destinationModule, self.channel)

    def setTargetCurrent(self, current):
        self.setCurrentLimit(current)

    def getTargetCurrent(self):
        return self.getCurrentLimit()

    def setTargetVelocity(self, velocity):
        setMotorTargetVelocity(self.commObj, self.destinationModule, self.channel, velocity)

    def getTargetVelocity(self):
        return getMotorTargetVelocity(self.commObj, self.destinationModule, self.channel)

    def setTargetPosition(self, position, tolerance):
        setMotorTargetPosition(self.commObj, self.destinationModule, self.channel, position, tolerance)

    def getTargetPosition(self):
        return getMotorTargetPosition(self.commObj, self.destinationModule, self.channel)

    def isAtTarget(self):
        return getMotorAtTarget(self.commObj, self.destinationModule, self.channel)

    def getPosition(self):
        position = getMotorEncoderPosition(self.commObj, self.destinationModule, self.channel)
        return position

    def resetPosition(self):
        resetMotorEncoder(self.commObj, self.destinationModule, self.channel)

    def getVelocity(self):
        bulkData = REVModule.getBulkInputData(self.commObj, self.destinationModule)
        val = int(bulkData[self.channel + VELOCITY_OFFSET])
        bits = int(16)
        if val & 1 << bits - 1 != 0:
            val = val - (1 << bits)
        return val

    def getCurrent(self):
        return self.motorCurrent.getADC(0)

    def setCurrentPID(self, p, i, d):
        setCurrentPIDCoefficients(self.commObj, self.destinationModule, self.channel, p, i, d)

    def getCurrentPID(self, p, i, d):
        return getCurrentPIDCoefficients(self.commObj, self.destinationModule, self.channel)

    def setVelocityPID(self, p, i, d):
        setVelocityPIDCoefficients(self.commObj, self.destinationModule, self.channel, p, i, d)

    def getVelocityPID(self):
        return getVelocityPIDCoefficients(self.commObj, self.destinationModule, self.channel)

    def setPositionPID(self, p, i, d):
        setPositionPIDCoefficients(self.commObj, self.destinationModule, self.channel, p, i, d)

    def getPositionPID(self):
        return getPositionPIDCoefficients(self.commObj, self.destinationModule, self.channel)

    def getBulkPIDData(self):
        return getBulkPIDData(self.commObj, self.destinationModule, self.channel)

    def init(self):
        self.setMode(0, 1)
        self.setPower(0)
        self.enable()
