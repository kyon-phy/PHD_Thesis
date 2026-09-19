#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import math
import os
import re
import sys

def is_bad_number(x: float) -> bool:
    return x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x)))

def read_limits_from_root(root_path: str):
    """
    Return (exp_upperlimit, exp_upperlimit_plus1, exp_upperlimit_minus1, exp_upperlimit_plus2, exp_upperlimit_minus2) from TTree 'stats' branches:
      - exp_upperlimit
      - exp_upperlimit_plus1
      - exp_upperlimit_minus1
      - exp_upperlimit_plus2
      - exp_upperlimit_minus2
    Prefer uproot; if unavailable, try PyROOT.
    """
    if not os.path.isfile(root_path):
        raise FileNotFoundError(f"ROOT file not found: {root_path}")

    # 1) Try uproot (recommended)
    try:
        import uproot
        import numpy as np

        with uproot.open(root_path) as f:
            if "stats" not in f:
                raise KeyError(f"'stats' TTree not found in {root_path}")
            t = f["stats"]

            # These usually are length-1 arrays; take first entry.
            exp_arr = t["exp_upperlimit"].array(library="np")
            plus1_arr = t["exp_upperlimit_plus1"].array(library="np")
            minus1_arr = t["exp_upperlimit_minus1"].array(library="np")
            plus2_arr = t["exp_upperlimit_plus2"].array(library="np")
            minus2_arr = t["exp_upperlimit_minus2"].array(library="np")

            exp = float(exp_arr[0]) if len(exp_arr) else float("nan")
            plus1 = float(plus1_arr[0]) if len(plus1_arr) else float("nan")
            minus1 = float(minus1_arr[0]) if len(minus1_arr) else float("nan")
            plus2 = float(plus2_arr[0]) if len(plus2_arr) else float("nan")
            minus2 = float(minus2_arr[0]) if len(minus2_arr) else float("nan")
            return exp, plus1, minus1, plus2, minus2

    except ImportError:
        pass
    except Exception as e:
        # If uproot exists but fails for some reason, still try PyROOT below
        uproot_err = e
    else:
        uproot_err = None

    # 2) Try PyROOT fallback
    try:
        import ROOT  # type: ignore

        f = ROOT.TFile.Open(root_path, "READ")
        if not f or f.IsZombie():
            raise RuntimeError(f"Cannot open ROOT file: {root_path}")
        t = f.Get("stats")
        if not t:
            raise KeyError(f"'stats' TTree not found in {root_path}")

        # read first entry
        if t.GetEntries() <= 0:
            return float("nan"), float("nan")

        t.GetEntry(0)
        plus2 = float(getattr(t, "exp_upperlimit_plus2"))
        minus2 = float(getattr(t, "exp_upperlimit_minus2"))
        f.Close()
        return plus2, minus2

    except Exception as e:
        msg = f"Failed to read ROOT limits from {root_path}.\n"
        if uproot_err is not None:
            msg += f"uproot error: {uproot_err}\n"
        msg += f"PyROOT error: {e}\n"
        raise RuntimeError(msg)

def build_new_limit_block(scan_min: float, scan_max: float, seed: int) -> str:
    """
    Generate the rewritten Limit block. Keep indentation consistent (4 spaces).
    """
    # 按你的要求：LimitBlind: TRUE，并加入 TOYS/Scan*
    return (
        'Limit: "limit"\n'
        '        POI: sqrt_mu\n'
        '        LimitType: TOYS\n'
        '        SplusBToys: 10000\n'
        '        BonlyToys: 10000\n'
        '        ScanSteps: 15\n'
        f'        ToysSeed: {seed}\n'
        f'        ScanMin: {scan_min:g}\n'
        f'        ScanMax: {scan_max:g}\n'
        '        LimitBlind: False\n'
        '\n'
    )

