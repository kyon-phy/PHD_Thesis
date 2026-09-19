#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import re
import sys
from array import array
import numpy as np

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# ========== 1) Parse sample directory names ==========
# Expected directory name format example:
#   *MU1500_gU1_5_23L0_2_alldecay_corrected
#   -> MU=1500, gU=1.5, beta=0.2


def parse_params_from_filename(filename, mass_point="1500"):
    """Extract MU, gU, beta from directory name"""
    RE_NAME = re.compile(
        # f".*MU{mass_point}_gU(?P<gUa>\d+)_(?P<gUb>\d+).*?23L(?P<betaA>\d+)_(?P<betaB>\d+).*?b33Rm1_0_noWeights_(?P<tag>[^.]+)",
        f".*MU{mass_point}_gU(?P<gUa>\d+)_(?P<gUb>\d+).*?23L(?P<betaA>\d+)_(?P<betaB>\d+).*?_noWeights_(?P<tag>[^.]+)",
        re.IGNORECASE,
    )
    m = RE_NAME.match(filename)
    if not m:
        return None
    gU = float(f"{int(m.group('gUa'))}.{int(m.group('gUb'))}")
    beta = float(f"{int(m.group('betaA'))}.{int(m.group('betaB'))}")
    tag = m.group("tag")
    # print(f"filename: {filename}, gU: {gU}, beta: {beta}, tag: {tag}")
    return (gU, beta, tag)

def get_histname(tag, SR_type):
    if "_Res" in tag and SR_type == "1b":
        histname = "met_SR_1tau0l1b_sch"
    elif "_NonRes" in tag and SR_type == "1b":
        histname = "met_SR_1tau0l1b_tch"
    elif "_Res" in tag and SR_type == "0b":
        histname = "met_WVR_1tau0l0b_sch"
    elif "_NonRes" in tag and SR_type == "0b":
        histname = "met_WVR_1tau0l0b_tch"
    else:
        print(f"[Error] Cannot find the histgram with the tag {tag}")
        return None
    return histname

# ========== 2) Read ROOT file and extract significance ==========
def read_yields(root_file_path, tag, SR_type, include_under_overflow=True):
    if not os.path.isfile(root_file_path):
        return None

    f = ROOT.TFile.Open(root_file_path, "READ")
    if not f or f.IsZombie():
        return None
    
    # read yields from histgram
    histname = get_histname(tag, SR_type)
    # print(f"file_path: {root_file_path}, histname: {histname}, tag: {tag}, SR_type: {SR_type}")
    h = f.Get(f"NOSYS/{histname}")
    Nbins = h.GetNbinsX()
    err = array('d', [0.0])
    yields = None
    if include_under_overflow:
        yields = h.IntegralAndError(0, Nbins+1, err)
    else:
        yields = h.IntegralAndError(1, Nbins, err)
    
    f.Close()
    return yields, err[0]

# ========== 3) Collect significance map ==========
def scan_input_dir(input_dir, SR_type, mass_point="1500", include_under_overflow=True):
    """
    Iterate over all files of input_dir,
    parse MU, gU, beta and extract significance.
    Returns dict: {(MU, gU, beta): Z}
    """
    zmap = {}
    for name in os.listdir(input_dir):
        full_path = os.path.join(input_dir, name)
        if not os.path.isfile(full_path):
            continue
        params = parse_params_from_filename(name, mass_point=mass_point)
        if not params:
            continue
        (gU, beta, tag) = params
        yields_and_error = read_yields(full_path, tag, SR_type, include_under_overflow=include_under_overflow)
        if yields_and_error is None:
            print(f"[WARN] yields and error missing for: {name}")
            continue
        zmap[(gU, beta, tag)] = yields_and_error
        if gU == 1.0 and beta == 0.2:
            print(f"full_path: {full_path}")
            print(f"mass={mass_point}, gU={gU}, beta={beta}, tag={tag} --> yields_and_error={yields_and_error}")
    return zmap

# ========== 4) Draw significance vs gU-beta for fixed MU ==========
# functions to generate the bin edges for limit plot
def generate_edges_with_E0(bin_center, E0):
    # calcualte the bin edges based on the center value of bin and the first bin edge E0
    N = len(bin_center)
    # set the first bin edge
    edges = [round(E0, 4)]
    # set the middle bin edges
    for i in range(N):
        Ei = edges[i]
        E_next = 2 * bin_center[i] - Ei
        # 精确到三位有效数字
        edges.append(round(E_next, 4))
    return array('d', edges)

def is_strictly_increasing(lst):
    """判断列表 lst 的值是否严格单调递增"""
    return all(x < y for x, y in zip(lst, lst[1:]))

