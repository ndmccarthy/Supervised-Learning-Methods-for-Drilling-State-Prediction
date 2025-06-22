from hmmlearn.hmm import GaussianHMM
from hmm_functions import *
import numpy as np

# retesting with only WOB

# prepare data
df_train, df_test = prepare_data() # grab all data
training_data = df_train[['WOB']].values # gives 2D array rather than series
testing_data = df_test[['WOB']].values

# set up for results
num_observations = len(df_test) # record for AIC/BIC later
results = pd.DataFrame()

# begin training and testing
print("Training and Testing Options")
for n_states in range(2, 11): # limiting number of states to 10 because difficult to interpret when higher

    # set up results
    model_result = dict.fromkeys(['Number of States', 'Converged', 'Iterations to Convergence', 'Log Likelihood', 'AIC', 'BIC'])
    model_result['Number of States'] = n_states
    n_params = count_hmm_parameters(n_states, num_observations) # calculate for AIC/BIC later

    # chose GaussianHMM because my states are single modal and my data is continuous
    model = GaussianHMM(n_components= n_states, # testing for 5 states
                        covariance_type= 'diag', # only one feature, so no worries about independence
                        random_state= 2021, # for reproducibility (Whoop!)
                        n_iter= 200,
                        verbose=True) # give EM updates of log likelihood
    try:
        model.fit(training_data) # train HMM

        if model.monitor_.converged:
            # predict states
            hidden_states = model.predict(testing_data) # test the model
            
            # record evaluation results
            model_result['Converged'] = 'True' # record if converged
            model_result['Iterations to Convergence'] = model.monitor_.iter # record the number of iterations it took to converge the model
            log_likelihood = model.score(testing_data) # record the log likelihood for the model
            model_result['Log Likelihood'] = log_likelihood 
            # calculate AIC and BIC
            model_result['AIC'] = 2 * n_params - 2 * log_likelihood
            model_result['BIC'] = np.log(num_observations) * n_params - 2 * log_likelihood

            # save predicted states with original data
            mapped = df_test.copy()
            mapped['Predicted State'] = hidden_states
            print(f'Saving mapped predictions for {n_states}-State Model')
            with pd.ExcelWriter(f"../../HMM_WOB/Mapped_Predictions/HMM_Mapping{n_states}.xlsx", engine='xlsxwriter') as writer:
                mapped.to_excel(writer, sheet_name=f"{n_states} States", index=False)

        else:
            model_result['Converged'] = 'False'

    except:
        continue

    # update results
    print(model_result)
    model_df = pd.DataFrame([model_result])
    results = pd.concat([results, model_df], ignore_index=True)

print(results)
print('Saving Results')
with pd.ExcelWriter(f"../../HMM_WOB/HMM_WOB_Evaluations.xlsx", engine='xlsxwriter') as writer:
    results.to_excel(writer, sheet_name=f"Evaluations", index=False)
print('HMM Training and Testing Complete!')