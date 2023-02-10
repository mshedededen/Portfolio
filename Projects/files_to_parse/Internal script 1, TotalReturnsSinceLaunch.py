# Packages required
import pandas as pd
import fnmatch
import datetime as dt
import os

# ----- CURRENT DIRECTORY CHECK -----#

current_directory = os.getcwd()
print("Current directory: {}".format(current_directory))

# -----

# ----- READ FILES -----

# Read in ALL fund prices uploaded to the website
path_prices = "F:/Operations & IT/Website refresh/Funds pages/Historical prices"

Price_balanced_fund_personal = "/BFPersonalPrices.xls"
Price_balanced_fund_legacy = "/BFLegacyPrices.xls"
Price_income_fund_personal = "/IFPersonalPrices.xls"
Price_income_fund_legacy = "/IFLegacyPrices.xls"
Price_HTT_fund_personal = "/HTTPrices.xls"
Price_smallercompanies_fund_personal = "/SCFPersonalPrices.xls"
Price_smallercompanies_fund_legacy = "/SCFLegacyPrices.xls"
Price_emergingmarkets_fund_personal = "/EMFPersonalPrices.xls"
Price_emergingmarkets_fund_legacy = "/EMFLegacyPrices.xls"

# Read in ALL dividends uploaded to the website
path_dividends = "F:/Operations & IT/Website refresh/Funds pages/Historical dividends"

Dividend_balanced_fund_personal = "/BFPersonalDividends.xls"
Dividend_balanced_fund_legacy = "/BFLegacyDividends.xls"
Dividend_income_fund_personal = "/IFPersonalDividends.xls"
Dividend_income_fund_legacy = "/IFLegacyDividends.xls"
Dividend_HTT_fund_personal = "/HTTDividends.xls"
Dividend_smallercompanies_fund_personal = "/SCFPersonalDividends.xls"
Dividend_smallercompanies_fund_legacy = "/SCFLegacyDividends.xls"
Dividend_emergingmarkets_fund_personal = "/EMFPersonalDividends.xls"
Dividend_emergingmarkets_fund_legacy = "/EMFLegacyDividends.xls"

# Read in UNPAID dividends file (found in F:/Investment Info/Statistics)
path_unpaid_dividends = "//Server02/Shared/Investment Info/Statistics/Dividend forecasts (not yet paid).xlsx"
unpaid_dividends = pd.read_excel(path_unpaid_dividends)

print("Files successfully read into script.")
# ----- FUNCTIONS -----

# 1.1 Reading Price file(s)
def website_prices_transform(path, file_name):
    if fnmatch.fnmatch(file_name, "*personal*"):
        df = pd.read_excel(path + file_name, skiprows = 3).iloc[:,1:4]
        df.columns = ["Date", "Fund_Price", "Ex_dividend"]
        return df
    elif fnmatch.fnmatch(file_name, "*legacy*"):
        df = pd.read_excel(path + file_name, skiprows = 5).iloc[:, 2:5]
        df.columns = ["Date", "Fund_Price", "Ex_dividend"]
        return df
    elif fnmatch.fnmatch(file_name, "*HTT*"):
        df = pd.read_excel(path + file_name, skiprows = 3).iloc[:,1:4]
        df.columns = ["Date", "Fund_Price", "Ex_dividend"]
        return df
    else:
        print("No personal or legacy files inserted. Check file names.")

# 1.2 Reading Dividend file(s)
def website_dividends_transform(path, file_name, fund_name):
    if fnmatch.fnmatch(file_name, "*personal*"):
        df = pd.read_excel(path + file_name, skiprows = 5).iloc[:, 2:6]
        df.columns = ["Ex_dividend_date", "Dividend_payment_date", "Dividend_rate", "Interim_or_final"]
        df["Dividend_rate"] = df["Dividend_rate"]/100
        #####
        df["Status"] = "Actual"
        #####
        return df
    elif fnmatch.fnmatch(file_name, "*legacy*"):#
        df = pd.read_excel(path + file_name, skiprows = 6).iloc[:, 2:6]
        df.columns = ["Ex_dividend_date", "Dividend_payment_date", "Dividend_rate", "Interim_or_final"]
        df["Dividend_rate"] = df["Dividend_rate"]/100
        #####
        df["Status"] = "Actual"
        #####
        return df
    elif fnmatch.fnmatch(file_name, "*HTT*"):
        df = pd.read_excel(path + file_name, skiprows = 5).iloc[:, 2:6]
        df.columns = ["Ex_dividend_date", "Dividend_payment_date", "Dividend_rate", "Interim_or_final"]
        df["Dividend_rate"] = df["Dividend_rate"]/100
        #####
        df["Status"] = "Actual"
        #####
        # Append any forecast dividends
        if len(unpaid_dividends[unpaid_dividends["Fund_name"] == fund_name]) > 0:
            print("Uploading forecasts...")
            # Add dividends to dividend file
            forecasts = unpaid_dividends[unpaid_dividends["Fund_name"] == fund_name].iloc[
                :,unpaid_dividends[unpaid_dividends["Fund_name"] == fund_name].columns != "Fund_name"
                ]
            df = df.append(forecasts)

        #####

        return df
    else:
        print("No personal or legacy files inserted. Check file names.")

