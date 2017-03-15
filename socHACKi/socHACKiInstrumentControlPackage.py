"""
Author: John Sochacki
This module is a collection of Instrument Control Classes
for test equiptment.  The implementations are specific to
what was needed at the time while remaining as general as possible.
"""

from comtypes import client
from comtypes import COMError

import datetime

import pandas as pd

from socHACKi.socHACKiUtilityPackage import AttrDict


class AgilentNetworkAnalyzer(object):
    """

    This is a wrapper the the ivi-com driver for agilent network analyzers.

    parameters
    ----

    INSTRUMENT_MODEL : String
                    'E5071C'
    INSTRUMENT_IP_ADDRESS : String
                    '172.26.128.119'
    ID_QUERY : Boolean
                    True
    RESET_UPON_INITIALIZATION : Boolean
                    True
    DEBUG_MODE : Boolean
                    False
    SIMULATION_MODE : Boolean
                    False

    """

    def __init__(self,
                 INSTRUMENT_MODEL,
                 INSTRUMENT_IP_ADDRESS,
                 ID_QUERY,
                 RESET_UPON_INITIALIZATION,
                 DEBUG_MODE,
                 SIMULATION_MODE):

        self.create_enums()
        self.INSTRUMENT_MODEL = INSTRUMENT_MODEL
        self.INSTRUMENT_IP_ADDRESS = INSTRUMENT_IP_ADDRESS
        self.ID_QUERY = ID_QUERY
        self.RESET_UPON_INITIALIZATION = RESET_UPON_INITIALIZATION
        self.DEBUG_MODE = DEBUG_MODE
        self.SIMULATION_MODE = SIMULATION_MODE

        self._NEXT_FREE_MEASUREMENT = 1

        self._ACTIVE_CHANNEL = 'Channel1'
        self._TIMEOUT_VALUE = 100
        self._TOTAL_MEASUREMENT_TIME = 0.1
        self._MEASUREMENT_TIME_SAMPLE_INTERVAL = 1

        if self.SIMULATION_MODE:
            self.OPTION_STRING = (
                'QueryInstrStatus={0}, '
                'Simulate={1}, '
                'DriverSetup=Model={2}').format(self.DEBUG_MODE,
                                                self.SIMULATION_MODE,
                                                self.INSTRUMENT_MODEL)
        else:
            self.OPTION_STRING = (
                'QueryInstrStatus={0}, '
                'Simulate={1}').format(self.DEBUG_MODE,
                                       self.SIMULATION_MODE)

        try:
            self.network_analyzer = client.CreateObject('AgilentNA.AgilentNA')
        except OSError as e:
            print(e, '\n')
            print('You are seeing this error because you do no have the '
                  'necessary IVI-COM and/or Keysight Libraries installed.')
        except NameError as e:
            print(e, '\n')
            print('You are seeing this error because you do no have the '
                  'comtypes module installed.  Please pip or conda '
                  'install version 1.1.2 of this package')

        try:
            self.network_analyzer.Initialize('TCPIP::{0}::INSTR'
                                        .format(self.INSTRUMENT_IP_ADDRESS),
                                        self.ID_QUERY,
                                        self.RESET_UPON_INITIALIZATION,
                                        self.OPTION_STRING)
        except COMError as e:
            print(e)
            print('\nYou are seeing this error because you have typed the wrong IP'
                  ' address or the instrument that you are trying to connect to'
                  ' is unavailable for some reason')
        else:
            pass

        if not self.network_analyzer.Initialized:
            print('There is an instrument at that address but it is not '
                  'accepting connections. Please check your setup and try again')
            raise SystemExit('User needs to go look at instrument and figure out why')

        if not self.INSTRUMENT_MODEL == self.network_analyzer.Identity.InstrumentModel:
            print('You have connected to an instrument that you did not intend '
                  'to connect to.  Please check your setup and try again')
            raise SystemExit('User needs to verify make and model of connecting device')

        self.IFormattedIO488 = self.network_analyzer.System.IO

    def disconnect(self):
        self.network_analyzer.Close()

    def send_scpi_command(self, Command):
        self.IFormattedIO488.WriteString(Command)
        try:
            Result = self.IFormattedIO488.ReadString()
        except COMError as e:
            Result = None
        return Result

    @property
    def ACTIVE_CHANNEL(self):
        if self._ACTIVE_CHANNEL == 'Channel1':
            return 'Channel1'
        elif self._ACTIVE_CHANNEL == 'Channel2':
            return 'Channel2'
        else:
            return 'Error in active channel'

    @ACTIVE_CHANNEL.setter
    def ACTIVE_CHANNEL(self, NewChannel):
        if 0 < int(NewChannel) < 3:
            if int(NewChannel) == 1:
                self._ACTIVE_CHANNEL = 'Channel1'
            else:
                self._ACTIVE_CHANNEL = 'Channel2'
        else:
            return ('Error, only integer values are supported and only '
                    'channels 1 and 2 are supported with this interface')

    @property
    def TIMEOUT_VALUE(self):
        return self._TIMEOUT_VALUE

    @TIMEOUT_VALUE.setter
    def TIMEOUT_VALUE(self, NewValue):
        self._TIMEOUT_VALUE = NewValue

    @property
    def TOTAL_MEASUREMENT_TIME(self):
        return self._TOTAL_MEASUREMENT_TIME

    @TOTAL_MEASUREMENT_TIME.setter
    def TOTAL_MEASUREMENT_TIME(self, NewValue):
        self._TOTAL_MEASUREMENT_TIME = NewValue

    @property
    def MEASUREMENT_TIME_SAMPLE_INTERVAL(self):
        return self._MEASUREMENT_TIME_SAMPLE_INTERVAL

    @MEASUREMENT_TIME_SAMPLE_INTERVAL.setter
    def MEASUREMENT_TIME_SAMPLE_INTERVAL(self, NewValue):
        self._MEASUREMENT_TIME_SAMPLE_INTERVAL = NewValue

    @property
    def measurement_stimulus(self):
        Channel = self.ACTIVE_CHANNEL
        if_bandwidth = self.network_analyzer.Channels.Item(Channel).IFBandwidth
        number_or_points = self.network_analyzer.Channels.Item(Channel).Points
        f_low = self.network_analyzer.Channels.Item(Channel).StimulusRange.Start
        f_high = self.network_analyzer.Channels.Item(Channel).StimulusRange.Stop
        f_step_size = (f_high - f_low) / (number_or_points - 1)
        time_per_measurement = self.network_analyzer.Channels.Item(Channel).SweepTime
        return {
                'IFBandwidth': if_bandwidth,
                'NumberOfPoints': number_or_points,
                'FLow': f_low,
                'FHigh': f_high,
                'FStepSize': f_step_size,
                'TimePerMeasurement': time_per_measurement
                }

    @measurement_stimulus.setter
    def measurement_stimulus(self, measurement_settings):
        Channel = self.ACTIVE_CHANNEL
        if measurement_settings.get('IFBandwidth') and \
                measurement_settings.get('NumberOfPoints') and \
                measurement_settings.get('FLow') and \
                measurement_settings.get('FHigh'):
            IFBandwidth = measurement_settings['IFBandwidth']
            NumberOfPoints = measurement_settings['NumberOfPoints']
            FLow = measurement_settings['FLow']
            FHigh = measurement_settings['FHigh']
            self.network_analyzer.Channels.Item(Channel).IFBandwidth = \
                int(IFBandwidth)
            self.network_analyzer.Channels.Item(Channel).Points = \
                int(NumberOfPoints)
            self.network_analyzer.Channels.Item(Channel).StimulusRange.Start = \
                int(FLow)
            self.network_analyzer.Channels.Item(Channel).StimulusRange.Stop = \
                int(FHigh)
        else:
            print('Insufficient settings provided. '
                    'You must provide: \n'
                    'IFBandwidth\nNumberOfPoints\nFLow\nFHigh')

    def setup_remote_single_trigger(self):
        Channel = self.ACTIVE_CHANNEL
        self.network_analyzer.Channels.Item(Channel).TriggerMode = \
            self.enums.AgilentNATriggerModeEnum.AgilentNATriggerModeContinuous
        self.network_analyzer.Trigger.Source = \
            self.enums.AgilentNATriggerSourceEnum.AgilentNATriggerSourceBus

    @property
    def NEXT_FREE_MEASUREMENT(self):
        return self._NEXT_FREE_MEASUREMENT

    def setup_measurements_logmag_expanded_phase_s2p(self):
        Channel = self.ACTIVE_CHANNEL
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement1').Create(1, 1)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement1').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementLogMag
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement2').Create(1, 1)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement2').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementUPhase
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement3').Create(2, 1)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement3').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementLogMag
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement4').Create(2, 1)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement4').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementUPhase
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement5').Create(1, 2)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement5').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementLogMag
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement6').Create(1, 2)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement6').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementUPhase
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement7').Create(2, 2)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement7').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementLogMag
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement8').Create(2, 2)
        self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement8').Format = \
            self.enums.AgilentNAMeasurementFormatEnum.AgilentNAMeasurementUPhase
        self._NEXT_FREE_MEASUREMENT = 9

    def take_logmag_exphase_s2p_measurement(self):
        Channel = self.ACTIVE_CHANNEL
        Timeout = self.TIMEOUT_VALUE
        s_parameters = {}
        self.network_analyzer.Channels.Item(Channel).TriggerSweep(Timeout)
        s_parameters['frequency'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement1').FetchX()
        s_parameters['S11_LOG_MAG'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement1').FetchFormatted()
        s_parameters['S11_EXP'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement2').FetchFormatted()
        s_parameters['S21_LOG_MAG'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement3').FetchFormatted()
        s_parameters['S21_EXP'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement4').FetchFormatted()
        s_parameters['S12_LOG_MAG'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement5').FetchFormatted()
        s_parameters['S12_EXP'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement6').FetchFormatted()
        s_parameters['S22_LOG_MAG'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement7').FetchFormatted()
        s_parameters['S22_EXP'] = \
            self.network_analyzer.Channels.Item(Channel).Measurements.Item('Measurement8').FetchFormatted()
        return s_parameters

    def take_phase_vs_time_measurement(self):
        # Loops speed is 100ms from here
        MEASUREMENT_TIME_IN_SECONDS = self.TOTAL_MEASUREMENT_TIME * 60
        MEASUREMENT_TIME_STEP_IN_US = self.MEASUREMENT_TIME_SAMPLE_INTERVAL * 1000000
        time_vector = [0]
        current_phase_df = []
        cumulative_phase_df = []
        measurement_start_time = []
        next_measurement_time = []
        S = []
        basedf = []
        count = 0

        measurement_start_time = datetime.datetime.now()
        S = self.take_logmag_exphase_s2p_measurement()
        next_measurement_time = measurement_start_time + datetime.timedelta(microseconds=MEASUREMENT_TIME_STEP_IN_US)
        basedf = pd.DataFrame.from_dict(S).set_index('frequency')
        cumulative_phase_df = \
            pd.DataFrame.from_dict(S).set_index('frequency').drop(
                                [basedf.S11_LOG_MAG.name,
                                 basedf.S21_LOG_MAG.name,
                                 basedf.S12_LOG_MAG.name,
                                 basedf.S22_LOG_MAG.name,
                                 basedf.S11_EXP.name,
                                 basedf.S12_EXP.name,
                                 basedf.S22_EXP.name],
                                axis=1,
                                inplace=False
                                  ).rename_axis({'S21_EXP': time_vector[count]}, axis=1).transpose()

        current_time_count = datetime.timedelta.total_seconds(datetime.datetime.now() - measurement_start_time)
        count = count + 1
        # To here
        while (current_time_count <= MEASUREMENT_TIME_IN_SECONDS):
            if datetime.datetime.now() >= next_measurement_time:
                S = self.take_logmag_exphase_s2p_measurement()
                time_vector.extend([datetime.timedelta.total_seconds(next_measurement_time-measurement_start_time)])
                next_measurement_time = next_measurement_time + datetime.timedelta(microseconds=MEASUREMENT_TIME_STEP_IN_US)
                current_phase_df = []
                current_phase_df = \
                    pd.DataFrame.from_dict(S).set_index('frequency').drop(
                                [basedf.S11_LOG_MAG.name,
                                 basedf.S21_LOG_MAG.name,
                                 basedf.S12_LOG_MAG.name,
                                 basedf.S22_LOG_MAG.name,
                                 basedf.S11_EXP.name,
                                 basedf.S12_EXP.name,
                                 basedf.S22_EXP.name],
                                axis=1,
                                inplace=False
                                  ).rename_axis({'S21_EXP': time_vector[count]}, axis=1).transpose()

                cumulative_phase_df = cumulative_phase_df.append(current_phase_df)
                count = count + 1
            current_time_count = datetime.timedelta.total_seconds(datetime.datetime.now() - measurement_start_time)
        return (S, cumulative_phase_df)

    def create_enums(self):
        AgilentNAErrorCodesEnum = \
            {
             'E_AGILENTNA_PERSONALITY_NOT_ACTIVE': 2147762705,
             'E_AGILENTNA_PERSONALITY_NOT_INSTALLED': 2147762706,
             'E_AGILENTNA_PERSONALITY_NOT_LICENSED': 2147762707,
             'E_AGILENTNA_IO_GENERAL': 2147762708,
             'E_AGILENTNA_IO_TIMEOUT': 2147762709,
             'E_AGILENTNA_MODEL_NOT_SUPPORTED': 2147762710,
             'E_AGILENTNA_WRAPPED_DRIVER_ERROR': 2147762712,
             'E_AGILENTNA_MAX_TIME_EXCEEDED': 2147484183,
             'E_AGILENTNA_ANY_STRING': 2147762713
             }
        AgilentNALimitTypeEnum = \
            {
             'AgilentNALimitTypeOff': 0,
             'AgilentNALimitTypeMaximum': 1,
             'AgilentNALimitTypeMinimum': 2
             }
        AgilentNAMarkerSearchTypeEnum = \
            {
             'AgilentNAMarkerSearchTypeTarget': 0,
             'AgilentNAMarkerSearchTypeTargetLeft': 1,
             'AgilentNAMarkerSearchTypeTargetRight': 2,
             'AgilentNAMarkerSearchTypeMax': 3,
             'AgilentNAMarkerSearchTypeMin': 4,
             'AgilentNAMarkerSearchTypePeak': 5,
             'AgilentNAMarkerSearchTypePeakLeft': 6,
             'AgilentNAMarkerSearchTypePeakRight': 7
             }
        AgilentNAMeasurementFormatEnum = \
            {
             'AgilentNAMeasurementLogMag': 0,
             'AgilentNAMeasurementLinMag': 1,
             'AgilentNAMeasurementPhase': 2,
             'AgilentNAMeasurementGroupDelay': 3,
             'AgilentNAMeasurementSWR': 4,
             'AgilentNAMeasurementReal': 5,
             'AgilentNAMeasurementImag': 6,
             'AgilentNAMeasurementPolar': 7,
             'AgilentNAMeasurementSmith': 8,
             'AgilentNAMeasurementSLinear': 9,
             'AgilentNAMeasurementSLogarithmic': 10,
             'AgilentNAMeasurementSComplex': 11,
             'AgilentNAMeasurementSAdmittance': 12,
             'AgilentNAMeasurementPLinear': 13,
             'AgilentNAMeasurementPLogarithmic': 14,
             'AgilentNAMeasurementUPhase': 15,
             'AgilentNAMeasurementPPhase': 16
             }
        AgilentNAMeasurementStatisticTypeEnum = \
            {
             'AgilentNAMeasurementStatisticTypeMean': 0,
             'AgilentNAMeasurementStatisticTypeStandardDeviation': 1,
             'AgilentNAMeasurementStatisticTypePeakToPeak': 2
             }
        AgilentNAMeasurementTraceMathEnum = \
            {
             'AgilentNAMeasurementTraceMathNone': 0,
             'AgilentNAMeasurementTraceMathDivided': 1,
             'AgilentNAMeasurementTraceMathMultiplied': 2,
             'AgilentNAMeasurementTraceMathSubtracted': 3,
             'AgilentNAMeasurementTraceMathAdded': 4
             }
        AgilentNASetFromMarkerValueEnum = \
            {
             'AgilentNAMarkerValueStart': 0,
             'AgilentNAMarkerValueStop': 1,
             'AgilentNAMarkerValueCenter': 2,
             'AgilentNAMarkerValueCW': 3,
             'AgilentNAMarkerValueReferenceLevel': 4,
             'AgilentNAMarkerValueElectricalDelay': 5
            }
        AgilentNASRQReasonEnum = \
            {
             'AgilentNASRQReasonStbErroQue': 1,
             'AgilentNASRQReasonEsrOPC': 2,
             'AgilentNASRQReasonEsrExecutionError': 4,
             'AgilentNASRQReasonEsrCommandError': 8,
             'AgilentNASRQReasonQuesLimitFail': 16
            }
        AgilentNAStatusRegisterEnum = \
            {
             'AgilentNAStatusRegisterStatusByte': 0,
             'AgilentNAStatusRegisterStandardEvent': 1,
             'AgilentNAStatusRegisterOperation': 2,
             'AgilentNAStatusRegisterQuestionable': 3,
             'AgilentNAStatusRegisterQuesLimit': 4
            }
        AgilentNASweepModeEnum = \
            {
             'AgilentNASweepModeSwept': 0,
             'AgilentNASweepModeStepped': 1,
             'AgilentNASweepModeFastStepped': 2,
             'AgilentNASweepModeFastSwept': 3
            }
        AgilentNASweepTypeEnum = \
            {
             'AgilentNASweepTypeLinFrequency': 0,
             'AgilentNASweepTypeLogFrequency': 1,
             'AgilentNASweepTypeSegment': 2,
             'AgilentNASweepTypePower': 3,
             'AgilentNASweepTypeCWTime': 4
            }
        AgilentNATriggerModeEnum = \
            {
             'AgilentNATriggerModeHold': 1,
             'AgilentNATriggerModeContinuous': 0
            }

        AgilentNATriggerSourceEnum = \
            {
             'AgilentNATriggerSourceInternal': 0,
             'AgilentNATriggerSourceExternal': 1,
             'AgilentNATriggerSourceBus': 2,
             'AgilentNATriggerSourceManual': 3
            }
        SParameterEnum = \
            {
             'S12': '+1,+2\n',
             'S13': '+1,+3\n',
             'S14': '+1,+4\n',
             'S23': '+2,+3\n',
             'S24': '+2,+4\n',
             'S34': '+3,+4\n'
            }
        self.enums = AttrDict()
        self.enums.AgilentNAErrorCodesEnum = \
            AttrDict(AgilentNAErrorCodesEnum)
        self.enums.AgilentNALimitTypeEnum = \
            AttrDict(AgilentNALimitTypeEnum)
        self.enums.AgilentNAMarkerSearchTypeEnum = \
            AttrDict(AgilentNAMarkerSearchTypeEnum)
        self.enums.AgilentNAMeasurementFormatEnum = \
            AttrDict(AgilentNAMeasurementFormatEnum)
        self.enums.AgilentNAMeasurementStatisticTypeEnum = \
            AttrDict(AgilentNAMeasurementStatisticTypeEnum)
        self.enums.AgilentNAMeasurementTraceMathEnum = \
            AttrDict(AgilentNAMeasurementTraceMathEnum)
        self.enums.AgilentNASetFromMarkerValueEnum = \
            AttrDict(AgilentNASetFromMarkerValueEnum)
        self.enums.AgilentNASRQReasonEnum = \
            AttrDict(AgilentNASRQReasonEnum)
        self.enums.AgilentNAStatusRegisterEnum = \
            AttrDict(AgilentNAStatusRegisterEnum)
        self.enums.AgilentNASweepModeEnum = \
            AttrDict(AgilentNASweepModeEnum)
        self.enums.AgilentNASweepTypeEnum = \
            AttrDict(AgilentNASweepTypeEnum)
        self.enums.AgilentNATriggerModeEnum = \
            AttrDict(AgilentNATriggerModeEnum)
        self.enums.AgilentNATriggerSourceEnum = \
            AttrDict(AgilentNATriggerSourceEnum)
        self.enums.SParameterEnum = \
            AttrDict(SParameterEnum)
