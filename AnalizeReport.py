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
from datetime import datetime
from datetime import date
import datetime as dt
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.enum.section import WD_ORIENT
from Analize import AnalizeAirData
plt.ion()


city_dic={
    31: 'Modiin Hinanit', # 31.90824, 35.00921
    40: 'Yad Rambam 1', # Obsolete ?
    64: 'Modiin', # 31.89295205, 34.99531847
    76: 'Carmei Yosef', # 31.84661321, 34.91951304
    77: 'Kfar Shmuel', # 31.89254, 34.92509 Non Active?
    78: 'Achisamach', # 31.9350483, 34.90873938
    367: 'Beit Hashmonai', # 31.88952134, 34.91520583
    338: 'Yad Rambam New', # 31.90413031, 34.89581407
    513: 'Shchunat Haomanim' # 31.915084, 34.874771 (was #193)
}

csv_file_name = 'output.csv'
wake_up_time = datetime.today().replace(hour = 8, minute=20)

analyze = AnalizeAirData()
while 1:
    crnt_time = datetime.today()


    if crnt_time > wake_up_time:
        future_time = datetime.today() + dt.timedelta(days=1)  # Set the next time to wake up
        yesterday = datetime.today() - dt.timedelta(days=1) # Calculate time window to analyze daily:
        start_date_time_daily = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date_time_daily = yesterday.replace(hour=23, minute=59, second=0, microsecond=0)
        daily_report_file_name = 'Daily_' + str(start_date_time_daily).replace(':', '-').replace(' ','-') + '_to_' + str(end_date_time_daily).replace(':', '-').replace(' ', '-')
        params_air=pd.read_excel('params_air.xlsx')

        # start_date_time_daily=datetime(2021, 1, 1, 0, 0, 0)
        # end_date_time_daily=datetime(2021, 12, 31, 23, 30, 0)

        start_timestamp=datetime.timestamp(start_date_time_daily)
        end_timestamp=datetime.timestamp(end_date_time_daily)

        print(f"Performing report at {datetime.today()} from {start_date_time_daily} to {end_date_time_daily}")

        df, min_time_stamp_in_df, max_time_stamp_in_df, param_name_vec = analyze.read_csv2dataframe(csv_file_name, start_timestamp, end_timestamp)

        t_win_vec_daily=np.arange(start_timestamp,end_timestamp+24*60*60,24*60*60)
        t_win_vec_weekly=np.arange(start_timestamp,end_timestamp,7*24*60*60)

        df_daily=pd.DataFrame([],columns= ('timestamp_strt','timestamp_end','datetime_strt','datetime_end','City','Id','param','mean_val','std_val','median_val','min','max','date_time'))
        df_weekly=pd.DataFrame([],columns= ('timestamp_strt','timestamp_end','datetime_strt','datetime_end','City','Id','param','mean_val','std_val','median_val','min','max','date_time'))

        for crnt_param in param_name_vec:
            for crnt_city in pd.unique(df.Id):
                for i_t_daily in range(0,len(t_win_vec_daily)-1):
                    crnt_daily_data=df[(df.Timestamp>=t_win_vec_daily[i_t_daily]) & (df.Timestamp<t_win_vec_daily[i_t_daily+1]) & (df.param==crnt_param) & (df.Id==crnt_city) & (df.valid=='True')]
                    if not(crnt_daily_data.empty):
                        data_vec=analyze.calc_period_data(crnt_daily_data, crnt_city, crnt_param)

                        crnt_df_daily=pd.DataFrame([data_vec],columns= ('timestamp_strt','timestamp_end','datetime_strt','datetime_end','City','Id','param','mean_val','std_val','median_val','min','max','date_time'))
                        df_daily=df_daily.append(crnt_df_daily)
                        b=1
                for i_t_weekly in range(0,len(t_win_vec_weekly)-1):
                    crnt_weekly_data = df[
                        (df.Timestamp > t_win_vec_daily[i_t_weekly]) & (df.Timestamp <= t_win_vec_daily[i_t_weekly + 1]) & (
                                    df.param == crnt_param) & (df.Id == crnt_city) & (df.valid == 'True')]
                    if not (crnt_weekly_data.empty):
                        data_vec = analyze.calc_period_data(crnt_weekly_data, crnt_city, crnt_param)
                        crnt_df_weekly = pd.DataFrame([data_vec], columns=(
                        'timestamp_strt', 'timestamp_end', 'datetime_strt','datetime_end','City', 'Id', 'param', 'mean_val', 'std_val', 'median_val', 'min', 'max','date_time'))
                        df_weekly = df_weekly.append(crnt_df_weekly)

                        c=1

        # filter df with rellevant time window:
        df = df[(df.Timestamp >= start_timestamp)  & (df.Timestamp <= end_timestamp)]

        # Plot results in dataframes:
        params_by_time_half_hr = params_air[["param","israel_half_hr","who_half_hr","eu_half_hr"]]
        analyze.plot_by_city(param_name_vec, df, city_codes, 'value', params_by_time_half_hr,'Half Hour',daily_report_file_name)

        # params_by_time_daily = params_air[["param","israel_24hr","who_24hr","eu_24hr"]]
        # analyze.plot_by_city(param_name_vec, df_daily, city_codes, 'max', params_by_time_daily,'24hr max','Weekly')

        crnt_time = datetime.today()  # Calculate current time
        time_to_sleep = future_time - crnt_time  # Calculate time to sleep until wakeup
        time_to_sleep_sec = time_to_sleep.seconds
        time.sleep(time_to_sleep_sec)

        a=1

