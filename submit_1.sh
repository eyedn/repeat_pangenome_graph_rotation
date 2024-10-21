#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           2_get_motif_data.sh
###############################################################################


sbatch --array=1-3201 1_align_genome_motifs.sh  