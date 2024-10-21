###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_motif_counts_pca.py
###############################################################################


import sys
import pandas as pd
from sklearn.decomposition import PCA


invar_df = sys.argv[1]
genomes_to_remove = sys.argv[2]
out = sys.argv[3]
pc_cols = [
    'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'
    ]

# load variant counts
data = pd.read_csv(invar_df, index_col=0)

# load test genomes labels that will not be included in the pca
with open(genomes_to_remove, 'r') as f:
    genomes_to_remove = [line.strip() for line in f.readlines()]

print(f"filtering out test genomes")
# filter out the genomes to exclude
data_filtered = data[~data.index.isin(genomes_to_remove)]

print(f"starting pca for {len(pc_cols)} components")
sys.stdout.flush()
pca = PCA(n_components=len(pc_cols))  
principal_components = pca.fit_transform(data)
print("PCA completed, converting to df")
sys.stdout.flush()


# create df for pca and send to csv
pca_df = pd.DataFrame(
    data = principal_components, columns = pc_cols, index = data.index
    )
pca_df.to_csv(out)
print("PCA df print to csv")
sys.stdout.flush()
