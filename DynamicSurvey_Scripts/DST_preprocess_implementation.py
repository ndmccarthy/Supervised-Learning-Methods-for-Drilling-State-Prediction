# using this file to run commands that only need to run once and for testing

from DST_preprocessing import *
from DST_storage import *


print("Grabbing Requested Run data")
requested_runs_df = pd.read_excel("../../Requested_Run_Log.xlsx")
print("Creating and Cleaning Rig and Run Dataframes")
for rig in rig_files:
    rig_name = rig[6:12] + "" + rig[13:16]
    print(f"{rig_name}")
    print(f"\tCleaning")
    rig_df = cleanRigData(rig)
    print(f"\tSaving")
    with pd.ExcelWriter(f"../../Cleaned_{rig_name}.xlsx", engine='xlsxwriter') as writer:
        rig_df.to_excel(writer, sheet_name=rig_name, index=False)
    print(f'\tLooking for runs...')
    for ii in range(len(requested_runs_df)):
        run = requested_runs_df.iloc[ii]
        if rig_name == run["Well"]:
            run_num = run["Run"]
            entire_name = rig_name + '_' + run_num
            print(f"\t{entire_name}")
            print(f"\t\tCreating Dataframe")
            run_df = createRunDF(rig_df, run)
            print(f"\t\tSaving")
            with pd.ExcelWriter(f"../../Cleaned_{entire_name}.xlsx", engine='xlsxwriter') as writer:
                run_df.to_excel(writer, sheet_name=entire_name, index=False)
            print(f"\t\tRun Completed")
    print(f"Rig Completed")
print('All preprocessing completed!') 