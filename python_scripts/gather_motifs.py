###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           gather_motifs.py
###############################################################################


import sys
import pickle
import numpy as np
from .convert_kmers_to_motifs import get_2


def gather(gt_HPRC, HPRC_chr1_cov, NCCK, NB, out_dir):
    # correct coverage, sex chrom dosage unadjusted
    genomes = np.loadtxt(gt_HPRC, dtype=object)
    ng = genomes.size
    cov = np.array([float(c) for g, c in np.loadtxt(HPRC_chr1_cov, dtype=object) if g in genomes])

    print("Loading cgt", end="")
    sys.stdout.flush()
    BS = ng//NB
    cgt = np.zeros([NCCK,ng], dtype=np.float32)
    for i in range(NB):
        BS_ = BS if i != NB-1 else ng - BS*i
        with open(f"{out_dir}/cgt.{i}.pickle", 'rb') as f:
            si = i*BS
            ei = i*BS + BS_
            cgt[:,si:ei] = pickle.load(f)
    print("Computing acgt")
    sys.stdout.flush()
    acgt = np.zeros_like(cgt, dtype=np.float32)
    acgt = cgt / cov
    print("Dumping acgt")
    sys.stdout.flush()
    with open("{out_dir}/acgt.pickle", 'wb') as f:
        pickle.dump(acgt, f, protocol=pickle.HIGHEST_PROTOCOL)
    return acgt


if __name__ == "__main__":
    get_file = sys.argv[1]
    gt_HPRC = sys.argv[2]
    HPRC_chr1_cov = sys.argv[3]
    total_batches = int(sys.argv[4])
    out = sys.argv[5]

    # get necessary kmer and motif data
    ks, ccks, tr_cck_ns, ki_map = get_2(get_file)

    NCCK = len(ccks)
    NB = total_batches

    ilcgt = gather(gt_HPRC, HPRC_chr1_cov, NCCK, NB, out)
