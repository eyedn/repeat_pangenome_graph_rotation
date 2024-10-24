###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           gather_prune_motifs.py
###############################################################################


import os
import sys
import pickle
import numpy as np
from sklearn.metrics import r2_score


def get_1(file_path):
    with open(file_path, 'rb') as f:
        ki_tr, ccki_tr = pickle.load(f)
    return ki_tr, ccki_tr

def get_2(file_path):
    with open(file_path, 'rb') as f:
        ks, ccks, tr_cck_ns, ki_map = pickle.load(f)
    tr_cck_ns = np.array(tr_cck_ns)
    return ks, ccks, tr_cck_ns, ki_map

def gather_motifs(gt_HPRC, NCCK, NB, out_dir):
    genomes = np.loadtxt(gt_HPRC, dtype=object)
    ng = genomes.size
    BS = ng//NB
    
    print(f"Loading batches...")
    print(BS, ng, NB)
    sys.stdout.flush()
    cgt = np.zeros([NCCK,ng], dtype=np.float32)
    for i in range(NB):
        print(f"Loading batch {i+1}")
        sys.stdout.flush()
        BS_ = BS if i != NB-1 else ng - BS*i
        si = i*BS
        ei = i*BS + BS_
        with open(f"{out_dir}/cgt.{i}.pickle", 'rb') as f:
            cgt[:,si:ei] = pickle.load(f)
    print("Dumping cgt...")
    sys.stdout.flush()
    with open(f"{out_dir}/cgt.pickle", 'wb') as f:
        pickle.dump(cgt, f, protocol=pickle.HIGHEST_PROTOCOL)
    return cgt

def adjust_coverage(cgt, gt_HPRC, HPRC_chr1_cov, out_dir):
    print("Loading coverage...")
    sys.stdout.flush()
    genomes = np.loadtxt(gt_HPRC, dtype=object)
    cov = np.array([float(c) for g, c in np.loadtxt(HPRC_chr1_cov, dtype=object) if g in genomes])
    print("Computing acgt...")
    sys.stdout.flush()
    cgt /= cov
    print("Dumping acgt...")
    sys.stdout.flush()
    with open(f"{out_dir}/acgt.pickle", 'wb') as f:
        pickle.dump(cgt, f, protocol=pickle.HIGHEST_PROTOCOL)
    return cgt

def compute_ld_r2(acgt, ccki_tr, ccks, r2_threshold, out_dir):
    # keep track of which variants have been pruned
    NL = len(ccki_tr)
    NM = len(ccks)
    pruned = np.zeros(NM, dtype=bool)

    print("Pruning...")
    print(NL, NM)
    sys.stdout.flush()
    for i in range(NL):
        locus_s = ccki_tr[i-1] if i != 0 else 0
        locus_e = ccki_tr[i]
        while locus_s != locus_e:
            if not pruned[locus_s]:
                locus_m = locus_s + 1
                while locus_m <= locus_e:
                    if not pruned[locus_m]:
                        r2 = r2_score(acgt[locus_s], acgt[locus_m])
                        if r2 > r2_threshold:
                            pruned[locus_m] = True
                    locus_m += 1
            locus_s += 1
        if (i + 1 ) % 500 == 0:
            print(f"{i} loci pruned")
    print(f"Dumping pruned...")
    sys.stdout.flush()
    with open(f"{out_dir}/cck_pruned_{r2_threshold}.pickle", 'wb') as f:
        pickle.dump(pruned, f, protocol=pickle.HIGHEST_PROTOCOL)
    return pruned


if __name__ == "__main__":
    get_1_file = sys.argv[1]
    get_2_file = sys.argv[2]
    gt_HPRC = sys.argv[3]
    HPRC_chr1_cov = sys.argv[4]
    total_batches = int(sys.argv[5])
    r2_threshold = float(sys.argv[6])
    out = sys.argv[7]

    ki_tr, ccki_tr = get_1(get_1_file)
    ks, ccks, tr_cck_ns, ki_map = get_2(get_2_file)
    NK = len(ks)
    NCCK = len(ccks)
    NB = 40

    acgt = None
    if os.path.exists(f"{out}/acgt.pickle"):
        print("acgt file found")
        with open(f"{out}/acgt.pickle", 'rb') as f:
            acgt =  pickle.load(f)
    else:
        cgt = None
        if os.path.exists(f"{out}/cgt.pickle"):
            print("cgt file found")
            with open(f"{out}/acgt.pickle", 'rb') as f:
                cgt = gather_motifs(gt_HPRC, NCCK, NB, out)
        else:
            print("creating cgt file")
            cgt = gather_motifs(gt_HPRC, NCCK, NB, out)
        print("creating acgt file")
        acgt =  adjust_coverage(cgt, gt_HPRC, HPRC_chr1_cov, out)
    
    cck_pruned = compute_ld_r2(acgt, ccki_tr, ccks, r2_threshold, out)
