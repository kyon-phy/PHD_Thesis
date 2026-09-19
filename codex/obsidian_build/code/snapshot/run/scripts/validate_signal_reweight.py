#!/usr/bin/env python3
"""Validate signal reweighting between two filelists.

For each signal DSID (567621-567634), open the 'reco' tree of the ntuples
listed in two filelists, match entries by eventNumber (per DSID+campaign),
and compare all 'weight_mc_corrected_GEN_gU*' branches.

Expectation:
  - 567621-567627: values should be IDENTICAL between the two productions
  - 567628-567634: values should be DIFFERENT

Usage:
  python3 validate_signal_reweight.py \
      --filelist-a ../../input/filelist.txt \
      --filelist-b ../../input/filelist_v04.txt
"""

import argparse
import sys
from collections import defaultdict

import numpy as np
import ROOT

TREE_NAME = "reco"
BRANCH_PREFIX = "weight_mc_corrected_GEN_gU"
DSIDS_SAME = list(range(567621, 567628))       # expect identical weights
DSIDS_DIFF = list(range(567628, 567635))       # expect different weights


def parse_filelist(path, dsids):
    """Return {(dsid, campaign): [file paths]} for the requested DSIDs."""
    groups = defaultdict(list)
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 4:
                continue
            try:
                dsid = int(parts[0])
            except ValueError:
                continue
            if dsid in dsids:
                groups[(dsid, parts[1])].append(parts[3])
    return groups


def list_gu_branches(filepath):
    """Return the sorted set of gU-corrected weight branches in one file."""
    f = ROOT.TFile.Open(filepath)
    if not f or f.IsZombie():
        raise RuntimeError(f"cannot open {filepath}")
    tree = f.Get(TREE_NAME)
    if not tree:
        raise RuntimeError(f"no '{TREE_NAME}' tree in {filepath}")
    branches = sorted(
        b.GetName() for b in tree.GetListOfBranches()
        if b.GetName().startswith(BRANCH_PREFIX)
    )
    f.Close()
    return branches


def load_group(files, branches):
    """Read eventNumber + weight branches into numpy arrays via RDataFrame."""
    paths = ROOT.std.vector("string")()
    for p in files:
        paths.push_back(p)
    rdf = ROOT.RDataFrame(TREE_NAME, paths)
    data = rdf.AsNumpy(["eventNumber"] + branches)

    ev = data["eventNumber"]
    uniq, counts = np.unique(ev, return_counts=True)
    n_dup = int(np.sum(counts > 1))
    if n_dup:
        # keep only event numbers that appear exactly once so matching is unambiguous
        keep_ev = uniq[counts == 1]
        mask = np.isin(ev, keep_ev)
        ev = ev[mask]
        for br in branches:
            data[br] = data[br][mask]
    order = np.argsort(ev)
    ev = ev[order]
    weights = {br: data[br][order] for br in branches}
    return ev, weights, n_dup


