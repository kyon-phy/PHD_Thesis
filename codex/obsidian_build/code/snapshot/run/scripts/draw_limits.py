#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from array import array
import numpy as np

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# ========== 1) Parse sample directory names ==========
# Expected directory name format example:
#   fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_5_23L0_2_alldecay_corrected
#   -> MU=1500, gU=1.5, beta=0.2
RE_NAME = re.compile(
    r".*SPLUSB_MU(?P<MU>\d+).*?gU(?P<gUa>\d+)_(?P<gUb>\d+).*?23L(?P<betaA>\d+)_(?P<betaB>\d+).*?alldecay_corrected",
    re.IGNORECASE,
)

def parse_params_from_dirname(dirname):
    """Extract MU, gU, beta from directory name"""
    m = RE_NAME.match(dirname)
    if not m:
        return None
    MU = int(m.group("MU"))
    gU = float(f"{int(m.group('gUa'))}.{int(m.group('gUb'))}")
    beta = float(f"{int(m.group('betaA'))}.{int(m.group('betaB'))}")
    return (MU, gU, beta)

# ========== 2) Read ROOT file and extract significance ==========
def read_significance(root_file_path):
    """
    Return significance value (float) from parameter.root.
    Supports two cases:
      B) TTree named 'stats' with a branch 'exp_significance'.
    """
    if not os.path.isfile(root_file_path):
        return None

    f = ROOT.TFile.Open(root_file_path, "READ")
    if not f or f.IsZombie():
        return None

    zval = None

    # read significance from TTree
    if zval is None:
        t = f.Get("stats")
        if t and isinstance(t, ROOT.TTree):
            if t.GetBranch("exp_significance"):
                buf = array("f", [0.0])
                t.SetBranchAddress("exp_significance", buf)
                if t.GetEntries() > 0:
                    t.GetEntry(0)
                    zval = float(buf[0])
            else:
                print(f"[WARN] exp_significance branch missing for: {root_file_path}")
                return None

    f.Close()
    return zval

# ========== 3) Collect significance map ==========
def scan_input_dir(input_dir):
    """
    Iterate over all subdirectories of input_dir,
    parse MU, gU, beta and extract significance.
    Returns dict: {(MU, gU, beta): Z}
    """
    zmap = {}
    for name in os.listdir(input_dir):
        full = os.path.join(input_dir, name)
        if not os.path.isdir(full):
            continue
        params = parse_params_from_dirname(name)
        if not params:
            continue
        (MU, gU, beta) = params
        root_path = os.path.join(full, "Significance", "Asymptotics", "parameter.root")
        z = read_significance(root_path)
        if z is None:
            print(f"[WARN] significance missing for: {name}")
            continue
        zmap[(MU, gU, beta)] = z
        print(f"MU={MU}, gU={gU}, beta={beta} --> Z={z:.3f}")
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

# get the contour graph after drawing the contour
def get_contour_graph(contour_index):
    # Get the object named "contours" from gROOT, which is a TObjArray,
    contours_obj = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    if contours_obj:
        # get TList object that contains the TGraph objects in the TObjArray
        contours_list = contours_obj.At(contour_index)
        if contours_list.At(0):
            # clone the contour graph to keep the original graph alive
            graph_clone = contours_list.At(0).Clone()
            # set plot properties
            graph_clone.SetLineColor(ROOT.kRed)
            graph_clone.SetLineStyle(1)
            graph_clone.SetLineWidth(3)
            # set ownership to False to keep the graph alive after the function returns
            ROOT.SetOwnership(graph_clone, False)
            return graph_clone
    else:
        print("No contours object found, ensure the contour is correctly drawn")
    return None

# get shaded region for b anomalies
def get_gU_limit_for_b_anomalies(MLQ):
    # limit for line gU^2*beta23*beta33, gU normalized while beta33=1, beta23=0.2
    gU_high = 1.4 * MLQ + 0.1
    gU_low = 0.55 * MLQ + 0.05
    return gU_high, gU_low

