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

source ~/.bashrc
set -eu
module load gcc/11.3.0 #usc samtools


date
# echo "task no.: $SLURM_ARRAY_TASK_ID"
# g=$(head -n $SLURM_ARRAY_TASK_ID /scratch1/tsungyul/n30488.hprc.full/1kg/genomes.txt | \
# 		tail -n 1)

g=$(head -n 1 /scratch1/tsungyul/n30488.hprc.full/1kg/genomes.txt | \
		tail -n 1)
echo "genome: $g"

rpgg=/scratch1/tsungyul/aydin/input/pan
fa=/scratch1/tsungyul/n30488.hprc.full/1kg/varcall1/fa/$g.fa
out=/scratch1/tsungyul/aydin/output/$g.aln.gz

/project/mchaisso_100/cmb-16/tsungyul/work/vntr/danbing-tk/bin/microdanbing -k 21 -qs $rpgg -f $fa | gzip >$out

date