def build_new_NormFactor_mu_block(scan_min: float, scan_max: float) -> str:
    """
    Generate the rewritten NormFactor "mu" block. Keep indentation consistent (4 spaces).
    """
    return (
        'NormFactor: "mu"\n'
        '        Category: Theory\n'
        f'        Max: {scan_max:g}\n'
        f'        Min: {scan_min:g}\n'
        '        Nominal: 1\n'
    )

def build_new_NormFactor_sqrt_mu_block(scan_min: float, scan_max: float) -> str:
    """
    Generate the rewritten NormFactor "sqrt_mu" block. Keep indentation consistent (4 spaces).
    """
    return (
        'NormFactor: "sqrt_mu"\n'
        '        Category: Theory\n'
        f'        Max: {scan_max:g}\n'
        f'        Min: {scan_min:g}\n'
        '        Nominal: 1\n'
    )
def build_new_NormFactor_bsm_block(scan_min: float, scan_max: float) -> str:
    """
    Generate the rewritten NormFactor "Norm_BSM" block. Keep indentation consistent (4 spaces).
    """
    return (
        'NormFactor: "Norm_BSM"\n'
        '    Category: Theory\n'
        f'    Expression: (sqrt_mu^2-sqrt_mu): sqrt_mu[1,{scan_min},{scan_max:g}]\n'
        '    '
    )  
    
def replace_limit_block(config_text: str, new_block: str) -> str:
    """
    Replace the block that starts with: Limit: "limit"
    and continues until the next top-level block (a line starting at column 0)
    or end-of-file.

    This is robust for typical config formats.
    """
    # Match from beginning-of-line Limit: "limit"
    # then consume following lines that are indented (start with whitespace) OR blank,
    # stop right before next non-indented non-blank line.
    pattern = re.compile(
        r'(?m)^Limit:\s*"limit"\s*\n'          # header line
        r'(?:^[ \t].*\n|^\s*\n)*'              # indented lines / blank lines
    )

    m = pattern.search(config_text)
    if not m:
        raise ValueError('Cannot find Limit block starting with: Limit: "limit"')

    start, end = m.start(), m.end()
    return config_text[:start] + new_block + config_text[end:]

def replace_NormFactor_mu_block(config_text: str, new_block: str) -> str:
    """
    Replace the block that starts with: NormFactor: "mu"
    and continues until the line that starts with 'Nominal:' (inclusive).
    """
    # Match from beginning-of-line NormFactor: "mu"
    # and consume through the first line at column 0 that starts with 'Nominal:'
    # with or without whitespace before the number, and optional whitespace after colon.
    pattern = re.compile(
        r'(?m)^NormFactor:\s*"mu"\s*\n'          # header line
        r'(?:^[ \t]+\S.*\n)*?'                   # non-empty indented lines (non-greedy)
        r'^[ \t]*Nominal:\s*.*\n'                # the Nominal: line
    )

    m = pattern.search(config_text)
    if not m:
        raise ValueError('Cannot find NormFactor block (NormFactor: "mu" ... Nominal:)')

    start, end = m.start(), m.end()
    return config_text[:start] + new_block + config_text[end:]

def replace_NormFactor_sqrt_mu_block(config_text: str, new_block: str) -> str:
    """
    Replace the block that starts with: NormFactor: "sqrt_mu"
    and continues until the line that starts with 'Nominal:' (inclusive).
    """
    # Match from beginning-of-line NormFactor: "sqrt_mu"
    # and consume through the first line at column 0 that starts with 'Nominal:'
    # with or without whitespace before the number, and optional whitespace after colon.
    pattern = re.compile(
        r'(?m)^NormFactor:\s*"sqrt_mu"\s*\n'          # header line
        r'(?:^[ \t]+\S.*\n)*?'                   # non-empty indented lines (non-greedy)
        r'^[ \t]*Nominal:\s*.*\n'                # the Nominal: line
    )

    m = pattern.search(config_text)
    if not m:
        raise ValueError('Cannot find NormFactor block (NormFactor: "sqrt_mu" ... Nominal:)')

    start, end = m.start(), m.end()
    return config_text[:start] + new_block + config_text[end:]