def get_b_anomalies_production_limit(MLQ, enable_cU=False):
    # limit for line gU^2*(1+Vcs/Vcb*beta23), gU normalized while beta33=1, beta23=0.2
    gU_high, gU_low = get_gU_limit_for_b_anomalies(MLQ)
    Vcs=0.97349
    Vcb=0.04182
    
    if not enable_cU:
        gU_beta_limit_high = gU_high**2 * (1+Vcs/Vcb*0.2)
        gU_beta_limit_low = gU_low**2 * (1+Vcs/Vcb*0.2)
        return gU_beta_limit_high, gU_beta_limit_low
    else:
        cU_high = get_cU(gU_high, MLQ * 1e3) # MLQ in GeV unit
        cU_low = get_cU(gU_low, MLQ * 1e3) # MLQ in GeV unit
        cU_beta_limit_high = cU_high**2 * (1+Vcs/Vcb*0.2)
        cU_beta_limit_low = cU_low**2 * (1+Vcs/Vcb*0.2)
        # print(f"cU_beta_limit_high: {cU_beta_limit_high}, cU_beta_limit_low: {cU_beta_limit_low}, gU_high: {gU_high}, gU_low: {gU_low}, cU_high: {cU_high}, cU_low: {cU_low}, MLQ: {MLQ}")
        return cU_beta_limit_high, cU_beta_limit_low

# fill the shaded region for b anomalies
def fill_between_curves(canvas, c, d, x_min, x_max, n_points=100, fill_color=ROOT.kGray+2, fill_style=3004):
    """
    在给定的canvas上填充由两条曲线 x^2*(1+Vcs/Vcb*y)=c 和 x^2*(1+Vcs/Vcb*y)=d 所限定的区域。
    要求 x 在 [x_min, x_max] 内，且 x ≠ 0（因此建议 x_min > 0）。
    
    参数：
      canvas    : 目标 ROOT.TCanvas
      c         : 曲线下界对应的常数
      d         : 曲线上界对应的常数
      x_min     : x 轴下限（建议大于 0）
      x_max     : x 轴上限
      n_points  : 用于生成曲线的采样点数，默认 100
      fill_color: 填充颜色，默认为 ROOT.kGray+2
      fill_style: 填充样式，默认为 3004（斜线填充）
      
    返回：
      填充区域的 TGraph 对象。
    """
    # 在 x 方向生成采样点
    xs = np.linspace(x_min, x_max, n_points)
    
    # 根据公式计算两条曲线的 y 值
    # y_lower = [c / (x**2) for x in xs]  # 下界： y = c/x²
    # y_upper = [d / (x**2) for x in xs]  # 上界： y = d/x²
    Vcs=0.97349
    Vcb=0.04182
    y_lower = [(c / x**2 - 1) / (Vcs/Vcb) for x in xs]  # 下界： y = (c/(x^2)-1)/(Vcs/Vcb)
    y_upper = [(d / x**2 - 1) / (Vcs/Vcb) for x in xs]  # 上界： y = (d/(x^2)-1)/(Vcs/Vcb)
    
    # 构造闭合多边形的顶点：
    # 先沿上界曲线正向采样，再沿下界曲线反向采样
    poly_x = list(xs) + list(xs[::-1])
    poly_y = list(y_upper) + list(y_lower[::-1])
    
    n_poly = len(poly_x)
    
    # 转换为 TGraph 需要的数组类型
    x_vals = array('d', poly_x)
    y_vals = array('d', poly_y)
    
    # 构造 TGraph 对象
    polygon = ROOT.TGraph(n_poly, x_vals, y_vals)
    ROOT.SetOwnership(polygon, False)
    polygon.SetFillColor(fill_color)
    polygon.SetLineColor(fill_color)
    polygon.SetFillStyle(fill_style)
    
    # 在给定的 canvas 上绘制填充阴影区域
    canvas.cd()
    polygon.Draw("F same")  # "F" 表示填充，"same" 保证叠加到已有图形上
    canvas.Update()
    
    print(f"已在 canvas {canvas.GetName()} 上填充 x^2*y 在 [{c}, {d}] 区间内的阴影区域。")
    return polygon

