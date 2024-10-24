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


max_batches=40 
r2=0.8
sbatch 4_gather_prune_motifs.sh $max_batches $r2