def replace_NormFactor_bsm_block(config_text: str, new_block: str) -> str:
    """
    Replace the block that starts with: NormFactor: "mu_interference"
    and continues until the *next* NormFactor, a comment, or the end of file.
    This matches exactly the block starting e.g.:
      NormFactor: "mu_interference"
          Category: Theory
          Expression: sqrt(mu): mu[1,scan_min,scan_max]
    and replaces it.
    """
    # Regex to match from line starting with NormFactor: "mu_interference"
    # and subsequent indented lines, until hitting another block or EOF.
    pattern = re.compile(
        r'(?m)^NormFactor:\s*"Norm_BSM"\s*\n'     # header
        r'(?:[ \t]+.*\n)*?'                              # non-greedy: match indented lines (including Expression)
        r'^[ \t]*'                                       # start of next line (column 0 or whitespace)
        r'(?=(?:Samples:|$))',                           # Lookahead: stop BEFORE 'Samples:' or end of file
    )
    m = pattern.search(config_text)
    if not m:
        raise ValueError('Cannot find NormFactor block (NormFactor: "Norm_BSM" ...)')

    start, end = m.start(), m.end()
    return config_text[:start] + new_block + config_text[end:]

def extract_x_from_config_filename(fname: str, combined: bool):
    """
    From config filename extract x in: noWeights_comb_{x}
    Example:
      config_..._noWeights_comb_MU5000_gU1_0_23L0_2.config
      -> x = MU5000_gU1_0_23L0_2
    """
    if not combined:
        m = re.search(r'noWeights_(.+?)\.config$', fname) # for combined fits.
    elif combined:
        m = re.search(r'noWeights_comb_0b1bSR_(.+?)\.config$', fname) # for bsm+inf fits.
    else:
        raise ValueError('Invalid flag for combined fits')
    return m.group(1) if m else None

def extract_y_from_foldername(dname: str):
    """
    From fit folder name extract y in: allVR_SPLUSB_{y}_noWeights
    Example:
      fit_..._allVR_SPLUSB_MU1500_gU1_0_23L0_2_noWeights_unblind_test
      -> y = MU1500_gU1_0_23L0_2
    """
    m = re.search(r'allVR_SPLUSB_(.+?)_noWeights', dname)
    return m.group(1) if m else None

