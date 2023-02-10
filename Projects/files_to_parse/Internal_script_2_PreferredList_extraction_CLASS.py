class PreferredList_extract:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
    
    def load_files(self):
        import pandas as pd
        self.preferred_list = pd.read_excel(self.input_path, sheet_name="1 Preferred List (Data)")
    
    def extract_preferred_list(self):
        self.bbg_import = self.preferred_list[self.preferred_list['Preferred_list_exists'] == True][["Security_name", "Bloomberg_ticker", "Asset_class", "Equity_country", "Fund_balanced_exists", "Fund_income_exists", "Fund_htt_exists", "Fund_smallercompanies_exists", "Fund_emergingmarkets_exists", "Fund_privateclient_or_AIM_exists"]]
        self.bbg_import = self.bbg_import.sort_values(by='Security_name')
        self.bbg_import = self.bbg_import.drop_duplicates()
    
    def save_preferred_list(self):
        self.bbg_import.to_csv(self.output_path, index=False)
        print("Preferred List successfully imported.")
        print(f"Preferred List filepath: {self.output_path}")

preferred_list = PreferredList_extract(
    input_path="F:/Investment Info/Preferred Stock List/Preferred List sheet (includes changes, updates, and history).xlsx",
    output_path="F:/Investment Info/Preferred Stock List/preferred_list_auto.csv",
)