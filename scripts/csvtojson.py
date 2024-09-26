import csv
import json

# Open the CSV file and JSON file
with open('data/iso3166.csv', 'r') as csvfile, open('data/iso3166-flat.json', 'w') as jsonfile:
    # Read the CSV file
    reader = csv.DictReader(csvfile)
    
    # Convert the rows to a list of dictionaries (each row is a dictionary)
    rows = list(reader)
    
    # Write the list of rows as a single JSON array to the file
    json.dump(rows, jsonfile, indent=4)
