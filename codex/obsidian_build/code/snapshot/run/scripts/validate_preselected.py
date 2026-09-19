#!/usr/bin/env python3
"""Validate preselected ntuples against the full (non-preselected) ones.

For each DSID+campaign, open the 'reco' tree in both directories, match
entries by eventNumber, and check:
  1. every preselected event exists in the full sample (subset check)
  2. all 'weight_mc_corrected_GEN_gU*' values are identical for matched events

Expectation: weights identical for ALL DSIDs; preselected has fewer events.

Usage:
  python3 validate_preselected.py \
      --dir-full  .../SIG/alldecay_betaR33_reweighted \
      --dir-presel .../SIG/alldecay_betaR33_reweighted_preselected
"""

import argparse
import glob
import os
import re
import sys
from collections import defaultdict

import numpy as np

from validate_signal_reweight import (
    BRANCH_PREFIX, list_gu_branches, load_group, compare_group,
)

RTAG_TO_CAMPAIGN = {"r14859": "mc20a", "r14860": "mc20d", "r14861": "mc20e"}
DIR_RE = re.compile(r"user\.zang\.(\d{6})\..*_(r\d{5})_")


def scan_dir(base):
    """Return {(dsid, campaign): [root files]} from a sample directory."""
    groups = defaultdict(list)
    for d in sorted(os.listdir(base)):
        m = DIR_RE.search(d)
        if not m:
            continue
        dsid = int(m.group(1))
        campaign = RTAG_TO_CAMPAIGN.get(m.group(2), m.group(2))
        files = sorted(glob.glob(os.path.join(base, d, "*.root")))
        if files:
            groups[(dsid, campaign)].extend(files)
    return groups


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir-full", required=True,
                    help="directory with the full (non-preselected) ntuples")
    ap.add_argument("--dir-presel", required=True,
                    help="directory with the preselected ntuples")
    ap.add_argument("--dsids", type=int, nargs="*", default=None,
                    help="restrict to these DSIDs (default: all found)")
    ap.add_argument("--rtol", type=float, default=1e-5)
    ap.add_argument("--threads", type=int, default=8)
    args = ap.parse_args()

    import ROOT
    ROOT.gROOT.SetBatch(True)
    if args.threads > 1:
        ROOT.EnableImplicitMT(args.threads)

    g_full = scan_dir(args.dir_full)
    g_presel = scan_dir(args.dir_presel)
    if args.dsids:
        keep = set(args.dsids)
        g_full = {k: v for k, v in g_full.items() if k[0] in keep}
        g_presel = {k: v for k, v in g_presel.items() if k[0] in keep}

    only_full = sorted(set(g_full) - set(g_presel))
    only_presel = sorted(set(g_presel) - set(g_full))
    if only_full:
        print(f"WARNING: groups only in {args.dir_full}: {only_full}")
    if only_presel:
        print(f"WARNING: groups only in {args.dir_presel}: {only_presel}")
    keys = sorted(set(g_full) & set(g_presel))
    if not keys:
        sys.exit("ERROR: no common (DSID, campaign) groups found")

    branches_f = list_gu_branches(g_full[keys[0]][0])
    branches_p = list_gu_branches(g_presel[keys[0]][0])
    branches = sorted(set(branches_f) & set(branches_p))
    print(f"Comparing {len(branches)} '{BRANCH_PREFIX}*' branches "
          f"(full has {len(branches_f)}, presel has {len(branches_p)})\n")

    dsid_summary = defaultdict(lambda: {"full": 0, "presel": 0, "common": 0,
                                        "orphan": 0, "diff_entries": 0,
                                        "max_rel": 0.0})

    for dsid, campaign in keys:
        ev_f, w_f, dup_f = load_group(g_full[(dsid, campaign)], branches)
        ev_p, w_p, dup_p = load_group(g_presel[(dsid, campaign)], branches)
        n_common, res = compare_group(ev_f, w_f, ev_p, w_p, branches, args.rtol)

        n_orphan = len(ev_p) - n_common   # preselected events missing in full
        tot_diff = sum(n for n, _ in res.values())
        max_rel = max((r for _, r in res.values()), default=0.0)
        n_diff_br = sum(1 for n, _ in res.values() if n > 0)

        s = dsid_summary[dsid]
        s["full"] += len(ev_f)
        s["presel"] += len(ev_p)
        s["common"] += n_common
        s["orphan"] += n_orphan
        s["diff_entries"] += tot_diff
        s["max_rel"] = max(s["max_rel"], max_rel)

        msg = (f"[{dsid} {campaign}] full:{len(ev_f)} presel:{len(ev_p)} "
               f"matched:{n_common} presel-not-in-full:{n_orphan} | "
               f"branches w/ diff: {n_diff_br}/{len(branches)} | "
               f"max reldiff: {max_rel:.3e}")
        if dup_f or dup_p:
            msg += f" | dropped dup eventNumbers full:{dup_f} presel:{dup_p}"
        print(msg, flush=True)

    print("\n===== per-DSID validation =====")
    n_fail = 0
    for dsid in sorted(dsid_summary):
        s = dsid_summary[dsid]
        problems = []
        if s["common"] == 0:
            problems.append("no matched events")
        if s["diff_entries"] > 0:
            problems.append(f"{s['diff_entries']} differing weight values")
        if s["orphan"] > 0:
            problems.append(f"{s['orphan']} presel events not in full sample")
        ok = not problems
        if not ok:
            n_fail += 1
        frac = s["presel"] / s["full"] if s["full"] else float("nan")
        status = "PASS" if ok else "FAIL (" + "; ".join(problems) + ")"
        print(f"  {dsid}: full={s['full']:>8}  presel={s['presel']:>8} "
              f"({frac:6.2%})  matched={s['common']:>8}  "
              f"max_reldiff={s['max_rel']:.3e}  -> {status}")

    print(f"\n{'ALL PASSED' if n_fail == 0 else f'{n_fail} DSID(s) FAILED'}")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
