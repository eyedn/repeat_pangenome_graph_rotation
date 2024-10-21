###############################################################################
#           Aydin Karatas
#           Repeat Pangenome Graph Project
#           ---
#           University of Southern California
#           Department of Quantitative and Computational Biology 
#           Chaisson Lab Rotation
#           ---
#           convert_kmers_to_motifs.py
###############################################################################


from sys import argv
import glob
import os
import numpy as np
import pickle


def get_1(file_path):
    with open(file_path, 'rb') as f:
        ki_tr, ccki_tr = pickle.load(f)
    return ki_tr, ccki_tr

def get_2(file_path):
    with open(file_path, 'rb') as f:
        ks, ccks, tr_cck_ns, ki_map = pickle.load(f)
    tr_cck_ns = np.array(tr_cck_ns)
    return ks, ccks, tr_cck_ns, ki_map

def load_single_gt(fn, gt, i1):
    with open(fn) as f:
        i0 = 0
        for line in f:
            gt[i0,i1] = int(line)
            i0 += 1

def compute_gt_cgt_single_batch(batch_num, kmer_dir, out_dir, ki_map, tr_cck_ns, NK, NCCK, NB):
    kmerfs = sorted(glob.glob(kmer_dir))
    ng = len(kmerfs)
    
    BS = ng // NB
    BS_ = BS if batch_num != NB-1 else ng - BS*batch_num

    print(f"batch {batch_num}: loading gt... ", end="")
    gt = np.zeros([NK, BS_], dtype=np.int32)
    for j in range(BS_):
        load_single_gt(kmerfs[batch_num*BS+j], gt, j)
    
    print(f"computing cgt... ", end="")
    cgt = np.zeros([NCCK, BS_], dtype=np.float32)
    for i0, i1 in ki_map.items():
        cgt[i1] += gt[i0]
    
    cgt /= tr_cck_ns[:, None]

    print("dumping gt... ", end="")
    with open(f"{out_dir}/gt.{batch_num}.pickle", 'wb') as f:
        pickle.dump(gt, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("dumping cgt...")
    with open(f"{out_dir}/cgt.{batch_num}.pickle", 'wb') as f:
        pickle.dump(cgt, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    get_1_file = argv[1]
    get_2_file = argv[2]
    batch_num = int(argv[3]) 
    total_batches = int(argv[4])
    kmers = argv[5]
    out = argv[6]
    
    if not os.path.exists(out):
        os.makedirs(out)

    # get necessary kmer and motif data
    ki_tr, ccki_tr = get_1(get_1_file)
    ks, ccks, tr_cck_ns, ki_map = get_2(get_2_file)

    NK = len(ks)
    NCCK = len(ccks)
    NB = total_batches

    compute_gt_cgt_single_batch(batch_num, kmers, out, ki_map, tr_cck_ns, NK, NCCK, NB)
