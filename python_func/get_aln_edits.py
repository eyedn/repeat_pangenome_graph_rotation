###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_aln_edits.py
###############################################################################


import typing
import gzip
import pandas as pd
from . import get_cigar_edits as fx


# given microdangtk aln.gz, create df document edits of each bubble
def get_aln_edits(id: str, aln_gz: typing.BinaryIO) -> pd.DataFrame:

    # dict will hold bubble edit info for df creation at end
    bubble_dict: typing.Dict[int, typing.List[str, int, int, int, int, int]] \
        = {}
    with gzip.open(aln_gz, "rt") as f:
        for i, line in enumerate(f.readlines()):
            # get edit info of fwd and rev aln
            bubble_aln = line.strip().split("\t")
            f_edits = fx.get_cigar_edits(bubble_aln[5])
            r_edits = fx.get_cigar_edits(bubble_aln[7])

            # edit information of best aln between fwd and rev used
            if f_edits[0] > r_edits[0]:
                edits = r_edits
            else:
                edits = f_edits
            bubble_dict[f"{id}_{i}"] = edits
    edits_df = pd.DataFrame(bubble_dict)
    edits_df_T = edits_df.T
    edits_df_T.columns = ["edit dist", "#X", "#D", "#I", "#*", "#(X,*)"]
    return edits_df_T
