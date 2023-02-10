# MSCI FX API daily extract for indices list

# -----
# Import libraries
import requests             #   HTTPS requests
import pandas as pd         #   Data wrangling
import numpy as np          #   I DON'T THINK THIS IS NEEDED
import json                 #   Handle JSON files (API data format)
import datetime as dt       #   Create and work with dates

# -----
# -----

# STEP 1: READ USEFUL LOCALLY-STORED FILES
# - Monthly Indices sheet: List of MSCI indices
# - MSCI Index API credentials: Stored in a separate .txt file for security
# - MSCI FX database: Previously extracted MSCI values

# Monthly Indices sheet: List of MSCI indices
filepath_indices = "F:/Investment Info/Statistics/Data_info/List of indices to export per month.xlsx"
indices = pd.read_excel(filepath_indices)
indices_msci = indices[indices['FX_Base'] != "-"]
print("Indices list successfully loaded.")
print("There are {} FX rates from MSCI.".format(
    indices_msci['Bloomberg Ticker'].value_counts().sum()
))

# MSCI Index API credentials
filepath_credentials = "F:/Investment Info/Statistics/Data_info/MSCI Index API/credentials.txt"
with open(filepath_credentials) as f:
    creds = f.read()
credentials = json.loads(creds)             # Transform credentials into a JSON (dictionary) format
print("Credentials successfully loaded.")

# MSCI Indices database
filepath_msci_data = "F:/Investment Info/Statistics/Data_raw_files/MSCI_fxRates.csv"
data_existing_msci = pd.read_csv(filepath_msci_data)
print("Existing database successfully loaded.")

# -----
# -----

# STEP 2: GENERATE A LIST OF DATES
# I want to create a bit of crude logic which enables users to decide if they want to append data onto the end of ...
# ... the existing MSCI indices sheet or create a new list of data.

cmd = input("Do you wish to append dates to existing MSCI table? (Y/N)")

# IF, command IS "N" (*I don't wish to append dates to existing MSCI table*):
if cmd == "N":
    start_date = input("Enter a start date (YYYYMMDD)")                             # Enter start date
    start_date = dt.datetime.strptime(start_date, "%Y%m%d").strftime("%Y%m%d")      # Convert to datetime format
    end_date = input("Enter a end date (YYYYMMDD)")                                 # Enter end date
    end_date = dt.datetime.strptime(end_date, "%Y%m%d").strftime("%Y%m%d")          # Convert to datetime format
    print("Running extract for the dates {} to {}.".format(start_date, end_date))
    # Build an empty dataframe
    df = pd.DataFrame(
        columns=[
            "Calculation_Date", "FX_Base",
            "FX_Quote", "Level"
            ]
    )
    file_name = "F:/Investment Info/Statistics/Data_raw_files/{}.csv".format(input("Please provide a name for the file."))
else:
    print("Appending data up to yesterday's close.")
    # Most recent extract + 1
    start_date = (dt.datetime.strptime(
        data_existing_msci["Calculation_Date"].max(), "%Y-%m-%d"
        ) + dt.timedelta(
            days = 1
            )).strftime("%Y%m%d")

    # ... Last business day as end date
    def get_last_business_day():
        now = dt.datetime.now()
        diff = 1
        if now.weekday() == 0: diff = 3
        elif now.weekday() == 6: diff = 2
        else : diff = 1
        return (now - dt.timedelta(days = diff))

    end_date = get_last_business_day().strftime("%Y%m%d")
    print("Running extract for the dates {} to {}.".format(start_date, end_date))
    # Use pre-existing dataframe
    df = data_existing_msci
    file_name = "F:/Investment Info/Statistics/Data_raw_files/MSCI_fxRates.csv"

# -----
# -----

# FUNCTIONS

# 1. Generate URL
def MSCI_API_FX_url(fx_universe, start_date, distribution_zone, cumulative):
    url_base = "https://api.msci.com/index/"
    url_type = "fx/v1.0/fxrates/"
    url_extension = "{}?calc_date={}&distribution_zone={}&cumulative={}".format(
        fx_universe,
        start_date,
        distribution_zone,
        cumulative
        )
    
    url = url_base + url_type + url_extension
    return url

# 2. Generate response
def MSCI_API_response(url, headers, API_key, API_secret):
    response = requests.request(
            "GET",
            url = url,
            headers=headers, 
            auth=(API_key,API_secret)
            )
    print('MSCI API response message: %s' % response)
    data = json.loads(response.text)
    return(data)

