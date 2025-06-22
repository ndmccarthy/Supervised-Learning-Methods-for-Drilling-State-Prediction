# this script helps infer which HMM implementations were the most useful by visualizing the results

import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# read in results
print("Reading in Data")
hmm_df = pd.read_excel("../../HMM_Evaluations.xlsx")
hmm_df.drop(columns=['Converged', 'Iterations to Convergence'], inplace= True)

# look at multiple linear regression model to identify most significant variables (feature set, states, or seed)
X_feats = ['Feature Set', 'Random Seed', 'Number of States']
y_feats = ['Log Likelihood', 'AIC', 'BIC']
'''
# make box plots for categorical independent variable (Feature Set)
for independent_var in X_feats:
    for dependent_var in y_feats:
        plt.figure(figsize=(6, 7))
        sns.boxplot(data=hmm_df, x=independent_var, y=dependent_var)
        plt.ylabel(dependent_var)
        plt.xticks(rotation=15)
        plt.title(f'Boxplots of {dependent_var} for {independent_var}')
        plt.show()

# closer look at certatin feature sets (for scale)
subset = ['All Vibration', 'Just Motor', 'Just Pulser']
filtered_df = hmm_df[hmm_df['Feature Set'].isin(subset)]
plt.figure(figsize=(6, 7))
sns.boxplot(data=filtered_df, x='Feature Set', y='Log Likelihood')
plt.ylabel(dependent_var)
plt.xticks(rotation=15)
plt.title(f'Boxplots of Loglikelihoods for Selected Feature Sets')
plt.show()

# make scatter/line plots for numeric independent variables
for independent_var in X_feats:
    X = hmm_df[[independent_var]].values
    for dependent_var in y_feats:
        y = hmm_df[dependent_var].values
        model = LinearRegression().fit(X, y)
        y_predict = model.predict(X)
        plt.figure()
        plt.scatter(X, y, label=f'{dependent_var} Data')
        plt.plot(X, y_predict, label=f'{dependent_var} Regression')
        plt.xlabel(independent_var)
        plt.title(f'Linear Regression of {dependent_var} for {independent_var}')  
        plt.legend()
        plt.show()
'''

# Just Pulser feature set had best log likelihood; let's take a closer look

#pd_df = hmm_df[hmm_df['Feature Set'] == 'Just Pulser']
#for independent_var in X_feats[1:]:
#    for dependent_var in y_feats:
#        plt.figure(figsize=(6, 7))
#        sns.boxplot(data=hmm_df, x=independent_var, y=dependent_var)
#        plt.ylabel(dependent_var)
#        plt.xticks(rotation=15)
#        plt.title(f'Boxplots of {dependent_var} for {independent_var}\nof Models Using Only Pulser Vibration')
#        plt.show()
'''
plt.figure()
plt.scatter(x=pd_df['AIC'], y=pd_df['Log Likelihood'], c=pd_df['Random Seed'], s=pd_df['Number of States'])
plt.xlabel('Number of States')
plt.ylabel('Log Likelihood')
plt.title(f'Log Likelihoods Based on Number of States \nfor Models with Only Pulser Vibration Data')
plt.show()
'''
for state_num in range(2, 16):
    new_df = hmm_df[hmm_df['Number of States'] == state_num]
    new_df = new_df[new_df['Log Likelihood'] >= -1250000]
    new_df['Random Seed'] = new_df['Random Seed'].astype(str)
    plt.figure()
    sns.scatterplot(data = new_df, x='Random Seed', y='Log Likelihood', hue='Feature Set', palette='tab10')
    plt.xticks(rotation=30)
    plt.xlabel('Random Seed')
    plt.ylabel('Log Likelihood')
    plt.title(f'Log Likelihoods for Models with {state_num} States')
    plt.legend(title = 'Feature Set')
    plt.show()