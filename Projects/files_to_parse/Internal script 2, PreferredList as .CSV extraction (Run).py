import pandas as pd
from Internal_script_2_PreferredList_extraction_CLASS import PreferredList_extract

preferred_list = PreferredList_extract(
    input_path="F:/Investment Info/Preferred Stock List/Preferred List sheet (includes changes, updates, and history).xlsx",
    output_path="F:/Investment Info/Preferred Stock List/preferred_list_auto.csv",
)

preferred_list.load_files()
preferred_list.extract_preferred_list()
preferred_list.save_preferred_list()