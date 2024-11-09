###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_sig_motifs.py
###############################################################################


import numpy as np
import pandas as pd
import pickle
import os
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests
import sys


if __name__ == "__main__":
    mask_g = sys.argv[1]
    meta = sys.argv[2]
    rare_pca = sys.argv[3]
    out = sys.argv[4]
    r2_threshold = float(sys.argv[5])

    # read in test genomes to mask in motif counts (read in later)
    mask_genomes = pd.read_csv(mask_g, header = None)
    mask_genome_ids = mask_genomes[0].dropna().tolist()

    # read in meta data
    meta_data_df = pd.read_csv(meta, sep='\t')

    # get indeces that genomes-to-be-masked will appear in motif counts
    mask_genome_indices = meta_data_df[meta_data_df["SampleID"].isin(mask_genome_ids)].index.tolist()

    # mask genomes that should not be considered
    meta_data_df = meta_data_df[~meta_data_df["SampleID"].isin(mask_genome_ids)]

    # read in pca data from rare motifs
    rare_pca_df = pd.read_csv(rare_pca, sep=',')

    # combines meta data and pca data
    merged_meta_df = meta_data_df.merge(rare_pca_df, how='left', right_on='Unnamed: 0', left_on='SampleID')

    # read in motif counts
    if os.path.exists(f"{out}/acgt.pickle"):
        print("acgt file found")
        sys.stdout.flush()
        with open(f"{out}/acgt.pickle", 'rb') as f:
            acgt =  pickle.load(f)
    else:
        print("acgt file NOT found. run job on CARC")
        sys.stdout.flush()
        exit

    # read in pruning results (False mean keep, True means pruned)
    if not os.path.exists(f"{out}/cck_pruned_combined_{r2_threshold}.pickle"):
        print("pruned file NOT found. run job on CARC")
        sys.stdout.flush()
        exit
    else:
        print(f"retrieving {out}/cck_pruned_combined_{r2_threshold}.pickle")
        sys.stdout.flush()
        with open(f"{out}/cck_pruned_combined_{r2_threshold}.pickle", 'rb') as f:
            pruned_0_8 = pickle.load(f)

    # prune motif counts features based on bool vector
    kept_motifs = acgt[~pruned_0_8]
    # convert pruned features to a df
    # transpose so each row is a sample and each column is a feature
    kept_motifs = np.array(kept_motifs).T
    kept_motifs_df = pd.DataFrame(kept_motifs, columns=[f'kept_motif_{i}' for i in range(kept_motifs.shape[1])])

    # mask genomes that should not be considered
    kept_motifs_df = kept_motifs_df[~kept_motifs_df.index.isin(mask_genome_indices)]

    # ensure the sample order matches between kept_motifs_df and df_metadata
    kept_motifs_df.index = merged_meta_df.index
    # combine metadata and kept features
    combined_data_df = pd.concat([merged_meta_df, kept_motifs_df], axis=1)

    # set up and run regression tests for each feature
    population_pvals = []
    superpopulation_pvals = []
    total_kept_motifs = len(kept_motifs_df.columns)
    for i, motif in enumerate(kept_motifs_df.columns):
        # population regression
        model_pop = ols(f"{motif} ~ C(Population) + Sex + PC1 + PC2 + PC3 + PC4 + PC5 + PC6 + PC7 + PC8 + PC9 + PC10", 
                        data=combined_data_df).fit()
        # collect all p-values related to 'Population' levels
        pop_pvalues = [pval for key, pval in model_pop.pvalues.items() if 'C(Population)' in key]
        population_pvals.append(min(pop_pvalues))  # use the minimum p-value for population levels

        # # superpopulation regression
        # model_superpop = ols(f"{motif} ~ C(Superpopulation) + Sex + PC1 + PC2 + PC3 + PC4 + PC5 + PC6 + PC7 + PC8 + PC9 + PC10", 
        #                      data=combined_data_df).fit()
        # # collect all p-values related to 'Superpopulation' levels
        # superpop_pvalues = [pval for key, pval in model_superpop.pvalues.items() if 'C(Superpopulation)' in key]
        # superpopulation_pvals.append(min(superpop_pvalues))  # use the minimum p-value for superpopulation levels

        if  (i % 10000) == 0:
            print(f"Processed {i + 1} motifs")
            sys.stdout.flush()

    population_pvals = np.array(population_pvals)
    population_corr_pvals = multipletests(population_pvals, method='fdr_bh')[1]
    with open(f"{out}/sig_motifs_masked_{r2_threshold}.pickle", 'wb') as f:
        pickle.dump(population_corr_pvals, f, protocol=pickle.HIGHEST_PROTOCOL)
