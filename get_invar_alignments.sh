#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_invar_alignments.sh
###############################################################################

#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=16000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=invaraln
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

aln=/scratch1/tsungyul/aydin/output/$g.aln.gz
out=/scratch1/tsungyul/aydin/output/$g.csv


python3 ./python_scripts/get_invar_alignments.py $g $aln $out

echo "all done!"
date