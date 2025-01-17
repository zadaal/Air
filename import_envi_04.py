# Ver 03 oak

import requests
import tablib
import time
# Use station IDs:
# 7 - Beit Shemesh (line #5)
# 32 - rehovot (line #12)
# 64 - Modiin (line #26)
# 76 - Carmei Yosef (line #34)
# 78 Achisamach (line #35)
# 367 Beit Hashmonai (line #111)
# 338 Yad Rambam
# 397 Mobile (line #122)

list_station_ids=[31, 40, 64, 76, 77, 78, 193, 367, 338]
city_dic=dict()
city_dic={
    31: 'Modiin Hinanit',
    40: 'Yad Rambam 1',
    64: 'Modiin',
    76: 'Carmei Yosef',
    77: 'Kfar Shmuel',
    78: 'Achisamach',
    193: 'Omanim Ramla',
    367: 'Beit Hashmonai',
    338: 'Yad Rambam New'
}

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
            r_by_loc = requests.get('https://api.svivaaqm.net/v1/envista/stations/{}'.format(str(sttn_id)),
                                    # headers={'Authorization': 'ApiToken 71e67c41-8478-4310-9293-196f559493ca',
                                    headers={'Authorization': 'ApiToken 745356f0-5eee-4da8-aa71-b739f4acc081',
                                             'envi-data-source': 'MANA'})
            json_by_city = r_by_loc.json()


            html_string='https://api.svivaaqm.net/v1/envista/stations/{}/data/latest'.format(str(sttn_id))
            r_by_loc_latest = requests.get(html_string,headers={'Authorization': 'ApiToken 745356f0-5eee-4da8-aa71-b739f4acc081','envi-data-source': 'MANA'})
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
#pyinstaller --onefile import_envi_04.py