def main():
    ap = argparse.ArgumentParser(
        description="Match configs to fit folders, read 2-sigma limits from ROOT, rewrite Limit block, and save to output dir."
    )
    ap.add_argument("config_dir", help="Folder A: configs (*.config)")
    ap.add_argument("fit_parent_dir", help="Folder B: contains many fit_* subfolders")
    ap.add_argument("out_dir", help="Output folder for rewritten configs")
    ap.add_argument("--root-relpath", default=os.path.join("Limits", "Asymptotics", "myLimit.root"),
                    help='Relative path to ROOT file inside each fit folder (default: "Limits/Asymptotics/myLimit.root")')
    ap.add_argument("--dry-run", action="store_true", help="Only print actions, do not write files")
    # add argument to specify the seed
    ap.add_argument("--seed", type=int, default=1234, help="Seed for the toy generation")
    ap.add_argument("--combined", action="store_true", help="Use BSM and interfence combined fits")
    args = ap.parse_args()

    config_dir = os.path.abspath(args.config_dir)
    fit_parent = os.path.abspath(args.fit_parent_dir)
    out_dir = os.path.abspath(args.out_dir)
    seed = args.seed
    combined = args.combined

    if not os.path.isdir(config_dir):
        print(f"[ERROR] config_dir not found: {config_dir}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(fit_parent):
        print(f"[ERROR] fit_parent_dir not found: {fit_parent}", file=sys.stderr)
        sys.exit(1)

    # Build mapping y -> fit_folder_path
    y_to_fitpath = {}
    for name in os.listdir(fit_parent):
        p = os.path.join(fit_parent, name)
        if not os.path.isdir(p):
            continue
        y = extract_y_from_foldername(name)
        if y:
            # if duplicates exist, keep the first; you can customize if needed
            y_to_fitpath.setdefault(y, p)

    os.makedirs(out_dir, exist_ok=True)

    # Process configs
    n_total = 0
    n_matched = 0
    n_written = 0
    n_skipped = 0

    for fname in sorted(os.listdir(config_dir)):
        if not fname.endswith(".config"):
            continue
        n_total += 1
        x = extract_x_from_config_filename(fname, combined)
        if not x:
            print(f"[SKIP] cannot extract x from filename: {fname}")
            n_skipped += 1
            continue

        fit_path = y_to_fitpath.get(x)
        if not fit_path:
            print(f"[SKIP] no matching fit folder for x={x} (file={fname})")
            n_skipped += 1
            continue

        root_path = os.path.join(fit_path, args.root_relpath)

        try:
            exp, plus1, minus1, plus2, minus2 = read_limits_from_root(root_path)

            # Default if NaN/Inf
            if is_bad_number(exp) or is_bad_number(plus1) or is_bad_number(minus1) or is_bad_number(plus2) or is_bad_number(minus2):
                scan_min, scan_max = 0, 50.0
            else:
                # scan_min = minus2 - abs(minus1 - minus2)
                scan_min = 0 # scan mu from to scan max
                scan_max = plus2 + abs(plus2 - plus1)
                if scan_min < 0:
                    scan_min = 0.0
                if scan_max < 1.1:
                    scan_max = 1.1
                if scan_min > exp:
                    # report error when the case
                    print(f"[ERROR] scan_min > exp: {scan_min} > {exp}")
                    sys.exit(1)
                if scan_max < exp:
                    # report error when the case
                    print(f"[ERROR] scan_max < exp: {scan_max} < {exp}")
                    sys.exit(1)

            new_block = build_new_limit_block(scan_min, scan_max, seed)
            if combined:
                new_NormFactor_sqrt_mu_block = build_new_NormFactor_sqrt_mu_block(scan_min, scan_max)
                new_NormFactor_bsm_block = build_new_NormFactor_bsm_block(scan_min, scan_max)
            else:
                new_NormFactor_mu_block = build_new_NormFactor_mu_block(scan_min, scan_max)
                
            cfg_path = os.path.join(config_dir, fname)
            with open(cfg_path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()

            new_text = replace_limit_block(text, new_block)
            if combined:
                new_text = replace_NormFactor_sqrt_mu_block(new_text, new_NormFactor_sqrt_mu_block)
                new_text = replace_NormFactor_bsm_block(new_text, new_NormFactor_bsm_block)
            else:
                new_text = replace_NormFactor_mu_block(new_text, new_NormFactor_mu_block)
            
            out_path = os.path.join(out_dir, fname)
            n_matched += 1

            print(f"[OK] {fname}")
            print(f"     x={x}")
            print(f"     fit={os.path.basename(fit_path)}")
            print(f"     root={root_path}")
            print(f"     plus2={plus2} minus2={minus2} => ScanMin={scan_min:g} ScanMax={scan_max:g}")
            print(f"     out={out_path}")

            if not args.dry_run:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(new_text)
                n_written += 1

        except Exception as e:
            print(f"[ERROR] {fname} (x={x}) failed: {e}", file=sys.stderr)
            n_skipped += 1

    print("\n=== Summary ===")
    print(f"Total configs:   {n_total}")
    print(f"Matched:         {n_matched}")
    print(f"Written:         {n_written}" if not args.dry_run else f"Written:         0 (dry-run)")
    print(f"Skipped/Failed:  {n_skipped}")

if __name__ == "__main__":
    main()
