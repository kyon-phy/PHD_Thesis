#!/usr/bin/env python3
"""Compare interference shapes: DSID 567627 (b33R=0) vs 567634 (b33R=-1).

Uses existing FastFrames histos (already include xsec/sumW weights).
Reports yield ratio and unit-normalized shape differences.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(False)

OUT = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04"
PLOTDIR = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots_inf_b33R_shape"
# PMG xsec (pb), signed for interference
XSEC = {
    "b33R0": -0.0019154,   # 567627
    "b33Rm1": -0.0019185,  # 567634
}

VARS = [
    "met_SR_1tau0l1b_sch",
    "met_WCR_0tau1l0b_sch",
    "met_topCR_1tau1l_sch",
    "met_WVR_1tau0l0b_sch",
    "met_topVR_1tau0l2b_sch",
]


def list_common():
    old, new = set(), set()
    for fn in os.listdir(OUT):
        if not fn.endswith(".root"):
            continue
        if "b33Rm1_0_alldecay_corrected_inf_" in fn:
            m = re.match(
                r"(MU1500_gU.+?)_b33Rm1_0_alldecay_corrected_inf_(Res|NonRes)\.root", fn
            )
            if m:
                new.add((m.group(1), m.group(2)))
        elif "b33Rm1" not in fn and re.match(
            r"MU1500_gU.+_alldecay_corrected_(Res|NonRes)_Inf\.root", fn
        ):
            m = re.match(
                r"(MU1500_gU.+?)_alldecay_corrected_(Res|NonRes)_Inf\.root", fn
            )
            if m:
                old.add((m.group(1), m.group(2)))
    return sorted(old & new)


def paths(tag, ch):
    # b33R=0 (567627): MU1500_*_alldecay_corrected_{Res,NonRes}_Inf.root
    # b33R=-1 (567634): MU1500_*_b33Rm1_0_alldecay_corrected_inf_{Res,NonRes}.root
    p0 = os.path.join(OUT, f"{tag}_alldecay_corrected_{ch}_Inf.root")
    pm1 = os.path.join(OUT, f"{tag}_b33Rm1_0_alldecay_corrected_inf_{ch}.root")
    return p0, pm1


def get_hist(path, var):
    f = ROOT.TFile.Open(path)
    if not f or f.IsZombie():
        return None
    h = f.Get(f"NOSYS/{var}")
    if not h:
        f.Close()
        return None
    h = h.Clone()
    h.SetDirectory(0)
    f.Close()
    return h


def shape_metrics(h0, h1):
    """Unit-normalize signed hists; return dict of shape/rate metrics."""
    y0 = h0.Integral(0, h0.GetNbinsX() + 1)
    y1 = h1.Integral(0, h1.GetNbinsX() + 1)
    nb = h0.GetNbinsX()
    s0 = h0.Clone("s0")
    s1 = h1.Clone("s1")
    if abs(y0) > 0:
        s0.Scale(1.0 / y0)
    if abs(y1) > 0:
        s1.Scale(1.0 / y1)

    # absolute shape difference (L1 / 2 -> [0,1] for positive PDFs; here signed)
    l1 = 0.0
    max_abs = 0.0
    max_rel = 0.0
    chi2 = 0.0
    ndof = 0
    for i in range(1, nb + 1):
        a = s0.GetBinContent(i)
        b = s1.GetBinContent(i)
        ea = s0.GetBinError(i)
        eb = s1.GetBinError(i)
        d = abs(a - b)
        l1 += d
        if d > max_abs:
            max_abs = d
        denom = max(abs(a), abs(b), 1e-12)
        rel = d / denom
        if rel > max_rel and denom > 1e-6:
            max_rel = rel
        var = ea * ea + eb * eb
        if var > 0 and (abs(a) > 1e-8 or abs(b) > 1e-8):
            chi2 += (a - b) ** 2 / var
            ndof += 1

    # KS on absolute-content clones (ROOT KS assumes non-negative)
    a0 = s0.Clone("a0")
    a1 = s1.Clone("a1")
    for i in range(0, nb + 2):
        a0.SetBinContent(i, abs(a0.GetBinContent(i)))
        a1.SetBinContent(i, abs(a1.GetBinContent(i)))
    if a0.Integral() > 0:
        a0.Scale(1.0 / a0.Integral())
    if a1.Integral() > 0:
        a1.Scale(1.0 / a1.Integral())
    ks = a0.KolmogorovTest(a1)  # probability
    ks_dist = a0.KolmogorovTest(a1, "M")  # max distance

    return {
        "yield0": y0,
        "yield1": y1,
        "yield_ratio": (y1 / y0) if abs(y0) > 0 else float("nan"),
        "l1_half": 0.5 * l1,  # ~ total-variation distance for PDFs
        "max_abs_bin": max_abs,
        "max_rel_bin": max_rel,
        "chi2_ndof": (chi2 / ndof) if ndof else float("nan"),
        "ndof": ndof,
        "ks_prob": ks,
        "ks_dist": ks_dist,
        "s0": s0,
        "s1": s1,
    }


def make_plot(tag, ch, var, m, outdir):
    s0, s1 = m["s0"], m["s1"]
    s0.SetLineColor(ROOT.kBlue + 1)
    s1.SetLineColor(ROOT.kRed + 1)
    s0.SetLineWidth(2)
    s1.SetLineWidth(2)
    s0.SetTitle(f"{tag} {ch} | {var};{var};unit-norm yield")
    c = ROOT.TCanvas("c", "c", 800, 700)
    c.Divide(1, 2)
    p1 = c.cd(1)
    p1.SetPad(0, 0.32, 1, 1)
    p1.SetBottomMargin(0.02)
    p1.SetLogy(False)
    s0.Draw("hist")
    s1.Draw("hist same")
    leg = ROOT.TLegend(0.55, 0.65, 0.88, 0.88)
    leg.AddEntry(s0, f"b33R=0 (567627)  N={m['yield0']:.3g}", "l")
    leg.AddEntry(s1, f"b33R=-1 (567634) N={m['yield1']:.3g}", "l")
    leg.Draw()
    p2 = c.cd(2)
    p2.SetPad(0, 0, 1, 0.32)
    p2.SetTopMargin(0.03)
    p2.SetBottomMargin(0.3)
    ratio = s1.Clone("ratio")
    ratio.Divide(s0)
    ratio.SetTitle(f";{var};(-1)/0")
    ratio.GetYaxis().SetRangeUser(0.5, 1.5)
    ratio.GetYaxis().SetTitleSize(0.1)
    ratio.GetYaxis().SetLabelSize(0.1)
    ratio.GetXaxis().SetTitleSize(0.12)
    ratio.GetXaxis().SetLabelSize(0.1)
    ratio.Draw("hist")
    line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1)
    line.SetLineStyle(2)
    line.Draw()
    os.makedirs(outdir, exist_ok=True)
    safe = f"{tag}_{ch}_{var}".replace("/", "_")
    c.SaveAs(os.path.join(outdir, f"{safe}.pdf"))
    c.Close()


def main():
    common = list_common()
    print(f"Common coupling points: {len(common)}")
    print(
        f"Xsec 567627 (b33R=0) = {XSEC['b33R0']}, "
        f"567634 (b33R=-1) = {XSEC['b33Rm1']}, "
        f"ratio = {XSEC['b33Rm1']/XSEC['b33R0']:.6f}"
    )

    # aggregate by channel and variable
    rows = []
    for tag, ch in common:
        p0, pm1 = paths(tag, ch)
        if not (os.path.exists(p0) and os.path.exists(pm1)):
            continue
        for var in VARS:
            # NonRes files use tch region names
            if ch == "NonRes":
                var_use = var.replace("_sch", "_tch")
            else:
                var_use = var
            h0 = get_hist(p0, var_use)
            h1 = get_hist(pm1, var_use)
            if h0 is None or h1 is None:
                # try original name
                h0 = get_hist(p0, var)
                h1 = get_hist(pm1, var)
            if h0 is None or h1 is None:
                continue
            if h0.GetNbinsX() != h1.GetNbinsX():
                continue
            m = shape_metrics(h0, h1)
            rows.append({"tag": tag, "ch": ch, "var": var_use, **m})

    if not rows:
        print("No comparable histograms found.")
        sys.exit(1)

    # summary for SR met only (main signal region)
    sr = [r for r in rows if "met_SR_1tau0l1b" in r["var"]]
    print(f"\n=== SR met comparisons: {len(sr)} ===")

    def summarize(subset, label):
        if not subset:
            print(f"{label}: empty")
            return
        yrs = [r["yield_ratio"] for r in subset]
        tvs = [r["l1_half"] for r in subset]
        kds = [r["ks_dist"] for r in subset]
        chi = [r["chi2_ndof"] for r in subset if r["chi2_ndof"] == r["chi2_ndof"]]
        print(f"\n{label} (N={len(subset)}):")
        print(
            f"  yield_ratio (-1/0):  mean={sum(yrs)/len(yrs):.4f}  "
            f"min={min(yrs):.4f}  max={max(yrs):.4f}"
        )
        print(
            f"  TV distance (0.5*L1): mean={sum(tvs)/len(tvs):.4f}  "
            f"min={min(tvs):.4f}  max={max(tvs):.4f}"
            f"   (0=identical shape, 1=no overlap)"
        )
        print(
            f"  KS distance:         mean={sum(kds)/len(kds):.4f}  "
            f"min={min(kds):.4f}  max={max(kds):.4f}"
        )
        if chi:
            print(
                f"  chi2/ndof (shape):   mean={sum(chi)/len(chi):.3f}  "
                f"min={min(chi):.3f}  max={max(chi):.3f}"
            )
        # worst shapes
        worst = sorted(subset, key=lambda r: -r["l1_half"])[:5]
        print("  worst TV shapes:")
        for r in worst:
            print(
                f"    {r['tag']:40s} {r['ch']:6s}  TV={r['l1_half']:.4f}  "
                f"Yratio={r['yield_ratio']:.4f}  KS={r['ks_dist']:.4f}"
            )
        best = sorted(subset, key=lambda r: r["l1_half"])[:3]
        print("  best TV shapes:")
        for r in best:
            print(
                f"    {r['tag']:40s} {r['ch']:6s}  TV={r['l1_half']:.4f}  "
                f"Yratio={r['yield_ratio']:.4f}"
            )

    summarize(sr, "SR met (all common points)")
    summarize([r for r in sr if r["ch"] == "Res"], "SR met Res only")
    summarize([r for r in sr if r["ch"] == "NonRes"], "SR met NonRes only")

    # also all regions summary
    by_var = defaultdict(list)
    for r in rows:
        by_var[r["var"].replace("_tch", "_sch")].append(r)
    print("\n=== mean TV distance by region (unit-norm shape) ===")
    for var, rs in sorted(by_var.items()):
        tvs = [r["l1_half"] for r in rs]
        yrs = [r["yield_ratio"] for r in rs]
        print(
            f"  {var:30s}  TV_mean={sum(tvs)/len(tvs):.4f}  "
            f"Yratio_mean={sum(yrs)/len(yrs):.4f}  N={len(rs)}"
        )

    # representative plots: median / worst / a few couplings
    os.makedirs(PLOTDIR, exist_ok=True)
    sr_sorted = sorted(sr, key=lambda r: r["l1_half"])
    to_plot = []
    if sr_sorted:
        to_plot.append(sr_sorted[len(sr_sorted) // 2])  # median
        to_plot.append(sr_sorted[-1])  # worst
        to_plot.append(sr_sorted[0])  # best
    # also pick gU1_5_23L0_2 Res/NonRes if present
    for want in [
        ("MU1500_gU1_5_23L0_2", "Res"),
        ("MU1500_gU1_5_23L0_2", "NonRes"),
        ("MU1500_gU1_0_23L0_2", "Res"),
    ]:
        for r in sr:
            if (r["tag"], r["ch"]) == want:
                to_plot.append(r)
    seen = set()
    for r in to_plot:
        key = (r["tag"], r["ch"], r["var"])
        if key in seen:
            continue
        seen.add(key)
        make_plot(r["tag"], r["ch"], r["var"], r, PLOTDIR)
        print(f"plot: {r['tag']} {r['ch']} TV={r['l1_half']:.4f}")

    # overall verdict
    mean_tv = sum(r["l1_half"] for r in sr) / len(sr)
    mean_yr = sum(r["yield_ratio"] for r in sr) / len(sr)
    print("\n=== VERDICT ===")
    print(f"Xsec ratio (b33R=-1 / b33R=0) = {XSEC['b33Rm1']/XSEC['b33R0']:.6f} (~identical)")
    print(f"SR yield ratio mean = {mean_yr:.4f}")
    print(f"SR shape TV distance mean = {mean_tv:.4f}")
    if mean_tv < 0.02:
        print("Shape change: NEGLIGIBLE (<2% TV)")
    elif mean_tv < 0.05:
        print("Shape change: SMALL (<5% TV)")
    elif mean_tv < 0.10:
        print("Shape change: MODERATE (5-10% TV)")
    else:
        print("Shape change: LARGE (>10% TV)")
    print(f"Plots -> {PLOTDIR}")


if __name__ == "__main__":
    main()
