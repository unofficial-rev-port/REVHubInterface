from . import REVmessages as REVMsg


def setSingleDIOOutput(commObj, destination, dioPin, value):
    setSingleDIOOutput = REVMsg.SetSingleDIOOutput()
    setSingleDIOOutput.payload.dioPin = dioPin
    setSingleDIOOutput.payload.value = value
    commObj.sendAndReceive(setSingleDIOOutput, destination)


def setAllDIOOutputs(commObj, destination, values):
    setAllDIOOutputs = REVMsg.SetAllDIOOutputs()
    setAllDIOOutputs.payload.values = values
    commObj.sendAndReceive(setAllDIOOutputs, destination)


def setDIODirection(commObj, destination, dioPin, directionOutput):
    setDIODirection = REVMsg.SetDIODirection()
    setDIODirection.payload.dioPin = dioPin
    setDIODirection.payload.directionOutput = directionOutput
    commObj.sendAndReceive(setDIODirection, destination)


def getDIODirection(commObj, destination, dioPin):
    getDIODirection = REVMsg.GetDIODirection()
    getDIODirection.payload.dioPin = dioPin
    packet = commObj.sendAndReceive(getDIODirection, destination)
    return packet.payload.directionOutput


def getSingleDIOInput(commObj, destination, dioPin):
    getSingleDIOInput = REVMsg.GetSingleDIOInput()
    getSingleDIOInput.payload.dioPin = dioPin
    packet = commObj.sendAndReceive(getSingleDIOInput, destination)
    return packet.payload.inputValue


def getAllDIOInputs(commObj, destination):
    getAllDIOInputs = REVMsg.GetAllDIOInputs()
    packet = commObj.sendAndReceive(getAllDIOInputs, destination)
    return packet.payload.inputValues


class DIOPin:

    def __init__(self, commObj, pinNumber, destinationModule):
        self.destinationModule = destinationModule
        self.pinNumber = pinNumber
        self.commObj = commObj

    def setDestination(self, destinationModule):
        self.destinationModule = destinationModule

    def getDestination(self):
        return self.destinationModule

    def setPinNumber(self, pinNumber):
        self.pinNumber = pinNumber

    def getPinNumber(self):
        return self.pinNumber

    def setOutput(self, value):
        setSingleDIOOutput(self.commObj, self.destinationModule, self.pinNumber, value)

    def getInput(self):
        return getSingleDIOInput(self.commObj, self.destinationModule, self.pinNumber)

    def setAsOutput(self):
        setDIODirection(self.commObj, self.destinationModule, self.pinNumber, 1)

    def setAsInput(self):
        setDIODirection(self.commObj, self.destinationModule, self.pinNumber, 0)

    def getDirection(self):
        getDIODirection(self.commObj, self.destinationModule, self.pinNumber)