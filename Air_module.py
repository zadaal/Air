import requests
import tablib
import time
import pandas as pd
from urllib3.util.retry import Retry


class DataImporter():
    def __init__(self, api_token='ApiToken 1cab20bf-0248-493d-aedc-27aa94445d15'):
        self.api_token = api_token

    def stations(self):
        try:
            r_by_loc = requests.get('https://air-api.sviva.gov.il/v1/envista/stations',
                                    headers={'Authorization': self.api_token,
                                             'envi-data-source': 'MANA'}, verify=False)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        json_all_cities = r_by_loc.json()
        json_all_cities_df = pd.DataFrame(json_all_cities)

        return json_all_cities, json_all_cities_df

    def station_data(self, sttn_id):
        r_by_loc = requests.get('https://air-api.sviva.gov.il/v1/envista/stations/{}'.format(str(sttn_id)),
                                headers={'Authorization': self.api_token,
                                         'envi-data-source': 'MANA'}, verify=False)
        json_by_city = r_by_loc.json()
        json_by_city_df =  pd.json_normalize(json_by_city)

        return json_by_city, json_by_city_df

    def station_latest_data(self, sttn_id):
        r_by_loc_latest = requests.get('https://air-api.sviva.gov.il/v1/envista/stations/{}/data/latest'.format(str(sttn_id)),
                                headers={'Authorization': self.api_token,
                                         'envi-data-source': 'MANA'}, verify=False)
        json_by_city_latest = r_by_loc_latest.json()
        json_by_city_latest_df = pd.DataFrame(json_by_city_latest['data'][0])

        return json_by_city_latest, json_by_city_latest_df

# class DataProcessor():

