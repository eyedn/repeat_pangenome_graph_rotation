#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           4_gather_prune_motifs.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mem=36000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=gpmot
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
echo "gather motif counts"
total_batches=$1
r2_threshold=$2
get_1="/project/mchaisso_100/cmb-17/vntr_genotyping/rpgg2_k21_84k/hprc/full.v1/output8/cdbg/ki_tr.ccki_tr.pickle"
get_2="/project/mchaisso_100/cmb-17/vntr_genotyping/rpgg2_k21_84k/hprc/full.v1/output8/cdbg/ks.ccks.tr_cck_ns.ki_map.pickle"
gt_HPRC="/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/LD_prune/input/genomes.txt"
HPRC_chr1_cov="/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/LD_prune/input/1kg_all.cov.tsv"
out="/scratch1/tsungyul/aydin/k2m_output"
python3 ./python_scripts/gather_prune_motifs.py $get_1 $get_2 $gt_HPRC $HPRC_chr1_cov $total_batches $r2_threshold $out
echo "all done!"
date
