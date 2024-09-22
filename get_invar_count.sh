#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_invar_count.sh
###############################################################################

#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=4000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=rpggaln
#SBATCH --output=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/slurm.%A_%a.%x.log 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=karatas@usc.edu


source ~/.bashrc
module load conda
conda init
conda activate rpgg_proj


date
echo "task no.: $SLURM_ARRAY_TASK_ID"

# get genome for this task
g=$(head -n $SLURM_ARRAY_TASK_ID /scratch1/tsungyul/n30488.hprc.full/1kg/genomes.txt | \
		tail -n 1)
echo "genome: $g"

rpgg=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/input/pan
fa=/scratch1/tsungyul/n30488.hprc.full/1kg/varcall1/fa/$g.fa
out=/scratch1/tsungyul/aydin/output/$g.pickle

python3 ./get_invar_count.py $fa $out

echo "all done!"
date
