#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_invar_counts_pca.sh
###############################################################################

#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=16000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=invarpca
#SBATCH --output=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/slurm.%A_%a.%x.log 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=karatas@usc.edu


source ~/.bashrc
module load conda
conda init
conda activate rpgg_proj


date

input=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/invar_data.csv
genomes_to_remove=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/genomes.1kg_plus_related.gt_HPRC.txt
out=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/invar_pca.csv

python3 ./python_scripts/get_invar_counts_pca.py $input $genomes_to_remove $out

echo "all done!"
date
