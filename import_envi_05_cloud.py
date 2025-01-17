import requests
import tablib
import time


list_station_ids=[31, 40, 64, 76, 77, 78, 367, 338, 513, 32, 139]
city_dic=dict()
city_dic={
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

# API Token ==================================================================================
API_Token = '<INSERT THE TOKEN CODE HERE>'

# GET LIST OF ALL LOCATIONS ===================================================================
# r_by_loc = requests.get('https://air-api.sviva.gov.il/v1/envista/stations',
#                         headers={'Authorization': API_Token,
#                                  'envi-data-source': 'MANA'}, verify=False)
#
# json_all_cities = r_by_loc.json()

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
            r_by_loc = requests.get('https://air-api.sviva.gov.il/v1/envista/stations/{}'.format(str(sttn_id)),
                                    headers={'Authorization': API_Token,
                                             'envi-data-source': 'MANA'}, verify=False)
            json_by_city = r_by_loc.json()


            html_string='https://air-api.sviva.gov.il/v1/envista/stations/{}/data/latest'.format(str(sttn_id))
            r_by_loc_latest = requests.get(html_string,headers={'Authorization': API_Token,'envi-data-source': 'MANA'}, verify=False)
            json_by_city_latest = r_by_loc_latest.json()
            jj = json_by_city_latest["data"][0]
            datetime = jj["datetime"]
            if datetime!=last_datetime:
                # last_datetime=datetime
                for i in range(0, len(jj["channels"])):
                    print("name: ", jj["channels"][i]["name"], ", value:", jj["channels"][i]["value"])
                    city_name=city_dic[json_by_city_latest["stationId"]]
                    vec_values = (
                    datetime, city_name, json_by_city_latest["stationId"], jj["channels"][i]["name"],
                    jj["channels"][i]["value"], jj["channels"][i]["status"], jj["channels"][i]["valid"])
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