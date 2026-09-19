import math
from array import array
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# =========================================================
# 1. 只需要改这里的数据
#    输入单位按 pb 写，程序会自动转成 fb 作图
# =========================================================
mass_TeV = [1.5, 2.0, 2.5, 4.0]

vis_pb_beta0 = [7.38e-05, 9.71e-05, 1.47e-04, 1.80e-04]      # |beta_R^33| = 0
vis_pb_beta1 = [9.7541e-05, 1.43031e-04, 1.65001e-04, 1.73340e-04]  # |beta_R^33| = 1

region_label = "SR1b-Res + SR1b-NonRes"
region_label2 = "SR0b-Res + SR0b-NonRes"
output_name = "visible_xsec_SR1b_SR0b"

# =========================================================
# 2. 一些可调的画图参数
# =========================================================
XMIN, XMAX = 1.4, 4.1
YMIN_TOP, YMAX_TOP = 0.03, 0.23   # 上图 y 轴范围（单位 fb）

# 文字位置（NDC）
atlas_x = 0.17
atlas_y = 0.88
line2_x = 0.17
line2_y = 0.82
line3_x = 0.17
line3_y = 0.76
line4_x = 0.17
line4_y = 0.70

# legend 位置
leg_x1, leg_y1 = 0.60, 0.73
leg_x2, leg_y2 = 0.99, 0.92
# legend text size
leg_text_size = 0.060

# 自定义 y 轴标题位置（NDC）
top_ylabel_x = 0.07
top_ylabel_y = 0.72

bot_ylabel_x = 0.07
bot_ylabel_y = 0.29

# =========================================================
# 3. 数据处理
# =========================================================
if not (len(mass_TeV) == len(vis_pb_beta0) == len(vis_pb_beta1)):
    raise ValueError("mass_TeV, vis_pb_beta0, vis_pb_beta1 长度必须一致")

# pb -> fb
vis_fb_beta0 = [x * 1000.0 for x in vis_pb_beta0]
vis_fb_beta1 = [x * 1000.0 for x in vis_pb_beta1]

ratio = []
for a, b in zip(vis_fb_beta0, vis_fb_beta1):
    if a == 0:
        ratio.append(0.0)
    else:
        ratio.append(b / a)

# ratio pad：让 y=1 在中间，上下对称
max_dev = max(abs(r - 1.0) for r in ratio)
pad = 0.03
step = 0.1
half_range = math.ceil((max_dev + pad) / step) * step
YMIN_BOT = 1.0 - half_range
YMAX_BOT = 1.0 + half_range

# ROOT arrays
xarr = array('d', mass_TeV)
y0arr = array('d', vis_fb_beta0)
y1arr = array('d', vis_fb_beta1)
rarr = array('d', ratio)

n = len(mass_TeV)

# =========================================================
# 4. 画布和 pad
# =========================================================
c = ROOT.TCanvas("c", "c", 900, 750)

pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.30, 1.0, 1.0)
pad2 = ROOT.TPad("pad2", "pad2", 0.0, 0.00, 1.0, 0.30)

pad1.SetLeftMargin(0.14)
pad1.SetRightMargin(0.04)
pad1.SetTopMargin(0.04)
pad1.SetBottomMargin(0.02)
pad1.SetTicks(1, 1)

pad2.SetLeftMargin(0.14)
pad2.SetRightMargin(0.04)
pad2.SetTopMargin(0.02)
pad2.SetBottomMargin(0.32)
pad2.SetTicks(1, 1)

pad1.Draw()
pad2.Draw()

# =========================================================
# 5. 上图
# =========================================================
pad1.cd()

frame1 = pad1.DrawFrame(XMIN, YMIN_TOP, XMAX, YMAX_TOP)
frame1.SetTitle("")

# 轴设置
frame1.GetXaxis().SetTitle("")
frame1.GetXaxis().SetLabelSize(0)

frame1.GetYaxis().SetTitle("")
frame1.GetYaxis().SetLabelSize(0.045)
frame1.GetYaxis().SetTitleSize(0.00)
frame1.GetYaxis().SetTitleOffset(1.1)
frame1.GetYaxis().SetNdivisions(508)