def get_bin_edges(centers, n_steps=10):
    """
    在区间 (2*c0-c1, c0) 内迭代搜索一个合适的 E0，
    使得生成的边界序列严格单调递增。
    
    参数:
      centers : list
         按升序排列的 bin 中心值数组
      n_steps : int
         网格搜索的步数
    返回:
      (E0, edges) : 成功找到的 E0 与对应的边界数组
    """
    c0, c1 = centers[0], centers[1]
    E0_low = 2*c0 - c1  # 下界
    E0_high = c0       # 上界
    for i in range(n_steps + 1):
        candidate_E0 = E0_low + i * (E0_high - E0_low) / n_steps
        edges = generate_edges_with_E0(centers, candidate_E0)
        if is_strictly_increasing(edges) and candidate_E0 > -0.5:
            print("Center: ", centers, " find the feasible E0 with step size: ", n_steps, " -> E0: ", candidate_E0, " edges: ", edges)
            return edges
    raise ValueError(f"cannot find the feasible E0 with step size: {n_steps} and centers: {centers}")


def load_mu_contour_graph(contour_root_path, mass_point):
    """Load expected mu contour graph for a given mass point from external ROOT file."""
    f = ROOT.TFile.Open(contour_root_path, "READ")
    if not f or f.IsZombie():
        print(f"[WARN] failed to open contour file: {contour_root_path}")
        return None

    graph_name = f"g_exp_mu_{mass_point}"
    g_src = f.Get(graph_name)

    if not g_src or not isinstance(g_src, ROOT.TGraph):
        print(f"[WARN] cannot find TGraph for mass point {mass_point} in {contour_root_path}")
        f.Close()
        return None

    g = g_src.Clone(f"g_overlay_mu_{mass_point}")
    g.SetDirectory(0) if hasattr(g, "SetDirectory") else None
    f.Close()
    return g