# draw limit plots
def draw_mu_slice(zmap, outdir, output_file):
    print("*********** draw mu slice ***********")
    mus = sorted({k[0] for k in zmap})
    gus = sorted({k[1] for k in zmap})
    betas = sorted({k[2] for k in zmap})
    gu_bin_edges = get_bin_edges(gus, n_steps=2)
    beta_bin_edges = get_bin_edges(betas, n_steps=2)

    print("mu: ", mus, " gu_bin_edges: ", gu_bin_edges, " beta_bin_edges: ", beta_bin_edges)
    for MU in mus:
        h2 = ROOT.TH2D(f"h2_mu_{MU}", f";g_{{U}};#beta_{{L}}^{{23}};Z (MU={MU} GeV)",
                       len(gu_bin_edges) - 1, gu_bin_edges,
                       len(beta_bin_edges) - 1, beta_bin_edges)

        for (mu, gu, be), z in zmap.items():
            if mu != MU:
                continue
            h2.Fill(gu, be, z)

        # set the contour level
        z_contour = np.array([0.47, 1.96])
        h2.SetContour(len(z_contour), z_contour)

        # draw the original plots and generate the contour graph
        c = ROOT.TCanvas(f"c_mu_{MU}", "", 900, 750)
        h2.Draw("cont LIST")
        c.Update() # always update the canvas to get the contour graph
        contour_graph = get_contour_graph(1) 

        # get the contour graph, 0 for Z=0.47, 1 for Z=1.96
        c2 = ROOT.TCanvas(f"c_mu2_{MU}", "", 900, 750)
        h2.Draw("text")
        if contour_graph: contour_graph.Draw("L same")
        c2.Update() 

        # draw latex
        lat = ROOT.TLatex()
        lat.SetNDC(True)
        lat.SetTextSize(0.035)
        lat.DrawLatex(0.15, 0.92, f"MU = {MU}")

        # draw b anomaly shaded regions
        gU_beta_limit_high, gU_beta_limit_low = get_b_anomalies_production_limit(MU * 1e-3)
        fill_between_curves(c2, gU_beta_limit_low, gU_beta_limit_high, gu_bin_edges[0], gu_bin_edges[-1])
        
        # write canvas and save as png and pdf
        os.makedirs(outdir, exist_ok=True)
        output_file.cd()
        c2.Write()
        c2.SaveAs(os.path.join(outdir, f"significance_mu{MU}.png"))
        

        # draw the original plots and generate the contour graph
        c.Close()
        c2.Close()
        del h2, contour_graph

def draw_beta_slice(zmap, outdir, output_file):
    print("*********** draw beta slice ***********")
    mus = sorted({k[0] for k in zmap})
    gus = sorted({k[1] for k in zmap})
    betas = sorted({k[2] for k in zmap})
    mu_bin_edges = get_bin_edges(mus, n_steps=3)
    gu_bin_edges = get_bin_edges(gus, n_steps=2)
    print("beta: ", betas, " mu_bin_edges: ", mu_bin_edges, " gu_bin_edges: ", gu_bin_edges)
        
    for beta in betas:
        h2 = ROOT.TH2D(f"h2_beta_{str(beta).replace('.','_')}",
                       f";M_{{U}} [GeV];g_{{U}};Z (beta={str(beta).replace('.','_')})",
                       len(mu_bin_edges) - 1, mu_bin_edges,
                       len(gu_bin_edges) - 1, gu_bin_edges)

        for (mu, gu, be), z in zmap.items():
            # if be != beta:
            # if be == beta and be == 0.2:
            if be == beta:
                print(f"h2_name: {h2.GetName()}, mu: {mu}, gu: {gu}, be: {be}, beta: {beta}, z: {z:.3f}")
                h2.Fill(mu, gu, z)

        # set the contour level
        z_contour = np.array([0.47, 1.96])
        h2.SetContour(len(z_contour), z_contour)

        # draw the original plots and generate the contour graph
        c = ROOT.TCanvas(f"c_beta_{str(beta).replace('.','_')}", "", 900, 750)
        h2.Draw("cont LIST")
        c.Update() # always update the canvas to get the contour graph
        contour_graph = get_contour_graph(1) 

        # draw the original plots and generate the contour graph
        c2 = ROOT.TCanvas(f"c_beta2_{str(beta).replace('.','_')}", "", 900, 750)
        h2.Draw("text")
        if contour_graph: contour_graph.Draw("L same")
        c2.Update() 

        # draw latex
        lat = ROOT.TLatex()
        lat.SetNDC(True)
        lat.SetTextSize(0.035)
        lat.DrawLatex(0.15, 0.92, f"#beta_{{L}}^{{23}} = {beta}")

        # draw b anomaly shaded regions
        x_range = [mu_bin_edges[0], mu_bin_edges[-1]]
        draw_b_anomalies_mass_region(c2, x_range, beta, fill_color=ROOT.kGray+1)

        # write canvas and save as png
        os.makedirs(outdir, exist_ok=True)
        output_file.cd()
        c2.Write()
        c2.SaveAs(os.path.join(outdir, f"significance_beta{str(beta).replace(',','_')}.png"))

        c.Close()
        c2.Close()
        del h2, contour_graph

