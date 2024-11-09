#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           5_get_sig_motifs.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mem=64000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=sigmot
#SBATCH --output=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/slurm.%A_%a.%x.log 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=karatas@usc.edu

source ~/.bashrc
module load conda
source activate rpgg_proj

# make sure numpy is found
which python
python -c "import sys; print(sys.path)"
python -c "import numpy; print(numpy.__version__)"


date
echo "findign sig motifs"
mask_g="/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/genomes.1kg_plus_related.gt_HPRC.txt"
meta="/project/mchaisso_100/cmb-17/vntr_genotyping/1kgr/20130606_g1k_3202_samples_ped_population.simple.tsv"
rare_pca="/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/rare_pca.csv"
out="/scratch1/tsungyul/aydin/k2m_output"
r2_threshold=$1

# get all significance testing for motifs
python3 ./python_scripts/gather_prune_motifs.py "$mask_g" "$meta" "$rare_pca" "$out" "$r2_threshold"
echo "all done!"
date
