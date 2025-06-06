# this script contains functions for cleaning the DST data

import pandas as pd

def cleanRigData(rig_file_path):
    # this function creates a pandas dataframe for the well spreadsheet data, gets rid of unwanted columns, renames columns, deals with nulls, and addresses datatypes
    col_to_drop = ["RT_TVD", "RT_ACTIVITY", "RT_Botm", "RT_SLIDE", "RT_ROP",
               "MR_INC.M", "MR_LINC.M", "MR_AZM.M", "MR_LAZM.MR", "MR_DIPA.M", "MR_MAGF.M", "MR_TEMP.M", "MR_VIBT.MR", "MR_GAMA.5S5A",
               "PD_Temperature", "PD_X Vibration", "PD_Y Vibration", "PD_Gamma"]
    new_col_names = {'Time': 'RT_Time',
                 'Depth': 'RT_Depth',
                 'Rotation_Validator': 'MR_ROTATION',
                 'Motor_RPM': "MR_RPM-AVG.MR",
                 'Surface_RPM': "RT_RPM.W",
                 'Slide_Validator': 'RT_SLIDE_BIT',
                 'Motor_Axial_Vibration': 'MR_VIBA.MR',
                 'Motor_Lateral_Vibration': 'MR_VIBL.MR',
                 'Pulser_Axial_Vibration': 'PD_Axial Vibration',
                 'Pulser_Lateral_Vibration': 'PD_Lateral Vibration',
                 'WOB': 'RT_WOB'}
    aggregated_cols = {'Flow_Validator': ['MR_FLOW.M', 'PD_Pump Event'],
                       'GPM': ['RT_PUMP_ON', 'RT_PUMP_OFF']}
    validation_cols = ['Flow_Validator', 'Rotation_Validator', 'Slide_Validator']
    # create data frame for well
    df = pd.read_excel(rig_file_path)
    # rename columns for clarity
    for key, value in new_col_names.items():
        # key is new name, value is old name
        df[key] = df[value]
    # delete irrelevant columns in well df
    col_to_drop += [*new_col_names.values()]
    df.drop(columns=col_to_drop, inplace=True)
    col_to_drop = [] # empty for future refill and reuse
    # fill nans with last recorded value
    df.ffill(inplace=True)
    # fill remaining nans (only at top where no recordings yet) with 0
    df.fillna(0, inplace=True)
    # fix PD_Pump Event to be int rather than string
    def stringToInt(cell):
        if cell == "Pumps Off Event":
            return 0
        elif cell == 'Pumps On Event':
            return 1
    df['PD_Pump Event'] = df["PD_Pump Event"].apply(stringToInt)
    # average columns that need to be combined
    for key, value in aggregated_cols.items():
        # key is new column, value is list of old column names
        df[key] = (df[value[0]] + df[value[1]]) / 2
        col_to_drop.append(value[0])
        col_to_drop.append(value[1])
    df.drop(columns=col_to_drop, inplace=True)
    # ensure timestamp is in datetime format
    df["Time"] = pd.to_datetime(df["Time"])
    # make validation columns booleans
    for val_col in validation_cols:
        df[val_col] = df[val_col].astype(bool)
    return df

def defineDSM(row):
    if row['Flow_Validator'] == True:
        if row['Slide_Validator'] == True:
            return 2 # Sliding Drilling
        elif row['Rotation_Validator'] == True:
            if row['WOB'] > 0:
                return 4 # Rotational Drilling
            return 3 # Rotating
        return 1 # Pumps On
    return 0 # Pumps Off

def findClosestMatch(df, date, depth):
    # returns the row id that corresponds closest to the given date and depth
    # dates must be only date (not time included)
    date = pd.to_datetime(date).date()
    df = df.copy() # avoiding modifying original dataframe
    df["Date"] = df["Time"].dt.date
    # filter by date
    filtered_df = df[(df["Date"] == date)]
    # make depth column integers
    depth_series = filtered_df["Depth"]
    # create column of absolute value of entry depth - given depth
    abs_series = abs(depth_series - depth)
    # find minimum in absolute series
    index = abs_series.idxmin()
    return index

def createRunDF(rig_df, run_specs):
    # extract filters
    start_date = run_specs["Date In"]
    end_date = run_specs["Date Out"]
    start_depth = run_specs["MD In"]
    end_depth = run_specs["MD Out"]
    # find first row of run
    start_id = findClosestMatch(rig_df, start_date, start_depth)
    end_id = findClosestMatch(rig_df, end_date, end_depth) + 1 # indexing is not inclusive of last index
    run_df = rig_df.loc[start_id: end_id].copy() # had to use .loc instead of .iloc because row names still correspond to original row number
    return run_df