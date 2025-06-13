# pip installed hmmlearn package 
import pandas as pd

def prepare_data():
    # read in data
    print('Reading Training Set 1')
    dfb = pd.read_excel('../../Cleaned_Flybar1WB.xlsx')
    print("Reading Training Set 2")
    dfc = pd.read_excel('../../Cleaned_Flybar1WC.xlsx')
    print("Reading Test Set")
    df_test = pd.read_excel('../../Cleaned_Flybar2WC.xlsx')
    # joining training data sets under assumption that they have to start and end on state 0
    dfc.drop(columns=['MR_RPM-MAG-AVG.MR', 'MR_GRAV.M'], inplace=True)
    df_train = pd.concat([dfb, dfc], ignore_index=True)
    # take out timestamps
    df_train.drop(columns=['Time'], inplace=True)
    df_test.drop(columns=['Time', 'MR_RPM-MAG-AVG.MR', 'MR_GRAV.M'], inplace=True)
    # standardize data to avoid overweighting some features over others
    print('Standardizing Data')
    mean = df_train.mean(axis=0)
    std = df_train.std(axis=0)
    df_train = (df_train - mean) / std
    df_test = (df_test - mean) / std
    print('All data prepared')
    return df_train, df_test

def count_hmm_parameters(n_components, n_features):
    # Initial state probabilities
    pi = n_components - 1
    # Transition matrix
    A = n_components * (n_components - 1)
    # Means
    mu = n_components * n_features
    # covariance type is full
    sigma = int(n_components * (n_features * (n_features + 1) / 2))
    return pi + A + mu + sigma


def save_results(collecting_results, df, states, n_states):
    if collecting_results:
        print('Saving Test Data and Predictions')
        df['Predicted_State'] = states.tolist()
        with pd.ExcelWriter(f"../../Test_Data_Predictions_{n_states}StateHMM.xlsx", engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name=f"{n_states} State HMM", index=False)