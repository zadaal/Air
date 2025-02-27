import requests
import tablib
import time
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from urllib3.util.retry import Retry
import plotly.express as px
import folium
import webbrowser
"""
Main module with various functions of Air monitoring package
Written By Alon
"""

class data_importer():
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
        json_all_cities_df[["latitude", "longitude"]] = pd.DataFrame(json_all_cities_df["location"].tolist(),
                                                               index=json_all_cities_df.index)
        json_all_cities_df["geometry"] = [
            Point(xy) for xy in zip(json_all_cities_df["longitude"], json_all_cities_df["latitude"])
        ]
        json_all_cities_gdf = gpd.GeoDataFrame(json_all_cities_df, geometry="geometry", crs="EPSG:4326")

        return json_all_cities, json_all_cities_gdf

    def station_data(self, sttn_id):
        r_by_loc = requests.get('https://air-api.sviva.gov.il/v1/envista/stations/{}'.format(str(sttn_id)),
                                headers={'Authorization': self.api_token,
                                         'envi-data-source': 'MANA'}, verify=False)
        json_by_city = r_by_loc.json()
        json_by_city_df = pd.json_normalize(json_by_city)

        return json_by_city, json_by_city_df

    def station_latest_data(self, sttn_id):
        data_processor_instance = data_processor()

        r_by_loc_latest = requests.get('https://air-api.sviva.gov.il/v1/envista/stations/{}/data/latest'.format(str(sttn_id)),
                                headers={'Authorization': self.api_token,
                                         'envi-data-source': 'MANA'}, verify=False)
        json_by_city_latest = r_by_loc_latest.json()
        # json_by_city_latest_df = pd.DataFrame(json_by_city_latest['data'][0])
        json_by_city_latest_df = data_processor_instance.json_to_df(json_by_city_latest)
        # Add city info
        json_by_city, json_by_city_df = self.station_data(sttn_id)
        # Validate location in json_by_city_df
        if (json_by_city_df["location.longitude"][0] == None):
            json_by_city_df[["location.latitude", "location.longitude"]] = (
                json_by_city_df["StationNotes"]
                .str.extract(r"lat\s*:\s*([\d\.]+)\s*long\s*:\s*([\d\.]+)")
                .astype(float)
            )



        joined_df = pd.merge(json_by_city_df, json_by_city_latest_df, how="cross")
        # Convert to geodataframe
        geometry = [Point(xy) for xy in zip(joined_df["location.longitude"], joined_df["location.latitude"])]
        joined_gdf = gpd.GeoDataFrame(joined_df, geometry=geometry, crs="EPSG:4326")

        return json_by_city_latest, joined_gdf

class data_processor():
    def json_to_df(self, data_json):
        data = data_json['data']
        channels_series = pd.DataFrame(data)['channels']
        channels_exploded = channels_series.explode()
        channels_parsed = pd.DataFrame(channels_exploded.tolist())
        # channels_parsed.insert(0, 'stationId', data_json['stationId'])
        # channels_parsed.insert(0, 'date', data[0]['datetime'])

        return channels_parsed

class data_plotter():
    def plot_stations(self, stations_gdf):
        fig = px.scatter_mapbox(
            stations_gdf,
            lat="latitude",
            lon="longitude",
            hover_name='stationId',  # optional: which column to display in hover
            hover_data = {
                'name': True,
                'active': True,
                'owner': True,
            },
            # color="red",  # optional: color points by a column
            zoom=10,
            mapbox_style="carto-positron"  #"open-street-map" or "carto-positron", "stamen-terrain", etc.
        )

        fig.show()

    def plot_stations_folium(self, stations_gdf):
        stations_gdf = stations_gdf.drop(columns=["monitors"])
        map_widget = stations_gdf.explore(tiles="CartoDB positron")
        map_widget.save("stations.html")
        webbrowser.open("stations.html")