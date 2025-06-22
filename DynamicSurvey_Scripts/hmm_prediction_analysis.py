# looking at parameter stats for best models with 2-15 states
# trying to identify how it distinguished states and usability by client
# using random forest to dertermine information gain for each state

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# initial_run_paths = f"../../HMM_Mapping_Data/HMM_Mapping{num_states}.xlsx"
# wob_run_paths = f"../../HMM_WOB/Mapped_Predictions/HMM_Mapping{num_states}.xlsx"

# initial_plot_paths = f"../../HMM_Prediction_Plots/{num_states}-State_{col.replace('_', '-')}.png"
# wob_plot_paths = f"../../HMM_WOB/WOB_Prediction_Plots/{num_states}-State_WOB-Model_{col.replace('_', '-')}.png"

# initial_state_limit = 16
# wob_state_limit = 11
'''
for num_states in range(2, 11):
    # read in data sets
    print(f'Reading in {num_states}-State Data')
    df = pd.read_excel(f"../../HMM_WOB/Mapped_Predictions/HMM_Mapping{num_states}.xlsx")
    df.drop(columns=['Depth'], inplace=True) # don't need to analyze depth

    # plot features by state
    print(f"Plotting {num_states}-State Features")
    for col in df.columns:
        if col != 'Predicted State':
            plt.figure(figsize=(8, 4))
            sns.boxplot(data=df, x='Predicted State', y=col)
            plt.title(f"{col} Distribution by Predicted State in {num_states}-State Model")
            plt.savefig(f"../../HMM_WOB/WOB_Prediction_Plots/{num_states}-State_WOB-Model_{col.replace('_', '-')}.png", bbox_inches='tight')
            plt.close()
print('Feature Analysis Complete')

'''

# now I want to look at how often each state occurs in each model
for num_states in range(2, 11):
    # read in data sets
    print(f'Reading in {num_states}-State Data')
    df = pd.read_excel(f"../../HMM_WOB/Mapped_Predictions/HMM_Mapping{num_states}.xlsx")

    # create answer set
    result_list = []

    # count number of entries for each state and divide by total to get % makeup
    total_count = len(df)
    for state in range(num_states):
        temp_df = df[df['Predicted State'] == state]
        count = len(temp_df)
        state_percent = round((count / total_count) * 100, 1)
        result_list.append({'State': state, 'Percentage': state_percent})

    result = pd.DataFrame(result_list)
    
    # plot results
    plt.figure()
    sns.barplot(data = result, x = 'State', y = 'Percentage')
    plt.title(f"State Make-up of {num_states}-State WOB Model")
    plt.xlabel('Hidden State')
    plt.ylabel('Percentage of Total Observations')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

    print(result)