# This script performs UMAP on rig data to reduce dimensionality.
# pip install umap-learn

import umap
import matplotlib.pyplot as plt
from hmm_functions import prepare_data
import pandas as pd

# read in and standardize data
df_train, df_test = prepare_data()

# reduce data
print("Reducing Data")
reducer = umap.UMAP()
red_train = reducer.fit_transform(df_train)
red_train_df = pd.DataFrame(red_train)

# plot reduced data
print("Plotting Reduced Data")
plt.figure()
plt.scatter(red_train[:, 0], red_train[:, 1])
plt.show()

# save data so don't need to process again
print('Saving Results')
with pd.ExcelWriter("../../UMAP_Training_Data.xlsx", engine='xlsxwriter') as writer:
    red_train_df.to_excel(writer, sheet_name="Reduced Training Data", index=False)
print('UMAP Processing Complete!')