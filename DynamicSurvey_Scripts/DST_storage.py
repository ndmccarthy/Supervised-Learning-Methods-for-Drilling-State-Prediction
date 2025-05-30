# this file is used to store unchanging variables concerning files

import pandas as pd

# store excel file paths
rig_files = ["C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/Flybar 1WB_filtered_data.xlsx", 
         "C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/Flybar 1WC_filtered_data.xlsx", 
         "C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/Flybar 2WC_filtered_data.xlsx"]
# create df of drill runs
runs_df = pd.read_excel("C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/Requested_Run_Log.xlsx")
# list columns to get rid of
col_to_drop = ["RT_TVD", "RT_ACTIVITY", "RT_Botm", "RT_SLIDE", 
               "MR_INC.M", "MR_LINC.M", "MR_AZM.M", "MR_LAZM.MR", "MR_DIPA.M", "MR_MAGF.M", "MR_TEMP.M", "MR_VIBT.MR",
               "PD_Temperature", "PD_X Vibration", "PD_Y Vibration"]
# create dictionary of columns used to calculate indicators
indicators = {"Flow": ["RT_PUMP_OFF", "RT_PUMP_ON"],
                "Rotation": ["MR_RPM-AVG.MR", "RT_RPM.W"],
                "Vibration": ["MR_VIBA.MR", "MR_VIBL.MR", "PD_Axial Vibration", "PD_Lateral Vibration"],
                "ROP": ["RT_ROP"],
                "WOB": ["RT_WOB"]}
# store paths for excel files to be created
new_file_paths = {'rig_data': "C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/cleaned_rig_data.xlsx",
                  'run_data': "C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/cleaned_run_data.xlsx",
                  'transformed_run_data': "C:/Users/nicol/OneDrive/Documents/Dynamic Survey Tool Project/transformed_run_data.xlsx"}
