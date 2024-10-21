#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           2_1_cat_aln_csv.sh
###############################################################################


csv_dir="/scratch1/tsungyul/aydin/output"
file_1="$csv_dir/HG00096.csv"
out="/project/mchaisso_100/cmb-17/vntr_genotyping/aydin/data/cigar_data.csv"

head -n 1 $file_1 > $out && tail -n +2 -q $csv_dir/*.csv >> $out
