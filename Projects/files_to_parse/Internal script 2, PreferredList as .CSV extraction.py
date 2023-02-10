# Load libraries
import pandas as pd

# Load files required
preferred_list = pd.read_excel("F:/Investment Info/Preferred Stock List/Preferred List sheet (includes changes, updates, and history).xlsx", sheet_name = "1 Preferred List (Data)")

bbg_import = preferred_list[preferred_list['Preferred_list_exists'] == True][["Security_name", "Bloomberg_ticker", "Asset_class", "Equity_country", "Fund_balanced_exists", "Fund_income_exists", "Fund_htt_exists", "Fund_smallercompanies_exists", "Fund_emergingmarkets_exists", "Fund_privateclient_or_AIM_exists"]]
bbg_import = bbg_import.sort_values(by = 'Security_name')
bbg_import = bbg_import.drop_duplicates()

# Extract preferred list
bbg_import.to_csv("F:/Investment Info/Misc/MS/Projects (big)/0 Bloomberg processes, Data preparation/preferred_list_auto.csv", index = False)
bbg_import.to_csv("F:/Investment Info/Preferred Stock List/preferred_list_auto.csv", index = False)
print("Preferred List successfully imported.")
print("Preferred List filepath: F:/Investment Info/Preferred Stock List/preferred_list_auto.csv")