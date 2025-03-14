"""
Create analyze reports of data read from the next station IDs:
# 7 - Beit Shemesh (line #5)
# 32 - rehovot (line #12)
# 64 - Modiin (line #26)
# 76 - Carmei Yosef (line #34)
# 78 Achisamach (line #35)
# 367 Beit Hashmonai (line #111)
# 397 Mobile (line #122)
# 338 Yad Rambam
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
"""
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.enum.section import WD_ORIENT
"""
# from Analize import AnalizeAirData
from air_module import data_analyzer as AnalizeAirData
from air_module import data_importer, data_plotter

plt.ion()










if __name__ == "__main__":
    city_codes = {
        31: 'Modiin Hinanit',  # 31.90824, 35.00921
        32: 'Rehovot',
        40: 'Yad Rambam 1',  # Obsolete ?
        64: 'Modiin',  # 31.89295205, 34.99531847
        76: 'Carmei Yosef',  # 31.84661321, 34.91951304
        77: 'Kfar Shmuel',  # 31.89254, 34.92509 Non Active?
        78: 'Achisamach',  # 31.9350483, 34.90873938
        367: 'Beit Hashmonai',  # 31.88952134, 34.91520583
        338: 'Yad Rambam New',  # 31.90413031, 34.89581407
        397: 'Mobile 7',
        513: 'Shchunat Haomanim',  # 31.915084, 34.874771 (was #193)
        514: 'Nesher',
        32: 'Rehovot',
        139: 'Rishon'
    }

    # log_filename = 'log_params.xlsx'
    csv_file_name = 'output.csv'
    # wake_up_time = datetime.today().replace(hour = 8, minute=20)

    analyze = AnalizeAirData()  # Create instance

    # GET ALL STATIONS DATA:
    # ==============================================
    if False:
        data_importer = data_importer()
        all_cities_json, all_cities_df = data_importer.get_stations_info()
    # analyze.plot_stations()

    # crnt_time = datetime.today()

    # if crnt_time > wake_up_time:
    # future_time = datetime.today() + dt.timedelta(days=1)  # Set the next time to wake up
    # yesterday = datetime.today() - dt.timedelta(days=1) # Calculate time window to analyze daily:
    # start_date_time_daily = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date_time_daily = datetime(2025, 1, 1, 0, 0, 0)
    # end_date_time_daily = yesterday.replace(hour=23, minute=59, second=0, microsecond=0)
    end_date_time_daily = datetime(2025, 3, 11, 0, 0, 0)
    T_window_back_sec = 2*24*60*60 # 14*24*60*60
    daily_report_file_name = 'Daily_' + str(start_date_time_daily).replace(':', '-').replace(' ', '-') + '_to_' + str(
        end_date_time_daily).replace(':', '-').replace(' ', '-')
    params_air = pd.read_excel('params_air.xlsx')
    params_air_tbl = pd.read_excel('params_air_TH.xlsx')

    # start_date_time_daily=datetime(2021, 1, 1, 0, 0, 0)
    # end_date_time_daily=datetime(2021, 12, 31, 23, 30, 0)

    start_timestamp = datetime.timestamp(start_date_time_daily)
    end_timestamp = datetime.timestamp(end_date_time_daily)

    target_datetime = pd.to_datetime("2025-01-17T16:00:00+02:00")

    print(f"Performing report at {datetime.today()} from {start_date_time_daily} to {end_date_time_daily}")

    """
    df, min_time_stamp_in_df, max_time_stamp_in_df, param_name_vec = analyze.read_csv2dataframe(csv_file_name,
                                                                                                start_timestamp,
                                                                                                end_timestamp)
    """
    gdf = analyze.read_csv2df(csv_file_name, start_datetime=start_date_time_daily, end_datetime=end_date_time_daily, export_to_excel=False)

    # plotter = data_plotter()
    # wd = gdf[gdf['Parameter'] == 'WD']['Value'].to_numpy()
    # plotter.plot_polar_wind_hist(wd)

    city_ids = gdf['Id'].unique()

    #======== RUN BY DEMAND ========================================================================================
    param_names_2_anlz_vec =  ['WD'] #['PM2.5','PM10'] # param_name_vec
    analyze.run_analyze_T(params_air_tbl, city_ids, gdf, 'israel_24hr', city_codes, param_names_2_anlz_vec, T_window_back_sec, True)

    #======== RUN SCHEDULED ========================================================================================
    param_name_vec = ['PM2.5','PM10']
    # Run every day analize in time windows of half an hour, hour, 8 hours:
    schedule.every().day.at("00:45").do(analyze.run_analyze_T, params_air_tbl, city_ids, gdf, 'israel_half_hr', city_codes, param_name_vec, T=24 * 60 * 60, flagPlot=False)
    schedule.every().day.at("00:46").do(analyze.run_analyze_T, params_air_tbl, city_ids, gdf, 'israel_hr', city_codes, param_name_vec, T=24 * 60 * 60, flagPlot=False)
    schedule.every().day.at("00:47").do(analyze.run_analyze_T, params_air_tbl, city_ids, gdf, 'israel_8hr', city_codes, param_name_vec, T=24 * 60 * 60, flagPlot=False)

    # Run the scheduled functions
    while True:
        schedule.run_pending()







