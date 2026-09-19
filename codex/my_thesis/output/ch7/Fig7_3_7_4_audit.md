# Fig. 7.3 / 7.4 排版修改时的历史核查

**后续更新（2026-09-20）：用户要求使用 `noWeights_BSM`，12 张 SR1b 图的 signal 已更换。最新来源及数值见 [noWeights_BSM_update.md](figure_audit/noWeights_BSM_update.md)。下文保留更换前的 `comb` 审计记录，其中“当前”指当时的 `comb` 版本。背景、误差带及排版结论仍适用。原逐 bin JSON 已备份至 `figure_audit/before_bsm_signal/verified_bins_and_provenance.json`；原报告完整备份也在该目录。CERN 输入现已成功读取，`comb = BSM + inf` 已逐 bin 证实，取代下文当时未能确认组成的限制。**

更新：2026-09-20。数值核查和本轮排版修改已完成；以下区分已经证实的来源和仍缺少的生产记录。

## 结论

- 当前 12 张图直接取自 **fit_results 的 EPS**，通过矢量指令修改标注、图例和裁剪，再用 Ghostscript 转成 PDF；不是从 INT note 的 PDF 截图重绘。
- 12 张图的每个 signal bin、各 background group 和 total background 均与当前 nominal ROOT / YAML 一致。最大 ROOT–YAML 差为 `1.78e-14` events。
- 另外解析了 EPS 中 signal 和五层 background stack 的实际折线坐标，逐 bin 对照 ROOT/YAML。最大差为 `0.746` EPS 坐标单位，即约 `0.187 pt`，符合 ROOT 输出整数绘图坐标的舍入精度。
- 本轮修改前后的 histogram 和 uncertainty 绘图指令哈希完全一致。未重分 bin、缩放或修改任何 histogram / uncertainty 数值。
- **当前图与 INT note 的图并非同一套数值输入，signal 读数不完全相同。** 差异已存在于来源文件，不能通过改图例或排版消除。
- 当前 uncertainty **包含系统误差**；INT note 对应 nominal 配置没有 `Systematic:` block，属于 MC 统计误差版本。

## 当前图的来源

根目录：

```text
/Users/zang/Desktop/fit_results/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/
```

直接绘图源：

```text
Plots/SR_1tau0l1b_loose_{Res,NonRes}_{variable}_N_minus_1_{suffix}.eps
Plots/SR_1tau0l1b_loose_{Res,NonRes}_{variable}_N_minus_1_{suffix}_prefit.yaml
```

`variable → suffix`：`InvM → InvM`、`met → met`、`mT → mT`、`tau_pT → tau_pT`、`nlightjets → nLightJets`、`dphi → dphi_taumet`。

底层 histogram：

```text
Histograms/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_histos.root
    <region>/<sample>/nominal/<region>_<sample>
```

使用 nominal 对象，未使用 `_orig`。Z+jets 是 `Zll + Znunu + Ztautau`。

误差带：

```text
Histograms/<region>.root
    TGraphAsymmErrors: Graph_from_<region>_Ztautau
```

这个 graph 是 **total background 的误差带**，名称继承了最后一个 sample。它的 `fY`、`fEYhigh`、`fEYlow` 分别与 YAML 的 total、up、down 逐 bin 一致。不要由名字推断它只是 Ztautau。该文件另一个对象叫 `h_tot_postFit`，但本次读取值实际与 `_prefit.yaml` 一致；真正的 `_postFit.root` 是另一文件，读数不同。

每张图完整绝对路径、ROOT object、所有 bin 数值和比较结果保存在 [verified_bins_and_provenance.json](figure_audit/verified_bins_and_provenance.json)。

## 与 INT note Figs. 6.2 / 6.3 的比较

INT 图位于：

```text
/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/figures/SR_Optimization/
    resonance_plots/SR_1tau0l1b_loose_sch_<variable>_N_minus_1_<suffix>.pdf
    nonresonance_plots/SR_1tau0l1b_loose_tch_<variable>_N_minus_1_<suffix>.pdf
```

### 已确切找到的原文件

两幅 INT 图的 (e) light-jet multiplicity 和 (f) Δφ，共四张 PDF，与以下目录中的 PDF **逐字节一致**：

```text
/Users/zang/Desktop/fit_results/fit_taunub_nom_1l_allVR_BONLY_MU1500_gU1_5_23L0_6_alldecay_corrected_N_minus_1/Plots/
```

