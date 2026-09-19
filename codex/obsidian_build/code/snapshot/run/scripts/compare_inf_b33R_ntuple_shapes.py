#!/usr/bin/env python3
"""Compare interference shapes: 567627 (b33R=0) vs 567634 (b33R=-1).

Fill MET (and related) from reco ntuples with Xsec/sumW normalisation,
then unit-normalise to quantify shape differences.
"""
from __future__ import annotations

import os
import re
from collections import defaultdict

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(False)
ROOT.EnableImplicitMT(4)

FILELIST = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/input/filelist_v05.txt"
SUMW = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/input/sum_of_weights_v05.txt"
PLOTDIR = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots_inf_b33R_shape"

XSEC = {
    567627: -0.0019154,  # b33R=0
    567634: -0.0019185,  # b33R=-1
}
LABEL = {567627: "b33R=0 (567627)", 567634: "b33R=-1 (567634)"}

# weight variations to compare
WEIGHTS = [
    ("NOSYS", "weight_mc_corrected_NOSYS", None),  # generator nominal
    ("gU1_5_23L0_2", "weight_mc_corrected_GEN_gU1_5_23L0_2", "GEN_gU1_5_23L0_2"),
    ("gU1_0_23L0_2", "weight_mc_corrected_GEN_gU1_0_23L0_2", "GEN_gU1_0_23L0_2"),
    ("gU2_5_23L1_0", "weight_mc_corrected_GEN_gU2_5_23L1_0", "GEN_gU2_5_23L1_0"),
]

# observables: (name, expr, nbins, xmin, xmax)
# tau leading pt: use first element if present else -1
OBSERVABLES = [
    ("MET", "MET_wpSet0_met_NOSYS/1000.", 40, 0, 2000),
    ("tau0_pt", "tau_pt_NOSYS.size()>0 ? tau_pt_NOSYS[0]/1000. : -1", 40, 0, 1000),
]


def load_files(dsid: int):
    files = []
    with open(FILELIST) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 4 and parts[0] == str(dsid):
                files.append(parts[-1])
    return files


def load_sumw(dsid: int, weight_name: str | None):
    """Sum of weights across campaigns. For NOSYS use GEN_MUR10_MUF10_PDF260800."""
    key = weight_name if weight_name else "GEN_MUR10_MUF10_PDF260800"
    total = 0.0
    with open(SUMW) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 5:
                continue
            if parts[0] == str(dsid) and parts[3] == key:
                total += float(parts[4])
    return total


def fill_hist(dsid: int, weight_branch: str, sumw_key: str | None, obs):
    files = load_files(dsid)
    if not files:
        raise RuntimeError(f"no files for {dsid}")
    sumw = load_sumw(dsid, sumw_key)
    xsec = XSEC[dsid]
    scale = xsec / sumw if abs(sumw) > 0 else 0.0

    name, expr, nb, xmin, xmax = obs
    chain = ROOT.TChain("reco")
    for p in files:
        # prefer local afs path from filelist; skip missing
        if os.path.exists(p):
            chain.Add(p)
        else:
            # try without root:// prefix variants already local in v05
            print(f"WARN missing {p}")
    if chain.GetEntries() == 0:
        raise RuntimeError(f"empty chain for {dsid}")

    df = ROOT.RDataFrame(chain)
    # inclusive + pass_all preselection variant
    h_all = (
        df.Define("obs", expr)
        .Define("w", f"({weight_branch})*({scale})")
        .Filter("obs >= 0")
        .Histo1D((f"h_{dsid}_{name}_all", f"{name};{name};xsec-norm yield", nb, xmin, xmax), "obs", "w")
    )
    h_pass = (
        df.Define("obs", expr)
        .Define("w", f"({weight_branch})*({scale})")
        .Filter("obs >= 0 && pass_all_wpSet0_NOSYS")
        .Histo1D((f"h_{dsid}_{name}_pass", f"{name};{name};xsec-norm yield", nb, xmin, xmax), "obs", "w")
    )
    # force event loop once
    h_all.GetEntries()
    return h_all.GetValue().Clone(), h_pass.GetValue().Clone(), scale, sumw, chain.GetEntries()


def metrics(h0, h1):
    y0 = h0.Integral(0, h0.GetNbinsX() + 1)
    y1 = h1.Integral(0, h1.GetNbinsX() + 1)
    s0, s1 = h0.Clone("s0"), h1.Clone("s1")
    if abs(y0) > 0:
        s0.Scale(1.0 / y0)
    if abs(y1) > 0:
        s1.Scale(1.0 / y1)
    nb = s0.GetNbinsX()
    l1 = 0.0
    max_abs = 0.0
    # mean |a-b| / mean(|a|+|b|)/2  relative
    for i in range(1, nb + 1):
        a, b = s0.GetBinContent(i), s1.GetBinContent(i)
        d = abs(a - b)
        l1 += d
        max_abs = max(max_abs, d)
    tv = 0.5 * l1

    # KS on absolute PDFs
    a0, a1 = s0.Clone("a0"), s1.Clone("a1")
    for i in range(0, nb + 2):
        a0.SetBinContent(i, abs(a0.GetBinContent(i)))
        a1.SetBinContent(i, abs(a1.GetBinContent(i)))
    if a0.Integral() > 0:
        a0.Scale(1.0 / a0.Integral())
    if a1.Integral() > 0:
        a1.Scale(1.0 / a1.Integral())
    ks = a0.KolmogorovTest(a1, "M") if a0.Integral() > 0 and a1.Integral() > 0 else float("nan")
    return {
        "y0": y0,
        "y1": y1,
        "yratio": y1 / y0 if abs(y0) > 0 else float("nan"),
        "tv": tv,
        "max_abs": max_abs,
        "ks": ks,
        "s0": s0,
        "s1": s1,
    }


