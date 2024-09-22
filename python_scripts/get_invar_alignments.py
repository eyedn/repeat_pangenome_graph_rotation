###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_invar_alignments.py
###############################################################################


from sys import argv
from func import get_aln_edits as fx


if __name__ == "__main__":
    g = argv[1]
    aln = argv[2]
    out = argv[3]

    aln_edits = fx.get_aln_edits(g, aln)
    aln_edits.to_csv(out)
