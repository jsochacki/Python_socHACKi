# %%
import datetime

import pandas as pd

from socHACKi.socHACKiInstrumentControlPackage import AgilentNetworkAnalyzer
from socHACKi.socHACKiUtilityPackage import ExcelHandler as xlh

import matplotlib.pyplot as plt

# %%

# Instrument Information
INSTRUMENT_MODEL = 'E5071C'
INSTRUMENT_IP_ADDRESS = '172.26.128.119'
ID_QUERY = True
RESET_UPON_INITIALIZATION = True
DEBUG_MODE = False
SIMULATION_MODE = False

INSTRUMENT_USB_ID = '2391::3337::MY46214933'
INSTRUMENT_USER_NAME = 'uname'
INSTRUMENT_USER_PSWD = 'psswd'

# Setup for Measurements
MEASUREMENT_TIME_IN_MINUTES = 15
MEASUREMENT_TIME_STEP_IN_SECONDS = 5

# Setup for Plotting
PLOT_FREQUENCIES = [10000000.0, 100000000.0]
PLOT_FREQUENCIES.extend([float(x) for x in range(1000000000, 21000000000, 1000000000)])

# Setup for the excel file export
RESULTS_FILE_PATH = 'Z:\\path\\to\\your\\desired\\folder'
FILE_NAME = 'Desired_Name_Of_File.xlsx'
SHEET_NAME = 'Column_Header_Is_Frequency_Hz'
START_COLUMN = 1
# %%
# Initialize the instrument and make the COM
na = AgilentNetworkAnalyzer(INSTRUMENT_MODEL,
                            INSTRUMENT_IP_ADDRESS,
                            ID_QUERY,
                            RESET_UPON_INITIALIZATION,
                            DEBUG_MODE,
                            SIMULATION_MODE)
# %%
# Recall a local state for ease of setup (skip recal, etc...)
na.network_analyzer.System.RecallState('C:\\path\\to\\state\\File.STA')
# %%
# Make sure that I can save the s parameter measurements that I want to
try:
    na.send_scpi_command(':MMEM:STOR:SNP:TYPE:S2P 1,2')
    assert(na.send_scpi_command(':MMEM:STOR:SNP:TYPE:S2P?') == na.enums.SParameterEnum.S12)
except AssertionError as e:
    print('Could not set the sparameter file format')
# %%
# Modify the setting based on changes over time (tuned settings)
na.ACTIVE_CHANNEL = 1
na.TIMEOUT_VALUE = 100
na.TOTAL_MEASUREMENT_TIME = MEASUREMENT_TIME_IN_MINUTES
na.MEASUREMENT_TIME_SAMPLE_INTERVAL = MEASUREMENT_TIME_STEP_IN_SECONDS
measurement_settings = na.measurement_stimulus
measurement_settings['IFBandwidth'] = 500.0
na.measurement_stimulus = measurement_settings
measurement_settings = na.measurement_stimulus
print(measurement_settings)
# %%
# Set up the measurements
na.setup_measurements_logmag_expanded_phase_s2p()

# Setup the Trigger
na.setup_remote_single_trigger()
# %%
# Take the measurement
S, cumulative_phase_df = na.take_phase_vs_time_measurement()
# %%
# Setup for data extraction (reduced/focused data set)
indicies_to_use = [index for index, value in enumerate(S['frequency']) if value in PLOT_FREQUENCIES]
reduced_set_cumulative_phase_df = \
    cumulative_phase_df.transpose().iloc[indicies_to_use].transpose()
reduced_set_cumulative_phase_df

reduced_set_cumulative_phase_delta_df = \
    reduced_set_cumulative_phase_df - reduced_set_cumulative_phase_df.loc[0]

reduced_set_cumulative_phase_delta_df.index.name = 'Time (s)'
# %%
# plot for inspection prior to save
time_vector = list(cumulative_phase_df.index.values)
Index = -1
plt.plot(time_vector, reduced_set_cumulative_phase_delta_df.transpose().loc[PLOT_FREQUENCIES[Index]], 'ro',
         time_vector, reduced_set_cumulative_phase_delta_df.transpose().loc[PLOT_FREQUENCIES[Index]], 'k', linewidth=2)
plt.axis([0,
          max(reduced_set_cumulative_phase_delta_df.index.values),
          min(reduced_set_cumulative_phase_delta_df[PLOT_FREQUENCIES[Index]].values),
          max(reduced_set_cumulative_phase_delta_df[PLOT_FREQUENCIES[Index]].values)])
plt.xlabel('Test Time in Seconds')
plt.ylabel('Phase Change in Degrees')
plt.title('Phase Change vs Time')
plt.grid(True)
plt.show()
# %%

# Save to excel file
xlh.save_to_excel(reduced_set_cumulative_phase_delta_df,
                  RESULTS_FILE_PATH,
                  FILE_NAME,
                  SHEET_NAME,
                  START_COLUMN)
# %%
na.disconnect()
