# used for making plotting functions on various spreadsheets for the project

import pandas as pd
import matplotlib.pyplot as plt
'''
# read in data (right now only first run recorded)
data_path = '..\cleaned_run_data.xlsx'
run_data = pd.read_excel(data_path)

# column groups
misc = ['OG_Index', 'RT_SLIDE_BIT']
time = ['RT_Time']
depth = ['RT_Depth']
flow = ['RT_PUMP_ON', 'RT_PUMP_OFF', 'MR_FLOW.M', 'PD_Pump Event']
rotation = ['RT_ROP', 'RT_RPM.W', 'MR_ROTATION', 'MR_RPM-AVG.MR']
weight = ['RT_WOB']
gamma = ['MR_GAMA.5S5A', 'PD_Gamma']
vibration =['MR_VIBA.MR', 'MR_VIBL.MR', 'PD_Axial Vibration', 'PD_Lateral Vibration']


# reduce data
drop_cols = misc + flow + rotation + weight + gamma + vibration
time_depth_df = run_data.drop(drop_cols, axis=1)
time_depth_df = pd.wide_to_long(time_depth_df, [time + depth], i=0, j=1)
print(time_depth_df.head())

# plot
#plotly.plot(time_depth_df, 'line')
'''

df = pd.read_excel("../../Cleaned_Flybar1WB.xlsx")
plt.figure()
plt.scatter(df['Motor_Axial_Vibration'], df['Motor_Lateral_Vibration'], c='blue')
plt.scatter(df['Pulser_Axial_Vibration'], df['Pulser_Lateral_Vibration'], c='red')
plt.title('Vibration Instances')
plt.xlabel('Axial')
plt.ylabel('Lateral')
plt.legend()
plt.show()