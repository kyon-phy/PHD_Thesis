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

本次只改显示内容：

- 删除 `fit_taunub_nom_1l_allVR_N_minus_1`，将 `0tau1l1b, Non-Resonance 0tauVR` 改成 `VRW-NonRes`，保留 `Pre-fit`。
- 在 $E_{\mathrm T}^{\mathrm{miss}}=400$ GeV 处加红色 L 形箭头，向右指示 VR 选择范围，并标注 VR。
- 按用户要求将右上角图例排成整体两列，去掉所有事件数。逐行顺序为 Data / W+jets；Diboson / $t\bar t$；single $t$ / Z+jets；Uncertainty。
- 背景名称和 RGB 颜色取自 [taunub paper arXiv:2606.02067v1 的 Figure 3（第 13 页）](https://arxiv.org/abs/2606.02067v1)：W+jets 粉色，Diboson 橙色，$t\bar t$ 蓝色，single $t$ 土黄色，Z+jets 灰绿色。公开图为三列，本修改版按用户要求重排为两列。
- Dijet 的全部 bin 为零，因此只移除图例中的零产额条目；histogram 本身保留。背景堆叠顺序、bin 路径、数据点、误差线和 ratio panel 均不变。

## 原始文件和格式转换

本次在 lxatut 找到的原生细分文件是 PNG、ROOT 和 YAML，**未找到对应的原生 EPS**。原始 PNG 没有显示数据点；原始 ROOT 中保留了 Data histogram。

- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met.png|lxatut 原始 PNG（无数据点）]]
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met_png_wrapped.pdf|原 PNG 转换的 PDF]]
- [原 PNG → PDF → EPS](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met_png_wrapped.eps)：按用户要求进行格式转换，内容保持原样，仍为位图封装。
- [lxatut 原始 ROOT](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/fit_taunub_N_minus_1_histos.root)
- [lxatut 原始 YAML（背景细分结果，无 Data 节）](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/VR_0tau1l1b_tch_met_N_minus_1_met_prefit.yaml)
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/original_lxatut/INT_note_original_JPEG_wrapped.pdf|原 INT note 中带 Data 的低清图]]：该 PDF 内嵌 1240×904 JPEG，来源为本地 INT note；不是从 lxatut 下载的图。

## 可编辑 EPS 的来源

为了保留数据点并能独立修改文字、颜色和图例，可编辑底稿从原始 ROOT 的 `_orig` histograms 恢复，再导出为矢量 EPS；**此 EPS 是恢复导出文件，不冒称远程原件**。

- [恢复底稿 EPS（保留原 label 和图例数字）](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/reconstructed/VRW_NonRes_MET_25GeV_ROOT_reconstructed.eps)
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/reconstructed/VRW_NonRes_MET_25GeV_ROOT_reconstructed.pdf|恢复底稿 PDF]]
- [[Paper review/图件归档/VRW-NonRes_MET_25GeV/reconstructed/VRW_NonRes_MET_25GeV_ROOT_reconstructed.png|恢复底稿 PNG]]

随后直接编辑这份 EPS 的文字、图例和颜色命令，插入 VR 箭头。没有重算、平滑、插值或重新分箱。

## 数值和路径核验

- 40 个 bin，宽度均为 25 GeV。
- Data 总数：176；总背景：146.614398。
- $425<E_{\mathrm T}^{\mathrm{miss}}<450$ GeV：Data = 17，总背景 = 6.548541，存储的 MC 统计误差合并后为 1.057141。
- 修改前后，在剔除注释/图例及颜色命令后，EPS 的全部原有绘图命令 SHA-256 相同：`0683cb2642278435a2741f95a464fc2fa38c245eac89df538b8d92dac1aa4067`。
- [逐 bin 数值及误差](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/histogram_values_unchanged.json)
- [来源、RGB 数值和完整核验记录](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/archive_manifest.json)
- [下载文件的远程 SHA-256](file:///Users/zang/Desktop/ICEPP/%E5%8D%9A%E5%A3%AB%E8%AF%BE%E9%A2%98/leptoquark/obsidian/LQ%20taunub%20search/Paper%20review/%E5%9B%BE%E4%BB%B6%E5%BD%92%E6%A1%A3/VRW-NonRes_MET_25GeV/original_lxatut/remote_sha256.txt)：下载后及复制到 vault 后均逐文件比对一致。

远程 ROOT 来源：

```
codex_lxatut / lxatut3.cern.ch
/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_N_minus_1/Histograms/fit_taunub_N_minus_1_histos.root

region: VR_0tau1l1b_tch_met_N_minus_1_met
object: <region>/<sample>/nominal/<region>_<sample>_orig
```

远程 PNG / YAML 来源为同批次的 `run/fit_taunub_N_minus_1/Plots/`。本地完整副本位于 `my_thesis/output/plb_comments/VRW_NonRes_fine_MET_archive/`。