# 图
gr0 = ROOT.TGraph(n, xarr, y0arr)
gr0.SetLineColor(ROOT.kBlack)
gr0.SetMarkerColor(ROOT.kBlack)
gr0.SetLineWidth(2)
gr0.SetLineStyle(2)
gr0.SetMarkerStyle(24)  # open circle
gr0.SetMarkerSize(1.2)

gr1 = ROOT.TGraph(n, xarr, y1arr)
gr1.SetLineColor(ROOT.kBlack)
gr1.SetMarkerColor(ROOT.kBlack)
gr1.SetLineWidth(2)
gr1.SetLineStyle(1)
gr1.SetMarkerStyle(20)  # filled circle
gr1.SetMarkerSize(1.2)

gr0.Draw("LP SAME")
gr1.Draw("LP SAME")

# 自定义上图 y 轴标题（放得更靠上，不在正中）
latex_y1 = ROOT.TLatex()
latex_y1.SetNDC()
latex_y1.SetTextFont(42)
latex_y1.SetTextSize(0.058)
latex_y1.SetTextAngle(90)
latex_y1.DrawLatex(top_ylabel_x, top_ylabel_y, "#it{#sigma}^{visible} [fb]")

# ATLAS label
latex = ROOT.TLatex()
latex.SetNDC()

latex.SetTextSize(0.055)
latex.DrawLatex(atlas_x, atlas_y, f"#it{{ATLAS}} #bf{{Internal}}")

latex.SetTextSize(0.05)
latex.DrawLatex(line2_x, line2_y, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
latex.DrawLatex(line3_x, line3_y, f"#bf{{{region_label}}}")
latex.DrawLatex(line4_x, line4_y, f"#bf{{{region_label2}}}")

# Legend
leg = ROOT.TLegend(leg_x1, leg_y1, leg_x2, leg_y2)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetTextAlign(13);
leg.AddEntry(gr0, "|#it{#beta}_{R}^{33}| = 0", "lp")
leg.AddEntry(gr1, "|#it{#beta}_{R}^{33}| = 1", "lp")
leg.SetTextSize(leg_text_size)
leg.Draw()

pad1.RedrawAxis()

# =========================================================
# 6. 下图 ratio
# =========================================================
pad2.cd()

frame2 = pad2.DrawFrame(XMIN, YMIN_BOT, XMAX, YMAX_BOT)
frame2.SetTitle("")

frame2.GetXaxis().SetTitle("#it{m}_{#it{U}_{1}} [TeV]")
frame2.GetXaxis().SetTitleSize(0.12)
frame2.GetXaxis().SetLabelSize(0.12)
frame2.GetXaxis().SetTitleOffset(1.05)
frame2.GetXaxis().SetNdivisions(508)

frame2.GetYaxis().SetTitle("")
frame2.GetYaxis().SetLabelSize(0.12)
frame2.GetYaxis().SetTitleSize(0.00)
frame2.GetYaxis().SetNdivisions(505)

# 自定义下图 y 轴标题
latex_y2 = ROOT.TLatex()
latex_y2.SetNDC()
latex_y2.SetTextFont(42)
latex_y2.SetTextSize(0.125)
latex_y2.SetTextAngle(90)
latex_y2.DrawLatex(
    bot_ylabel_x,
    bot_ylabel_y,
    "#it{#sigma}^{visible}_{|#it{#beta}_{R}^{33}|=1} / #it{#sigma}^{visible}_{|#it{#beta}_{R}^{33}|=0}"
)

# y = 1 参考线
line = ROOT.TLine(XMIN, 1.0, XMAX, 1.0)
line.SetLineColor(ROOT.kBlack)
line.SetLineWidth(1)
line.Draw()

gr_ratio = ROOT.TGraph(n, xarr, rarr)
gr_ratio.SetLineColor(ROOT.kBlack)
gr_ratio.SetMarkerColor(ROOT.kBlack)
gr_ratio.SetLineWidth(2)
gr_ratio.SetMarkerStyle(20)
gr_ratio.SetMarkerSize(1.2)
gr_ratio.Draw("LP SAME")

pad2.RedrawAxis()

# =========================================================
# 7. 输出
# =========================================================
c.SaveAs(output_name + ".pdf")

print("Saved:", output_name + ".pdf")