# -----
# -----

# API inputs
url = "https://api.msci.com/index/fx/v1.0/fxrates/CORE%20DM?calc_date=20190131&distribution_zone=WORLD&cumulative=true"
headers = {'accept': "application/json",'accept-encoding': "deflate,gzip"}
API_key = credentials["client_id"]
API_secret = credentials["client_secret"]

# -----
# -----

# STEP 3: GENERATE RESPONSES FROM MSCI API

fx_responses = pd.DataFrame(columns = [
    "Calculation_Date", "FX_Base", "FX_Quote", "Level"
])

# Generate data derived from MSCI API
#   Layer 1: "fxRates"
#   Layer 2: "FX_RATES"
#   Layer 3: Each currency ISO

for i in pd.bdate_range(start_date, end_date):
    # 1. Generate URL for all dates
    url = MSCI_API_FX_url(
        fx_universe="ALL",
        start_date=i.strftime("%Y%m%d"),
        distribution_zone="WORLD",
        cumulative="true")
    print("The API for {} is {}".format(i, url))
    # 2. Generate response for all URLs
    data = MSCI_API_response(
            url=url,
            headers=headers,
            API_key=API_key,
            API_secret=API_secret)
    # 3. Retreive data
    for n, fx in enumerate(data['fxRates']['FX_RATES']):
        if "ISO_currency_symbol" in data['fxRates']['FX_RATES'][n].keys():
            ISO_currency_symbol = data['fxRates']['FX_RATES'][n]["ISO_currency_symbol"]
            spot_fx_today = data['fxRates']['FX_RATES'][n]["spot_fx_today"]
        #print("USD-{}: {}".format(ISO_currency_symbol, spot_fx_today))

    # 4. Append data into dataset
        row = pd.DataFrame([{
            "Calculation_Date": i,
            "FX_Base": "USD",
            "FX_Quote": ISO_currency_symbol,
            "Level": spot_fx_today
        }]
        )
        fx_responses = fx_responses.append(row, ignore_index=True)

# -----
# -----

# Calculate cross FX rates, based on USD as the base currency
# Indices list
other_currencies = list(indices_msci["FX_Quote"].unique())

# All possible FX rates
#other_currencies = list(df["FX_Quote"].unique())

# -----

# Create dictionary of other FX rates so these can be cross-multiplied to get
# new FX rates like EUR-JPY.

cross_fx = {}

for i in other_currencies:
    # Loop through other_currencies and put all FX rates into an individual list
    cross_fx[i] = fx_responses[fx_responses["FX_Quote"] == i].reset_index(drop=True)
    
# -----
# -----

# FUNCTIONS

# 3. Convert FX rates enable cross FX
def convert_FX(base, quote):
    # Create empty dataframe
    df = pd.DataFrame(columns = cross_fx[base].columns)
    # Column fill: Calculation_Date
    Calculation_Date = cross_fx[base].Calculation_Date
    # Column fill: FX_Base
    FX_Base = base
    # Column fill: FX_Quote
    FX_Quote = quote
    # Column fill: Level (a.k.a. price!)
    Level = (1/cross_fx[base]["Level"]) * cross_fx[quote]["Level"]
    # Add columns to empty dataframe
    df.Calculation_Date = Calculation_Date
    df.FX_Base= FX_Base
    df.FX_Quote = FX_Quote
    df.Level = Level

    # Return: df
    return (df)


# -----
# -----

# Cross convert currencies

for i in other_currencies:
    if i != "USD":
        print("Converting {}...".format(i))
        for j in other_currencies:
            if i not in j:
                # do something
                x = convert_FX(base=i, quote=j)
                fx_responses = pd.concat([fx_responses, x], ignore_index=True)
            else:
                continue
        else:
            continue

# -----
# -----

# Final adjustments

# Convert YYYYMMDD format to datetime
fx_responses["Calculation_Date"] = pd.to_datetime(fx_responses["Calculation_Date"])
df["Calculation_Date"] = pd.to_datetime(df["Calculation_Date"])
# Combine dataframes
df = pd.concat([df, fx_responses])
# Sort dataframes
df= df.sort_values("Calculation_Date").reset_index(drop = True)

# -----
# -----

# Upload to F-Drive
df.to_csv(
    file_name, index = False
)
print("Successfully uploaded to F-Drive in file location: F:\Investment Info\Statistics\Data_raw_files.")

# -----