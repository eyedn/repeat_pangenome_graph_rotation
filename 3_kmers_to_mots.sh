#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           3_kmers_to_mots.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --mem=16000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=k2m
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
echo "batch no.: $SLURM_ARRAY_TASK_ID"
echo "converting kmers to motifs"
total_batches=$1
get_1="/project/mchaisso_100/cmb-17/vntr_genotyping/rpgg2_k21_84k/hprc/full.v1/output8/cdbg/ki_tr.ccki_tr.pickle"
get_2="/project/mchaisso_100/cmb-17/vntr_genotyping/rpgg2_k21_84k/hprc/full.v1/output8/cdbg/ks.ccks.tr_cck_ns.ki_map.pickle"
kmers="/scratch1/tsungyul/n30488.hprc.full/1kg/genotype/*.tr.kmers"
out="/scratch1/tsungyul/aydin/k2m_output"
python3 ./python_scripts/convert_kmers_to_motifs.py $get_1 $get_2 $SLURM_ARRAY_TASK_ID $total_batches "$kmers" $out
echo "all done!"
date
