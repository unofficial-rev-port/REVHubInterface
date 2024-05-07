from . import REVcomm as REVComm
from .REVI2C import I2CDevice
import sys, time
VcselPeriodPreRange = 0
VcselPeriodFinalRange = 1

class REV2mSensor(I2CDevice):

    def __init__(self, commObj, channel, destinationModule, debugEnable=False):
        I2CDevice.__init__(self, commObj, channel, destinationModule, self._ADDRESS_I2C_DEFAULT)
        self._debug_enable = debugEnable
        self.setType('REV2mSensor')

    def _debugPrint(self, val):
        if self._debug_enable == True:
            print(val)

    def Is2mDistanceSensor(self):

        def VL53L0X_check(addr, expected, numBytes=1):
            value = self.readRegister(addr, numBytes)
            if value != expected:
                self._debugPrint('Register (' + hex(addr) + ') expected (' + hex(expected) + ') got (' + hex(value) + ')')
                return False
            return True

        status = VL53L0X_check(192, 238)
        if status == False:
            return False
        status = VL53L0X_check(193, 170)
        if status == False:
            return False
        status = VL53L0X_check(194, 16)
        if status == False:
            return False
        status = VL53L0X_check(97, 0, 2)
        if status == False:
            return False
        return True

    def GetDistance(self):
        pass

    def initialize(self):
        self.writeRegister(136, 0)
        self.writeRegister(128, 1)
        self.writeRegister(255, 1)
        self.writeRegister(0, 0)
        self._stop_variable = self.readRegister(145)
        self._debugPrint('stop_variable: ' + hex(self._stop_variable))
        self.writeRegister(0, 1)
        self.writeRegister(255, 0)
        self.writeRegister(128, 0)
        writeTmp = self.readRegister(self._MSRC_CONFIG_CONTROL) | 18
        self._debugPrint('_MSRC_CONFIG_CONTROL | 0x12: ' + hex(writeTmp))
        self.writeRegister(self._MSRC_CONFIG_CONTROL, writeTmp)
        self._debugPrint('Initial signal rate: ' + str(self.getSignalRateLimit()))
        self.setSignalRateLimit(0.25)
        self._debugPrint('New signal rate: ' + str(self.getSignalRateLimit()))
        self.writeRegister(self._SYSTEM_SEQUENCE_CONFIG, 255)
        if self.getSpadInfo() == False:
            self._debugPrint('FATAL: getSpadInfo() returned False')
            return False
        ref_spad_map = []
        self.writeByte(self._GLOBAL_CONFIG_SPAD_ENABLES_REF_0)
        for i in range(0, 6):
            tmp = self.readByte()
            self._debugPrint('SPAD[' + str(i) + ']: ' + hex(tmp))
            ref_spad_map.append(tmp)

        self.writeRegister(255, 1)
        self.writeRegister(self._DYNAMIC_SPAD_REF_EN_START_OFFSET, 0)
        self.writeRegister(self._DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 44)
        self.writeRegister(255, 0)
        self.writeRegister(self._GLOBAL_CONFIG_REF_EN_START_SELECT, 180)
        first_spad_to_enable = 0
        if self._spad_type_is_aperture == True:
            first_spad_to_enable = 12
        self._debugPrint('first_spad_to_enable: ' + str(first_spad_to_enable))
        spads_enabled = 0
        for i in range(0, 48):
            tmpIdx = i / 8
            if i < first_spad_to_enable or spads_enabled == self._spad_count:
                ref_spad_map[tmpIdx] &= ~(1 << i % 8)
                self._debugPrint('TMP IDX A: ' + str(tmpIdx) + ' set to ' + hex(ref_spad_map[tmpIdx]))
            elif ref_spad_map[tmpIdx] >> i % 8 & 1 != 0:
                self._debugPrint('TMP IDX B: spads_enabled+=1')
                spads_enabled += 1

        self.writeByte(self._GLOBAL_CONFIG_SPAD_ENABLES_REF_0)
        for data in ref_spad_map:
            self.writeByte(data)

        self.writeRegister(255, 1)
        self.writeRegister(0, 0)
        self.writeRegister(255, 0)
        self.writeRegister(9, 0)
        self.writeRegister(16, 0)
        self.writeRegister(17, 0)
        self.writeRegister(36, 1)
        self.writeRegister(37, 255)
        self.writeRegister(117, 0)
        self.writeRegister(255, 1)
        self.writeRegister(78, 44)
        self.writeRegister(72, 0)
        self.writeRegister(48, 32)
        self.writeRegister(255, 0)
        self.writeRegister(48, 9)
        self.writeRegister(84, 0)
        self.writeRegister(49, 4)
        self.writeRegister(50, 3)
        self.writeRegister(64, 131)
        self.writeRegister(70, 37)
        self.writeRegister(96, 0)
        self.writeRegister(39, 0)
        self.writeRegister(80, 6)
        self.writeRegister(81, 0)
        self.writeRegister(82, 150)
        self.writeRegister(86, 8)
        self.writeRegister(87, 48)
        self.writeRegister(97, 0)
        self.writeRegister(98, 0)
        self.writeRegister(100, 0)
        self.writeRegister(101, 0)
        self.writeRegister(102, 160)
        self.writeRegister(255, 1)
        self.writeRegister(34, 50)
        self.writeRegister(71, 20)
        self.writeRegister(73, 255)
        self.writeRegister(74, 0)
        self.writeRegister(255, 0)
        self.writeRegister(122, 10)
        self.writeRegister(123, 0)
        self.writeRegister(120, 33)
        self.writeRegister(255, 1)
        self.writeRegister(35, 52)
        self.writeRegister(66, 0)
        self.writeRegister(68, 255)
        self.writeRegister(69, 38)
        self.writeRegister(70, 5)
        self.writeRegister(64, 64)
        self.writeRegister(14, 6)
        self.writeRegister(32, 26)
        self.writeRegister(67, 64)
        self.writeRegister(255, 0)
        self.writeRegister(52, 3)
        self.writeRegister(53, 68)
        self.writeRegister(255, 1)
        self.writeRegister(49, 4)
        self.writeRegister(75, 9)
        self.writeRegister(76, 5)
        self.writeRegister(77, 4)
        self.writeRegister(255, 0)
        self.writeRegister(68, 0)
        self.writeRegister(69, 32)
        self.writeRegister(71, 8)
        self.writeRegister(72, 40)
        self.writeRegister(103, 0)
        self.writeRegister(112, 4)
        self.writeRegister(113, 1)
        self.writeRegister(114, 254)
        self.writeRegister(118, 0)
        self.writeRegister(119, 0)
        self.writeRegister(255, 1)
        self.writeRegister(13, 1)
        self.writeRegister(255, 0)
        self.writeRegister(128, 1)
        self.writeRegister(1, 248)
        self.writeRegister(255, 1)
        self.writeRegister(142, 1)
        self.writeRegister(0, 1)
        self.writeRegister(255, 0)
        self.writeRegister(128, 0)
        self.writeRegister(self._SYSTEM_INTERRUPT_CONFIG_GPIO, 4)
        writeTmp = self.readRegister(self._GPIO_HV_MUX_ACTIVE_HIGH) & -17
        self.writeRegister(self._GPIO_HV_MUX_ACTIVE_HIGH, writeTmp)
        self.writeRegister(self._SYSTEM_INTERRUPT_CLEAR, 1)
        self.writeRegister(self._SYSTEM_SEQUENCE_CONFIG, 232)
        self.writeRegister(self._SYSTEM_SEQUENCE_CONFIG, 1)
        if self.performSingleRefCalibration(64) == False:
            self._debugPrint('performSingleRefCalibration(0x40) returned False')
            return False
        self.writeRegister(self._SYSTEM_SEQUENCE_CONFIG, 2)
        if self.performSingleRefCalibration(0) == False:
            self._debugPrint('performSingleRefCalibration(0x00) returned False')
            return False
        self.writeRegister(self._SYSTEM_SEQUENCE_CONFIG, 232)
        self.setTimeout(200)
        self.startContinuous()
        return True

    def setSignalRateLimit(self, limit_Mcps):
        if limit_Mcps < 0.0 or limit_Mcps > 51.99:
            print('Invalid Signal Rate: ' + str(limit_Mcps))
        self.writeShort(self._FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, int(limit_Mcps * 128))
        return True

    def getSignalRateLimit(self):
        return float(self.readRegister(self._FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, 2)) / 128

    def getSpadInfo(self):
        self.writeRegister(128, 1)
        self.writeRegister(255, 1)
        self.writeRegister(0, 0)
        self.writeRegister(255, 6)
        writeTmp = self.readRegister(131) | 4
        self.writeRegister(131, writeTmp)
        self.writeRegister(255, 7)
        self.writeRegister(129, 1)
        self.writeRegister(128, 1)
        self.writeRegister(148, 107)
        self.writeRegister(131, 0)
        self.writeRegister(131, 1)
        writeTmp = self.readRegister(146)
        self._spad_count = writeTmp & 127
        self._spad_type_is_aperture = True
        self._debugPrint('SPAD INFO: Scout: ' + str(self._spad_count) + ' type is aperture: ' + str(self._spad_type_is_aperture))
        if writeTmp >> 7 & 1 == 0:
            self._spad_type_is_aperture = False
        self.writeRegister(129, 0)
        self.writeRegister(255, 6)
        writeTmp = self.readRegister(131) & -5
        self.writeRegister(131, writeTmp)
        self.writeRegister(255, 1)
        self.writeRegister(0, 1)
        self.writeRegister(255, 0)
        self.writeRegister(128, 0)
        return True

    def setMeasurementTimingBudget(self, budget_us):
        StartOverhead = 1320
        EndOverhead = 960
        MsrcOverhead = 660
        TccOverhead = 590
        DssOverhead = 690
        PreRangeOverhead = 660
        FinalRangeOverhead = 550
        MinTimingBudget = 20000
        if budget_us < MinTimingBudget:
            return False
        used_budget_us = StartOverhead + EndOverhead
        enables = self.getSequenceStepEnables()
        timeouts = self.getSequenceStepTimeouts(enables)
        if enables.tcc:
            used_budget_us += timeouts.msrc_dss_tcc_us + TccOverhead
        if enables.dss:
            used_budget_us += 2 * (timeouts.msrc_dss_tcc_us + DssOverhead)
        elif enables.msrc:
            used_budget_us += timeouts.msrc_dss_tcc_us + MsrcOverhead
        if enables.pre_range:
            used_budget_us += timeouts.pre_range_us + PreRangeOverhead
        if enables.final_range:
            used_budget_us += FinalRangeOverhead
            if used_budget_us > budget_us:
                return False
            final_range_timeout_us = budget_us - used_budget_us
            final_range_timeout_mclks = self.timeoutMicrosecondsToMclks(final_range_timeout_us, timeouts.final_range_vcsel_period_pclks)
            if enables.pre_range:
                final_range_timeout_mclks += timeouts.pre_range_mclks
            self.writeShort(self._FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, self.encodeTimeout(final_range_timeout_mclks))
            self._measurement_timing_budget_us = budget_us
        return True

    def getMeasurementTimingBudget(self):
        StartOverhead = 1910
        EndOverhead = 960
        MsrcOverhead = 660
        TccOverhead = 590
        DssOverhead = 690
        PreRangeOverhead = 660
        FinalRangeOverhead = 550
        budget_us = StartOverhead + EndOverhead
        enables = self.getSequenceStepEnables()
        timeouts = self.getSequenceStepTimeouts(enables)
        if enables.tcc:
            budget_us += timeouts.msrc_dss_tcc_us + TccOverhead
        if enables.dss:
            budget_us += 2 * (timeouts.msrc_dss_tcc_us + DssOverhead)
        elif enables.msrc:
            budget_us += timeouts.msrc_dss_tcc_us + MsrcOverhead
        if enables.pre_range:
            budget_us += timeouts.pre_range_us + PreRangeOverhead
        if enables.final_range:
            budget_us += timeouts.final_range_us + FinalRangeOverhead
        measurement_timing_budget_us = budget_us
        return budget_us

    class SequenceStepEnables:
        tcc = False
        msrc = False
        dss = False
        pre_range = False
        final_range = False

    class SequenceStepTimeouts:
        pre_range_vcsel_period_pclks = 0.0
        final_range_vcsel_period_pclks = 0.0
        msrc_dss_tcc_mclks = 0.0
        pre_range_mclks = 0.0
        final_range_mclks = 0.0
        msrc_dss_tcc_us = 0.0
        pre_range_us = 0.0
        final_range_us = 0.0

    def getSequenceStepEnables(self):
        sequence_config = self.readRegister(self._SYSTEM_SEQUENCE_CONFIG)
        enables = self.SequenceStepEnables()
        enables.tcc = False
        if sequence_config >> 4 & 1 != 0:
            enables.tcc = True
        enables.dss = False
        if sequence_config >> 3 & 1 != 0:
            enables.dss = True
        enables.msrc = False
        if sequence_config >> 2 & 1 != 0:
            enables.msrc = True
        enables.pre_range = False
        if sequence_config >> 6 & 1 != 0:
            enables.pre_range = True
        enables.final_range = False
        if sequence_config >> 7 & 1 != 0:
            enables.final_range = True
        return enables

    def getSequenceStepTimeouts(self, enables):
        timeouts = self.SequenceStepTimeouts()
        timeouts.pre_range_vcsel_period_pclks = self.getVcselPulsePeriod(VcselPeriodPreRange)
        timeouts.msrc_dss_tcc_mclks = self.readRegister(self._MSRC_CONFIG_TIMEOUT_MACROP) + 1
        timeouts.msrc_dss_tcc_us = self.timeoutMclksToMicroseconds(timeouts.msrc_dss_tcc_mclks, timeouts.pre_range_vcsel_period_pclks)
        timeouts.pre_range_mclks = self.decodeTimeout(self.readRegister(self._PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, 2))
        timeouts.pre_range_us = self.timeoutMclksToMicroseconds(timeouts.pre_range_mclks, timeouts.pre_range_vcsel_period_pclks)
        timeouts.final_range_vcsel_period_pclks = self.getVcselPulsePeriod(VcselPeriodFinalRange)
        timeouts.final_range_mclks = self.decodeTimeout(self.readRegister(self._FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, 2))
        if enables.pre_range:
            timeouts.final_range_mclks -= timeouts.pre_range_mclks
        timeouts.final_range_us = self.timeoutMclksToMicroseconds(timeouts.final_range_mclks, timeouts.final_range_vcsel_period_pclks)
        return timeouts

    def decodeTimeout(self, reg_val):
        return ((reg_val & 255) << ((reg_val & 65280) >> 8)) + 1

    def getVcselPulsePeriod(self, vcselPeriodType):
        if vcselPeriodType == VcselPeriodPreRange:
            return self.decodeVcselPeriod(self.readRegister(self._PRE_RANGE_CONFIG_VCSEL_PERIOD))
        else:
            if vcselPeriodType == VcselPeriodFinalRange:
                return self.decodeVcselPeriod(self.readRegister(self._FINAL_RANGE_CONFIG_VCSEL_PERIOD))
            return 255

    def decodeVcselPeriod(self, reg_val):
        val = reg_val + 1 << 1
        return val

    def timeoutMclksToMicroseconds(self, timeout_period_mclks, vcsel_period_pclks):
        macro_period_ns = self.calcMacroPeriod(vcsel_period_pclks)
        return (timeout_period_mclks * macro_period_ns + macro_period_ns / 2) / 1000

    def calcMacroPeriod(self, vcsel_period_pclks):
        val = (2304 * vcsel_period_pclks * 1655 + 500) / 1000
        return val

    def timeoutMicrosecondsToMclks(self, timeout_period_us, vcsel_period_pclks):
        macro_period_ns = self.calcMacroPeriod(vcsel_period_pclks)
        return (timeout_period_us * 1000 + macro_period_ns / 2) / macro_period_ns

    def encodeTimeout(self, timeout_mclks):
        ls_byte = 0
        ms_byte = 0
        if timeout_mclks > 0:
            ls_byte = timeout_mclks - 1
            while ls_byte & 0xFFFFFFF0 > 0:
                ls_byte >>= 1
                ms_byte += 1

            return ms_byte << 8 | ls_byte & 255
        else:
            return 0

    def performSingleRefCalibration(self, vhv_init_byte):
        self.writeRegister(self._SYSRANGE_START, 1 | vhv_init_byte)
        self.writeRegister(self._SYSTEM_INTERRUPT_CLEAR, 1)
        self.writeRegister(self._SYSRANGE_START, 0)
        return True

    def startContinuous(self, period_ms=0):
        self.writeRegister(128, 1)
        self.writeRegister(255, 1)
        self.writeRegister(0, 0)
        self.writeRegister(145, self._stop_variable)
        self.writeRegister(0, 1)
        self.writeRegister(255, 0)
        self.writeRegister(128, 0)
        if period_ms != 0:
            osc_calibrate_val = self.readRegister(OSC_CALIBRATE_VAL, 0)
            if osc_calibrate_val != 0:
                period_ms *= osc_calibrate_val
            self.writeRegister(self._SYSRANGE_START, 4)
        else:
            self._debugPrint('Starting Continuous Read!')
            self.writeRegister(self._SYSRANGE_START, 2)

    def stopContinuous(self):
        self.writeRegister(self._SYSRANGE_START, 1)
        self.writeRegister(255, 1)
        self.writeRegister(0, 0)
        self.writeRegister(145, 0)
        self.writeRegister(0, 1)
        self.writeRegister(255, 0)
        self._debugPrint('Stopping Continuous Read!')

    def setTimeout(self, timeout):
        self._io_timeout = timeout

    def getTimeout(self):
        return self._io_timeout

    def readRangeContinuousMillimeters(self):
        if self._io_timeout > 0:
            self._ioElapsedTime = 0
        start_time = time.time()
        while self.readRegister(self._RESULT_INTERRUPT_STATUS) & 7 == 0:
            ioElapsedTime = time.time() - start_time
            if ioElapsedTime > self._io_timeout * 0.001:
                self._debugPrint('Read timeout!')
                return 65535

        range = self.readRegister(self._RESULT_RANGE_STATUS + 10, 2)
        self.writeRegister(self._SYSTEM_INTERRUPT_CLEAR, 1)
        return range

    _stop_variable = 0
    _spad_count = 0
    _spad_type_is_aperture = False
    _measurement_timing_budget_us = 0
    _debug_enable = False
    _io_timeout = 0

    def readRegister(self, addr, numBytes=1):
        self.writeByte(addr)
        if numBytes == 1:
            return self.readByte()
        else:
            tmp = self.readMultipleBytes(numBytes)
            retval = tmp >> 8 & 255 | tmp << 8 & 65280
            return retval

    def writeRegister(self, register, value):
        self.writeMultipleBytes(2, register + (value << 8))

    def writeShort(self, register, short):
        tmp = short
        self.writeMultipleBytes(3, register + (tmp << 16))

    _ADDRESS_I2C_DEFAULT = 41
    _SYSRANGE_START = 0
    _SYSTEM_THRESH_HIGH = 12
    _SYSTEM_THRESH_LOW = 14
    _SYSTEM_SEQUENCE_CONFIG = 1
    _SYSTEM_RANGE_CONFIG = 9
    _SYSTEM_INTERMEASUREMENT_PERIOD = 4
    _SYSTEM_INTERRUPT_CONFIG_GPIO = 10
    _GPIO_HV_MUX_ACTIVE_HIGH = 132
    _SYSTEM_INTERRUPT_CLEAR = 11
    _RESULT_INTERRUPT_STATUS = 19
    _RESULT_RANGE_STATUS = 20
    _RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN = 188
    _RESULT_CORE_RANGING_TOTAL_EVENTS_RTN = 192
    _RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF = 208
    _RESULT_CORE_RANGING_TOTAL_EVENTS_REF = 212
    _RESULT_PEAK_SIGNAL_RATE_REF = 182
    _ALGO_PART_TO_PART_RANGE_OFFSET_MM = 40
    _I2C_SLAVE_DEVICE_ADDRESS = 138
    _MSRC_CONFIG_CONTROL = 96
    _PRE_RANGE_CONFIG_MIN_SNR = 39
    _PRE_RANGE_CONFIG_VALID_PHASE_LOW = 86
    _PRE_RANGE_CONFIG_VALID_PHASE_HIGH = 87
    _PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT = 100
    _FINAL_RANGE_CONFIG_MIN_SNR = 103
    _FINAL_RANGE_CONFIG_VALID_PHASE_LOW = 71
    _FINAL_RANGE_CONFIG_VALID_PHASE_HIGH = 72
    _FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = 68
    _PRE_RANGE_CONFIG_SIGMA_THRESH_HI = 97
    _PRE_RANGE_CONFIG_SIGMA_THRESH_LO = 98
    _PRE_RANGE_CONFIG_VCSEL_PERIOD = 80
    _PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI = 81
    _PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO = 82
    _SYSTEM_HISTOGRAM_BIN = 129
    _HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT = 51
    _HISTOGRAM_CONFIG_READOUT_CTRL = 85
    _FINAL_RANGE_CONFIG_VCSEL_PERIOD = 112
    _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI = 113
    _FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO = 114
    _CROSSTALK_COMPENSATION_PEAK_RATE_MCPS = 32
    _MSRC_CONFIG_TIMEOUT_MACROP = 70
    _SOFT_RESET_GO2_SOFT_RESET_N = 191
    _IDENTIFICATION_MODEL_ID = 192
    _IDENTIFICATION_REVISION_ID = 194
    _OSC_CALIBRATE_VAL = 248
    _GLOBAL_CONFIG_VCSEL_WIDTH = 50
    _GLOBAL_CONFIG_SPAD_ENABLES_REF_0 = 176
    _GLOBAL_CONFIG_SPAD_ENABLES_REF_1 = 177
    _GLOBAL_CONFIG_SPAD_ENABLES_REF_2 = 178
    _GLOBAL_CONFIG_SPAD_ENABLES_REF_3 = 179
    _GLOBAL_CONFIG_SPAD_ENABLES_REF_4 = 180
    _GLOBAL_CONFIG_SPAD_ENABLES_REF_5 = 181
    _GLOBAL_CONFIG_REF_EN_START_SELECT = 182
    _DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD = 78
    _DYNAMIC_SPAD_REF_EN_START_OFFSET = 79
    _POWER_MANAGEMENT_GO1_POWER_FORCE = 128
    _VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV = 137
    _ALGO_PHASECAL_LIM = 48
    _ALGO_PHASECAL_CONFIG_TIMEOUT = 48


if __name__ == '__main__':
    commMod = REVComm.REVcomm()
    commMod.openActivePort()
    REVModules = commMod.discovery()
    numHubs = len(REVModules)
    if numHubs < 1:
        sys.exit()
    else:
        print('Found ' + str(numHubs) + ' hubs.')
    sensor = REV2mSensor(commMod, 0, REVModules[0].getAddress(), False)
    isSensor = sensor.Is2mDistanceSensor()
    print(str(isSensor))
    if isSensor:
        sensor.initialize()
        for i in range(0, 50):
            print(sensor.readRangeContinuousMillimeters())

    else:
        print('No sensor found, quitting...')
    commMod.closeActivePort()