###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           get_cigar_edits.py
###############################################################################


import typing


# given a cigar string of an alignment, generate edits info
def get_cigar_edits(cigar: str) -> typing.List[int]:

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
