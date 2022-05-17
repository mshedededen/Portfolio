#   Fetch in prices for companies located in invested_companies table

#   PSEUDOCODE
#   1. Connect to database
#   2. Read in database as dataframe
#   3. Using Quandl, fetch prices for invested_companies from the previous week
#   4. Format into the database format
#   5. Append prices into the table

# -----

#   1. CONNECT TO DATABASE
from distutils.log import error
from operator import concat
from matplotlib.pyplot import close
import psycopg2         #   to connect to PostgreSQL database
import numpy as np      #   to perform mathematical calculations
import pandas as pd     #   to manipulate dataframes
import yfinance as yf   #   to extract financials
import datetime as dt   #   to get today's date
import sqlalchemy       #   to connect to PostgreSQL database

conn = sqlalchemy.create_engine("postgresql+psycopg2://postgres:123@localhost/equity_research_dashboard")
print("Database connected")

#   2. READ IN DATABASE AS DATAFRAME
#invested_companies = pd.read_sql_query("SELECT * FROM invested_companies", conn)
invested_companies = pd.read_excel("C:/Users/shedd/Documents/MyLearning/Data Science/DS Projects/Equity research dashboard/Version 2 (May 2022)/Portfolio positions log.xlsx", sheet_name = "Positions")

#   3. USING YAHOO FINANCE, FETCH PRICES FOR invested_companies FROM THE PREVIOUS WEEK
# Yahoo Finance requires an extension to import prices for non-US companies. The following code adds this information in for fetching the correct prices.
invested_companies["country_extension"] = ""
for i in range(len(invested_companies["Equity_country"])):
    if invested_companies["Equity_country"][i] == "UK": invested_companies["country_extension"][i] = ".L"
    elif invested_companies["Equity_country"][i] == "Germany": invested_companies["country_extension"][i] = ".DE"
    elif invested_companies["Equity_country"][i] == "France": invested_companies["country_extension"][i] = ".PA"
    else: invested_companies["country_extension"][i] = ""
# If further unique country_listed values are added, these need to be inserted into the code. Ideally, all countries' extensions across the Yahoo Finance universe would be added.

def previous_days(M_or_F):
    today = dt.datetime.now()
    # Previous Friday
    closest_friday = today + dt.timedelta(days = (5-today.weekday()))   # Note: This is actually "sort of" incorrect. Yahoo Finance 'end date' argument takes date minus 1, for some reason.
    if closest_friday > today:
        closest_friday = closest_friday - dt.timedelta(days = 7)        
    # Previous Monday
    closest_monday = closest_friday - dt.timedelta(days = 5)
    # Convert dates to yyyy-mm-dd format
    closest_friday = closest_friday.strftime("%Y-%m-%d")
    closest_monday = closest_monday.strftime("%Y-%m-%d")
    # Allow users to return Monday or Friday
    if M_or_F == "Monday" or M_or_F == "M" or M_or_F == "Mon":
        return closest_monday
    elif M_or_F == "Friday" or M_or_F == "F" or M_or_F == "Fri":
        return closest_friday
    else:
        error

# The following code retrieves prices from Yahoo Finance.
df = yf.download(list(invested_companies["Ticker_simple"] + invested_companies["country_extension"]), start = previous_days("M"), end = previous_days("F"))
df = df["Adj Close"].reset_index()

#   4. FORMAT INTO THE DATABASE FORMAT
# The format is TICKER, DATE, CLOSE PRICE.
# Pivot dataframe longer, before reordering.
df = pd.melt(frame = df, id_vars = "Date", value_vars = df.columns[1:], var_name = "ticker", value_name = "price_close")
df = df[["ticker", "Date", "price_close"]]
# Remove any country extensions in the ticker column.
df["ticker"] = df["ticker"].str.split(".").str[0]
df = df.rename(columns = {"Date":"price_date"})
#   5. APPEND PRICES INTO THE TABLE
df.to_sql("prices_companies_V2", conn, # insert df into prices_companies TABLE using the conn CONNECTION.
    if_exists = "append",           # Ensure data is appended, not overwritten.
    index = False                   # We do not wish the index to be included in the table.
    )