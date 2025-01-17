import csv
from datetime import datetime

def filter_csv(start_time, end_time, station_id, material_type):
    with open('output.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header row
        results = []
        for row in reader:
            timestamp = datetime.fromisoformat(row[0])
            if start_time <= timestamp <= end_time and int(row[2]) == station_id and row[3] == material_type:
                results.append(row[4])
        return results


start_time = datetime.fromisoformat('2023-03-04T01:30:00+02:00')
end_time = datetime.fromisoformat('2023-03-04T01:40:00+02:00')
station_id = 513
material_type = 'PM2.5'

results = filter_csv(start_time, end_time, station_id, material_type)
print(results)