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
import time 
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

def compute_partial_ld_r2(acgt, ccki_tr, ccks, r2_threshold, out_dir, start_idx, end_idx):
    # keep track of which variants have been pruned
    init_locus_start = ccki_tr[start_idx] if start_idx != 0 else 0
    pruned_size = ccki_tr[end_idx] - init_locus_start
    pruned = np.zeros(pruned_size, dtype=bool)
    print(f"Pruning loci from {start_idx} to {end_idx}...")
    print(f"r^2 threshold = {r2_threshold}")
    print(f"partial motif count: {pruned_size} / {len(ccks)}")
    sys.stdout.flush()
    start_time = time.time()

    # loop through all loci
    for i in range(start_idx, end_idx + 1):
        curr_m = ccki_tr[i-1] if i != 0 else 0
        locus_e = ccki_tr[i] - 1
        # loop through all motifs in each loci
        while curr_m < locus_e:
            # skipped pruned motifs
            if not pruned[curr_m - init_locus_start]:
                iter_m = curr_m + 1
                # comparte current motif with all other motifs in loci
                while iter_m <= locus_e:
                    # skipped pruned motifs
                    if not pruned[iter_m - init_locus_start]:
                        r2 = r2_score(acgt[curr_m], acgt[iter_m])
                        if r2 > r2_threshold:   # prune if necessary
                            pruned[iter_m - init_locus_start] = True
                    iter_m += 1
            curr_m += 1
        if (i + 1 - start_idx) % 100 == 0:
            compute_time = time.time() - start_time
            print(f"Pruned {i + 1 - start_idx} loci in {compute_time:.2f} seconds")
            sys.stdout.flush()
        
    # pickle vector of pruned status
    print(f"Dumping pruned...")
    sys.stdout.flush()
    with open(f"{out_dir}/cck_pruned_{r2_threshold}_{start_idx}_{end_idx}.pickle", 'wb') as f:
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
    start_idx = int(sys.argv[8])
    end_idx = int(sys.argv[9]) 

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
            with open(f"{out}/cgt.pickle", 'rb') as f:
                cgt = gather_motifs(gt_HPRC, NCCK, NB, out)
        else:
            print("creating cgt file")
            cgt = gather_motifs(gt_HPRC, NCCK, NB, out)
        print("creating acgt file")
        acgt =  adjust_coverage(cgt, gt_HPRC, HPRC_chr1_cov, out)
    
    cck_pruned = compute_partial_ld_r2(acgt, ccki_tr, ccks, r2_threshold, out, start_idx, end_idx)
