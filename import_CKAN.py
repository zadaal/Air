import requests
import json

url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=782cfb94-ebbd-4f41-aba2-80c298457a58&limit=5&q=title:jones'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")