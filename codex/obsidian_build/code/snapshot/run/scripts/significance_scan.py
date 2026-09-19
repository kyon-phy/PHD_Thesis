#!/usr/bin/env python3
"""
Scan MET cut bin index and compute significance curves from signal/background ROOT files.
"""

import argparse
import ctypes
import math
import os
import sys

import numpy as np
import ROOT

# 0b SR (met)
RES_HIST_PATH = "met_WVR_1tau0l0b_Res_met_N_minus_1"
NONRES_HIST_PATH = "met_WVR_1tau0l0b_NonRes_met_N_minus_1"

# 0b SR (mT)
# RES_HIST_PATH = "mT_tau_met_WVR_1tau0l0b_Res_mT_N_minus_1"
# NONRES_HIST_PATH = "mT_tau_met_WVR_1tau0l0b_NonRes_mT_N_minus_1"

# 1b SR (met) note: BG hist and sig hist Nbins are differencent! bin width is also different! need to reproduce the background hist if 1b SR scan is needed!
# RES_HIST_PATH = "met_SR_1tau0l1b_Res_met_N_minus_1"
# NONRES_HIST_PATH = "met_SR_1tau0l1b_NonRes_met_N_minus_1;1"

# 1b SR (mT) note: BG hist and sig hist Nbins are differencent! bin width is also different! need to reproduce the background hist if 1b SR scan is needed!
# RES_HIST_PATH = "mT_SR_1tau0l1b_Res_mT_N_minus_1"
# NONRES_HIST_PATH = "mT_SR_1tau0l1b_NonRes_mT_N_minus_1"

NOSYS_DIR = "NOSYS"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan histogram integrals and draw Res/NonRes/combined significance."
    )
    parser.add_argument("--signal", required=True, help="Signal ROOT file path")
    parser.add_argument("--background", required=True, help="Background ROOT file path")
    parser.add_argument(
        "--sys-error",
        type=float,
        default=0.0,
        help="Relative background systematic uncertainty (e.g. 0.2 for 20%%).",
    )
    parser.add_argument(
        "--output",
        default="significance_scan.png",
        help="Output figure path (png/pdf).",
    )
    parser.add_argument(
        "--yield-output",
        default=None,
        help="Output path for S/B yield plot. Default: <output> with '_yields' suffix.",
    )
    parser.add_argument(
        "--ymax",
        type=float,
        default=None,
        help="Optional y-axis maximum.",
    )
    return parser.parse_args()


def get_hist(file_handle, dir_name, hist_name):
    if not file_handle.cd(dir_name):
        raise RuntimeError(f"TDirectory not found or cannot cd: {dir_name}")

    hist = ROOT.gDirectory.Get(hist_name)
    if not hist:
        # raise RuntimeError(f"File: {file_handle.GetName()}, Directory: {dir_name}, Histogram: {hist_name} not found")
        return None
    else:
        hist_clone = hist.Clone(f"{hist.GetName()}_clone")
        hist_clone.SetDirectory(0)
        return hist_clone

def scan_integral_from_bin(hist, nbins_max):
    values = []
    errors = []
    for a in range(0, nbins_max + 1):
        err = ctypes.c_double(0.0)
        val = hist.IntegralAndError(a, nbins_max+1, err)
        values.append(float(val))
        errors.append(float(err.value))
    return values, errors


def get_significance(s_val, b_val, b_stats_error, sys_error):
    """Compute significance Z."""
    if s_val <= 0 or b_val <= 0:
        return 0.0

    n_val = s_val + b_val
    sigma = np.sqrt((b_val * sys_error) ** 2 + b_stats_error**2)

    if sigma <= 0:
        # Fall back to no-uncertainty Asimov significance.
        inner = (1.0 + (s_val / b_val))
        if inner <= 0:
            return 0.0
        z2 = 2.0 * ((s_val + b_val) * np.log(inner) - s_val)
        return float(np.sqrt(max(z2, 0.0)))

    num1 = n_val * (b_val + sigma * sigma)
    den1 = b_val * b_val + n_val * sigma * sigma
    num2 = b_val * b_val + n_val * sigma * sigma
    den2 = b_val * (b_val + sigma * sigma)

    if num1 <= 0 or den1 <= 0 or num2 <= 0 or den2 <= 0:
        return 0.0

    significance_sq = 2.0 * (
        n_val * np.log(num1 / den1)
        - (b_val * b_val / (sigma * sigma)) * np.log(num2 / den2)
    )
    return float(np.sqrt(max(significance_sq, 0.0)))


