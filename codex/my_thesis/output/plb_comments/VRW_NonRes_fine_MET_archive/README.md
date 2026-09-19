---
type: figure-archive
updated: 2026-09-19
tags: [PLB, referee-response, VRW, histogram, figure-archive]
region: VRW-NonRes
variable: MET
bin_width_GeV: 25
fit_state: prefit
---

# VRW-NonRes MET 细分图归档

用于 [[Paper review/taunub_PLB_Jiaqi_Stergios_comparison#R1-16 VR discrepancy：是否提供检查图|R1-16 的 VR discrepancy 回复]]。这是一张历史诊断图，保留原始 40 个 bin（0–1000 GeV，25 GeV/bin）；不是重新进行最终模型的 fit。

## 修改版

![[Paper review/图件归档/VRW-NonRes_MET_25GeV/modified/VRW_NonRes_MET_25GeV_paper_style.png|900]]

- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/modified/VRW_NonRes_MET_25GeV_paper_style.pdf|修改版矢量 PDF]]
- [修改版 EPS](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/modified/VRW_NonRes_MET_25GeV_paper_style.eps)
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/modified/VRW_NonRes_MET_25GeV_paper_style.png|修改版高清 PNG]]

当前版的显示修改：

- 删除 `fit_taunub_nom_1l_allVR_N_minus_1`，将 `0tau1l1b, Non-Resonance 0tauVR` 改成 `VRW-NonRes`，保留 `Pre-fit`。
- 在 $E_{\mathrm T}^{\mathrm{miss}}=400$ GeV 处加红色 L 形箭头，向右指示 VR 选择范围，并标注 VR。
- 按用户要求将右上角图例排成整体两列，去掉所有事件数。逐行顺序为 Data / W+jets；Diboson / $t\bar t$；single $t$ / Z+jets；Uncertainty。
- 背景名称和 RGB 颜色取自 [taunub paper arXiv:2606.02067v1 的 Figure 3（第 13 页）](https://arxiv.org/abs/2606.02067v1)：W+jets 粉色，Diboson 橙色，$t\bar t$ 蓝色，single $t$ 土黄色，Z+jets 灰绿色。公开图为三列，本修改版按用户要求重排为两列。
- Dijet 不列入图例；nominal histogram 中原有的 1e-6/bin 数值仍保留在堆叠中。背景堆叠顺序不变。
- 图例放大到与原始带 Data 位图相同的文字比例；原图以 1240×904 画布为参照。普通文字和图例采用 `SetTextFont(43)`、`SetTextSize(30)`；ATLAS 采用 `SetTextFont(73)`，恢复粗斜体。数据点采用 `SetMarkerStyle(20)`、`SetMarkerSize(2.0)`，恢复原图的实心圆大小。
- EPS 使用 `SetLineScalePS(2)`，避免导出后线条比位图过粗。坐标轴标题固定在原图边距内，避免大字重叠或裁切。

## 原始文件和格式转换

本次在 lxatut 找到的原生细分文件是 PNG、ROOT 和 YAML，**未找到对应的原生 EPS**。原始 PNG 没有显示数据点；原始 ROOT 中保留了 Data histogram。

- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met.png|lxatut 原始 PNG（无数据点）]]
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met_png_wrapped.pdf|原 PNG 转换的 PDF]]
- [原 PNG → PDF → EPS](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met_png_wrapped.eps)：按用户要求进行格式转换，内容保持原样，仍为位图封装。
- [lxatut 原始 ROOT](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/fit_taunub_N_minus_1_histos.root)
- [lxatut 原始 YAML（背景细分结果，无 Data 节）](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met_prefit.yaml)
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/original_lxatut/INT_note_original_JPEG_wrapped.pdf|原 INT note 中带 Data 的低清图]]：该 PDF 内嵌 1240×904 JPEG，来源为本地 INT note；不是从 lxatut 下载的图。

## 可编辑 EPS 的来源

当前可编辑底稿使用 lxatut 原始 ROOT 中供绘图使用的 **nominal histograms（不带 `_orig` 后缀）**，保留所有 bin，并读取区域 ROOT 中已保存的总背景误差带。通过 ROOT 导出矢量 EPS，再转换为 PDF 和高清 PNG；**这是恢复导出文件，不是远程找到的原生 EPS**。

**2026-09-19 修正：** 上一版误用了处理前的 `_orig` histograms。最后一个 bin 的 Z+jets 为负，使 single-top 的堆叠位置落到对数坐标之外。上一版的“路径 hash 相同”只证明后续样式编辑没有改变那个错误底稿，不能证明底稿与原绘图一致，故撤回该结论。当前版改用已存储的 nominal 内容及绘图误差带；不手动截断负 bin、不改变源文件、不重新拟合。旧版仅保存在本地 `superseded_2026-09-19_raw_orig/` 供追溯，不应使用。

- [恢复底稿 EPS（保留原 label 和图例数字）](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/reconstructed/VRW_NonRes_MET_25GeV_ROOT_reconstructed.eps)
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/reconstructed/VRW_NonRes_MET_25GeV_ROOT_reconstructed.pdf|恢复底稿 PDF]]
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/reconstructed/VRW_NonRes_MET_25GeV_ROOT_reconstructed.png|恢复底稿 PNG]]

修改版和恢复底稿共用同一组 nominal bin 及误差带，仅改变文字、图例、颜色和 VR 箭头。没有平滑、插值或重新分箱。原带 Data 的 JPEG 用作文字、marker 和布局参考；数值核验以下载的 ROOT/YAML 为准。

## 数值和路径核验

- 40 个 bin，宽度均为 25 GeV。
- Data 总数：176；总背景：146.614558。
- $425<E_{\mathrm T}^{\mathrm{miss}}<450$ GeV：Data = 17，总背景 = 6.519261，保存的绘图误差为 1.057434。
- 最后一个 bin（975–1000 GeV）：single top = 0.028432814，总背景 = 0.322783285，保存的绘图误差 = 0.727573787；single-top 色块已恢复。
- 40 个 bin 的总背景和误差带均与原始绘图 ROOT 及 YAML 一致。分别读回恢复底稿与修改版的验证 ROOT：每组背景、Data、误差带坐标及 Data/Bkg. 坐标均与源数据核对通过。这里只保留数值核验结论，不再使用旧版的绘图路径 hash 证明原图一致性。
- [逐 bin 数值及误差](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/histogram_values_unchanged.json)
- [来源、RGB 数值和完整核验记录](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/archive_manifest.json)
- [下载文件的远程 SHA-256](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/remote_sha256.txt)：下载后及复制到 vault 后均逐文件比对一致。

远程 ROOT 来源：

```
codex_lxatut / lxatut3.cern.ch
/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_N_minus_1/Histograms/fit_taunub_N_minus_1_histos.root

region: VR_0tau1l1b_tch_met_N_minus_1_met
object: <region>/<sample>/nominal/<region>_<sample>

uncertainty file: Histograms/VR_0tau1l1b_tch_met_N_minus_1_met.root
uncertainty object: Graph_from_VR_0tau1l1b_tch_met_N_minus_1_met_Dijet
```

额外下载的区域 ROOT SHA-256：`b2c59a84433e5f3122948899817da8556a20178874c95bea3778756258084a47`。

远程 PNG / YAML 来源为同批次的 `run/fit_taunub_N_minus_1/Plots/`。本地完整副本位于 `my_thesis/output/plb_comments/VRW_NonRes_fine_MET_archive/`。

