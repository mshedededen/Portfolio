# financials_companies_fetch

# libraries
import numpy as np      #   to perform mathematical calculations
import pandas as pd     #   to manipulate dataframes
import datetime as dt   #   to get years for each financial statement, to standardise
import sqlalchemy       #   to connect to PostgreSQL database

# read excel sheets in
filepath = "C:/Users/shedd/Documents/MyLearning/Data Science/DS Projects/Equity research dashboard/financials_MSFT.xlsx"
df = pd.read_excel(filepath)
# transform data to be long rather than wide
df = pd.melt(frame = df, id_vars = ["Ticker", "Statement", "Line item"], value_vars = df.columns[3:], var_name = "Date", value_name = "Value")
df["Financial year"] = df["Date"].dt.year

# insert data into table within database
conn = sqlalchemy.create_engine("postgresql+psycopg2://postgres:123@localhost/equity_research_dashboard") # Connect to database
df.rename(columns = {"Ticker": "ticker", "Statement": "statement", "Line item":"line_item", "Date":"date", "Value": "value", "Financial year": "financialyear"}, inplace = True)
df.to_sql("financials_companies", conn, # insert df into prices_companies TABLE using the conn CONNECTION.
    if_exists = "append",               # Ensure data is appended, not overwritten.
    index = False                       # We do not wish the index to be included in the table.
    )