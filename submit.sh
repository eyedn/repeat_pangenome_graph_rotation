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


genomes=$(wc -l < /scratch1/tsungyul/n30488.hprc.full/1kg/genomes.txt) 

sbatch \
	--ntasks=1 \
	--time=48:00:00 \
	--mem=16000 \
	--partition=qcb \
	--account=mchaisso_100 \
	-N 1 \
	--job-name=rpggaln \
	--output=slurm.%A_%a.%x.log \
	--constraint=xeon-2665,avx \
	--exclude=b10-10 \
	--mail-type=ALL \
	--mail-user=karatas@usc.edu \
	--array=0-1 \
	./align.sh 
