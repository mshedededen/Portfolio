# This script currently extracts the Eurozone Harmonised Consumer Price Index from St Louis Federal Reserve
# Q: Why not from Eurostat (direct source)? Their online database is really old-fashioned.

# -----

# Libraries
from urllib import response
import pandas as pd
import datetime as dt
import requests
import numpy as np
import io

# -----
# -----

# Fetching files from St Louis FED website direct
today_date = str(dt.datetime.utcnow().date())

URL_EUCPI = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=CP0000EZ19M086NEST&vintage_date={}&revision_date={}&nd=1996-01-01'.format(today_date, today_date)   # URL has been shrunk (through trial and error) down to core parts to get what is needed

response_EUCPI = requests.get(URL_EUCPI)

print('EU CPI response message: ', response_EUCPI)

# -----
# -----

# Function 1: Turning response into data
def StLouisFED_transformations(response_data):
    df = pd.read_csv(io.StringIO(response_data.text))               # Read as a .csv (St Louis FED is really clean)
    df.columns = ["Date", "Value"]                                  # Change column names

    # Convert to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    def last_day_of_month(any_day):
        # The day 28 exists in every month. 4 days later, it's always next month
        next_month = any_day.replace(day=28) + dt.timedelta(days=4)
        # subtracting the number of the current day brings us back one month
        return next_month - dt.timedelta(days=next_month.day)

    empty_list = []
    for i in df['Date']: empty_list.append(last_day_of_month(i))

    df['Date'] = empty_list

    df['Value'] = df['Value'].astype('float64')

    return df

# -----

# Function 2: Calculate CPI plus X percent
def CPI_plus_pct(df, annual_pct_over_CPI, period):
    # 1 Calculate STATIC monthly benchmark figure. Inputs are CPI (e.g. annual benchmark) and frequency (e.g. monthly)
    x = (1 + annual_pct_over_CPI) ** (period / 12)                           # 12, because CPI is calculated monthly
    # 2 Calculate pct_change of CPI
    y = df['Value'].pct_change()
    # 3 Add (1) and (2) together as a vector
    z = y + x - 1
    # 4 Multiply (3) by t-1 CPI figure
    new_figure = []
    for i in range(len(df)):
        if i == 0:
            a = df['Value'][i]
            new_figure.append(a)
        else:
            a = new_figure[i-1] * (1 + z[i])
            new_figure.append(a)
    fieldname = 'CPI_plus_' + str(int(annual_pct_over_CPI * 100)) + 'pct'
    df[fieldname] = new_figure
    return df

print('Functions successfully loaded.')

# -----
# -----

df_eucpi = StLouisFED_transformations(response_data = response_EUCPI)

# -----
# -----

# CPI plus 1 percent
df_eucpi = CPI_plus_pct(df = df_eucpi, annual_pct_over_CPI = 0.01, period = 1)
# CPI plus 2 percent
df_eucpi = CPI_plus_pct(df = df_eucpi, annual_pct_over_CPI = 0.02, period = 1)
# CPI plus 3 percent
df_eucpi = CPI_plus_pct(df = df_eucpi, annual_pct_over_CPI = 0.03, period = 1)
# CPI plus 4 percent
df_eucpi = CPI_plus_pct(df = df_eucpi, annual_pct_over_CPI = 0.04, period = 1)
# CPI plus 5 percent
df_eucpi = CPI_plus_pct(df = df_eucpi, annual_pct_over_CPI = 0.05, period = 1)

# -----
# -----

df_eucpi.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_EuroAreaCPI_automatic.csv", index = False)
df_eucpi.to_excel("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_EuroAreaCPI_automatic.xlsx", index = False)

print('EuroArea CPI data successfully imported.')

# -----