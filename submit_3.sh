#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           submit_3.sh
###############################################################################


max_batches=40
sbatch --array=1-$max_batches%50 3_kmers_to_mots.sh $max_batches 
