# this script contains functions for cleaning the DST data

import pandas as pd


def findClosestMatch(df, date, depth):
    # returns the row id that corresponds closest to the given date and depth
    # dates must be only date (not time included)
    date = pd.to_datetime(date).date()
    df = df.copy() # avoiding modifying original dataframe
    df["Date"] = df["RT_Time"].dt.date
    # filter by date
    filtered_df = df[(df["Date"] == date)]
    # make depth column integers
    depth_series = filtered_df["RT_Depth"]
    # create column of absolute value of entry depth - given depth
    abs_series = abs(depth_series - depth)
    # find minimum in absolute series
    index = abs_series.idxmin()
    return index
    

def cleanRigData(rig_file_path, drop_columns):
    # this function creates a pandas dataframe for the well spreadsheet data and gets rid of unwanted columns and rows without depth readings
    # create data frame for well
    df = pd.read_excel(rig_file_path)
    # delete irrelevant columns in well df
    df = df.drop(columns=drop_columns)
    # if no depth reading, delete the row
    df = df.dropna(subset=["RT_Depth"])
    # remove rows that have no data (outside of time and depth)
    exclude_cols = ["RT_Time", "RT_Depth"]
    rows_to_drop = df[df.drop(columns=exclude_cols).isna().all(axis=1)].index
    df = df.drop(rows_to_drop)
    # ensure timestamp is in datetime format
    df["RT_Time"] = pd.to_datetime(df["RT_Time"])
    return df

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

def transformRunData(run_df, indicator_dict):
    transformed_run_df = run_df.copy()
    def process_row(row, prev_row):
        for indicator in indicator_dict.keys():
            calculated = calculateIndicator(indicator_dict, indicator, row)
            if calculated is not None:
                row[indicator] = calculated
            else:
                row[indicator] = prev_row.get(indicator, None)  # Get previous row's indicator value
        prev_row.update(row)  # Update prev_row dictionary
        return row
    prev_row = {}
    transformed_run_df = transformed_run_df.apply(lambda row: process_row(row, prev_row), axis=1)
    # Drop unnecessary columns
    cols_to_drop = [col for sublist in indicator_dict.values() for col in sublist]
    transformed_run_df.drop(columns=cols_to_drop, inplace=True, errors='ignore')
    return transformed_run_df

def calculateIndicator(indicator_dict, indicator, df_row):
    col_list = indicator_dict[indicator]
    measurements = []
    for item in col_list:
        measurement = df_row[item]
        if pd.isna(measurement) != True: # when cell is not nan, add it to the measurement set
            measurements.append(measurement)
    if len(measurements) == 0:
        return None
    if len(measurements) == 1:
        return measurements[0]
    else:
        calculated_indicator = sum(measurements)/len(measurements)
        return calculated_indicator
    
#def calculateDSM(indicators, row):
    # estimates drilling state machine based on flow, vibration, rotation, and WOB

def saveToExcel(df_dict, file_path):
    # the excel must already exist for this to work since we are only appending sheets
    print("Saving:")
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        for key, df in df_dict.items():
            print(f"\t{key}")
            df.to_excel(writer, sheet_name=key)

def createCleanRigandRunDfs(rig_files: list, col_to_drop: list, requested_runs_df):
    print("Creating and Cleaning Rig and Run Dataframes")
    rig_dfs = {}
    run_dfs = {}
    for rig in rig_files:
        rig_name = rig[62:70] + " " + rig[70:72]
        print(f"\t{rig_name}")
        rig_df = cleanRigData(rig, col_to_drop)
        rig_dfs[rig_name] = rig_df
        for ii in range(len(requested_runs_df)):
            run = requested_runs_df.iloc[ii]
            if rig_name == run["Well"]:
                run_num = run["Run"]
                print(f"\t\t{run_num}")
                entire_name = rig_name + ' ' + run_num
                run_df = createRunDF(rig_df, run)
                run_dfs[entire_name] = run_df
    return (rig_dfs, run_dfs)