四张图均使用 `(MU, gU, betaL23) = (1.5 TeV, 1.5, 0.6)`。因此 INT note 的 NonRes (e,f) 也使用 1.5 TeV，并非 2.5 TeV。

同 binning 下，图中所有 bin 的总和如下（旧 → 当前；不是 final SR yield）：

- Res nlightjets：background `11.068418 → 10.579854`；signal `5.837053 → 5.202734`。
- Res Δφ：background `8.978275 → 8.502445`；signal `5.635393 → 5.098147`。
- NonRes nlightjets：background `48.807989 → 48.053194`；signal `11.638983 → 14.880639`。
- NonRes Δφ：background `32.433683 → 32.171734`；signal `8.155960 → 10.829518`。

### 前四个 panel

INT note 每组 (a–d) 是 raster image PDF，不能从其中提取精确 histogram 数值。图例可直接确认：Res 使用 `(1.5 TeV, 1.5, 0.6)`，NonRes 使用 `(2.5 TeV, 2.5, 1.0)`。当前 NonRes 六张图统一使用 `(3.0 TeV, 2.5, 1.0)`。

旧图使用 `200 GeV` bins，范围到 `1600 GeV`；当前使用 `100 GeV` bins，范围到 `1500 GeV`（Res MET 从 `200 GeV` 开始）。因此不能直接比较单个 bin 的高度或把曲线高度差都归因于物理变化。

上述 MU1500 nominal 目录及以下 MU2500 nominal 目录有对应 YAML，可以作版本比较，但**尚未证明是这八张 raster PDF 的精确生产输入**：

```text
/Users/zang/Desktop/fit_results/fit_taunub_nom_1l_allVR_BONLY_MU2500_gU2_5_23L1_0_alldecay_corrected_N_minus_1/Plots/
```

JSON 中这些项标为 `candidate for raster note panel; not exact provenance`，不当作精确 note 数字。

### 同 benchmark 仍有差异的原因及边界

旧配置读取 `MU1500_gU1_5_23L0_6_alldecay_corrected_BSM`；生产配置使用 DSID 567621 和 `weight_mc_corrected_GEN_gU1_5_23L0_6`。当前配置读取 `MU1500_gU1_5_23L0_6_noWeights_comb`；对应新生产配置的直接生成 BSM 样本为 DSID 570619，并另有 interference 样本 570771。即使参数相同，这些也不是同一个统计样本或权重流程。

本地没有找到生成这个 **确切 `_noWeights_comb.root` 文件**的历史合并记录，因此没有仅凭 `comb` 后缀断言其组成，更没有把差额全归因于 interference。AFS 原文件本轮未能读取：lxatut3 不可直连，lxplus 的现有 SSH 认证未通过。完整分解需要该生产目录的 BSM / interference / comb ROOT。

background 差别也已存在于 YAML。以 Res Δφ 为例，Diboson 总量 `1.023064 → 0.683528`，W+jets `5.670814 → 5.540572`。新生产配置在 Diboson DSID 列表中排除了 **700604**，注释原因是 mc20a 文件的磁盘问题；这提供了明确的输入完整性线索，但缺少原始合并记录，不能把全部差额确认为该 DSID。本轮保留原图数值，未自行补加。

## Fig. 7.3(f) uncertainty

在 Δφ = 0.4–0.6 bin：

- INT note：`2.655828 ± 0.181890` events。
- 当前图：`2.460089 ± 0.777484` events。

当前配置声明了 tau / jet / b-tagging 等系统误差及 W+jets、top、diboson 等 modelling 误差。仅 W+jets heavy-flavour 的 30% variation，在此 bin 就给出约 `0.528179` events 的偏移。因此当前大误差带不能作为 stat-only band 与旧图比较。

ROOT uncertainty graph 与 YAML 逐 bin 相同，且本轮 EPS error-band 指令未改变。caption 已明确包含 systematic contributions。直接将未经处理的 TH1 bin errors 平方相加并不能在所有 bin 还原绘图 band；它不等同于 TRExFitter 的完整误差构造。本轮验证的是已存储的 band 及配置含义，没有宣称独立重算了全部 nuisance-parameter 传播。

配置证据目录：

```text
/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search/10_来源与维护/代码快照/2026-09-07/taunub/
```