# ========== 5) Draw interference fraction with BSM-only yields ==========
def draw_inf_fraction(
    zmap,
    outdir,
    output_file,
    mass_point="1500",
    SR_type="1b",
    num_tag="inf_Res",
    den_tag="bsm_Res",
    contour_root_path=None,
):
    gus = sorted({k[0] for k in zmap})
    betas = sorted({k[1] for k in zmap})
    tag = {k[1] for k in zmap}
    if len(gus) < 2:
        print(f"[WARNING] only one gU point found: {gus[0]}")
        gu_bin_edges = [gus[0], gus[0] + 0.01]
    else:
        gu_bin_edges = get_bin_edges(gus, n_steps=2)
    if len(betas) < 2:
        print(f"[WARNING] only one beta point found: {betas[0]}")
        beta_bin_edges = [betas[0], betas[0] + 0.01]
    else:
        beta_bin_edges = get_bin_edges(betas, n_steps=2)
    hist_name = f"MU{mass_point}_SR{SR_type}_h_interference_fraction_{num_tag}_over_{den_tag}"

    if "_Res" in den_tag:
        region = "Res"
    elif "_NonRes" in den_tag:
        region = "NonRes"
    else:
        region = None

    # Draw interference yield fraction
    # h2 = ROOT.TH2D(hist_name, f"{region} N_{{Interference}}/N_{{BSM}};g_{{U}};#beta_{{L}}^{{23}};",
    if len(gus) >= 2 and len(betas) >= 2:
        h2 = ROOT.TH2D(hist_name, f";g_{{U}};#beta_{{L}}^{{23}};",
                       len(gu_bin_edges) - 1, gu_bin_edges,
                       len(beta_bin_edges) - 1, beta_bin_edges)
    else:
        # creat a dummy histogram 
        xbins = array('d', [0.0, 0.5, 1.0])
        ybins = array('d', [0.0, 0.1, 0.2])
        h2 = ROOT.TH2D(hist_name, f";g_{{U}};#beta_{{L}}^{{23}};", 2, xbins, 2, ybins)
        
    h2.Sumw2()
    tiny = 1e-300  # 防止除零的小数
    pairs_done = 0
    missing = 0
    zero_den = 0

    for gu in gus:
        for be in betas:
            A = zmap.get((gu, be, num_tag), None)  # (yield, err)
            B = zmap.get((gu, be, den_tag), None)

            if (A is None) or (B is None):
                missing += 1
                continue

            Ay, Aerr = float(A[0]), float(A[1])
            By, Berr = float(B[0]), float(B[1])

            if abs(By) < tiny:
                zero_den += 1
                continue

            R = Ay / By
            # 误差传播（若 Ay==0 则第一项视作 0）
            termA = 0.0 if abs(Ay) < tiny else (Aerr / Ay)**2
            termB = (Berr / By)**2
            Rerr = abs(R) * (termA + termB)**0.5

            # 4) 放进对应 bin
            ix = h2.GetXaxis().FindBin(gu)
            iy = h2.GetYaxis().FindBin(be)
            h2.SetBinContent(ix, iy, R)
            h2.SetBinError(ix, iy, Rerr)
            pairs_done += 1
            
            # print the yield and the ratio for specific gU and beta points
            if gu == 1.0 and be == 0.2:
                print(f"mass={mass_point}, gU={gu}, beta={be}, tag={num_tag} --> yields: {A}, error: {Aerr}")
                print(f"mass={mass_point}, gU={gu}, beta={be}, tag={den_tag} --> yields: {B}, error: {Berr}")
                print(f"mass={mass_point}, gU={gu}, beta={be}, tag={num_tag} over {den_tag} --> ratio: {R}, error: {Rerr}")

    print(f"[INFO] ratio points filled: {pairs_done}, missing pairs: {missing}, zero denominator: {zero_den}")

    # Draw the hist on canvas 
    c = ROOT.TCanvas(f"c_{hist_name}", "", 900, 750)
    h2.SetContour(50)
    # scale to 100%
    h2.Scale(100.0)
    ROOT.gStyle.SetPaintTextFormat(".2f%%")
    # draw the text
    h2.Draw("COLZ TEXT")  # TEXT 可显示数值；不想显示可改为 "COLZ"

    g_mu = load_mu_contour_graph(contour_root_path, mass_point)
    if g_mu:
        g_mu.SetLineColor(ROOT.kRed)
        g_mu.SetLineWidth(3)
        g_mu.SetLineStyle(1)
        g_mu.Draw("L SAME")

    # draw the legend and latex
    lat = ROOT.TLatex(); lat.SetNDC(True); lat.SetTextSize(0.045)
    lat.DrawLatex(0.6, 0.85, f"#it{{ATLAS}} #bf{{Internal}}")
    lat2 = ROOT.TLatex(); lat2.SetNDC(True); lat2.SetTextSize(0.04)
    lat2.DrawLatex(0.6, 0.8, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
    lat3 = ROOT.TLatex(); lat3.SetNDC(True); lat3.SetTextSize(0.04)
    lat3.DrawLatex(0.6, 0.75, f"#bf{{M_{{U}} = {mass_point} GeV}}")
    lat4 = ROOT.TLatex(); lat4.SetNDC(True); lat4.SetTextSize(0.04)
    lat4.DrawLatex(0.6, 0.7, f"#bf{{SR{SR_type}-{region}}}")
    lat5 = ROOT.TLatex(); lat5.SetNDC(True); lat5.SetTextSize(0.04)
    lat5.DrawLatex(0.6, 0.65, f"#bf{{1b + 0b exp.}}")
    lat6 = ROOT.TLatex(); lat6.SetNDC(True); lat6.SetTextSize(0.04)
    lat6.DrawLatex(0.6, 0.6, f"#bf{{Interference/BSM}}")

    c.Update()

    os.makedirs(outdir, exist_ok=True)
    output_file.cd()
    h2.Write()
    c.Write()
    c.SaveAs(os.path.join(outdir, f"{hist_name}.pdf"))


# ========== main ==========
def main():
    # add the argument to include under overflow
    parser = argparse.ArgumentParser()
    parser.add_argument("--include_under_overflow", action="store_true", default=True)
    parser.add_argument("--input_dir", type=str, default=None)
    parser.add_argument("--out_dir", type=str, default="plots")
    parser.add_argument("--SR_type", type=str, default="1b")
    parser.add_argument("--mass_point", type=str, default="1500")
    parser.add_argument(
        "--mu_contour_file",
        type=str,
        default="plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp/output_mu_contours.root",
    )
    args = parser.parse_args()
    include_under_overflow = args.include_under_overflow
    input_dir = args.input_dir
    out_dir = args.out_dir
    SR_type = args.SR_type
    mass_point = args.mass_point
    mu_contour_file = args.mu_contour_file
    

    zmap = scan_input_dir(input_dir, SR_type, mass_point=mass_point, include_under_overflow=include_under_overflow)
    if not zmap:
        print("[ERROR] No valid samples found. Check folder names and files.")
        sys.exit(2)

    print(f"[INFO] Collected {len(zmap)} points:")
    for k, v in sorted(zmap.items()):
        if "combined" in k[2]:
            continue
        print(f"mass={mass_point}, gU={k[0]:>4}  beta={k[1]:>4} tag={k[2]:>4} --> yields: {v[0]}, error: {v[1]}")

    # # create output file
    output_file = ROOT.TFile("plots/output_yields.root", "RECREATE")
    draw_inf_fraction(
        zmap,
        out_dir,
        output_file,
        mass_point=mass_point,
        SR_type=SR_type,
        num_tag="inf_NonRes",
        den_tag="bsm_NonRes",
        contour_root_path=mu_contour_file,
    )
    draw_inf_fraction(
        zmap,
        out_dir,
        output_file,
        mass_point=mass_point,
        SR_type=SR_type,
        num_tag="inf_Res",
        den_tag="bsm_Res",
        contour_root_path=mu_contour_file,
    )

if __name__ == "__main__":
    main()
