#!/usr/bin/env python3
"""Compare GEN_gU* sum-of-weights between two sum_of_weights files.

File format per line: DSID campaign simtype variation value

Expectation (same as the ntuple-level check):
  - 567621-567627: sums should be IDENTICAL (up to float32 precision)
  - 567628-567634: sums should be DIFFERENT

Usage:
  python3 compare_sum_of_weights.py \
      --file-a ../../input/sum_of_weights.txt \
      --file-b ../../input/sum_of_weights_v04.txt
"""

import argparse
import sys
from collections import defaultdict

VAR_PREFIX = "GEN_gU"
DSIDS_SAME = list(range(567621, 567628))
DSIDS_DIFF = list(range(567628, 567635))


def parse(path, dsids):
    """Return {(dsid, campaign, variation): value}."""
    out = {}
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 5:
                continue
            try:
                dsid = int(parts[0])
            except ValueError:
                continue
            if dsid in dsids and parts[3].startswith(VAR_PREFIX):
                out[(dsid, parts[1], parts[3])] = float(parts[4])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file-a", required=True)
    ap.add_argument("--file-b", required=True)
    ap.add_argument("--dsids", type=int, nargs="*",
                    default=DSIDS_SAME + DSIDS_DIFF)
    ap.add_argument("--rtol", type=float, default=1e-5,
                    help="relative tolerance for 'identical' (default 1e-5; "
                         "float32 rounding gives ~1e-7 level differences)")
    args = ap.parse_args()

    dsids = set(args.dsids)
    a = parse(args.file_a, dsids)
    b = parse(args.file_b, dsids)

    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    if only_a:
        groups = sorted({(k[0], k[1]) for k in only_a})
        print(f"WARNING: (DSID, campaign) only in {args.file_a}: {groups}")
    if only_b:
        groups = sorted({(k[0], k[1]) for k in only_b})
        print(f"WARNING: (DSID, campaign) only in {args.file_b}: {groups}")

    common = sorted(set(a) & set(b))
    if not common:
        sys.exit("ERROR: no common entries")

    per_dsid = defaultdict(list)  # dsid -> [(campaign, var, va, vb, reldiff)]
    for key in common:
        va, vb = a[key], b[key]
        denom = max(abs(va), abs(vb))
        rel = abs(va - vb) / denom if denom > 0 else 0.0
        per_dsid[key[0]].append((key[1], key[2], va, vb, rel))

    print(f"Comparing {len(common)} '{VAR_PREFIX}*' sum-of-weights entries\n")

    n_fail = 0
    for dsid in sorted(per_dsid):
        rows = per_dsid[dsid]
        n_diff = sum(1 for r in rows if r[4] > args.rtol)
        diff_vars = sorted({r[1] for r in rows if r[4] > args.rtol})
        max_rel = max(r[4] for r in rows)
        expect_same = dsid in DSIDS_SAME
        is_same = n_diff == 0
        if expect_same:
            ok = is_same
            status = "PASS (identical as expected)" if ok else \
                     "FAIL (expected identical but found differences)"
        else:
            ok = not is_same
            status = "PASS (different as expected)" if ok else \
                     "FAIL (expected different but sums are identical)"
        if not ok:
            n_fail += 1
        print(f"  {dsid}: entries={len(rows):>3}  diff={n_diff:>3}  "
              f"diff_variations={len(diff_vars):>2}  "
              f"max_reldiff={max_rel:.3e}  -> {status}")

    print(f"\n{'ALL PASSED' if n_fail == 0 else f'{n_fail} DSID(s) FAILED'}")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
