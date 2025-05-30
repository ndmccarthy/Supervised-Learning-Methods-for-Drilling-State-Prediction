# using this file to run commands that only need to run once and for testing

from DST_preprocessing import *
from DST_storage import *

run_path = new_file_paths["run_data"]
df = pd.read_excel(run_path, sheet_name='Flybar 1 WB Run 7')
new_df = transformRunData(df, indicators)
print(new_df.head(25))
