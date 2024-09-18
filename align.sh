#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           align.sh
###############################################################################

source ~/.bashrc
set -eu
module load gcc/11.3.0


date
echo "task no.: $SLURM_ARRAY_TASK_ID"
genome=$(head -n $SLURM_ARRAY_TASK_ID /scratch1/tsungyul/n30488.hprc.full/1kg/genomes.txt | \
		tail -n 1)
echo "genome: $genome"

rpgg=/scratch1/tsungyul/aydin/input/pan
fa=/scratch1/tsungyul/n30488.hprc.full/1kg/varcall1/fa/$genome.fa
out=/scratch1/tsungyul/aydin/output/$genome.aln.gz

/project/mchaisso_100/cmb-16/tsungyul/work/vntr/danbing-tk/bin/microdanbing -k 21 -qs $rpgg -f $fa | gzip >$out

date