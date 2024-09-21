###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_bubble_alignments.py
###############################################################################
from sys import argv
import typing
import gzip
import pandas as pd


# given microdangtk aln.gz, create df document edits of each bubble
def get_aln_edits(id: str, aln_gz: typing.BinaryIO) -> pd.DataFrame:

    # dict will hold bubble edit info for df creation at end
    bubble_dict: typing.Dict[int, typing.List[str, int, int, int, int, int]] \
        = {}
    with gzip.open(aln_gz, "rt") as f:
        for i, line in enumerate(f.readlines()):
            # get edit info of fwd and rev aln
            bubble_aln = line.strip().split("\t")
            f_edits = get_bubble_edits(bubble_aln[5])
            r_edits = get_bubble_edits(bubble_aln[7])

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

# given a cigar string of a bubble's alignment, generate edits info
def get_bubble_edits(cigar: str) -> typing.List[int]:

    # stores edit counts: #all, #X, #D, #I, #*, #(X,*)
    edit_counter: typing.List[int] = [0, 0, 0, 0, 0, 0] 
    # stores int value for possible missalignment
    missaln_counter: typing.List[str] = []

    length = len(cigar)
    idx = 0
    while idx < length:
        if cigar[idx] == "X": # mismatch
            edit_counter[0] += 1
            edit_counter[1] += 1
            missaln_counter = []
            idx += 1   # skip extra char
        elif cigar[idx] == "D": # deletion
            edit_counter[0] += 1
            edit_counter[2] += 1
            missaln_counter = []
            idx +=1   # skip extra char
        elif cigar[idx] == "I": # insertion
            edit_counter[0] += 1
            edit_counter[3] += 1
            missaln_counter = []
        elif cigar[idx] == "*": # missaligned ending
            # add final numbers in cigar stored in `missaln_counter`
            edit_counter[0] += int("".join(missaln_counter))
            edit_counter[4] += int("".join(missaln_counter))
        elif cigar[idx] == "=": # clear missalign counter for matches
            missaln_counter = []
        else:
            missaln_counter.append(cigar[idx])
        idx += 1
    # combine mismatches and missalignment into one category
    edit_counter[5] = edit_counter[1] + edit_counter[4]
    return edit_counter


if __name__ == "__main__":
    g = argv[1]
    aln = argv[2]
    out = argv[3]

    aln_edits = get_aln_edits(g, aln)
    aln_edits.to_csv(out)
