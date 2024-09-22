###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_invar_count.py
###############################################################################


from sys import argv
from func import get_seq_count_dict as fx
from func import pickle_obj as gx


if __name__ == "__main__":
    fa = argv[1]
    out = argv[2]

    invars = fx.get_seq_count_dict(fa)
    gx.pickle_obj(invars, out)
