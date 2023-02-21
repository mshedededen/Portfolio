# Net zero project: Commuting (scope 3 emissions)
# Pseudocode:
#   1. Finance team/ Input up-to-date list of employees (as at end of financial year) and details.
#   2. Middle office(MO)/ List passed to MO, who run this scrip.
# The script is outputted back into the folder, where Finance now have a complete list of commuting emissions.

# -----
# Load required libraries
import pandas as pd         # For data transformations
import openrouteservice     # For open source mapping information
import json                 # To manage JSON file structures
import time                 # To manage speed data is extracted from ORS's API
import numpy as np          # For numerical functions

# Note:
# OpenRouteService has a key included, however this key may at some point become invalid.
# To generate a new key, go to https://openrouteservice.org/dev and replace existing key/token in the code.
# -----

# -----
# Load data and make initial transformations
df = pd.read_excel(
    "F:/General/SECR - Decarbonisation/2021-2022/Data Period End 30042022/Commuting data, unprocessed.xlsx"
    )
df['CO2 emissions (kilogram/kilometre)'] = df['CO2 emissions (kilogram/kilometre)'].replace('-', np.nan)
df['CO2 emissions (kilogram/kilometre)'] = df['CO2 emissions (kilogram/kilometre)'].astype(float)

# Note:
# Within the Excel sheet, the character '-' indicates null data points.
# To make this into a 'float' datatype, that can be calculated, these '-' characters are converted into 'NaN' values.
# -----

# -----
# Convert postcodes to longitude and latitude
client = openrouteservice.Client(key='5b3ce3597851110001cf6248a4390aecab714073a1665eb50c45bdf3') # Initialize API, requiring API key.
# 1. Convert office postcodes to lon, lat
Office_coords = []
for n, i in enumerate(df['Office postcode'].unique()):
    if not(pd.isna(i)):
        json_out = openrouteservice.geocode.pelias_structured(client = client, postalcode=i)
        if len(json_out['features']) != 0:
            coords = json_out['features'][0]['geometry']['coordinates']
    else:
        coords = float('NaN')
    Office_coords.append(coords)
unique_office_coords = pd.DataFrame(data = {'Unique postcodes': df['Office postcode'].unique(),
                     'Unique coordinates': Office_coords})

# 2. Convert home postcodes to lat, long
Home_coords = []
for n, i in enumerate(df['Postcode'].unique()):
    if not(pd.isna(i)):
        json_out = openrouteservice.geocode.pelias_structured(client = client, postalcode=i)
        if len(json_out['features']) != 0:
            coords = json_out['features'][0]['geometry']['coordinates']
    else:
        coords = float('NaN')
    Home_coords.append(coords)

unique_home_coords = pd.DataFrame(data = {'Unique postcodes': df['Postcode'].unique(),
                                    'Unique coordinates': Home_coords}
                                    )

# Stitching up coordinates with unique coordinates
# 1. Office postcodes and coordinates
df = pd.merge(left=df, right=unique_office_coords, left_on='Office postcode', right_on='Unique postcodes', how='left')
df.drop('Unique postcodes', axis=1,  inplace=True)
df.rename(columns={'Unique coordinates': 'Office coordinates'}, inplace=True)
# 2. Home postcodes and coordinates
df = pd.merge(left=df, right=unique_home_coords, left_on='Postcode', right_on='Unique postcodes', how='left')
df.drop('Unique postcodes', axis=1,  inplace=True)
df.rename(columns={'Unique coordinates': 'Home coordinates'}, inplace=True)

# Note (explanation of what this code chunk does):
# 1. Loop through all postcodes, excluding the ones that are invalid (e.g. staff that don't have an office)
# 2. Search for postcode using OSR API, to generate a geocode (fancy name for coordinates)
# 3. Append coordinates into an array, and insert back into dataframe
# -----

# -----
# Print distances (this is only using car as the means of transportation - ideally, modes of transport would have different disatances but alas...)
distances = []
for i in df.index:
    if i != 0 and i %35 == 0:
        print('Please wait for 60 seconds, to prevent exceeding API limit')
        time.sleep(60) # Sleep 60 seconds per every 35 queries to avoid timeout.

    if not(pd.isna(df['Office coordinates'])[i]):
        distances.append(openrouteservice.distance_matrix.distance_matrix(client=client, locations = [df['Office coordinates'][i], df['Home coordinates'][i]], units = 'km', metrics = ['distance'])['distances'][0][1])
    else:
        distances.append(0)
    print('Distances calculated for {}'.format(df['Name'][i]))

df['Distance'] = distances
print('Each staff member distance between office and home uploaded.')
# -----

# -----
# Calculate TOTAL CO2 emissions, from commuting, per employee
# Write to new .xlsx file
df['Total CO2 emissions (kilogram/kilometre)'] = df['Distance'] * df['CO2 emissions (kilogram/kilometre)'] * df['Days active'] * 2 # Includes return journeys
df.to_excel("F:\General\SECR - Decarbonisation\Commuting data, processed {}.xlsx".format(
    df['End date (former employees)'].max().strftime('%Y%m%d')
), index=False)
print('Output file successfully saved at the following location: F:\General\SECR - Decarbonisation\Commuting data, processed {}.xlsx'.format(df['End date (former employees)'].max().strftime('%Y%m%d')))