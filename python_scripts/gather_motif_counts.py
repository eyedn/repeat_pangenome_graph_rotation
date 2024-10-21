###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           gather_motif_counts.py
###############################################################################


from sys import argv
from func import convert_pickled_dicts_to_df as fx


if __name__ == "__main__":
    dir = argv[1]
    out = argv[2]

    combined_dict = fx.convert_pickled_dicts_to_df(dir)
    combined_dict.to_csv(out)
