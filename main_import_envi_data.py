# Ver 07 oak
# import pip_system_certs
# import pip_system_certs.wrapt_requests

# import ssl
# import urllib3
# from urllib3 import request
# from request import certifi
# import urlopen

import requests
import tablib
import time
import pandas as pd
from urllib3.util.retry import Retry
import air_module

list_station_ids=[31, 40, 64, 76, 77, 78, 367, 338, 513, 32, 139]
city_dic=dict()
city_dic={
    31: 'Modiin Hinanit', # 31.90824, 35.00921
    32: 'Rehovot',
    40: 'Yad Rambam 1', # Obsolete ?
    64: 'Modiin', # 31.89295205, 34.99531847
    76: 'Carmei Yosef', # 31.84661321, 34.91951304
    77: 'Kfar Shmuel', # 31.89254, 34.92509 Non Active?
    78: 'Achisamach', # 31.9350483, 34.90873938
    367: 'Beit Hashmonai', # 31.88952134, 34.91520583
    338: 'Yad Rambam New', # 31.90413031, 34.89581407
    397: 'Mobile 7',
    513: 'Shchunat Haomanim', # 31.915084, 34.874771 (was #193)
    514: 'Nesher',
    32: 'Rehovot',
    139: 'Rishon'
}

# api_token = 'ApiToken 745356f0-5eee-4da8-aa71-b739f4acc081' # Alon
api_token = 'ApiToken 1cab20bf-0248-493d-aedc-27aa94445d15' # Bahat
# GET LIST OF ALL LOCATIONS ===================================================================
data_importer = air_module.data_importer(api_token)
data_processor = air_module.data_processor()
json_all_cities, json_all_cities_df = data_importer.stations()
data_plotter = air_module.data_plotter()

# Get and plot locations
stations_json, stations_gdf = data_importer.stations()
# data_plotter.plot_stations(stations_gdf)
data_plotter.plot_stations_folium(stations_gdf)
# READ SPECIFIC LOCATIONS FROM city_dic ===================================================================

t_crnt = time.time()
dt_sec=.5*60
t_next=0 #t_crnt+dt_sec
flag_prfrm=1
last_datetime='2021'
teledata = tablib.Dataset()
teledata_hdr = tablib.Dataset(headers=['Time','City','Id', 'parameter','value','status','valid'])
with open('output.csv', 'a+') as f:
    f.write(teledata_hdr.export('csv'))
while flag_prfrm:

    t_crnt = time.time()
    if t_crnt>t_next:
        print(t_crnt)
        for sttn_id in list_station_ids:
            json_by_city, json_by_city_df = data_importer.station_data(sttn_id)
            city_data_latest_json, city_data_latest_df = data_importer.station_latest_data(sttn_id)
            
            latest_data = city_data_latest_json["data"][0]
            datetime = latest_data["datetime"]
            if datetime!=last_datetime:
                # Parse data
                city_data_latest_df = data_processor.json_to_df(city_data_latest_json)

                # last_datetime=datetime
                for i in range(0, len(latest_data["channels"])):
                    print("name: ", latest_data["channels"][i]["name"], ", value:", latest_data["channels"][i]["value"])
                    city_name=city_dic[city_data_latest_json["stationId"]]
                    vec_values = (
                        datetime, city_name, city_data_latest_json["stationId"], latest_data["channels"][i]["name"],
                        latest_data["channels"][i]["value"], latest_data["channels"][i]["status"], latest_data["channels"][i]["valid"])
                    teledata.append(vec_values)

        # with open('output.xlsx', 'ab') as f:
        #     f.write(teledata.export('xlsx'))
                with open('output.csv', 'a+', newline='') as f:
                    f.write(teledata.export('csv'))
                teledata = tablib.Dataset()
        last_datetime = datetime
        t_next = t_crnt + dt_sec
    # t_crnt = time.time()
    time.sleep(10 * 60)
a=1

# import PyInstaller.__main__
# PyInstaller.__main__.run([
#     'import_envi_05.py',
#     '--onefile',
#     '--windowed'
# ])

#pyinstaller --onefile import_envi_05.py