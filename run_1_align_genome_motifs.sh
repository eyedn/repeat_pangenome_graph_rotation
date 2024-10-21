#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           1_align_genome_motifs.sh
###############################################################################


#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=8000
#SBATCH --partition=chaissonlab
#SBATCH --account=mchaisso_100
#SBATCH -N 1
#SBATCH --job-name=alnmots
#SBATCH --output=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/log/slurm.%A_%a.%x.log 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=karatas@usc.edu


source ~/.bashrc
set -eu
module load gcc/11.3.0 #usc samtools
module load conda
conda init
conda activate rpgg_proj


# 1. get genome for this task
date
echo "task no.: $SLURM_ARRAY_TASK_ID"
g=$(head -n $SLURM_ARRAY_TASK_ID /scratch1/tsungyul/n30488.hprc.full/1kg/genomes.txt | \
		tail -n 1)
echo "genome: $g"
echo "aligning to rppg"
rpgg=/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/input/pan
fa=/scratch1/tsungyul/n30488.hprc.full/1kg/varcall1/fa/$g.fa
danbing_aln=/scratch1/tsungyul/aydin/output/$g.aln.gz
/project/mchaisso_100/cmb-16/tsungyul/work/vntr/danbing-tk/bin/microdanbing \
	-k 21 \
	-qs $rpgg \
	-f $fa \
	| gzip >$danbing_aln
echo "all done!"

# 2. get edit distance info of alignments 
date
echo "getting alignment distances"
aln_data=/scratch1/tsungyul/aydin/output/$g.csv
python3 ./python_scripts/get_motif_alignments.py $g $danbing_aln $aln_data
echo "all done!"

# 3. create python dictionaries for motif existance
date
echo "algning to rppg"
motif_out=/scratch1/tsungyul/aydin/output/$g.pickle
python3 ./python_scripts/get_motif_count.py $fa $motif_out
echo "all done!"
date
