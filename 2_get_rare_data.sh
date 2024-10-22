#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           2_get_rare_data.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=12:00:00
#SBATCH --mem=16000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=rardat
#SBATCH --output=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/slurm.%A_%a.%x.log 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=karatas@usc.edu


source ~/.bashrc
module load conda
conda init
conda activate rpgg_proj


# 1. get edit distance/cigar data from alignment
date
echo "getting cigar data"
cigar_csv_dir="/scratch1/tsungyul/aydin/output"
file_1="$cigar_csv_dir/HG00096.csv"
cigar_out="/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/cigar_data.csv"
head -n 1 $file_1 > $cigar_out && tail -n +2 -q $cigar_csv_dir/*.csv \
    >> $cigar_out
echo "all done!"

# 2. get data for rare variant counts
date
echo "gather rare variant counts"
counts_input=/scratch1/tsungyul/aydin/output
counts_out=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/rare_data.csv
python3 ./python_scripts/gather_motif_counts.py $counts_input $counts_out
echo "all done!"

# 3. get matrix for performing rare variant pca
date
echo "all done!"
genomes_to_remove=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/genomes.1kg_plus_related.gt_HPRC.txt
pca_out=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/rare_pca.csv
python3 ./python_scripts/get_motif_counts_pca.py $counts_out $genomes_to_remove $pca_out
echo "all done!"
date