# Appending Personal and Legacy files for prices AND dividends
# RULE: Personal pricing supercedes Legacy files, always
# 2.1 Append price files
def append_prices(path, personal_file, legacy_file):
    # Retreive ALL personal file: Personal class dividends supercede legacy class dividends, in aggregate
    df_personal = website_prices_transform(path, file_name = personal_file)
    # Retreive first relevant dividend from legacy class, in aggregate
    df_legacy = website_prices_transform(path = path, file_name = legacy_file)
    df_legacy = df_legacy[df_legacy["Date"] < min(df_personal["Date"])]
    # Concatenate files
    df = pd.concat(
        objs = [
            df_personal,  # Transforming personal file
            df_legacy     # Transforming legacy file
        ],
        join = "outer"
    )
    # Return final dataframe
    return df

# 2.2 Append dividend files
def append_dividends(path, personal_file, legacy_file, fund_name):
    # Retreive ALL personal file: Personal class dividends supercede legacy class dividends, in aggregate
    df_personal = website_dividends_transform(path = path, file_name = personal_file, fund_name=fund_name)
    # Retreive first relevant dividend from legacy class, in aggregate
    df_legacy = website_dividends_transform(path = path, file_name = legacy_file, fund_name=fund_name)
    df_legacy = df_legacy[df_legacy["Dividend_payment_date"] < min(df_personal["Dividend_payment_date"])]
    # Concatenate files
    df = pd.concat(
        objs = [
            df_personal,
            df_legacy
        ],
        join = "outer"
    )
    #####
    
    # Append any forecast dividends
    if len(unpaid_dividends[unpaid_dividends["Fund_name"] == fund_name]) > 0:
        print("Uploading dividend forecasts for {}.".format(fund_name))
        # Add dividends to dividend file
        forecasts = unpaid_dividends[unpaid_dividends["Fund_name"] == fund_name].iloc[
            :,unpaid_dividends[unpaid_dividends["Fund_name"] == fund_name].columns != "Fund_name"
            ]
        df = df.append(forecasts)

    #####

    # Return final dataframe
    return df

# 3 GENERATE COMMON DATE WITH PRICING FILES, TO ENABLE MERGING
def common_price_dividend_date(dividend_file, price_file):
    # 1 Create empty list, which files are inserted into
    nearest_date = []
    # 2 Find closest next date that dividends can be linked to price (e.g. if XD date is a Saturday, we look for the Monday or next price)
    dividend_file = dividend_file[dividend_file["Ex_dividend_date"] < pd.to_datetime(dt.date.today())]
    # N.B. Using dt.datetime puts the time (e.g. 08:45.52) in there, which therefore means x < y, even if the dates of x and y are the equivalent. But, dates are in datetime format, so hence pd.to_datetime(dt.date.today())

    for i in dividend_file["Ex_dividend_date"]:                             # Using Ex Dividend Date because...?
        if i not in price_file["Date"]:
            count = i - price_file["Date"]                                  # Distance between each XD date and each price date
            nearest_date.append(i - max(count[count <= dt.timedelta(0)]))   # Search for next valid date (e.g. MAX date exluding all dates in the past)
        else:
            nearest_date.append(i)                                          # If XD date occurs on a date we have prices for, use this date
    # 3 Add nearest date as a field in the dividend file
    dividend_file["Nearest_dividend_date"] = nearest_date

    return(dividend_file)

# 4 FUNCTION TO COMBINE FILES
def combine_price_dividend_files(dividend_file, price_file):
    price_dividend_file = pd.merge(
        left = price_file,
        right = common_price_dividend_date(dividend_file = dividend_file, price_file = price_file),
        left_on = "Date", right_on = "Nearest_dividend_date", how = "outer"
        )
    price_dividend_file = price_dividend_file.drop(columns = "Nearest_dividend_date")
    price_dividend_file = price_dividend_file.sort_values(by = "Date", ascending = True)
    price_dividend_file["Dividend_rate"] = price_dividend_file["Dividend_rate"].fillna(0)

    return price_dividend_file


