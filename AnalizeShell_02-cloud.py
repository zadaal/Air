"""
Create analyze reports of data read from stations
"""

import csv
import os.path
import schedule
from datetime import datetime
from datetime import date
import datetime as dt
import time
import requests
import tablib
import pandas as pd
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.enum.section import WD_ORIENT
from Analize import AnalizeAirData
plt.ion()


city_codes={
    31: 'Modiin Hinanit', # 31.90824, 35.00921
    40: 'Yad Rambam 1', # Obsolete ?
    64: 'Modiin', # 31.89295205, 34.99531847
    76: 'Carmei Yosef', # 31.84661321, 34.91951304
    77: 'Kfar Shmuel', # 31.89254, 34.92509 Non Active?
    78: 'Achisamach', # 31.9350483, 34.90873938
    367: 'Beit Hashmonai', # 31.88952134, 34.91520583
    338: 'Yad Rambam New', # 31.90413031, 34.89581407
    513: 'Shchunat Haomanim', # 31.915084, 34.874771 (was #193)
    32: 'Rehovot',
    139: 'Rishon'
}

# log_filename = 'log_params.xlsx'
csv_file_name = 'output.csv'


analyze = AnalizeAirData() # Create instance



start_date_time_daily = datetime(2023, 3, 11, 0, 0, 0)
end_date_time_daily = datetime(2023, 3, 15, 13, 30, 0)
daily_report_file_name = 'Daily_' + str(start_date_time_daily).replace(':', '-').replace(' ','-') + '_to_' + str(end_date_time_daily).replace(':', '-').replace(' ', '-')
params_air=pd.read_excel('params_air.xlsx')
params_air_tbl=pd.read_excel('params_air_TH.xlsx')



start_timestamp=datetime.timestamp(start_date_time_daily)
end_timestamp=datetime.timestamp(end_date_time_daily)

print(f"Performing report at {datetime.today()} from {start_date_time_daily} to {end_date_time_daily}")

df, min_time_stamp_in_df, max_time_stamp_in_df, param_name_vec = analyze.read_csv2dataframe(csv_file_name, start_timestamp, end_timestamp)
city_ids = pd.unique(df.Id)


def run_analyze_T(params_air_tbl, city_ids, df, timeWindowStr, city_codes, param_name_vec, T, flagPlot):
    # Get the time window of T seconds
    start_time = datetime.now() - dt.timedelta(seconds=T)
    df_window = df[df['date_time'] >= start_time]
    if timeWindowStr == 'israel_half_hr':
        timeWindowSec = 0.5 * 60 * 60
    elif timeWindowStr == 'israel_hr':
        timeWindowSec = 1 * 60 * 60
    elif timeWindowStr == 'israel_24hr':
        timeWindowSec = 24 * 60 * 60
    elif timeWindowStr == 'israel_8hr':
        timeWindowSec = 8 * 60 * 60
    elif timeWindowStr == 'israel_yr':
        timeWindowSec = 365 * 24 * 60 * 60
    for crnt_param in param_name_vec:
        thresholdValue = params_air_tbl.loc[params_air_tbl['param'] == crnt_param][timeWindowStr].values[0]
        for crnt_city in city_ids:
            # Run the analysis on the time window
            city_name = city_codes.get(crnt_city, 'default_value')
            timestamps, values = analyze.moving_average_threshold(df_window, timeWindow = timeWindowSec, city = city_name, param = crnt_param, threshold = thresholdValue, flagPlot=flagPlot)
            plt.ion()
            # Save the result to a log file
            if len(values) != 0:
                log_df = pd.DataFrame({'Report Date': [datetime.now().strftime("%Y-%m-%d")],
                                       'Report Time': [datetime.now().strftime("%H:%M:%S")],
                                       'Time Window': timeWindowStr,
                                       'Station Name': city_name,
                                       'Parameter': crnt_param,
                                       'Time Stamps': [timestamps],
                                       'Values': [values],
                                       'TH Value': [thresholdValue]})
                if os.path.isfile(log_filename):
                    existing_data = pd.read_excel(log_filename)
                    new_data = pd.concat([existing_data, log_df], ignore_index=True)
                    new_data.to_excel(log_filename, index=False)

                    # # Append data to an existing Excel file with openpyxl
                    # with pd.ExcelWriter(log_filename, engine='openpyxl', mode='a') as writer:
                    #     log_df.to_excel(writer, sheet_name='Sheet2')
                else:
                    log_df.to_excel(log_filename, index=False)
                    # # Create a new Excel file with xlsxwriter
                    # with pd.ExcelWriter(log_filename, engine='xlsxwriter') as writer:
                    #     log_df.to_excel(writer, sheet_name='Sheet1')

                # return timestamps, values



#======== RUN BY DEMAND ========================================================================================
param_names_2_anlz_vec =  ['PM2.5','PM10'] #['PM2.5','PM10'] # param_name_vec
analyze.run_analyze_T(params_air_tbl, city_ids, df, 'israel_24hr', city_codes, param_names_2_anlz_vec, T = 11*24*60*60, flagPlot=True)

#======== RUN SCHEDULED ========================================================================================

# Run every day analize in time windows of half an hour, hour, 8 hours:
schedule.every().day.at("00:45").do(analyze.run_analyze_T, params_air_tbl, city_ids, df, 'israel_half_hr', city_codes, param_name_vec, T=24*60*60, flagPlot=False)
schedule.every().day.at("00:46").do(analyze.run_analyze_T, params_air_tbl, city_ids, df, 'israel_hr', city_codes, param_name_vec, T=24*60*60, flagPlot=False)
schedule.every().day.at("00:47").do(analyze.run_analyze_T, params_air_tbl, city_ids, df, 'israel_8hr', city_codes, param_name_vec, T=24*60*60, flagPlot=False)

# Run the scheduled functions
while True:
    schedule.run_pending()

