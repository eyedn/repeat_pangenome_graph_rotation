###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_invar_counts_pca.py
###############################################################################


import sys
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


invar_df = sys.argv[1]
out = sys.argv[2]
pc_cols = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5']

data = pd.read_csv(invar_df, index_col = 0) 

# standardize the data and apply pca
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)
print(f"starting pca for {len(pc_cols)} components")
sys.stdout.flush()
pca = PCA(n_components = len(pc_cols))  
principal_components = pca.fit_transform(data_scaled)
print("PCA completed, converting to df")
sys.stdout.flush()

# create df for pca and send to csv
pca_df = pd.DataFrame(
    data = principal_components, columns = pc_cols, index = data.index
    )
pca_df.to_csv(out)
print("PCA df print to csv")
sys.stdout.flush()
