from hmmlearn.hmm import GaussianHMM
from hmm_functions import *
import numpy as np

seeds = [792022, 2, 4, 11191998, 2021, 112, 26, 61225, 1130, 61]
included_features = {'Motor Reliance': ['GPM', 'Motor_RPM', 'Motor_Axial_Vibration', 'Motor_Lateral_Vibration', 'WOB'], 
                     'Pulser Reliance': ['GPM', 'Motor_RPM', 'Pulser_Axial_Vibration', 'Pulser_Lateral_Vibration', 'WOB'],
                     'All Vibration': ['Motor_Axial_Vibration', 'Motor_Lateral_Vibration', 'Pulser_Axial_Vibration', 'Pulser_Lateral_Vibration'],
                     'Just Motor': ['Motor_Axial_Vibration', 'Motor_Lateral_Vibration'],
                     'Just Pulser': ['Pulser_Axial_Vibration', 'Pulser_Lateral_Vibration']}



df_train, df_test = prepare_data() # grab all data
num_observations = len(df_test) # record for AIC/BIC later
print("Training and Testing Options")
# set up storage for results
results = pd.DataFrame()
for set_name, feature_list in included_features.items():
    model_result = dict.fromkeys(['Feature Set', 'Number of States', 'Random Seed', 'Converged', 'Iterations to Convergence', 'Log Likelihood', 'AIC', 'BIC'])
    # only use indicated columns per run
    model_result['Feature Set'] = set_name
    training_data = df_train[feature_list]
    testing_data = df_test[feature_list]
    for n_states in range(2, 16):
        model_result['Number of States'] = n_states
        n_params = count_hmm_parameters(n_states, num_observations) # calculate for AIC/BIC later
        for seed in seeds:
            model_result['Random Seed'] = seed
            # chose GaussianHMM because my states are single modal and my data is continuous
            model = GaussianHMM(n_components= n_states, # testing for 5 states
                                covariance_type= 'full', # features are not independent
                                random_state= seed, # for reproducibility
                                n_iter= 200,
                                verbose=True) # give EM updates of log likelihood
            try:
                model.fit(training_data) # train HMM
                if model.monitor_.converged:
                    model_result['Converged'] = 'True' # record if converged
                    model_result['Iterations to Convergence'] = model.monitor_.iter # record the number of iterations it took to converge the model
                    hidden_states = model.predict(testing_data) # test the model
                    log_likelihood = model.score(testing_data) # record the log likelihood for the model
                    model_result['Log Likelihood'] = log_likelihood 
                    # calculate AIC and BIC
                    model_result['AIC'] = 2 * n_params - 2 * log_likelihood
                    model_result['BIC'] = np.log(num_observations) * n_params - 2 * log_likelihood
                else:
                    model_result['Converged'] = 'False'
            except:
                continue
            print(model_result)
            model_df = pd.DataFrame([model_result])
            results = pd.concat([results, model_df], ignore_index=True)
print(results)
print('Saving Results')
with pd.ExcelWriter(f"../../HMM_Evaluations.xlsx", engine='xlsxwriter') as writer:
    results.to_excel(writer, sheet_name=f"Evaluations", index=False)
print('HMM Training and Testing Complete!')