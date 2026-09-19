# 第九章草稿：来源、取舍与待确认项

撰写日期：2026-09-19。正文：`Chapters/CH9_Systematics_uncertainties.tex`。

## 本次优先级与使用版本

按用户本次明确要求采用 **paper > INT note > Obsidian 总结**。这覆盖了写作 skill 中原先的 INT 优先规则。配置快照用于解释实现与标记差异，不用它无声覆盖 paper。

- Paper 正文：`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/paper_draft/ANA-EXOT-2025-06-PAPER/sections/systeamtics.tex`；配套 `sections/results.tex` 提供单 bin fit 和 MC statistical uncertainty 的边界。
- 编译后的 paper：`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/paper_draft/artifacts/ANA-EXOT-2025-06-PAPER.pdf`，封面日期 16 September 2026，§8 在 PDF 第 10 页。编译日期本身不证明新的公开版本。
- 公开版本：实时核对 [arXiv:2606.02067v1](https://arxiv.org/html/2606.02067v1)，提交日期 2026-06-01；当前 arXiv 记录仍只列 v1。§8 的主要数值与本地 paper 一致。论文正文没有自引这篇分析 paper。
- INT 主参考：`../references/ANA_EXOT_2025_06_INT1.pdf`，20 April 2026，166 页，§9 为 PDF 第 60–74 页，Appendix H 第 147–148 页，Appendix J 第 151–154 页。
- INT 可读源文件：`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/sections/Systematics.tex`、`sections/Appendices/SysValidation.tex`。该目录同名编译 PDF 的日期却是 12 March 2026，因此不能用它替代 April reference PDF。
- 较早 paper：`../references/ATL-COM-PHYS-2026-015.pdf` 为 26 May 2026 draft 3.3；`paper_draft/ANA_EXOT_2025_06_PAPER.pdf` 为 20 April 2026 draft 1.1。只用于版本比较。

Obsidian 内容通过 `obsidian_agent` MCP 实时读取，未修改 vault：

- `6_Systematics/Experimental_systematics与校准来源.md`，document-map version `c8be3d`。
- `6_Systematics/Theory_systematics与transfer-factor处理.md`，version `6ef881`。
- `6_Systematics/Systematics来源与分析实现总览.md`，version `b320b6`。
- `6_Systematics/Systematics待补资料清单.md`，version `fb8808`。
- `6_Systematics/Wjets_HF约30percent的依据与适用边界.md`，version `90f362`。

## 顺序与前文章节衔接

保留 INT 的大纲顺序：

1. Luminosity/pile-up → tau → jets/MET → flavour tagging → electrons/muons。
2. Transfer factor → W+jets → top → Z+fake tau → other backgrounds → signal → smoothing/relaxed selection → numerical summary。

第 5 章已经交代 nominal generator、PDF、tune、signal/interference 生成与 fast/full simulation，因此本章引用 `sec:signal_samples`、`sec:background_samples`、`eq:signal_interference`，没有重列 generator 表或重讲 MC chain。Luminosity 引用 `sec:dataset_selection`，trigger 引用 `sec:analysis_triggers`；pile-up reweighting 接续原 CH9 TODO，在这里说明数据 μ profile 的重标定与变分。

第 6 章已经定义 object reconstruction、TES nominal calibration、JES steps、GN2 architecture、efficiency scale factors 和 MET vector。本章引用各对象 section、`eq:ch6_met_vector`，不重复 SF 公式、RNN/GN2 网络结构或 WP selection 表。

第 8 章已经解释 CR normalisation、W flavour-transfer validation 和 ZVR fake-tau 检查。本章保留与不确定性直接相关的简要结果，引用 `sec:ch8_strategy`、`sec:ch8_top`、`subsec:ch8_vrw`、`subsec:ch8_zvr`；没有重新放验证分布。

三篇参考 thesis 的 systematics 章节均作了有限只读比较：Sugizaki ch.8、Aoki ch.9、Zhang ch.8。只采用共同的说明深度：区分 detector/modelling，解释如何构造 variation，再说明如何改变 selected yield；fit inference 留给后章。没有借用任何一篇的具体分析选择、数值、文句或独有组织。

## 已处理的冲突和歧义

### W+HF 20% / 30%

INT §9.2.1 与旧 summary 表仍有 20%，paper 明确 30%，Obsidian 所引配置也为 30%。草稿使用 30%，并保留 Res/NonRes 独立参数。未复制 INT 中基于旧 20% 设定的 sensitivity reduction 或 significance 数字。

已只读核对 `../obsidian_build/code/snapshot/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config` 第 2932–2951 行：作用于 `W*`，region patterns 选择 1b/2b，Res 和 NonRes 为不同 NP。正文解释为对 tagged-region W yield 的整体变分，而不是逐事例仅重加权 truth-HF，也不是 b-tag efficiency uncertainty。

### Tau Tight / Medium scale-factor convention

Paper 给 Tight ID 的 1-prong 5–8%、3-prong 6–11%；草稿按最高优先级保留这些数值及 prong/pT dependence。它们是 calibration SF uncertainties，不是总 signal-yield uncertainty。

但所查 `../obsidian_build/code/snapshot/TauXFastFrame/Root/TauXFastFrame.cc` 第 82 行实际组合 `tau_ID_effSF_MediumRNN`、`tau_Reco_effSF_MediumRNN` 与 LooseRNN eVeto SF。这比当前 CH6 仅描述“eVeto 使用 Medium ID 对应 calibration”的范围更广。

**待最终生产核对：** 需要对应最终拟合 ntuple/histogram 版本及 SF 分支，才能消除 paper Tight 数值与旧代码快照的差异。本次不以旧快照改写 paper，也不修改 CH6。正文引用 CH6 的 eVeto convention，未声称从快照证明了最终 Tight SF 的实现。

### FTAG Medium / Loose

INT prose 写 Medium，紧接着的 NP table 却写 Loose 并列 B 0–84、C 0–55、Light 0–41。Paper 不给 reduction scheme。TopCP 快照 `TauX_Gnt1NtupleMaker.py` 第 282–296 行对 Continuous event SF 显式设置三个 flavour 均为 Medium，calibration file 为 `MC20_2025-06-17_GN2v01_v4.root`。

草稿采用 INT prose 的 Medium，与快照一致；省略存在矛盾的 NP 总数。不能把 Continuous 输出配置当作最终每个 fixed WP / histogram 的完整生产证明。

### Transfer factor 的绝对比值与相对修正

INT Eqs. 9.1–9.9 的 double ratio 是明确的；Eq. 9.10 的示意 likelihood 容易把绝对 TF 再乘到 SR nominal yield 上。草稿不用该 likelihood，而写

`N_R = lambda * N_R_nominal * kappa_R`，其中 `kappa_R = T_R_varied / T_R_nominal`。

CR 归一化参数沿用第 8 章定义；没有把观测 CR 总数直接等同于该背景的 CR 产额。正文的单源公式有意只隔离 theory transfer term，实验与 MC statistical 项另行进入 fit。

### Relaxed selection 的 >1b / ≥1b

INT top 小节早段写 `>1b`，后续详细 procedure 明确为 `N_b >= 1` 取代 `N_b = 1`。草稿采用后者。Appendix H 的 smoothing validation 则是 TopVR `N_b >= 2`，两个研究不混用。

### 数值表与最终 nuisance effect

草稿表只保留 INT 两张 summary 表中 **SR1b** 的 transfer-factor evaluation 数值；paper 未给这些逐源数值，故由 INT 补足。caption 明确它们是 symmetrisation 前的有符号 variation，不是 post-fit uncertainty，也不是全部 SR0b/VR 的最终输入清单。

快照中的最终 fit 对同一 topology 的多个 SR/VR 使用若干共同 OVERALL modifiers，而 INT 原始研究表对 VR 还给出不同数值。因此没有把 INT 的全部 VR 表复制为最终 fit 配置。W PDF 与 alpha_s、top PDF 等也可能在配置中合并或省略，不按原始表行数声称最终 NP 数量。

### Minor backgrounds

Paper 省略了旧稿中 minor backgrounds 30% 的概括句，但并未明确否定该设定；INT 与 Toy 配置支持，故草稿补入。配置第 2901–2930 行中 fake-tau 100% 用于 `Znunu,Zll` 的含 tau 区域，30% Z modelling 用于 `Ztautau,Zll` 的 SR/VR，存在适用范围重叠。正文没有把所有 Z 分量强行划成互斥的 100% 或 30%，也没有声称这些数字是 inclusive cross-section 的精度。

## 对象与理论 PDF 核对

以下参考只读使用；摘出的文本和新下载 PDF 存在 `tmp/ch9_sources/`，原库未修改。

- `../references/systematics/LuminosityForPhysics _ Atlas _ TWiki.pdf`：PDF 第 4 页的 Run-2 0.83% 与 paper/CH5 一致。内部页面不进入 bibliography。
- `../references/systematics/JetUncertaintiesRel22 _ AtlasProtected _ TWiki.pdf`：PDF 第 1–2 页的 MC20/AF3、CategoryReduction/FullJER；第 7 页明确 MC/pseudo-data smearing 是同一 JER template 的构造输入，不能作为两组独立 NP。正文保留方法，省略内部工具路径和近似 NP 数量。
- `../references/s10052-021-09402-3.pdf`：公开 JES/JER 论文 §5.3、§5.3.1、§6，PDF 第 23–32 页，支持 flavour/pile-up/high-pT components、correlation reduction 与 resolution 方法。已有 key `ATLAS2021JetCalibration` 即 paper 的 JETM-2018-05。
- `tmp/ch6_sources/met.pdf`：§8，PDF 第 23–26 页，支持 soft-term 沿 hard-term 的 scale、parallel/perpendicular resolutions 与 Zee calibration。已有 key `ATLAS2025METPerformance` 即 paper 的 JETM-2020-03。
- `tmp/ch6_sources/tau_r22.pdf` 及新取得的 ATL-PHYS-PUB-2015-045、ATLAS-CONF-2017-029：支持 TES、detector response、physics-list、non-closure 与 in situ 方法。旧 note 中 2–6% 等历史精度不覆盖 paper 的更新数值，因此没有移植。新 PDF 来自 ATLAS 官方静态页面。
- `tmp/ch6_sources/electron_perf.pdf`、`electron_eff_run2.pdf`、`muon_calib.pdf`、`muon_id.pdf`：用于确认 energy/momentum calibration 与 efficiency、sagitta 的不同物理来源；沿用 CH6/CH5 已有公开引用。
- 新取得的 FTAG-2018-01、FTAG-2020-08、FTAG-2019-02 全文：支持 b/c/light calibration 的 uncertainty 方法；特别是 FTAG-2018-01 §10.4 支持 covariance/eigenvector 处理。这些旧 tagger 性能论文不能证明 GN2v01 的特定数值或最终 NP 数量，草稿没有这样使用。
- `../references/systematics/PmgWeakBosonProcesses _ AtlasProtected _ TWiki.pdf` 第 14–15 页：Sherpa 2.2.11 ME+PS 7-point、Hessian/alternative PDF、EW weights、HF normalisation difference。通用处方中的 CKKW/QSF 变化在 INT 本分析部分未落实，草稿没有擅自新增为已实施 uncertainty。
- `../references/systematics/PmgTopProcesses _ AtlasProtected _ TWiki.pdf` 第 4–5、9–10 页：pthard、PS、ISR/FSR、hdamp、recoil、DR/DS；使用 Run-2 分析设定，没有套用页面中的全部 Run-3/其他过程建议。
- **补齐此前缺失的公开 W+HF 原始引用**：ATL-PHYS-PUB-2017-006 §5，从 [INSPIRE 保存的 CERN 原始 PDF](https://inspirehep.net/files/73a3a21fe94e744667cadec828a25966) 取得并核对。它提供 generator/phase-space dependence；与 PMGR-2021-01、STDM-2018-43、HIGG-2020-20 共同支持 flavour modelling 的动机，不独立给出本分析的 30% prior。
- ATL-PHYS-PUB-2020-023 从 [公开原始 PDF](https://inspirehep.net/files/3b351d68370826da9b07cf96145485f3) 取得，核对 matching、PS、scale、hdamp、recoil 的来源。2020 note 的具体 matching 样本不是 2025/2026 recommendation 的 pthard 配置，正文具体选择由本分析 INT/PMG 决定。
- Czakon et al., arXiv:1705.04105：已读 NNLO QCD differential calculation 的原始 PDF；Frixione et al., arXiv:0805.3067 §4：已读 DR/DS 定义。只保留 paper 所用的 NNLO top-pT variation，不推断使用了该论文全部 NLO EW corrections。
- Ball et al., arXiv:2203.05506：检查公开 HTML 的 PDF uncertainty prescription，引用只用于 PDF uncertainty 方法；本分析 nominal PDF 仍是 CH5 的 NNPDF3.0，未改为 PDF4LHC21。
- Friedman, SLAC-176 §4.2，及 [ROOT 6.36 的 TH1::SmoothArray 源码](https://root.cern.ch/doc/v636/TH1_8cxx_source.html)：已核对 `353QH twice` 名称与其原始 reference。ROOT 文档明确回引该报告 §4.2。

## 留在作者记录中的实现边界

1. Tau SF 生产版本问题见上；提交前应以最终产物确认，不用旧 code snapshot 作最后结论。
2. Signal 的 10–20% 来自 INT 的量级总结，并非所有参数点或所有区域统一的常数。Scale/PDF 对 signed interference template 的最终相关性和逐点数值，现有 paper/INT 不足以完整重建；正文仅说明 interference 保持独立，不声称它与 BSM-only 共用某个确定 nuisance。
3. EW 段按 paper 把 approximate NLO correction 的作用作为 uncertainty；没有从通用的 additive/multiplicative/exponentiated 三种可能，虚构本分析已使用三者 envelope 或某一种作为 nominal。
4. FullJER 描述遵循 INT 声明的 FullJER prescription 和对应 PDF。未声称已逐事件复现 histogram construction。
5. `MC20_2025-06-17_GN2v01_v4.root`、tau 2025-prerec、electron 2025 map 等版本留在来源记录，正文不给大段内部 filename/NP-code inventory。若要制作可复现 NP appendix，应另以最终 branches 与 fit inputs 核对。
6. 本章没有将所有 systematic impacts 与 observed-data statistics 作新的数值排名；最终 fit 结果与 ranking 属于 CH10。

## 文件和排版变更

- `\chapter{Systematics Uncertainties}` 改为 `\chapter{Systematic Uncertainties}`：修正标题中的形容词形式，章号和原 label 不变。
- 保留两个 `\section`，新增按 INT 顺序的 `\subsection` 和 labels；它们形成编号小节并进入目录。`\subsubtitle{...}` 使用项目已有定义，显示段首粗体小标题，不新增编号层级。
- `\begin{align}...\end{align}` 排版并编号 transfer factor、variation、modifier、scale combinations 与 smoothing 公式；`\notag` 取消仅用于换行的那一行编号。
- 含数学的 W/Z 小节标题使用 `\texorpdfstring{数学标题}{纯文本}`：正文保持数学符号，PDF bookmark 使用可解析文字。
- 数值表前加 `\clearpage`，在完整介绍段之后换页，使表与后续 symmetrisation/MC-stat 说明连续排在同一页，避免浮动表插入一个句子的中间。表用 `table[!htbp]`，允许当前位置、页顶、页底或独立浮动页；`!` 放宽默认的浮动体占页比例限制；`\centering` 居中；局部 `spacing{1}` 和 `\small` 使较长 caption/表格使用单倍行距及较小字号；`tabular{lrr}` 使来源左对齐、两列数值右对齐；`\toprule/\midrule/\bottomrule` 显示 booktabs 横线。表格没有缩放数字或截断内容。
- Preview 使用项目类的 `oneside`，并通过 `\setcounter{chapter}{8}` 保留 Chapter 9 编号；`xr-hyper` 仅导入所需的 18 个前文章节 labels，`[nocite]` 不导入原论文 citation numbers；preview 自己生成 bibliography。
- Preview 的 `\clearpage` 在 bibliography 前输出浮动表格并换页；bibliography 使用 `spacing{0.9}` 与局部 `\small`，缩小行距和字号，使独立预览的参考文献紧凑呈现；不改变整篇 thesis 的 bibliography 格式。
- 原 CH9 两行中文 pile-up TODO 已由正文取代；删除注释本身不改变可见排版。

验证结果与具体输出页数另见 `CH9_validation.md`。
