#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           submit.sh
###############################################################################

#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=16000
#SBATCH --partition=qcb
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=rpggaln
#SBATCH --output=slurm.%A_%a.%x.log 
###SBATCH --constraint=xeon-2665,avx
###SBATCH --exclude=b10-10
###SBATCH --mail-type=ALL
###SBATCH --mail-user=karatas@usc.edu
###SBATCH --array=0-1

./align.sh --input=input_${SLURM_ARRAY_TASK_ID}
