###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           pickle_obj.py
###############################################################################


import pickle
import os


def pickle_obj(a: any, out: os.PathLike[str]) -> None:

    with open(out, 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(out, 'rb') as handle:
        b = pickle.load(handle)

    print(f"pickle successful? {a == b}")
    