def draw_gU_1D(zmap, outdir, outputfile):
    print("*********** draw gU slice ***********")
    mus = sorted({k[0] for k in zmap})
    gus = sorted({k[1] for k in zmap})
    betas = sorted({k[2] for k in zmap})
    first_canvas = True

    for MU in mus:
        for beta in betas:
            # creat and fill TGraph
            # 创建两个TGraph对象
            g1 = ROOT.TGraph()
            g1.SetName(f"g1_mu_{MU}_beta_{str(beta).replace('.','_')}")
            g1.SetTitle(f"MU={MU} GeV, beta={beta};g_{{U}};Significance")

            g1_square = ROOT.TGraph()
            g1_square.SetName(f"g1_square_mu_{MU}_beta_{str(beta).replace('.','_')}")
            g1_square.SetTitle(f"MU={MU} GeV, beta={beta};g_{{U}}^{{2}};Significance")

            # 填充数据点
            point_index = 0
            for (mu, gu, be), z in zmap.items():
                if mu != MU or be != beta or gu == 5:
                    continue
                g1.SetPoint(point_index, gu, z)
                g1_square.SetPoint(point_index, gu**2, z)
                point_index += 1

            # 绘图
            c = ROOT.TCanvas(f"c_mu_{MU}_beta_{str(beta).replace('.','_')}", "", 900, 750)
            g1.SetMarkerStyle(20)
            g1.SetLineColor(ROOT.kBlue)
            g1.Draw("ALP")   # A:坐标轴, L:连线, P:点
            c.Update()

            c2 = ROOT.TCanvas(f"c_mu2_{MU}_beta_{str(beta).replace('.','_')}", "", 900, 750)
            g1_square.SetMarkerStyle(21)
            g1_square.SetLineColor(ROOT.kRed)
            g1_square.Draw("ALP")
            c2.Update()

            # save as PDF
            if first_canvas:
                c.Print(f"{outdir}/gU_1D_plots.pdf(")
                c2.Print(f"{outdir}/gU_1D_plots.pdf")
                first_canvas = False
            else:
                c.Print(f"{outdir}/gU_1D_plots.pdf")
                c2.Print(f"{outdir}/gU_1D_plots.pdf")
            # 写入输出文件
            outputfile.cd()
            c.Write()
            c2.Write()

            # 清理
            del g1, g1_square, c, c2
    # close the pdf
    final_canvas = ROOT.TCanvas("c_end", "", 1, 1)
    final_canvas.Print(f"{outdir}/gU_1D_plots.pdf)")  # 关闭 PDF 文件