# 5 Function to calculate all fields found in TOTAL RETURNS since launch.xlsx
def TR_formulae(df, starting_number_of_units):
    # 1 Calucate units which can be purchased with a single dividend
    df["Units_per_dividend"] = df["Dividend_rate"] / df["Fund_Price"] # Dividends are reinvested at 4 dps

    # 2 Calculate cumulative units
    Cumulative_units = []
    for i in range(len(df)):
        if i < 1: Cumulative_units.append(starting_number_of_units)
        else:
            x = round((df["Units_per_dividend"][i] * Cumulative_units[i-1]), 3) + Cumulative_units[i-1]
            Cumulative_units.append(x)
    df["Cumulative_units"] = Cumulative_units
    
    # 3 Calculate Total Value
    df["Total_value"] = df["Fund_Price"] * df["Cumulative_units"]
    
    # 4 Calculate Total Return, Daily
    df["Total_return_daily"] = df["Total_value"].pct_change(periods = 1)
    
    # 5 Calculate Total Return, since inception
    Total_return_based_100 = []
    for i in range(len(df)):
        if i < 1: Total_return_based_100.append(1)
        else: Total_return_based_100.append((Total_return_based_100[i-1] * (df["Total_return_daily"][i]+1)))
    df["Total_return_based_100"] = Total_return_based_100
    
    # 6 Calculate Capital Return, Daily
    df["Capital_return_daily"] = df["Fund_Price"].pct_change(periods = 1)

    # 7 Calculate dividend yield
    dividend_yield = []
    for n, i in enumerate(df["Date"]):
        # Calculate dividend rate over a TTM period
        dividend_yield.append(
            sum(df[(df["Date"] <= i) & (df["Date"] > (i - dt.timedelta(days = 365)))]["Dividend_rate"]) 
            / float(df[df["Date"] == i]["Fund_Price"]))
            
    df["Dividend_yield"] = dividend_yield
    
    return df

print("Local functions successfully read into script.")

# ----- TRANSFORMATIONS -----
# 1.1 Combine price files
Price_balanced_fund = append_prices(path = path_prices, personal_file = Price_balanced_fund_personal, legacy_file = Price_balanced_fund_legacy)
Price_income_fund = append_prices(path = path_prices, personal_file = Price_income_fund_personal, legacy_file = Price_income_fund_legacy)
Price_HTT_fund = website_prices_transform(path = path_prices, file_name = Price_HTT_fund_personal)
Price_smallercompanies_fund = append_prices(path = path_prices, personal_file = Price_smallercompanies_fund_personal, legacy_file = Price_smallercompanies_fund_legacy)
Price_emergingmarkets_fund = append_prices(path = path_prices, personal_file = Price_emergingmarkets_fund_personal, legacy_file = Price_emergingmarkets_fund_legacy)

# 1.2 Combine dividend files
Dividend_balanced_fund = append_dividends(path = path_dividends, personal_file = Dividend_balanced_fund_personal, legacy_file = Dividend_balanced_fund_legacy, fund_name="McInroy & Wood Balanced Fund")
Dividend_income_fund = append_dividends(path = path_dividends, personal_file = Dividend_income_fund_personal, legacy_file = Dividend_income_fund_legacy, fund_name="McInroy & Wood Income Fund")
Dividend_HTT_fund = website_dividends_transform(path = path_dividends, file_name = Dividend_HTT_fund_personal,fund_name="McInroy & Wood HTT Fund")
Dividend_smallercompanies_fund = append_dividends(path = path_dividends, personal_file = Dividend_smallercompanies_fund_personal, legacy_file = Dividend_smallercompanies_fund_legacy, fund_name="McInroy & Wood Smaller Companies Fund")
Dividend_emergingmarkets_fund = append_dividends(path = path_dividends, personal_file = Dividend_emergingmarkets_fund_personal, legacy_file = Dividend_emergingmarkets_fund_legacy, fund_name="McInroy & Wood Emerging Markets Fund")

# 2 Combine price AND dividend files
Price_dividend_balanced_fund = combine_price_dividend_files(dividend_file = Dividend_balanced_fund, price_file = Price_balanced_fund).reset_index(drop = True)
Price_dividend_income_fund = combine_price_dividend_files(dividend_file = Dividend_income_fund, price_file = Price_income_fund).reset_index(drop = True)
Price_dividend_HTT_fund = combine_price_dividend_files(dividend_file = Dividend_HTT_fund, price_file = Price_HTT_fund).reset_index(drop = True)
Price_dividend_smallercompanies_fund = combine_price_dividend_files(dividend_file = Dividend_smallercompanies_fund, price_file = Price_smallercompanies_fund).reset_index(drop = True)
Price_dividend_emergingmarkets_fund = combine_price_dividend_files(dividend_file = Dividend_emergingmarkets_fund, price_file = Price_emergingmarkets_fund).reset_index(drop = True)