关键文件：

- `TRXconfig/config_taunub_plot_nom_1l_w_beamspot_v04_N_minus_1.config`
- `TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_N_minus_1_unblind_0b1bSR_fullRegion_v3.config`
- `config_taunub/config_taunub_plot_nom_1l_w_beamspot_v04_N_minus_1.yml`
- `config_taunub/config_taunub_plot_sys_1l_w_beamspot_v04_N_minus_1_fullRegion.yml`

## 本轮排版修改

- Legend 改为两列，左上从 U1 开始；原字体、颜色和符号保留。
- 红箭头标 final selection，方向为保留范围。Res：mass 800、MET 200、mT 200、tau pT 200；NonRes：MET 400、mT 600、tau pT 200、Δφ 1.2。没有质量要求的 NonRes mass 图和没有 Δφ 要求的 Res Δφ 图不加箭头。
- 2026-09-20 后续修改：箭头改为 paper `figures/Aux/post_fit_plots/SR1b_Res_InvM.pdf` 的 **L 形**，从横轴向上延伸，顶部转向保留范围。按该 PDF 矢量元素复现：线宽 2.5 pt、竖线长 185.25 pt、水平线段长 30.75 pt、实心箭头头部 12.5 × 11 pt；上界 cut 采用水平镜像。移除了之前悬空的短竖刻度箭头。10 个箭头的实际 PDF 元素尺寸已经逐个验证，记录为 `figure_audit/paper_arrow_style.json`。
- Light-jet histogram 的整数值位于 `[n,n+1)` bin；箭头分别在最后接受 bin 的右边缘 4 / 2，表示接受 `Nlight≤3 / ≤1`，指向左侧。未平移 bin。
- Light-jet、Δφ 的 `Events` 标题上对齐；tau pT、light-jet、Δφ 的横坐标主字号改为 paper 使用的 95 EPS units = 23.75 pt，保持靠右，下标按原比例调整。只有文字被调整。
- 副标题匹配横坐标：`m_{b tau_had}`、`pT^{tau_had}`、`Number of light jets`、`Delta phi(tau_had, MET)`。遵循图中的下标 had，而非另造上标记号。
- 两个 figure 内行间 `\par\medskip` 改成 `\\`，按用户偏好显式换行；移除最后一行后的多余 `\par\medskip`，caption 使用正常间距。figure 仍为 `[htpb]`，subfigure 仍为 `0.49\linewidth`。
- Caption 增加红箭头和 systematic contributions；NonRes signal 描述按实际颜色改为 purple dashed line。

修改后的 LaTeX 行：

```latex
\caption{$m_{b\tau_{\mathrm{had}}}$.}
\caption{$\pT^{\tau_{\mathrm{had}}}$.}
\caption{Number of light jets.}
\caption{$\Delta\phi(\tau_{\mathrm{had}},\met)$.}
\end{subfigure}\\
```

`\caption{...}` 设置各 panel 的副标题；`\mathrm{had}` 使 had 保持正体，下标位置与图内一致。质量的下标和 pT 的上标保留各自物理含义。`\Delta\phi` 直接写出图内角度记号。行尾 `\\` 开始下一行；原来的 `\par` 分段及 `\medskip` 额外竖直留白被移除。长 caption 仍使用原来的 `\caption[短标题]{正文}` 结构，方括号中的图目录标题未变。

## 复现及检查

```sh
PYTHONPATH=tmp/ch7_plot_deps:tmp/skill_validation_deps /usr/local/bin/python3 scripts/ch7/audit_sr_figures.py
/usr/local/bin/python3 scripts/ch7/restyle_eps.py --sr1b-only
```

重画后再运行 audit。`--sr1b-only` 仅更新这 12 张图，保留 SR0b 文件。

本轮修改前副本保存在 `output/ch7/figure_audit/before_restyle/`。当前来源清单为 `output/ch7/figure_manifest.json`。主文只修改了 Fig. 7.3 / 7.4 figure blocks，保留其他同期编辑。

CH7 preview 编译通过，共 22 页；图仍为 Fig. 7.3（第 7 页）和 Fig. 7.4（第 10 页）。已有 document-class、bibliography、fancyhdr、hyperref 和 TikZ-Feynman warnings；无 LaTeX error，未出现本轮图文引起的 overfull box 或未定义引用。
