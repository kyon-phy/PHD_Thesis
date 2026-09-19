#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import argparse
import math

import ROOT
ROOT.gROOT.SetBatch(True)

def find_root_files(folder):
    patterns = [os.path.join(folder, "**", "*.root"), os.path.join(folder, "*.root")]
    files = set()
    for p in patterns:
        files.update(glob.glob(p, recursive=True))
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        print(f"[WARN] No ROOT files found under: {folder}")
    return sorted(files)

def build_chain(files, treename):
    chain = ROOT.TChain(treename)
    for f in files:
        added = chain.Add(f)
        if added == 0:
            print(f"[WARN] Failed to add {f} to TChain({treename})")
    return chain

def to_list(stdvec, cast=None):
    if cast is None:
        return [stdvec[i] for i in range(stdvec.size())]
    return [cast(stdvec[i]) for i in range(stdvec.size())]

def charvec_to_int01_list(stdvec):
    out = []
    n = stdvec.size()
    for i in range(n):
        x = stdvec[i]
        if isinstance(x, str):               # e.g. '\x00', '\x01'
            out.append(ord(x))               # -> 0 或 1
        elif isinstance(x, (bytes, bytearray)): # e.g. b'\x00'
            out.append(x[0])                 # -> 0 或 1
        else:
            out.append(int(x))               # 已经是数值就转 int
    return out

def rel_diff(a, b):
    return abs(a - b) / abs(b)

def sanitize_name(name: str) -> str:
    keep = []
    for ch in name:
        if ch.isalnum() or ch in "_":
            keep.append(ch)
        else:
            keep.append("_")
    return "".join(keep)