def build_significance(scan_s, scan_b, scan_b_err, sys_error):
    out = []
    for s_val, b_val, b_err in zip(scan_s, scan_b, scan_b_err):
        out.append(get_significance(s_val, b_val, b_err, sys_error))
    return out


def make_graph(x_vals, y_vals, color, title):
    graph = ROOT.TGraph(len(x_vals))
    for i, (x_val, y_val) in enumerate(zip(x_vals, y_vals)):
        graph.SetPoint(i, float(x_val), float(y_val))
    graph.SetLineColor(color)
    graph.SetLineWidth(3)
    graph.SetTitle(title)
    return graph


def main():
    args = parse_args()
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)

    sig_file = ROOT.TFile.Open(args.signal, "READ")
    if not sig_file or sig_file.IsZombie():
        raise RuntimeError(f"Cannot open signal file: {args.signal}")

    bkg_file = ROOT.TFile.Open(args.background, "READ")
    if not bkg_file or bkg_file.IsZombie():
        raise RuntimeError(f"Cannot open background file: {args.background}")

    try:
        s_res_hist = get_hist(sig_file, NOSYS_DIR, RES_HIST_PATH)
        b_res_hist = get_hist(bkg_file, NOSYS_DIR, RES_HIST_PATH)
        s_nonres_hist = get_hist(sig_file, NOSYS_DIR, NONRES_HIST_PATH)
        b_nonres_hist = get_hist(bkg_file, NOSYS_DIR, NONRES_HIST_PATH)
    finally:
        sig_file.Close()
        bkg_file.Close()

    # Use minimum common bin count for safety if files differ.
    nbins_res = min(s_res_hist.GetNbinsX(), b_res_hist.GetNbinsX())
    nbins_nonres = min(s_nonres_hist.GetNbinsX(), b_nonres_hist.GetNbinsX())
    nbins_scan = min(nbins_res, nbins_nonres)

    if nbins_scan <= 0:
        raise RuntimeError("Invalid histograms: no bins available for scan.")

    # 1) Res scan
    s_res, s_res_err = scan_integral_from_bin(s_res_hist, nbins_scan)
    b_res, b_res_err = scan_integral_from_bin(b_res_hist, nbins_scan)

    # 2) NonRes scan
    s_nonres, s_nonres_err = scan_integral_from_bin(s_nonres_hist, nbins_scan)
    b_nonres, b_nonres_err = scan_integral_from_bin(b_nonres_hist, nbins_scan)

    # 3) Significance curves
    res_significance = build_significance(s_res, b_res, b_res_err, args.sys_error)
    nonres_significance = build_significance(
        s_nonres, b_nonres, b_nonres_err, args.sys_error
    )
    combined_significance = [
        math.sqrt(r_val * r_val + n_val * n_val)
        for r_val, n_val in zip(res_significance, nonres_significance)
    ]

    # x-axis uses(a - 1) * binWidth (GeV), per requested convention.
    bin_width = s_res_hist.GetXaxis().GetBinWidth(1)
    x_vals = [(a_val - 1) * bin_width for a_val in range(0, len(res_significance))]

    graph_res = make_graph(x_vals, res_significance, ROOT.kRed + 1, "Res")
    graph_nonres = make_graph(x_vals, nonres_significance, ROOT.kBlue + 1, "NonRes")
    graph_combined = make_graph(
        x_vals, combined_significance, ROOT.kGreen + 2, "Combined"
    )

    canvas = ROOT.TCanvas("c_significance", "Significance Scan", 900, 700)
    x_max = max(x_vals) if x_vals else 1.0
    if x_max <= 0:
        x_max = bin_width
    frame = canvas.DrawFrame(
        0.0, 0.0, float(x_max), max(combined_significance) * 1.25 + 1e-6
    )
    frame.SetTitle("Significance scan;E_{T}^{miss} [GeV];Z")
    if args.ymax is not None and args.ymax > 0:
        frame.SetMaximum(args.ymax)

    graph_res.Draw("L SAME")
    graph_nonres.Draw("L SAME")
    graph_combined.Draw("L SAME")

    legend = ROOT.TLegend(0.62, 0.72, 0.88, 0.88)
    legend.SetBorderSize(0)
    legend.AddEntry(graph_res, "Res significance", "l")
    legend.AddEntry(graph_nonres, "NonRes significance", "l")
    legend.AddEntry(graph_combined, "Combined significance", "l")
    legend.Draw()

    canvas.SaveAs(args.output)

    # 4) Yield curves: S_Res, B_Res, S_NonRes, B_NonRes
    graph_s_res = make_graph(x_vals, s_res, ROOT.kRed + 1, "S_{Res}")
    graph_b_res = make_graph(x_vals, b_res, ROOT.kBlue + 1, "B_{Res}")
    graph_s_nonres = make_graph(x_vals, s_nonres, ROOT.kMagenta + 2, "S_{NonRes}")
    graph_b_nonres = make_graph(x_vals, b_nonres, ROOT.kOrange + 7, "B_{NonRes}")

    yield_y_max = max(s_res + b_res + s_nonres + b_nonres) if x_vals else 1.0
    if yield_y_max <= 0:
        yield_y_max = 1.0

    canvas_yield = ROOT.TCanvas("c_yields", "Signal/Background Yield Scan", 900, 700)
    frame_yield = canvas_yield.DrawFrame(0.0, 0.0, float(x_max), float(yield_y_max) * 1.25)
    frame_yield.SetTitle("Yield scan;E_{T}^{miss} [GeV];Yield")

    graph_s_res.Draw("L SAME")
    graph_b_res.Draw("L SAME")
    graph_s_nonres.Draw("L SAME")
    graph_b_nonres.Draw("L SAME")

    legend_yield = ROOT.TLegend(0.58, 0.66, 0.88, 0.88)
    legend_yield.SetBorderSize(0)
    legend_yield.AddEntry(graph_s_res, "S_{Res}", "l")
    legend_yield.AddEntry(graph_b_res, "B_{Res}", "l")
    legend_yield.AddEntry(graph_s_nonres, "S_{NonRes}", "l")
    legend_yield.AddEntry(graph_b_nonres, "B_{NonRes}", "l")
    legend_yield.Draw()

    if args.yield_output:
        yield_output = args.yield_output
    else:
        out_base, out_ext = os.path.splitext(args.output)
        out_ext = out_ext if out_ext else ".png"
        yield_output = f"{out_base}_yields{out_ext}"
    canvas_yield.SaveAs(yield_output)

    print("Scan complete.")
    print(f"Output plot: {args.output}")
    print(f"Yield plot: {yield_output}")
    print(f"Points scanned: {len(x_vals)}")
    best_idx = int(np.argmax(combined_significance))
    print(
        "Best combined significance: "
        f"a={best_idx}, E_{{T}}^{{miss}}={x_vals[best_idx]:.4f} GeV, Z={combined_significance[best_idx]:.4f}, "
        f"ResZ={res_significance[best_idx]:.4f}, "
        f"NonResZ={nonres_significance[best_idx]:.4f}, "
        f"CombinedZ={combined_significance[best_idx]:.4f}, "
        f"S_Res={s_res[best_idx]:.4f}, "
        f"B_Res={b_res[best_idx]:.4f}, "
        f"S_NonRes={s_nonres[best_idx]:.4f}, "
        f"B_NonRes={b_nonres[best_idx]:.4f}, "
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
