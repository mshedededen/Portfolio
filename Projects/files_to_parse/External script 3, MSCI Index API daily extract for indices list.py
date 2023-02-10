# -----
# Import libraries
import requests             #   HTTPS requests
import pandas as pd         #   Data wrangling
import json                 #   Handle JSON files (API data format)
import datetime as dt       #   Create and work with dates

# -----
# -----

# STEP 1: READ USEFUL LOCALLY-STORED FILES
# - Monthly Indices sheet: List of MSCI indices
# - MSCI Index API credentials: Stored in a separate .txt file for security
# - MSCI Indices database: Previously extracted MSCI values

# ----- Monthly Indices sheet: List of MSCI indices -----
# Read file
filepath_indices = "F:/Investment Info/Statistics/Data_info/List of indices to export per month.xlsx"
indices = pd.read_excel(filepath_indices)
# Subset file
indices_msci = indices[indices['Data source'] == "MSCI"]
indices_bloomberg = indices[indices['Data source'] == "Bloomberg"]
print("Indices list successfully loaded.")
print("There are {} indices from MSCI and {} indices from Bloomberg.".format(
    indices_msci['Bloomberg Ticker'].value_counts().sum(),
    indices_bloomberg['Bloomberg Ticker'].value_counts().sum()
))

# ----- MSCI Index API credentials -----
# Read file
filepath_credentials = "F:/Investment Info/Statistics/Data_info/MSCI Index API/credentials.txt"
with open(filepath_credentials) as f:
    creds = f.read()
# Transform credentials into a JSON (dictionary) format
credentials = json.loads(creds)
print("Credentials successfully loaded.")

# ----- MSCI Indices database -----
# Read file
filepath_msci_data = "F:/Investment Info/Statistics/Data_raw_files/MSCI_indices.csv"
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
            "Calculation Date", "MSCI Index Code", "MSCI Index name",
            "Index Variant", "ISO", "Level", "Yield", "Ticker"
            ]
    )
    file_name = "F:/Investment Info/Statistics/Data_raw_files/{}.csv".format(input("Please provide a name for the file."))
else:
    print("Appending data up to yesterday's close.")
    # Most recent extract + 1
    start_date = (dt.datetime.strptime(
        data_existing_msci["Calculation Date"].max(), "%Y-%m-%d"
        ) + dt.timedelta(
            days = 1
            )).strftime("%Y%m%d")
    # Last Friday as end date
    #def get_last_friday():
    #    now = dt.datetime.now()
    #    closest_friday = now + dt.timedelta(days=(4 - now.weekday()))
    #    return (closest_friday if closest_friday < now
    #            else closest_friday - dt.timedelta(days=7))

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
    file_name = "F:/Investment Info/Statistics/Data_raw_files/MSCI_indices.csv"

# -----
# -----

# FUNCTIONS

# 1. Generate URL
def MSCI_API_url(index_code, start_date, end_date, data_frequency, currency, index_variant, output):
    url_base = "https://api.msci.com/index/"
    url_type = "performance/v1.0/indexes/"
    url_extension = "{}/close?start_date={}&end_date={}&data_frequency={}&currency={}&index_variant={}&output={}".format(
        index_code,
        start_date, end_date,
        data_frequency, currency,
        index_variant, output
        )
    
    url = url_base + url_type + url_extension
    return url

# -----
# -----

# For i in indices_msci:

for i, name in enumerate(indices_msci["Name"]):
    print("Name: {}. Code: {}".format(name, indices_msci["MSCI code"][indices_msci.index[i]]))
# - Generate inputs
    url = MSCI_API_url(
        index_code=indices_msci["MSCI code"][indices_msci.index[i]],        # Loop through MSCI index code (basically, a ticker symbol)
        start_date=start_date, end_date=end_date,                           # Start date and End date
        data_frequency="daily",                                             # Enter: Frequency of data being extracted
        currency=indices_msci["ISO"][indices_msci.index[i]],                # Enter: Currency returns will be displayed in
        index_variant=indices_msci["MSCI variant"][indices_msci.index[i]],  # Enter: Index variant of data being extracted
        output="INDEX_PERFORMANCE"                                          # Different tyoes of API (e.g. INDEX_PERFORMANCE, DESCRIPTION)
    )
    # Headers 
    headers = {'accept': "application/json",'accept-encoding': "deflate,gzip"}

    # Credentials
    API_key = credentials["client_id"]
    API_secret = credentials["client_secret"]

