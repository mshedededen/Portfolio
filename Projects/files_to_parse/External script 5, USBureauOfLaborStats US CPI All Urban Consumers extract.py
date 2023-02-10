# -----

# Libraries
import pandas as pd
import requests
import datetime as dt
import json

# -----
# -----

# Read key from credentials
# Read file
filepath_credentials = "F:/Investment Info/Statistics/Data_info/Bureau of Labor Statistics API/Credentials.txt"
with open(filepath_credentials) as f:
    creds = f.read()
# Transform credentials into a JSON (dictionary) format
credentials = json.loads(creds)
print("Credentials successfully loaded.")

# -----
# -----

# Function which runs the API for
def BureauLaborStatsAPI(seriesID, startyear, endyear, increment = 9):
    # Compile API
    def CompileAPI(seriesID, startyear, endyear):
        headers = {"Content-type": "application/json"}
        parameters = json.dumps({"seriesid": [seriesID],"startyear":startyear, "endyear":endyear, "registrationkey" : credentials["key"]})
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=parameters, headers=headers)
        print("API response: {}".format(p))
        return json.loads(p.text)
    # Unwrap API contents
    def UnwrapAPI(json_data):
        df = pd.DataFrame(columns = ["Year", "Month", "MonthName", "Value"])
        for n, i in enumerate(json_data["Results"]["series"]):
            for n1, i1 in enumerate(i["data"]):
                # Add values into a one row dataframe, to append to 'df'
                df = df.append(pd.DataFrame(
                    [
                        {"Year": i1["year"],
                        "Month": i1["period"],
                        "MonthName": i1["periodName"],
                        "Value": i1["value"]}
                    ]
                    ))
        return df

    df = pd.DataFrame(columns = ["Year", "Month", "MonthName", "Value"])

    # Extract API on 10-period (9-year, e.g. 1960-1969) increments
    counter = int(startyear)
    while counter < int(endyear):
        # Conditional statement: Start date (apart from first time) must always be +1 year after endyear
        if counter > int(startyear):
            counter = counter + 1
        start_date = counter
        # Conditional statement: Final increment will be a different length
        if int(endyear) - counter < increment:
            counter = counter + (int(endyear) - counter)
        else:
            counter = counter +  increment
        end_date = counter
        # Apply functions to retreive API
        df = df.append(UnwrapAPI(CompileAPI(seriesID, startyear = str(start_date), endyear = str(end_date))))
    return df

# Function which transforms data into a timeseries format
def transform_dates(df):
    # Current format is Year, Month
    # 1. Remove "M" character from start of month
    # 2. Fetch last day of the month for each security; convert to datetime format
    # 3. Tidy up data and remove unncessary columns, so it is ["Date", "Value"]

    # Remove "M" character from start of month
    df["Month"] = df["Month"].str.strip("M")

    # 2. Fetch last day of the month for each security; convert to datetime format
    def last_day_of_month(any_day):
        # The day 28 exists in every month. 4 days later, it's always next month
        next_month = any_day.replace(day=28) + dt.timedelta(days=4)
        # subtracting the number of the current day brings us back one month
        return next_month - dt.timedelta(days=next_month.day)
    # Convert to datetime
    empty_list = []
    for i in pd.to_datetime(pd.DataFrame({"year": df["Year"], "month": df["Month"], "day": 1})):
        empty_list.append(last_day_of_month(i))
    df["Date"] = empty_list

    # 3. Tidy up data and remove unncessary columns, so it is ["Date", "Value"]
    return df[["Date", "Value"]].sort_values("Date")

# -----
# -----

# Run API (only a limited number of extracts available oer day)
df_uscpi = transform_dates(BureauLaborStatsAPI(seriesID="CUUR0000AA0", startyear="1960", endyear="2022"))

# Save down data to F/Drive
df_uscpi.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_USCPI_automatic.csv", index = False)
df_uscpi.to_excel("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_USCPI_automatic.xlsx", index = False)
print('US CPI (All Urban Consumers) data successfully imported.')