def draw_beta_1D(zmap, outdir, outputfile):
    print("*********** draw gU slice ***********")
    mus = sorted({k[0] for k in zmap})
    gus = sorted({k[1] for k in zmap})
    betas = sorted({k[2] for k in zmap})
    first_canvas = True

    for MU in mus:
        for GU in gus:
            # creat and fill TGraph
            # 创建两个TGraph对象
            g1 = ROOT.TGraph()
            g1.SetName(f"g1_mu_{MU}_gu_{str(GU).replace('.','_')}")
            g1.SetTitle(f"MU={MU} GeV, gU={GU};#beta_{{L}}^{{23}};Significance")

            g1_square = ROOT.TGraph()
            g1_square.SetName(f"g1_square_mu_{MU}_beta_{str(GU).replace('.','_')}")
            g1_square.SetTitle(f"MU={MU} GeV, gu={GU};#beta_{{L}}^{{23}}*#beta_{{L}}^{{23}};Significance")

            # 填充数据点
            point_index = 0
            for (mu, gu, be), z in zmap.items():
                if mu != MU or gu != GU:
                    continue
                g1.SetPoint(point_index, be, z)
                g1_square.SetPoint(point_index, be**2, z)
                point_index += 1

            # 绘图
            c = ROOT.TCanvas(f"c_mu_{MU}_beta_{str(GU).replace('.','_')}", "", 900, 750)
            g1.SetMarkerStyle(20)
            g1.SetLineColor(ROOT.kBlue)
            g1.Draw("ALP")   # A:坐标轴, L:连线, P:点
            c.Update()

            c2 = ROOT.TCanvas(f"c_mu2_{MU}_beta_{str(GU).replace('.','_')}", "", 900, 750)
            g1_square.SetMarkerStyle(21)
            g1_square.SetLineColor(ROOT.kRed)
            g1_square.Draw("ALP")
            c2.Update()

            # save as PDF
            if first_canvas:
                c.Print(f"{outdir}/beta_1D_plots.pdf(")
                c2.Print(f"{outdir}/beta_1D_plots.pdf")
                first_canvas = False
            else:
                c.Print(f"{outdir}/beta_1D_plots.pdf")
                c2.Print(f"{outdir}/beta_1D_plots.pdf")
            # 写入输出文件
            outputfile.cd()
            c.Write()
            c2.Write()

            # 清理
            del g1, g1_square, c, c2
    # close the pdf
    final_canvas = ROOT.TCanvas("c_end", "", 1, 1)
    final_canvas.Print(f"{outdir}/beta_1D_plots.pdf)")  # 关闭 PDF 文件

# ========== 5) Draw significance vs MU-gU for fixed beta ==========
# add shading to canvas
def draw_b_anomalies_mass_region(canvas, x_range, beta23, fill_color=ROOT.kGray+1):
    # factors to convert beta23=0 to beta23=1.0 or 0.2
    Vcs=0.97349
    Vcb=0.04182
    gU_sf = np.sqrt((1+0.2*Vcs/Vcb)/(1+beta23*Vcs/Vcb)) # gU^2*(1+Vcs/Vcb*beta23)=c
    print(f"beta23: {beta23}, gU_sf: {gU_sf}, x_range: {x_range}")
    # get gU limit for b anomalies favored region for x axis mass range
    gU_high_0, gU_low_0 = get_gU_limit_for_b_anomalies(x_range[0] * 1e-3)
    gU_high_1, gU_low_1 = get_gU_limit_for_b_anomalies(x_range[1] * 1e-3)
    line1 = [(x_range[0], gU_high_0 * gU_sf), (x_range[1], gU_high_1 * gU_sf)]
    line2 = [(x_range[0], gU_low_0 * gU_sf), (x_range[1], gU_low_1 * gU_sf)]

    points = []
    for pt in line1:
        points.append(pt)
    for pt in reversed(line2):
        points.append(pt)
    
    npoints = len(points)
    x_vals = array('d', [pt[0] for pt in points])
    y_vals = array('d', [pt[1] for pt in points])
    
    # construct closed polygon
    poly = ROOT.TGraph(npoints, x_vals, y_vals)
    print("npoints: ", npoints, " x_vals: ", x_vals, " y_vals: ", y_vals)
    ROOT.SetOwnership(poly, False)
    poly.SetFillColor(fill_color)
    poly.SetLineColor(fill_color)
    poly.SetFillStyle(3004)  # modify fill style, 3004 for dashed fill
    
    # draw shading on the canvas
    canvas.cd()
    poly.Draw("f same")
    canvas.Update()

# ========== main ==========
def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_dir> [out_dir=plots]")
        sys.exit(1)

    input_dir = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "plots"

    zmap = scan_input_dir(input_dir)
    if not zmap:
        print("[ERROR] No valid samples found. Check folder names and files.")
        sys.exit(2)

    print(f"[INFO] Collected {len(zmap)} points:")
    for k, v in sorted(zmap.items()):
        print(f"  MU={k[0]:>4}  gU={k[1]:>4}  beta={k[2]:>4}  --> Z={v:.3f}")

    # # create output file
    output_file = ROOT.TFile("plots/output_TH2D.root", "RECREATE")

    # draw_mu_slice(zmap, out_dir, output_file)
    # draw_beta_slice(zmap, out_dir, output_file)
    draw_gU_1D(zmap, out_dir, output_file)
    draw_beta_1D(zmap, out_dir, output_file)
    print(f"[DONE] Plots saved to: {out_dir}/")

if __name__ == "__main__":
    main()