# - Generate URL
    print("URL is: {}".format(url))

# - Generate API response
# Request rsponse from API
    response = requests.request(
        "GET",
        url = url,
        headers=headers, 
        auth=(API_key,API_secret)
        )
    print('MSCI API response message: %s' % response)

    # Transform data into JSON format
    data = json.loads(response.text)

    # Print levels within JSON file
    for i in data.keys():

        # Curreny Indexes
        if i == "currency_indexes":
            print("Index type: Currency Index.")
            for t in data[i]:
                for keys, items in t.items():
                    # Extract:
                    if "CURRENCY_INDEX_DESCRIPTION" in keys:
                        for keys2, items2 in t[keys].items():
                            # - Date of calculation
                            if "calc_date" == keys2:
                                calc_date = items2
                            # - MSCI index code
                            elif "msci_index_code" == keys2:
                                msci_index_code = items2
                        print("- Calculation date: {}. Index code: {}.".format(calc_date, msci_index_code))   # (optional line)                        
                    
                    # - Index Performance data 
                    elif "INDEX_PERFORMANCE" in keys:
                        for keys2, items2 in t[keys].items():
                            if "index_variant_type" == keys2:
                                index_variant_type = items2
                            elif "ISO_currency_symbol" == keys2:
                                iso_curreency_symbol = items2
                            elif "level_eod" == keys2:
                                level_eod = items2
                            #elif "yield" == keys2:
                            #    yield_index = items2
                            elif "real_time_ticker" == keys2:
                                real_time_ticker = items2
                        # Print to validate MSCI extracts
                        print("- Index Variant Type: {}. ISO: {}. Level: {}.".format(index_variant_type, iso_curreency_symbol, level_eod))
                    
                # Append data into dataset
                row = pd.DataFrame([{
                    "Calculation Date": calc_date, 
                    "MSCI Index Code": msci_index_code,
                    "MSCI Index name": name,
                    "Index Variant": index_variant_type,
                    "ISO": iso_curreency_symbol, 
                    "Level": level_eod, 
                    "Yield": pd.NA, 
                    "Ticker": pd.NA
                    }]
                )

                df = df.append(row, ignore_index=True)

        # Typical Indexes
        elif i == "indexes":
            print("Index type: Price Index.")
            for t in data[i]:
                for keys, items in t.items():
                # Extract:
                    # - Date of calculation
                    if "calc_date" == keys:
                       calc_date = items
                    # - MSCI index code
                    elif "msci_index_code" == keys:
                        msci_index_code = items
                        # - Index Performance data
                    elif "INDEX_PERFORMANCE" == keys:
                        for keys2, items2 in items[0].items():
                            if "index_variant_type" == keys2:
                                index_variant_type = items2
                            elif "ISO_currency_symbol" == keys2:
                                iso_curreency_symbol = items2
                            elif "level_eod" == keys2:
                                level_eod = items2
                            elif "yield" == keys2:
                                yield_level = items2
                            elif "real_time_ticker" == keys2:
                                real_time_ticker = items2
                print("- Calculation date: {}. Index code: {}.".format(calc_date, msci_index_code))   # (optional line)
                print("- Index Variant Type: {}. ISO: {}. Level: {}. Yield: {}. Ticker: {}".format(index_variant_type, iso_curreency_symbol, level_eod, yield_level, real_time_ticker))

                # Append data into dataset
                row = pd.DataFrame([{
                    "Calculation Date": calc_date, 
                    "MSCI Index Code": msci_index_code,
                    "MSCI Index name": name,
                    "Index Variant": index_variant_type,
                    "ISO": iso_curreency_symbol, 
                    "Level": level_eod, 
                    "Yield": yield_level, 
                    "Ticker": real_time_ticker
                    }]
                )

                df = df.append(row, ignore_index=True)

# -----
# -----

# Reset index, meaning i enumerates correctly
df = df.reset_index(drop = True)
# Convert YYYYMMDD format to datetime
df['Calculation Date'] = pd.to_datetime(df['Calculation Date'])

# -----
# -----

# Upload to F-Drive
df.to_csv(
    file_name, index = False
)
print("Successfully uploaded to F-Drive in file location: F:\Investment Info\Statistics\Data_raw_files.")

# -----