def plot(name, sel, wlabel, m, outdir):
    s0, s1 = m["s0"], m["s1"]
    s0.SetLineColor(ROOT.kBlue + 1)
    s1.SetLineColor(ROOT.kRed + 1)
    s0.SetLineWidth(2)
    s1.SetLineWidth(2)
    s0.SetTitle(f"Interference {name} [{sel}] {wlabel};{name};unit norm")
    c = ROOT.TCanvas("c", "c", 800, 700)
    c.Divide(1, 2)
    p1 = c.cd(1)
    p1.SetPad(0, 0.32, 1, 1)
    p1.SetBottomMargin(0.02)
    ymax = max(s0.GetMaximum(), s1.GetMaximum()) * 1.3
    s0.SetMaximum(ymax)
    s0.Draw("hist")
    s1.Draw("hist same")
    leg = ROOT.TLegend(0.50, 0.62, 0.88, 0.88)
    leg.AddEntry(s0, f"{LABEL[567627]}  Y={m['y0']:.3g}", "l")
    leg.AddEntry(s1, f"{LABEL[567634]} Y={m['y1']:.3g}", "l")
    leg.SetBorderSize(0)
    leg.Draw()
    txt = ROOT.TLatex()
    txt.SetNDC()
    txt.SetTextSize(0.04)
    txt.DrawLatex(0.15, 0.85, f"TV={m['tv']:.4f}  KS={m['ks']:.4f}  Y(-1)/Y(0)={m['yratio']:.3f}")
    p2 = c.cd(2)
    p2.SetPad(0, 0, 1, 0.32)
    p2.SetTopMargin(0.03)
    p2.SetBottomMargin(0.3)
    # ratio of unit-norm shapes (careful with zeros)
    r = s1.Clone("r")
    r.Divide(s0)
    r.SetTitle(f";{name};(-1)/0")
    r.GetYaxis().SetRangeUser(0.5, 1.5)
    r.GetYaxis().SetTitleSize(0.1)
    r.GetYaxis().SetLabelSize(0.1)
    r.GetXaxis().SetTitleSize(0.12)
    r.GetXaxis().SetLabelSize(0.1)
    r.Draw("hist")
    line = ROOT.TLine(r.GetXaxis().GetXmin(), 1, r.GetXaxis().GetXmax(), 1)
    line.SetLineStyle(2)
    line.Draw()
    os.makedirs(outdir, exist_ok=True)
    c.SaveAs(os.path.join(outdir, f"inf_{name}_{sel}_{wlabel}.pdf"))
    c.Close()


def main():
    print(f"Xsec 567627={XSEC[567627]}, 567634={XSEC[567634]}, ratio={XSEC[567634]/XSEC[567627]:.6f}")
    for dsid in (567627, 567634):
        files = load_files(dsid)
        print(f"DSID {dsid}: {len(files)} files")

    results = []
    for wlabel, wbranch, sumw_key in WEIGHTS:
        print(f"\n===== weight {wlabel} =====")
        for obs in OBSERVABLES:
            name = obs[0]
            h0_all, h0_pass, sc0, sw0, n0 = fill_hist(567627, wbranch, sumw_key, obs)
            h1_all, h1_pass, sc1, sw1, n1 = fill_hist(567634, wbranch, sumw_key, obs)
            print(f"  {name}: Nevt {n0}/{n1}, sumW {sw0:.4g}/{sw1:.4g}, scale {sc0:.4g}/{sc1:.4g}")
            for sel, ha, hb in (("inclusive", h0_all, h1_all), ("pass_all", h0_pass, h1_pass)):
                m = metrics(ha, hb)
                results.append({"w": wlabel, "obs": name, "sel": sel, **m})
                print(
                    f"    [{sel:10s}] yield0={m['y0']:.4g} yield1={m['y1']:.4g} "
                    f"ratio={m['yratio']:.4f}  TV={m['tv']:.4f}  KS={m['ks']:.4f}"
                )
                plot(name, sel, wlabel, m, PLOTDIR)

    print("\n=== VERDICT (unit-normalised shapes) ===")
    for sel in ("inclusive", "pass_all"):
        sub = [r for r in results if r["sel"] == sel and r["obs"] == "MET"]
        if not sub:
            continue
        mean_tv = sum(r["tv"] for r in sub) / len(sub)
        mean_yr = sum(r["yratio"] for r in sub) / len(sub)
        print(f"MET {sel}: mean TV={mean_tv:.4f}, mean yield ratio={mean_yr:.4f} over {len(sub)} weights")
        if mean_tv < 0.02:
            verdict = "NEGLIGIBLE"
        elif mean_tv < 0.05:
            verdict = "SMALL"
        elif mean_tv < 0.10:
            verdict = "MODERATE"
        else:
            verdict = "LARGE"
        print(f"  -> shape change: {verdict}")
    print(f"Plots: {PLOTDIR}")


if __name__ == "__main__":
    main()
