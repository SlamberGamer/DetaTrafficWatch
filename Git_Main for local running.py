import googlemaps
import pandas as pd
import csv
from datetime import datetime
import os.path

# Function to count the number of rows in a specific column of a CSV file
def count_data_in_column(csv_file_name, column_name):
    with open(csv_file_name, mode='r', newline='', encoding='utf-8', errors='ignore') as csv_file:
        df = pd.read_csv(csv_file)
        return len(df[column_name]) - 1

# Initialize Google Maps API client with the provided API key
gmaps = googlemaps.Client(key='PUT_IN_YOUR_API')

# Set origin and destination coordinates
origin = 'PUT_IN_YOUR_LOCATION' #EG: 'F962+5P Arau, Perlis' OR '6.460621086195773, 100.35181053780218'
destination = 'PUT_IN_YOUR_LOCATION' #EG: 'F962+5P Arau, Perlis' OR '6.460621086195773, 100.35181053780218'

# Set the number of API calls and the interval between calls
num_calls = 1
interval = 3600

# Initialize an empty list to store results
results = []

# Set the output file name
file_name = 'travel_data.csv'

# Check if the output file exists; if not, create it with the header row
if not os.path.isfile(file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8', errors='ignore') as csv_file:
        fieldnames = ['Data', 'time', 'Distance Origin to Destination', 'Distance Destination to Origin', 'Origin to Destination (Hours)', 'Origin to Destination (Seconds)', 'Destination to Origin (Hours)', 'Destination to Origin (Seconds)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

# Loop through the desired number of API calls
# for i in range(num_calls):
try:
    # Call the Google Maps API to get distance and duration between the origin and destination
    origin_destination = gmaps.distance_matrix(origin, destination,
                                               traffic_model='best_guess',
                                               departure_time='now')

    print(origin_destination)

    destination_origin = gmaps.distance_matrix(destination, origin,
                                               traffic_model='best_guess',
                                               departure_time='now')

    print(destination_origin)

    # Add the results to the results list
    results.append({
        'timestamp': datetime.now(),
        'Distance Origin to Destination': origin_destination['rows'][0]['elements'][0]['distance']['text'],
        'Distance Destination to Origin': destination_origin['rows'][0]['elements'][0]['distance']['text'],
        'Origin to Destination (Hours)': origin_destination['rows'][0]['elements'][0]['duration_in_traffic']['text'],
        'Origin to Destination (Seconds)': origin_destination['rows'][0]['elements'][0]['duration_in_traffic']['value'],
        'Destination to Origin (Hours)': destination_origin['rows'][0]['elements'][0]['duration_in_traffic']['text'],
        'Destination to Origin (Seconds)': destination_origin['rows'][0]['elements'][0]['duration_in_traffic']['value']
    })

    now = datetime.now()
    date = now.date().strftime('%Y-%m-%d')
    time = now.time().strftime('%H:%M:%S')

    # Append the results to the output CSV file
    with open(file_name, mode='a', newline='', encoding='utf-8', errors='ignore') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([date,
                         time,
                         origin_destination['rows'][0]['elements'][0]['distance']['text'],
                         destination_origin['rows'][0]['elements'][0]['distance']['text'],
                         origin_destination['rows'][0]['elements'][0]['duration_in_traffic']['text'],
                         origin_destination['rows'][0]['elements'][0]['duration_in_traffic']['value'],
                         destination_origin['rows'][0]['elements'][0]['duration_in_traffic']['text'],
                         destination_origin['rows'][0]['elements'][0]['duration_in_traffic']['value']])
        csv_file.flush()

    # Display the row count for each loop iteration
    column_to_count = 'Distance Origin to Destination'
    count = count_data_in_column(file_name, column_to_count)
    print(f'Total Data Collected . . . {count}')

    # Wait for the specified interval before the next API call
    # import time
    # time.sleep(interval)

except:
    pass

# time.sleep(100)
pass
