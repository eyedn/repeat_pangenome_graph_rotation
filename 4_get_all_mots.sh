#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           kmers_to_mots_ipynb.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --mem=16000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=getmot
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
#TODO: python script goes here
echo "all done!"
date