# 3 Calculate remaining fields (formulae) found in TOTAL RETURNS since launch file
price_dividend_balanced_fund = TR_formulae(df = Price_dividend_balanced_fund, starting_number_of_units = 100)
Price_dividend_income_fund = TR_formulae(df = Price_dividend_income_fund, starting_number_of_units = 100)
Price_dividend_HTT_fund = TR_formulae(df = Price_dividend_HTT_fund, starting_number_of_units = 100)
Price_dividend_smallercompanies_fund = TR_formulae(df = Price_dividend_smallercompanies_fund, starting_number_of_units = 100)
Price_dividend_emergingmarkets_fund = TR_formulae(df = Price_dividend_emergingmarkets_fund, starting_number_of_units = 100)

# 4 Combine files
price_dividend_balanced_fund.insert(loc = 0, column = "Portfolio name", value = "MW Balanced Fund")
Price_dividend_income_fund.insert(loc = 0, column = "Portfolio name", value = "MW Income Fund")
Price_dividend_HTT_fund.insert(loc=0, column = "Portfolio name", value = "MW HTT Fund")
Price_dividend_smallercompanies_fund.insert(loc=0, column = "Portfolio name", value = "MW Smaller Companies Fund")
Price_dividend_emergingmarkets_fund.insert(loc=0, column="Portfolio name", value = "MW Emerging Markets Fund")

combined_df = pd.concat(
    [price_dividend_balanced_fund, Price_dividend_income_fund, Price_dividend_HTT_fund, Price_dividend_smallercompanies_fund, Price_dividend_emergingmarkets_fund],
    ignore_index=True
    )

print("Transformations of data successfully completed.")
# 4 Save files in various locations in various formats on the F DrivE
if dt.datetime.today().weekday() == 4:  # Clause to save additional files down every Friday as a backup
    Price_dividend_balanced_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/FRIDAY BACKUP Prices_balanced_fund.csv", index = False)
    Price_dividend_income_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/FRIDAY BACKUP Prices_income_fund.csv", index = False)
    Price_dividend_HTT_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/FRIDAY BACKUP Prices_HTT_fund.csv", index = False)
    Price_dividend_smallercompanies_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/FRIDAY BACKUP Prices_smallercompanies_fund.csv", index = False)
    Price_dividend_emergingmarkets_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/FRIDAY BACKUP Prices_emergingmarkets_fund.csv", index = False)

# 4.1 Investment Info/Statistics

writer = pd.ExcelWriter("F:/Investment Info/Statistics/Data_raw_files/Prices_MWP_automatic.xlsx")                                   # Write files to Excel
price_dividend_balanced_fund.to_excel(excel_writer = writer, sheet_name = "Balanced_fund_price", index = False)                     # Write each file to a different sheet in the same Excel file
Price_dividend_income_fund.to_excel(excel_writer = writer, sheet_name = "Income_fund_price", index = False)                         # Write each file to a different sheet in the same Excel file
Price_dividend_HTT_fund.to_excel(excel_writer = writer, sheet_name = "HTT_fund_price", index = False)                               # Write each file to a different sheet in the same Excel file
Price_dividend_smallercompanies_fund.to_excel(excel_writer = writer, sheet_name = "SmallerCompanies_fund_price", index = False)     # Write each file to a different sheet in the same Excel file
Price_dividend_emergingmarkets_fund.to_excel(excel_writer = writer, sheet_name = "EmergingMarkets_fund_price", index = False)       # Write each file to a different sheet in the same Excel file
writer.save()                                                                                                                       # Save writer

# 4.2 Investment Info/Statistics/Data_raw_files/
Price_dividend_balanced_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_balanced_fund.csv", index = False)
Price_dividend_income_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_income_fund.csv", index = False)
Price_dividend_HTT_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_HTT_fund.csv", index = False)
Price_dividend_smallercompanies_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_smallercompanies_fund.csv", index = False)
Price_dividend_emergingmarkets_fund.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_emergingmarkets_fund.csv", index = False)
combined_df.to_csv("//Server02/Shared/Investment Info/Statistics/Data_raw_files/Prices_MWP_automatic.csv", index = False)

print("Most recent prices of MWP funds successfully saved.")