###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_seq_count_dict.py
###############################################################################


import sys
import typing
import os
from Bio.Seq import Seq


# given an fa file, generate a counts dict of each unique loc + seq
def get_seq_count_dict(fa: os.PathLike[str]) -> typing.Dict[str, int]:
    
    invar_dict: typing.Dict[str, int] = {}
    with open(fa, "r") as f:
            lines = f.readlines()

            # deal with lines 2 at a time
            # ex.   >28907.100
            #       AGTGCCAAGCATATGTCATTTCACTCTGTGTACATATGTAAGG  
            for i in range(0, len(lines), 2):
                loc = lines[i].strip().split(".")[0][1:]
                if i + 1 >= len(lines):
                    print(f"Error: Missing pair for line {i}.")
                    sys.exit(1)
                seq_f = Seq(lines[i + 1].strip())
                seq_r = seq_f.reverse_complement()

                # only use the fwd or reverse string depending on alpha. order
                if seq_f > seq_r:
                    key = f"{loc}_{seq_r}"
                else:
                    key = f"{loc}_{seq_f}"

                # add seq
                if key in invar_dict:
                    invar_dict[key] += 1
                else:
                    invar_dict[key] = 1
    return invar_dict
