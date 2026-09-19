# Chapter 7：pre-fit yields、Z 和 MET scan 核对

核对日期：2026-09-17。论文中的原有文字和 cutflow 保留；新增 final-selection pre-fit 数值及独立 MET 检查图。

## 1. 先用 paper 验证 post-fit

Paper 的依据是 `ANA-EXOT-2025-06-PAPER-auxmat.tex` 中三张 SR/CR/VR yields 表（约第 106–211 行），背景为 **仅在 CR 中拟合的 background-only fit**。

匹配的 fit 目录为：

`/Users/zang/Desktop/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_BONLY/fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_5_23L0_6_alldecay_corrected`

虽然内层目录含 `SPLUSB`，实际背景结果由 `Tables/Table_postfit_nosigs.yaml` 以及 `Plots/*_postfit.yaml` 核对，不能仅凭目录名判断 fit 类型。

- SR1b-Res：YAML 为 2.694835767 ± 0.825067856，paper 为 2.69 ± 0.83。
- SR1b-NonRes：YAML 为 1.879372203 ± 0.709240027，paper 为 1.88 ± 0.71。
- SR0b-Res：YAML 为 36.433219781 ± 7.295711517，paper 为 36.4 ± 7.3。
- SR0b-NonRes：YAML 为 38.252065600 ± 9.898138235，paper 为 38.3 ± 9.9。
- 12 个 SR/CR/VR 的 central yields 均与 paper 显示精度一致。CRW-Res 的 uncertainty 为 21.494，paper 写 22；其余误差按 paper 的精度基本一致，完整原值见 `paper_postfit_check.csv`。没有将 paper 的 22 当成 YAML 的精确值。
- `background_components.csv` 保留各区域、各过程的 pre-fit/post-fit 数字。WVR 的旧输出名称对应后来使用的 SR0b 选择。

**重要：`Table_prefit.yaml` 中 `Total` 可包含信号。** 本次 background 取 `Plots/*_prefit.yaml` 的 `Total`，并用各 background process 的和检查；post-fit 的 table 使用 `_nosigs` 版本。

## 2. Pre-fit S、B、Z

按 Ch7 现有公式使用绝对背景不确定度 `sigma_b = 0.30 × B`，signal 取 pure BSM，不含 interference。

- SR1b-Res，(M_U [TeV], g_U, beta_L23) = (1.5, 1.5, 0.6)：S = 4.261972633，B = 2.439244703，Z = 1.949858967。
- SR1b-NonRes，(2.5, 2.5, 1.0)：S = 6.583055999，B = 2.096818226，Z = 2.941717592。
- SR1b-NonRes，(3.0, 2.5, 1.0)：S = 4.171363527，B = 2.096818226，Z = 2.046514726。

第三项仅保留在作者核对文件中，未加入正文新表。它与现有 loose 图所用 `_modified` 一版的 signal normalization 不同，不能用这项数值解释另一版图的面积。

Res 信号来自上述已验证目录。2.5/3.0 TeV 信号来自对应 `TwoSided_HF0_3_HFSeperated_Renamed_SPLUSB/..._alldecay_corrected/Plots/*_prefit.yaml`；**只取 pre-fit signal**。脚本逐项确认这些文件的 pre-fit B 与已验证的 background-only 输出完全一致（数值容差 1e-12），没有使用 S+B post-fit background。

SR0b 的相应 pre-fit B 分别为 31.662282437 和 42.094310556。该旧 fit 将两区域作为 WVR，表中信号被置零，**这不代表物理信号为零**。因此未将这些零用于计算 SR0b 的 Z，也未从另一版输出拼接 signal。精确复现 paper 对应的 SR0b signal+interference 仍需要同版本、实际启用这些信号的模板。本次新增 Z 表限于有完整证据的 SR1b。

`validated_prefit_yields.csv` 保存完整数值。这里的 Z 是 optimisation counting metric，不是 final profile-likelihood significance。

## 3. INT note cutflow 和 Z

INT 第六章 cutflow 末行是 Res (4.2, 2.4)、NonRes (6.6, 2.1)。与上述验证数值的差别分别为：Res S +1.48%、B +1.64%；NonRes S −0.26%、B −0.15%。按用户允许的“差不多即可沿用”，原 cutflow 全表保留为 optimisation study；没有把最后一行替换成另一版 fit 的值而造成混表。fit_results 的文件清单中没有名称含 cutflow/cut_flow/cut-flow 的替代表。

但 INT 的 Z = 2.2、3.3 **不能**由同表的 S、B 和 30% 相对背景误差复现：

- 用 `sigma_b=0.30B` 得到 1.94037、2.94581。
- 若将 `sigma_b` 直接设为绝对的 0.3 event，则得到 2.16631、3.27325，恰好分别舍入成 2.2、3.3。

这提示原文的 30% 与当时实际输入可能存在口径差别；未找到当时的计算实现，**不能据此断言原因**。Ch7 保留明确写出的 30% 相对误差，报告重新计算的结果。两种口径并列在 `int_note_Z_check.csv`，没有暗中改变公式定义。

## 4. Obsidian hist 路线与版本差异

通过 Obsidian MCP 读取了 `5_Histogram与Fit/图片索引/Histogram图片搜索索引.md` 的“来源范围”，以及 `modified3000__SR_1tau0l1b_NonRes_met_N_minus_1_met.md` 图卡，随后读取链接的本地 YAML。

