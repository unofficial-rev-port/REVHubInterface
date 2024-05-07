from . import REVMotor, REVServo, REVADC, REVDIO, REVI2C


class Module:

    def __init__(self, commObj, address, parent):
        self.commObj = commObj
        self.address = address
        self.parent = parent
        self.motors = []
        self.servos = []
        self.i2cChannels = []
        self.adcPins = []
        self.dioPins = []

    def init_periphs(self):
        for i in range(0, 4):
            self.motors.append(REVMotor.Motor(self.commObj, i, self.address))
            self.motors[-1].setMode(0, 1)
            self.motors[-1].setPower(0)
            self.i2cChannels.append(REVI2C.I2CChannel(self.commObj, i, self.address))

        for j in range(0, 8):
            self.dioPins.append(REVDIO.DIOPin(self.commObj, j, self.address))

        for k in range(0, 6):
            self.servos.append(REVServo.Servo(self.commObj, k, self.address))
            self.servos[-1].init()

        for l in range(0, 4):
            self.adcPins.append(REVADC.ADCPin(self.commObj, l, self.address))

    def killSwitch(self):
        for i in range(0, 4):
            self.motors[i].disable()

        for j in range(0, 8):
            pass

        for k in range(0, 6):
            self.servos[k].disable()

        for l in range(0, 15):
            pass

    def getParentStatus(self):
        return self.parent

    def getAddress(self):
        return self.address

    def getStatus(self):
        return self.commObj.getModuleStatus(self.address)

    def getModuleAddress(self):
        return self.address

    def sendKA(self):
        return self.commObj.keepAlive(self.address)

    def sendFailSafe(self):
        self.commObj.failSafe(self.address)

    def setAddress(self, newAddress):
        self.commObj.setNewModuleAddress(self.address, newAddress)
        self.address = newAddress
        for motor in self.motors:
            motor.setDestination(newAddress)

        for servo in self.servos:
            servo.setDestination(newAddress)

        for i2cChannel in self.i2cChannels:
            i2cChannel.setDestination(newAddress)

        for adcPin in self.adcPins:
            adcPin.setDestination(newAddress)

        for dioPin in self.dioPins:
            dioPin.setDestination(newAddress)

    def getInterface(self, interface):
        return self.commObj.queryInterface(self.address, interface)

    def setLEDColor(self, red, green, blue):
        self.commObj.setModuleLEDColor(self.address, red, green, blue)

    def getLEDColor(self):
        return self.commObj.getModuleLEDColor(self.address)

    def setLEDPattern(self, pattern):
        """ Example:
      from REVmessages import LEDPattern

      hub = REVModules()
      my_pattern = LEDPattern()
      my_pattern.set_step(0, 255, 0, 0, 10) # set first step to red for 1 second
      my_pattern.set_step(1, 0, 255, 0, 10) # set second step to green for 1 second
      hub.REVModules[0].setLEDPattern(my_pattern)
      hub.REVModules[0].keepAlive()
      """
        return self.commObj.setModuleLEDPattern(self.address, pattern)

    def setLogLevel(self, group, verbosity):
        self.commObj.debugLogLevel(self.address, group, verbosity)

    def getBulkData(self):
        return self.commObj.getBulkInputData(self.address)

    def enableCharging(self):
        self.commObj.phoneChargeControl(self.address, 1)

    def disableCharging(self):
        self.commObj.phoneChargeControl(self.address, 0)

    def chargingEnabled(self):
        return self.commObj.phoneChargeQuery(self.address)

    def debugOutput(self, length, hint):
        self.commObj.injectDataLogHint(self.address, length, hint)

    def setAllDIO(self, values):
        REVDIO.setAllDIOOutputs(self.address, values)

    def getAllDIO(self):
        return REVDIO.getAllDIOInputs(self.address)

    def getVersionString(self):
        versionRaw = '' + self.commObj.readVersionString(self.address)
        versionStr = ''
        for i in range(0, int(len(versionRaw) / 2)):
            tmpHex = int(str(versionRaw)[i * 2] + str(versionRaw)[i * 2 + 1], 16)
            versionStr = versionStr + chr(tmpHex)
        return versionStr

    def setIMUBlockReadConfig(self, startRegister, numberOfBytes, readInterval_ms):
        REVI2C.imuBlockReadConfig(self.address, startRegister, numberOfBytes, readInterval_ms)

    def getIMUBlockReadConfig(self):
        return REVI2C.imuBlockReadQuery(self.address)

    def getBulkMotorData(self):
        return self.commObj.getBulkMotorData(self.address)

    def getBulkADCData(self):
        return self.commObj.getBulkADCData(self.address)

    def getBulkI2CData(self):
        return self.commObj.getBulkI2CData(self.address)

    def getBulkServoData(self):
        return self.commObj.getBulkServoData(self.address)