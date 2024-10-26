#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           4_get_all_mots.sh
###############################################################################

r2=$1
max_batches=40 
num_loci=30488
num_jobs=100
sbatch --array=1-$num_jobs 4_gather_prune_motifs.sh $max_batches $r2 $num_loci $num_jobs
