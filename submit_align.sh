#!/usr/bin/env bash

###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           submit_align.sh
###############################################################################


# at intervals, submit alignment job
si=1
ei=499
sbatch --array=$si-$ei align.sh
si=500
ei=999
while true; do
	sleep 120
	n=$(sq | wc -l)
	if [ $n -lt 500 ] ; then 
		echo $si $ei
		sbatch --array=$si-$ei align.sh
		if [ "$ei" == "3201" ] ; then 
			break
		fi
		si=$((ei+1))
		ei=$((ei+500<3202 ? ei+500 : 3201))
	fi
done
