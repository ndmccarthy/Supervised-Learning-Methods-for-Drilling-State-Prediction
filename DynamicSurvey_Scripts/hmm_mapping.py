# looking at most successful HMM implementations and recording labels for visual inspection

from hmmlearn.hmm import GaussianHMM
from hmm_functions import *
import numpy as np

best_combos = {'Just Pulser': {11191998: [2, 14],
                               2021: [5, 6, 9, 10],
                               61225: [7],
                               1130: [8],
                               26: [11],
                               792022: [12],
                               2: [13],
                               61: [15]},
               'Just Motor': {4: [3],
                              2021: [4]}} # dict(feature set: {seed: [number of states]})
included_features = {'Just Motor': ['Motor_Axial_Vibration', 'Motor_Lateral_Vibration'],
                     'Just Pulser': ['Pulser_Axial_Vibration', 'Pulser_Lateral_Vibration']}

df_train, df_test = prepare_data() # grab all data
num_observations = len(df_test) # record for AIC/BIC later

print("Training and Testing Options")
for feature_set, options in best_combos.items():
    features = included_features[feature_set]
    training_data = df_train[features]
    test_data = df_test[features]
    print(f"Feature Set: {feature_set}")
    for seed, states in options.items():
        print(f"Random Seed: {seed}")
        for state in states:
            print(f"Number of States: {state}")
            n_params = count_hmm_parameters(state, num_observations) # calculate for AIC/BIC later
            # chose GaussianHMM because my states are single modal and my data is continuous
            model = GaussianHMM(n_components= state,
                                covariance_type= 'full', # features are not independent
                                random_state= seed, # for reproducibility
                                n_iter= 200,
                                verbose=True) # give EM updates of log likelihood
            model.fit(training_data) # train HMM
            print(f'Iterations: {model.monitor_.iter}') # record the number of iterations it took to converge the model

            print("Predicting states for test data...")
            hidden_states = model.predict(test_data) # test the model
            results = df_test.copy()
            results['Predicted State'] = hidden_states

            log_likelihood = model.score(test_data) # record the log likelihood for the model
            print(f'Log Likelihood: {log_likelihood}')
            # calculate AIC and BIC
            print(f'AIC: {2 * n_params - 2 * log_likelihood}')
            print(f"BIC: {np.log(num_observations) * n_params - 2 * log_likelihood}")
            
            print('Saving Results')
            with pd.ExcelWriter(f"../../HMM_Mapping{state}.xlsx", engine='xlsxwriter') as writer:
                results.to_excel(writer, sheet_name=f"{state} States", index=False)
print('HMM Mapping Complete!')