索引的 `fullRegion_v3` / `fullRegion_v3_modified` 不是与 paper 附表完全匹配的一版：SR1b 的 post-fit B 为 2.71668、1.82995，pre-fit B 为 2.33299、2.02893；例如 NonRes diboson 与匹配 paper 的结果明显不同。没有用这些输出替代 paper 对应的 final-selection yields。现有 CH7 loose distributions 使用这些文件；本次保留原图，不改其读数，也不把它们当作新验证表的数值来源。

## 5. MET N−1 scan 与双 panel 图

找到可用于两个 optimisation benchmarks 的 **nominal N−1**，无需 loose fallback：

- `fit_taunub_nom_1l_allVR_BONLY_MU1500_gU1_5_23L0_6_alldecay_corrected_N_minus_1/Plots/SR_1tau0l1b_sch_met_N_minus_1_met_prefit.yaml`
- `fit_taunub_nom_1l_allVR_BONLY_MU2500_gU2_5_23L1_0_alldecay_corrected_N_minus_1/Plots/SR_1tau0l1b_tch_met_N_minus_1_met_prefit.yaml`

这些 N−1 输出没有同目录 post-fit 配对，因此作为 **单独的 optimisation cross-check**，不声称与最终 paper fit 文件逐 bin 相同。它们在 nominal threshold 的 S、B 与已验证最终数值均相差不到 1%：Res (4.236916108, 2.434959354)，NonRes (6.583055999, 2.107354938)。未重新缩放使它们强行对齐。

处理方法：

1. 原生 200 GeV bins，不插值、不拆 bin、不改变 event yields。保留 baseline MET > 200 GeV，扫描可用的 bin 下边界 200, 400, …, 1400 GeV。
2. 每个阈值的 S、B 是该阈值以上所有 YAML bins 的和，包含末 bin 已存储的内容；不在 YAML 上限之外外推。恢复 nominal threshold 后，S 与同目录单 bin SR yield 在浮点精度内一致；B 的小差异原样保留。
3. 用相同 30% 相对背景不确定度重算 Z。没有用各 bin 的误差平方和替代总 B 的 30%，也没有假设未知的 nuisance covariance。
4. B ≤ 2 的点以空心点和虚线显示，只展示曲线趋势，不参与 cut choice。满足 B > 2 时，最优的可用阈值分别是 200、400 GeV。Res 在 600 GeV 的较大 Z 不满足 B > 2，不能据此改最终 cut。
5. 两幅分布图下 panel 为 cumulative Z，横轴位置表示积分起点；不是 per-bin significance。两区用了不同 signal benchmarks，未将二者随意组合成一个 Z。
6. 上 panel 每个背景 stack 高度由原 YAML 逐 bin 相加。仅按 paper 的图例将 W/Z 衰变道归并，严格检查归并总和等于 YAML `Total`。绘图 bar 的实际高度也与输入数组自动比较。
7. 颜色取自 paper `figures/Aux/post_fit_plots/SR1b_NonRes_met.pdf` 的 PDF colour operators；图例为 W+jets、Diboson、ttbar、single t、Z+jets、Uncertainty。没有画 data，也没有 ATLAS/Internal 字符。左上仅 sqrt(s)/luminosity 与 SR 两行。
8. 由于原始 bins 为 200 GeV，y 轴为 Events / 200 GeV，未为了改成 paper 的 100 GeV bin 宽而调整读数。Hatched band 使用 YAML 原有 uncertainty；Z 的独立 30% 假设另作明确标注。

输出：`Figs/CH7/significance/` 下的 scan 一张、MET+Z 两张，均有 PDF 和 PNG；逐阈值数值见两个 `*_met_scan.csv`。`manifest.json` 记录实际输入、SHA256、阈值检查与方法。可由 `scripts/ch7/validate_yields_and_scan.py` 重现。

INT PDF 的 Fig. N.1 位于 reference PDF 第 164 页。新图参考其 MET threshold–Z 折线形式；曲线数值完全来自上述 YAML 和本章公式，没有复制原图曲线。

## 6. LaTeX 改动与格式说明

只新增 verified pre-fit 数值段落、一张表、MET scan 说明和两组图；原 cutflow、原 loose N−1 图及既有用户文字保持不变。

- `\begin{table}[htbp]`：允许表在当前位置、页顶、页底或浮动页排版。
- `\small`：仅在表环境中缩小字号。
- `\begin{tabular}{lcrrr}`：SR 左对齐、benchmark 居中，S/B/Z 三列右对齐。
- `\toprule`、`\midrule`、`\bottomrule`：沿用 booktabs 横线。
- `\begin{figure}[htbp]`：沿用章节浮动图放置规则。
- `\includegraphics[width=\linewidth]{...SR1b_met_significance_scan.pdf}`：将已有左右 panel 的扫描 PDF 缩放至当前行宽；不改变图中的数值。
- `\begin{subfigure}{0.49\linewidth}` 与内部 `width=\linewidth`：每幅 MET+Z 图占正文行宽的 49%。`\hfill` 将剩余空隙放在两图之间。
- `\caption[短标题]{完整图注}`：短标题用于插图目录，完整图注解释 benchmark、cumulative Z 和 B > 2 条件。
- 新 `\label`/`\ref`：为 pre-fit 表、scan 图、MET+Z 图提供自动编号和交叉引用。
- 没有新增公式，也没有修改现有 Z 公式的单行排版。

完整逐行改动保存为 `chapter_changes.diff`；修改前的章节备份位于 `output/ch7/review/significance_validation_20260917/CH7_event_selection.before.tex`。
