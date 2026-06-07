

import csv
import json

csv_file = '../data/LocationList_20240610.csv'
json_file = '../data/LocationList_20240610.json'

data = []
with open(csv_file, 'r') as csvfile:  # Open the file in binary mode
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        # Convert latitude and longitude to numbers
        row['lat'] = float(row['lat'])
        row['lng'] = float(row['lng'])
        data.append(row)

with open(json_file, 'w') as jsonfile:  # Open the file without specifying encoding
    json.dump(data, jsonfile, indent=4)