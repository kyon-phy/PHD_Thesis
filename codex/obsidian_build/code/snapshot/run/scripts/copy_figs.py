import os
import shutil

source_dir = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots_paper_test"
dest_base = "/afs/cern.ch/work/z/zang/LQanalysis/ANA-EXOT-2025-06-PAPER/figures"
map_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paper_figs_map.txt")


def load_map(path):
    pairs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            src_name, dst_rel = line.split(None, 1)
            pairs.append((src_name.strip(), dst_rel.strip()))
    return pairs


def main():
    for src_name, dst_rel in load_map(map_file):
        src = os.path.join(source_dir, src_name)
        dst = os.path.join(dest_base, dst_rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.isfile(src):
            print(f"[WARN] missing source: {src}")
            continue
        shutil.copy(src, dst)
        print(f"[OK] {src_name} -> {dst_rel}")


if __name__ == "__main__":
    main()
