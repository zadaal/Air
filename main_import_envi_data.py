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
# Instantiate your modules (adjust as needed)
data_importer = air_module.data_importer(api_token)
data_processor = air_module.data_processor()
data_plotter = air_module.data_plotter()

# Fetch and plot station locations
all_cities_json, all_cities_df = data_importer.get_stations_info()
if False:
    data_plotter.plot_stations_folium(all_cities_df)

# Prepare for data collection
flag_prfrm = True
last_datetime = '2021'

# Initialize tablib dataset with header row
teledata_hdr = tablib.Dataset(headers=['Time', 'City', 'Id', 'parameter', 'value', 'status', 'valid'])
with open('output.csv', 'a+') as f:
    f.write(teledata_hdr.export('csv'))

while flag_prfrm:
    # Current timestamp just for reference/printing
    print("Current timestamp:", time.time())

    # Loop over your stations and fetch latest data
    for sttn_id in list_station_ids:
        json_by_city, json_by_city_df = data_importer.station_data(sttn_id)
        city_data_latest_json, city_data_latest_df = data_importer.station_latest_data(sttn_id)

        latest_data = city_data_latest_json["data"][0]
        datetime_value = latest_data["datetime"]

        # Only record if there's a newer timestamp than the last one
        if datetime_value != last_datetime:
            city_data_latest_df = data_processor.json_to_df(city_data_latest_json)

            # Build and store rows from the latest data
            teledata = tablib.Dataset()
            for channel in latest_data["channels"]:
                print("Name:", channel["name"], ", Value:", channel["value"])
                city_name = city_dic[city_data_latest_json["stationId"]]
                vec_values = (
                    datetime_value,
                    city_name,
                    city_data_latest_json["stationId"],
                    channel["name"],
                    channel["value"],
                    channel["status"],
                    channel["valid"]
                )
                teledata.append(vec_values)

            # Append these rows to the CSV file
            with open('output.csv', 'a+', newline='') as f:
                f.write(teledata.export('csv'))

            # Update last_datetime
            last_datetime = datetime_value

    # Sleep for 10 minutes before next acquisition
    time.sleep(10 * 60)

a = 1

# import PyInstaller.__main__
# PyInstaller.__main__.run([
#     'import_envi_05.py',
#     '--onefile',
#     '--windowed'
# ])

#pyinstaller --onefile import_envi_05.py