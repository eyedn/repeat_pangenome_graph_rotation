#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           3_kmers_to_mots_ipynb.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=32000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=k2m
#SBATCH --error=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/ipynb_stderr.%A_%a.%x.log 
#SBATCH --output=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/ipynb_stdout.%A_%a.%x.log 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=karatas@usc.edu


source ~/.bashrc
module load conda
conda init
conda activate rpgg_proj
cd /project/mchaisso_100/cmb-17/vntr_genotyping/aydin


XDG_RUNTIM_DIR=""
node=$(hostname -s)
port=9888
echo -e "
ssh -N -L ${port}:${node}:${port} karatas@endeavour.usc.edu
"
jupyter lab --port=$port --no-browser --ip=$(hostname -s)