def compare_group(ev_a, w_a, ev_b, w_b, branches, rtol):
    """Match by eventNumber and compare each branch.

    Returns (n_common, per-branch dict {branch: (n_diff, max_reldiff)}).
    """
    common, idx_a, idx_b = np.intersect1d(
        ev_a, ev_b, assume_unique=True, return_indices=True
    )
    n_common = len(common)
    results = {}
    for br in branches:
        va = w_a[br][idx_a].astype(np.float64)
        vb = w_b[br][idx_b].astype(np.float64)
        close = np.isclose(va, vb, rtol=rtol, atol=0.0, equal_nan=True)
        n_diff = int(np.sum(~close))
        denom = np.maximum(np.abs(va), np.abs(vb))
        with np.errstate(divide="ignore", invalid="ignore"):
            reldiff = np.where(denom > 0, np.abs(va - vb) / denom, 0.0)
        results[br] = (n_diff, float(np.max(reldiff)) if n_common else 0.0)
    return n_common, results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--filelist-a", required=True,
                    help="first filelist (e.g. filelist.txt, reweighted)")
    ap.add_argument("--filelist-b", required=True,
                    help="second filelist (e.g. filelist_v04.txt, original)")
    ap.add_argument("--dsids", type=int, nargs="*",
                    default=DSIDS_SAME + DSIDS_DIFF)
    ap.add_argument("--rtol", type=float, default=1e-5,
                    help="relative tolerance for 'identical' (default 1e-5)")
    ap.add_argument("--threads", type=int, default=8)
    args = ap.parse_args()

    ROOT.gROOT.SetBatch(True)
    if args.threads > 1:
        ROOT.EnableImplicitMT(args.threads)

    dsids = set(args.dsids)
    groups_a = parse_filelist(args.filelist_a, dsids)
    groups_b = parse_filelist(args.filelist_b, dsids)

    keys = sorted(set(groups_a) & set(groups_b))
    only_a = sorted(set(groups_a) - set(groups_b))
    only_b = sorted(set(groups_b) - set(groups_a))
    if only_a:
        print(f"WARNING: groups only in {args.filelist_a}: {only_a}")
    if only_b:
        print(f"WARNING: groups only in {args.filelist_b}: {only_b}")
    if not keys:
        sys.exit("ERROR: no common (DSID, campaign) groups found")

    # use branches present in both productions
    branches_a = list_gu_branches(groups_a[keys[0]][0])
    branches_b = list_gu_branches(groups_b[keys[0]][0])
    branches = sorted(set(branches_a) & set(branches_b))
    print(f"Comparing {len(branches)} '{BRANCH_PREFIX}*' branches "
          f"(A has {len(branches_a)}, B has {len(branches_b)})\n")

    # per-DSID accumulation over campaigns
    dsid_summary = defaultdict(lambda: {"common": 0, "diff_entries": 0,
                                        "diff_branches": set(), "max_rel": 0.0})

    for dsid, campaign in keys:
        ev_a, w_a, dup_a = load_group(groups_a[(dsid, campaign)], branches)
        ev_b, w_b, dup_b = load_group(groups_b[(dsid, campaign)], branches)
        n_common, res = compare_group(ev_a, w_a, ev_b, w_b, branches, args.rtol)

        tot_diff = sum(n for n, _ in res.values())
        max_rel = max((r for _, r in res.values()), default=0.0)
        diff_brs = [br for br, (n, _) in res.items() if n > 0]

        s = dsid_summary[dsid]
        s["common"] += n_common
        s["diff_entries"] += tot_diff
        s["diff_branches"] |= set(diff_brs)
        s["max_rel"] = max(s["max_rel"], max_rel)

        msg = (f"[{dsid} {campaign}] A:{len(ev_a)} B:{len(ev_b)} "
               f"matched:{n_common} | branches w/ diff: "
               f"{len(diff_brs)}/{len(branches)} | max reldiff: {max_rel:.3e}")
        if dup_a or dup_b:
            msg += f" | dropped dup eventNumbers A:{dup_a} B:{dup_b}"
        print(msg, flush=True)

    print("\n===== per-DSID validation =====")
    n_fail = 0
    for dsid in sorted(dsid_summary):
        s = dsid_summary[dsid]
        expect_same = dsid in DSIDS_SAME
        is_same = s["diff_entries"] == 0
        if s["common"] == 0:
            status, ok = "NO MATCHED EVENTS", False
        elif expect_same:
            ok = is_same
            status = "PASS (identical as expected)" if ok else \
                     "FAIL (expected identical but found differences)"
        else:
            ok = not is_same
            status = "PASS (different as expected)" if ok else \
                     "FAIL (expected different but values are identical)"
        if not ok:
            n_fail += 1
        print(f"  {dsid}: matched={s['common']:>8}  "
              f"diff_values={s['diff_entries']:>10}  "
              f"diff_branches={len(s['diff_branches']):>2}/{len(branches)}  "
              f"max_reldiff={s['max_rel']:.3e}  -> {status}")

    print(f"\n{'ALL PASSED' if n_fail == 0 else f'{n_fail} DSID(s) FAILED'}")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
