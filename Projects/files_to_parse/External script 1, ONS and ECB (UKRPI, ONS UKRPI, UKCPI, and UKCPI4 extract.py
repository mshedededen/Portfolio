# This script currently ONLY extracts UK RPI and UK CPI data
# This script may be adjusted / expanded to extract other data publicly available on the ONS website

# -----

# Libraries
import pandas as pd
import datetime as dt
import requests
import io
import numpy as np

# -----
# -----

# Fetching files from ONS website direct
URL_UKRPI = 'https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/chaw/mm23'
URL_UKCPI = 'https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7bt/mm23'

response_UKRPI = requests.get(URL_UKRPI)
response_UKCPI = requests.get(URL_UKCPI)


print('UK RPI response message: ', response_UKRPI)
print('UK CPI response message: ', response_UKCPI)

# -----
# -----

def ONS_transformations(response_data):
    # Read response into a dataframe format
    df = pd.read_csv(io.StringIO(response_data.text), skiprows = 7)
    df.columns = ["Date", "Value"]                                  # Change column names
    df["Date"] = df["Date"].astype("str")                           # Convert 'Date' column to string, required for slicing
    df = df[df["Date"].str.len() == 8]                              # Filter, using text, annual and quarterly RPI numbers
    df.reset_index(drop = True, inplace = True)                     # Reset index, now that final dataset is ready

    def last_day_of_month(any_day):                                 # Function to retrieve final day of the month
        next_month = any_day.replace(day=28) + dt.timedelta(days=4) # The day 28 exists in every month. 4 days later, it's always next month
        return next_month - dt.timedelta(days=next_month.day)       # subtracting the number of the current day brings us back one month
    
    new_date_list = []
    for i in range(len(df)):
        new_date = dt.datetime.strptime(df["Date"][i], "%Y %b")
        new_date = last_day_of_month(new_date)
        new_date_list.append(new_date)
    
    df.loc[:, "Date"] = new_date_list
    #df["Date"] = new_date_list

    df["Value"] = df["Value"].astype("float64")

    return df

# -----

# Function 4: Calculate CPI plus X percent
def CPI_plus_pct(df, annual_pct_over_CPI, period, method = "New"):
    if method == "New":
    # 'New' method refers to ensure that the difference is effectively always exactly annual_pct_over_CPI
    # Issue was that annual_pct_over_CPI ^ (1/12) can create minut differences between annual_pct_over_CPI and the difference(s)
        new_figure = []
        for n, i in enumerate(df["Value"]):
            if np.isnan(df["Value"].shift(12)[n]):
            # Conditional statement: Apply where n <= 12
                if n == 0:
                    new_figure.append(df["Value"][n])
                # Conditional statement: Apply where n == 0
                else:
                # Conditional statement: Apply where n != 0 & n <= 12
                    new_figure.append(
                        ((df["Value"][n]/df["Value"][0]) + ((1+annual_pct_over_CPI)**(n/12)-1))*df["Value"][0]
                    )
            else:
            # Conditional statement: Apply where n > 12
                value = new_figure[n-12] * (
                    1 + df["Value"].pct_change(periods = 12)[n] + annual_pct_over_CPI
                )
                new_figure.append(value)
        fieldname = 'CPI_plus_' + str(int(annual_pct_over_CPI * 100)) + 'pct'
        df[fieldname] = new_figure
    elif method == "Old":
    # 'Old' method refers to previous way of doing things
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
    else:
        print("Invalid input for 'method'")
    return df

print('Functions successfully loaded.')

# -----
# -----

df_rpi = ONS_transformations(response_data = response_UKRPI)
df_cpi = ONS_transformations(response_data = response_UKCPI)

# -----
# -----

df_rpi.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_UKRPI_automatic.csv", index = False)
df_rpi.to_excel("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_UKRPI_automatic.xlsx", index = False)

# -----
# -----

# AS old period-agnostic CPI + x% calculations

# CPI plus 1 percent
df_cpi_old = CPI_plus_pct(df = df_cpi, annual_pct_over_CPI = 0.01, period = 1, method = "Old")
# CPI plus 2 percent
df_cpi_old = CPI_plus_pct(df = df_cpi_old, annual_pct_over_CPI = 0.02, period = 1, method = "Old")
# CPI plus 3 percent
df_cpi_old = CPI_plus_pct(df = df_cpi_old, annual_pct_over_CPI = 0.03, period = 1, method = "Old")
# CPI plus 4 percent
df_cpi_old = CPI_plus_pct(df = df_cpi_old, annual_pct_over_CPI = 0.04, period = 1, method = "Old")
# CPI plus 5 percent
df_cpi_old = CPI_plus_pct(df = df_cpi_old, annual_pct_over_CPI = 0.05, period = 1, method = "Old")

df_cpi_old.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_UKCPI_monthly_automatic.csv", index = False)
df_cpi_old.to_excel("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_UKCPI_monthly_automatic.xlsx", index = False)

# -----
# -----

# HS new annual CPI + x% calculations

# CPI plus 1 percent
df_cpi_new = CPI_plus_pct(df = df_cpi, annual_pct_over_CPI = 0.01, period = 1, method = "New")
# CPI plus 2 percent
df_cpi_new = CPI_plus_pct(df = df_cpi_new, annual_pct_over_CPI = 0.02, period = 1, method = "New")
# CPI plus 3 percent
df_cpi_new = CPI_plus_pct(df = df_cpi_new, annual_pct_over_CPI = 0.03, period = 1, method = "New")
# CPI plus 4 percent
df_cpi_new = CPI_plus_pct(df = df_cpi_new, annual_pct_over_CPI = 0.04, period = 1, method = "New")
# CPI plus 5 percent
df_cpi_new = CPI_plus_pct(df = df_cpi_new, annual_pct_over_CPI = 0.05, period = 1, method = "New")

print("CPI transformations complete.")

df_cpi_new.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_UKCPI_annual_automatic.csv", index = False)
df_cpi_new.to_excel("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_UKCPI_annual_automatic.xlsx", index = False)

print('United Kingdom RPI and CPI data successfully imported.')