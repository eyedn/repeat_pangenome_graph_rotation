#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           20241014.1kg.kmers2matrix.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=12:00:00
#SBATCH --mem=64000
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
echo -e "
localhost:${port}
"
jupyter lab --port=$port --no-browser --ip=$(hostname -s)
