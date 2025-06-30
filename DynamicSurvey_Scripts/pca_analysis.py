# attempting to map HMM states to real drilling states

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

for num_states in [7, 10]:
    print(f"Number of States: {num_states}")
    # Load your dataset
    df = pd.read_excel(f"../../HMM_WOB/Mapped_Predictions/HMM_Mapping{num_states}.xlsx")

    # Select only numeric features (including unused but interesting ones)
    feature_cols = ['GPM', 'Motor_RPM', 'WOB', 'Pulser_Axial_Vibration', 'Pulser_Lateral_Vibration']
    X = df[feature_cols]

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Keep 2 or 3 components for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Create a DataFrame with principal components and predicted state
    pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
    pca_df['Predicted_State'] = df['Predicted State']

    # sample 5% of data to plot so not too overcrowded
    sample_df = pca_df.sample(frac=0.05, random_state=2021)

    '''
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=sample_df, x='PC1', y='PC2', hue='Predicted_State', palette='tab10')
    plt.title(f"PCA of Features Colored by Predicted HMM State\n({num_states}-State WOB Model)")
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    plt.legend(title="HMM State")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    '''
    # identify which features affect components the most
    loadings = pd.DataFrame(pca.components_.T,
                            index=feature_cols,
                            columns=['PC1', 'PC2'])
    print("PCA Loadings:\n", loadings)

    abs_loadings = loadings.abs() # grabbing absolute values since strength can be measured in positive or negative directions

    # Sort by PC1 to make the chart easier to read (optional)
    abs_loadings = abs_loadings.sort_values(by='PC1', ascending=False)

    # Setup
    features = abs_loadings.index
    y = np.arange(len(features))
    height = 0.35

    fig, ax = plt.subplots(figsize=(10, len(features) * 0.5))
    ax.barh(y - height/2, abs_loadings['PC1'], height, label='PC1', color='teal')
    ax.barh(y + height/2, abs_loadings['PC2'], height, label='PC2', color='salmon')

    # Labeling
    ax.set_yticks(y)
    ax.set_yticklabels(features)
    ax.set_xlabel("Absolute Loading Magnitude")
    ax.set_title(f'Absolute Loadings of {num_states}-State WOB Model')
    ax.legend()
    ax.grid(True, axis='x')
    plt.tight_layout()
    plt.show()

    '''
    # graph pca_loadings
    for pc in abs_loadings.columns:
        plt.figure(figsize=(8, 4))
        abs_loadings[pc].sort_values(ascending=False).plot(kind='barh', color='teal')
        plt.title(f'Absolute Loadings for {pc} of {num_states}-State WOB Model')
        plt.xlabel('Absolute Loading Magnitude')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    
    # sample 5% of data to plot so not too overcrowded
    df_samples = df.sample(frac=0.05, random_state=2021)

    # look at pairs of features to identify strongest correlations
    sns.pairplot(df_samples, vars=feature_cols, hue='Predicted State', palette='tab10', plot_kws={'alpha': 0.5, 's': 10})
    plt.suptitle("Feature Scatterplots Colored by HMM State", y=1.02)
    plt.show()
    '''