def collect_dataset(chain, sf_branches):
    out = {}
    n_entries = chain.GetEntries()
    br_exist = lambda b: bool(chain.GetListOfBranches().FindObject(b))
    required = ["eventNumber", "randomRunNumber", "jet_pt_NOSYS", "jet_eta", "jet_phi", "jet_select_GN2v01_FixedCutBEff_85_NOSYS"]
    for b in required:
        if not br_exist(b):
            raise RuntimeError(f"Missing branch '{b}' in dataset1")
    for sf in sf_branches:
        if not br_exist(sf):
            raise RuntimeError(f"Missing SF branch '{sf}' in dataset1")

    for i in range(n_entries):
        chain.GetEntry(i)
        key = (int(getattr(chain, "eventNumber")), int(getattr(chain, "randomRunNumber")))
        out[key] = {
            "pt":  to_list(getattr(chain, "jet_pt_NOSYS")),
            "eta": to_list(getattr(chain, "jet_eta")),
            "phi": to_list(getattr(chain, "jet_phi")),
            "select": charvec_to_int01_list(getattr(chain, "jet_select_GN2v01_FixedCutBEff_85_NOSYS")),
            "sf":  {sf: getattr(chain, sf) for sf in sf_branches},
        }
        # # print the first 10 entries
        # if i < 10:
        #     print(f"[INFO] Entry {i}: {key}")
        #     print(f"[INFO] pt: {out[key]['pt']}")
        #     print(f"[INFO] eta: {out[key]['eta']}")
        #     print(f"[INFO] phi: {out[key]['phi']}")
        #     print(f"[INFO] select: {out[key]['select']}")
        #     print(f"[INFO] sf: {out[key]['sf']}")
        # show the percentage of the progress when loop over 10% of the entries
        if (i+1) % (n_entries // 10) == 0:
            percentage = (i+1) / n_entries * 100
            print(f"[INFO] progress: {percentage:.2f}%")
            print(f"[INFO] Indexed {i+1}/{n_entries} entries")
    return out

def compare_and_fill(chain2, refmap, hists, h_all, sf_branches, pt_tol=0.05, etaphisq_tol=0.05):
    n_entries = chain2.GetEntries()
    br_exist = lambda b: bool(chain2.GetListOfBranches().FindObject(b))
    required = ["eventNumber", "randomRunNumber", "jet_pt_NOSYS", "jet_eta", "jet_phi", "jet_select_GN2v01_FixedCutBEff_85_NOSYS"]
    for b in required:
        if not br_exist(b):
            raise RuntimeError(f"Missing branch '{b}' in dataset2")
    for sf in sf_branches:
        if not br_exist(sf):
            raise RuntimeError(f"Missing SF branch '{sf}' in dataset2")

    stats = {
        "n_evt_total": 0,
        "n_evt_matched": 0,
        "n_jet_compared": 0,
        "n_jet_filled_per_sf": {sf: 0 for sf in sf_branches},
        "n_jet_filled_all_product": 0,
        "n_events_R21": 0,
        "n_events_R22": 0,
    }

    for i in range(n_entries):
        chain2.GetEntry(i)
        stats["n_evt_total"] += 1
        key = (int(getattr(chain2, "eventNumber")), int(getattr(chain2, "randomRunNumber")))
        if key not in refmap:
            continue
        stats["n_evt_matched"] += 1

        rec1 = refmap[key]
        pt1, eta1, phi1, sf1_map, select1 = rec1["pt"], rec1["eta"], rec1["phi"], rec1["sf"], rec1["select"]

        pt2   = to_list(getattr(chain2, "jet_pt_NOSYS"))
        eta2  = to_list(getattr(chain2, "jet_eta"))
        phi2  = to_list(getattr(chain2, "jet_phi"))
        select2 = charvec_to_int01_list(getattr(chain2, "jet_select_GN2v01_FixedCutBEff_85_NOSYS"))
        sf2_map = {sf: getattr(chain2, sf) for sf in sf_branches}

        n = min(len(pt1), len(pt2), len(eta1), len(eta2), len(phi1), len(phi2), len(select1), len(select2))
        if n <= 0:
            continue

        n_bjets = 0
        for j in range(n):
            stats["n_jet_compared"] += 1
            # compare pt
            if rel_diff(pt1[j], pt2[j]) > pt_tol:
                continue
            # compare deltaR
            v1 = eta1[j]*eta1[j] + phi1[j]*phi1[j]
            v2 = eta2[j]*eta2[j] + phi2[j]*phi2[j]
            if rel_diff(v1**0.5, v2**0.5) > etaphisq_tol:
                continue
            # select bjet 85% WP
            if select1[j] == select2[j] and select1[j] == 1:
                n_bjets += 1

        # compute the SFs while bjets >= 1
        if n_bjets >= 1:
            # 逐 SF 填充
            for sf in sf_branches:
                v1 = sf1_map.get(sf, 1.0)
                v2 = sf2_map.get(sf, 1.0)
                ratio = v2 / v1
                if math.isfinite(ratio):
                    hists[sf].Fill(ratio)
                    stats["n_jet_filled_per_sf"][sf] += 1

            # —— 所有 SF 相乘的比值 —— #
            prod1, prod2 = 1.0, 1.0
            for sf in sf_branches:
                v1 = sf1_map.get(sf, 1.0)
                v2 = sf2_map.get(sf, 1.0)
                prod1 *= v1
                prod2 *= v2

            ratio_all = prod2 / prod1
            if math.isfinite(ratio_all):
                h_all.Fill(ratio_all)
                stats["n_jet_filled_all_product"] += 1
                stats["n_events_R21"] += prod1
                stats["n_events_R22"] += prod2

        # show the percentage of the progress when loop over 10% of the entries
        if (i+1) % (n_entries // 10) == 0:
            percentage = (i+1) / n_entries * 100
            print(f"[INFO] progress: {percentage:.2f}%")
            print(f"[INFO] Scanned {i+1}/{n_entries} entries in dataset2")

    return stats

def main():
    parser = argparse.ArgumentParser(description="Compare SF branches between two ROOT datasets and draw separate (non-normalized) histograms + product-of-all-SFs histogram.")
    parser.add_argument("--filepath1", required=True, help="Folder for dataset1 (.root files)")
    parser.add_argument("--filepath2", required=True, help="Folder for dataset2 (.root files)")
    parser.add_argument("--tree", default="reco", help="TTree name (default: reco)")
    parser.add_argument("--out", default="sf_ratio.root", help="Output ROOT file")
    parser.add_argument("--bins", type=int, default=100, help="Histogram bins")
    parser.add_argument("--xmin", type=float, default=0.5, help="Histogram x-min")
    parser.add_argument("--xmax", type=float, default=1.5, help="Histogram x-max")
    parser.add_argument("--pt_tol", type=float, default=0.05, help="Relative tolerance for jet_pt_NOSYS")
    parser.add_argument("--etaphisq_tol", type=float, default=0.05, help="Relative tolerance for (eta^2+phi^2)")
    parser.add_argument(
        "--sfs",
        default="weight_ftag_effSF_GN2v01_Continuous_NOSYS",
        help="Comma-separated SF branch names to compare (vector<float>)"
    )
    parser.add_argument("--png_dir", default="plots", help="Directory to save per-SF PNGs (empty to skip)")
    args = parser.parse_args()

    sf_branches = [s.strip() for s in args.sfs.split(",") if s.strip()]
    if not sf_branches:
        print("[ERROR] No SF branches provided.")
        sys.exit(1)

    files1 = find_root_files(args.filepath1)
    files2 = find_root_files(args.filepath2)
    if not files1 or not files2:
        print("[ERROR] One of the input folders has no ROOT files. Abort.")
        sys.exit(1)

    chain1 = build_chain(files1, args.tree)
    chain2 = build_chain(files2, args.tree)
    if chain1.GetEntries() == 0 or chain2.GetEntries() == 0:
        print("[ERROR] One of the chains is empty. Check tree name and files.")
        sys.exit(1)

    print("[INFO] Indexing dataset1...")
    refmap = collect_dataset(chain1, sf_branches)
    print(f"[INFO] Indexed events in dataset1: {len(refmap)}")

    # 为每个 SF 建直方图
    hists = {}
    for sf in sf_branches:
        hname = f"h_ratio__{sanitize_name(sf)}"
        title = f"{sf} ratio (dataset2 / dataset1);ratio;entries"
        h = ROOT.TH1F(hname, title, args.bins, args.xmin, args.xmax)
        h.SetDirectory(0)
        hists[sf] = h

    # —— 新增：所有 SF 乘积的直方图 —— #
    h_all = ROOT.TH1F("h_ratio__ALL_SFs_product",
                      "Product of SFs ratio (dataset2 / dataset1);ratio;entries",
                      args.bins, args.xmin, args.xmax)
    h_all.SetDirectory(0)

    print("[INFO] Scanning dataset2 and filling histograms...")
    stats = compare_and_fill(chain2, refmap, hists, h_all, sf_branches, pt_tol=args.pt_tol, etaphisq_tol=args.etaphisq_tol)

    print("[INFO] Stats:")
    print(f"  - n_evt_total:   {stats['n_evt_total']}")
    print(f"  - n_evt_matched: {stats['n_evt_matched']}")
    print(f"  - n_jet_compared:{stats['n_jet_compared']}")
    for sf in sf_branches:
        print(f"  - filled ({sf}): {stats['n_jet_filled_per_sf'][sf]}")
    print(f"  - filled (ALL_SFs_product): {stats['n_jet_filled_all_product']}")
    print(f"  - n_events_R21: {stats['n_events_R21']}")
    print(f"  - n_events_R22: {stats['n_events_R22']}")
    if stats['n_events_R21'] == 0:
        print(f"  - n_events_R22/R21: N/A")
    else:
        print(f"  - n_events_R22/R21: {stats['n_events_R22'] / stats['n_events_R21']:.4f}")

    # 输出 ROOT + PNG
    of = ROOT.TFile(args.out, "RECREATE")

    save_png = bool(args.png_dir)
    if save_png and not os.path.isdir(args.png_dir):
        os.makedirs(args.png_dir, exist_ok=True)

    def draw_and_save(h, title, png_basename):
        c = ROOT.TCanvas(f"c_{sanitize_name(png_basename)}", title, 900, 650)
        h.SetLineWidth(2)
        h.Draw("HIST")
        ymax = 1.2 * h.GetMaximum()
        if ymax <= 0:
            ymax = 1.0
        h.SetMaximum(ymax)
        line = ROOT.TLine(1.0, 0.0, 1.0, ymax)
        line.SetLineStyle(2)
        line.SetLineColor(1)
        line.Draw()
        c.Write()
        if save_png:
            out_png = os.path.join(args.png_dir, f"{sanitize_name(png_basename)}.png")
            c.SaveAs(out_png)
            print(f"[INFO] Saved: {out_png}")

    # 单独的每个 SF 图
    for sf, h in hists.items():
        h.Write()
        draw_and_save(h, sf, sanitize_name(sf))

    # ALL product 图
    h_all.Write()
    draw_and_save(h_all, "ALL SFs product ratio", "ALL_SFs_product")

    of.Close()
    print(f"[INFO] Wrote histograms & canvases to: {args.out}")

if __name__ == "__main__":
    main()
