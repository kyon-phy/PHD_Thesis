# CH6 重写稿：来源与取舍

2026-09-09。从 Tracks 起重写九节；前言按用户已确认的版本保留。2026-09-10 新增独立的 Object definition in the analysis 一节，并在前言的章节导航句中加入 analysis definitions。按 reconstruction → identification → isolation → calibration 安排适用的主题，以编号列表描述顺序步骤，以项目列表呈现并列输入或要求。

## 分析定义

以下内容以只读参考库 `../references/ANA_EXOT_2025_06_INT1.pdf` 的 2026-04-20 版本为准：

- §5.2 / Table 5.1：electron baseline pT > 10 GeV、|eta| < 2.47、过渡区排除、TightLH、Loose_VarRad、impact parameters；signal 额外 HighPtCaloOnly。
- §5.3 / Table 5.2：muon baseline pT > 10 GeV、|eta| < 2.5、Loose、Loose_VarRad；signal 额外 Medium、Tight_VarRad。保留 combined momentum 校准含义，不在正文列配置字符串。
- §5.4 / Table 5.3：tau baseline pT > 20 GeV、1/3 tracks、单位电荷、Loose RNN / Loose eVeto；signal Tight RNN、SR pT > 200 GeV。2026-09-10 对照后续区域表，在新增对象定义节区分 SR 的 200 GeV 与 top CR/VR 的 100 GeV；完整区域选择仍留在 CH7。低 pT muon rejection 的 2 GeV、非 calo-tagged 条件保留，并与 baseline-muon OR 分开。
- §5.4：Tight tau-ID 候选使用 Medium tau-ID 对应的 electron-rejection scale factor，正文仅陈述本分析的实际约定。未复述内部协商过程，也未声称影响可以忽略。尚无已核实的公开资料专门给出这一 scale-factor 约定，因此不附一个实际不支持该约定的公开引用。
- §5.5 / Table 5.4：EMPFlow anti-kt R=0.4、pT > 20 GeV、|eta| < 2.5、LooseBad、NNJVT FixedEffPt、GN2v01 85%；保留 JetArea → Residual → EtaJES → GSC → Insitu 的校准含义，最后一步仅用于数据。未套用其他论文中的旧 JVT 数值阈值。
- §5.6 / Table 5.5：track soft term、Tight MET 工作点。结合已核对的 TopCPTool / FastFrames 输入配置，保留轻子工作点、MET 自身 jet 选择、共享信号处理和读入已计算 MET 的区别。
- §5.7：OR 采用完整十步顺序，包括 electron–electron shared-track rejection，以及 NumTrack < 3 AND ghost association 的 jet–muon 条件。此前正文按公开论文写的不同版本已替换。
- §5.8：PV 至少两条 tracks，选最高 sum(pT²)。500 MeV 的 vertex-track 阈值由公开 taunub 论文 §5 交叉核对。

本人的 INT note，以及本分析论文 *Search for a leptoquark in events with a hadronically decaying τ-lepton and missing transverse momentum using pp collisions at √s = 13 TeV with the ATLAS detector*（arXiv:2606.02067，CERN-EP-2026-136，稿件编号 ATL-COM-PHYS-2026-015），可以提供写作所需的信息和资料，分析定义仍以 INT note 为准。但这两份文档本身永远不作为被引用的文献，也不在正文、图注或脚注中写“引用自”它们，即使已有公开版本。

采用的内容若在 note 或论文中已标注参考文献，应沿用该内容对应的原始公开文献，核对原文后直接用 `\cite{...}` 引用。保留原有的内容与文献对应关系，不因禁引 note 或本分析论文而漏掉它们引用的原始文献，也不任意替换。按文献身份匹配或复用 BibTeX key，由本论文自动编号，不照抄来源中的参考文献序号。TWiki 等内部资料仍不得引用。没有另外出处的本分析自身选择条件直接陈述，不附自引，也不用不支持该条件的公开资料替代。这里的来源记录仅供作者使用，不进入论文正文。

## 2026-09-10：对象定义与配置核对

新增 `objects/object_definition.tex`，由 `CH6.tex` 在 flavour tagging 后、overlap removal 前调用。baseline 条件集中于 Table 6.2，signal 的附加条件按对象列出。此前对象章节保留工作点的含义，移除重复的分析切选列表。所有引用仍指向已有的公开技术文献；本节的分析自身选择条件不附自引。

Obsidian 入口为 `4_Objects与DAOD/DAOD处理与Object定义.md`、`5_Histogram与Fit/FastFrames处理流程与Histogram.md`、`11_数据处理Pipeline/Pipeline_FastFrames配置用途表.md` 和 `10_来源与维护/代码版本与资料来源.md`。实际代码核对使用资料库 `11_数据处理Pipeline/源码快照/2026-09-08/` 下的：

- `TopCP/source/TauX_Gnt1makerAlg/python/TauX_Gnt1NtupleMaker.py`，以及配套的 working-point helper。另核对 `../obsidian_build/code/defaults/` 中的 electron/muon defaults 和 `tau_selection_loose_eleid.conf`。
- `FastFrame/taunub/config_taunub/config_taunub_plot_sys_1l_w_beamspot_v04.yml`：资料库标记为 PAPER 流程的背景与数据配置。
- `FastFrame/taunub/config_taunub/config_taunub_plot_sys_1l_sigs_noWeights_v04.yml`：相应信号配置。
- `FastFrame/TauXFastFrame/Root/TauXFastFrame.cc`：工作点集合与下游预选的组合方式、GN2v01 分类。

核对结果和写作取舍：

- 两份生产 YAML 的四类 baseline 预选一致。wrapper 的 electron/muon 5 GeV 和 jet 15 GeV 是上游输出阈值；最终分析使用 electron/muon 10 GeV、tau/jet 20 GeV。不能将输出阈值写成分析 baseline。
- tau 的 Loose selection 配置已包括 20 GeV、接受度、1/3 tracks、单位电荷和 Loose RNN electron rejection。C++ 将 `*_select_wpSet0_NOSYS` 与 YAML 的 `presel_*` 做逻辑 AND，因此 `tau_select_LooseRNN_noElVeto_NOSYS` 不会撤销上游 Loose electron veto。低 pT muon rejection 的精确条件按 INT note Table 5.3 陈述。
- signal electron 在 baseline 上再要求 `TightLH_HighPtCaloOnly`；signal muon 再要求 `Medium_Tight_VarRad`；signal tau 再要求 Tight RNN。并非把 baseline 选择替换成另一集合。额外保存的 HighPt muon ID、其他 b-tagging 工作点等没有自动成为本分析选择。
- INT note §7.2 / Table 7.2 支持 top CR 中 tau 100 GeV、electron/muon 28 GeV；Table 7.4 支持 top VR 中 tau 100 GeV；WCR 与单轻子零 tau 区域使用 electron/muon 200 GeV；SR 使用 tau 200 GeV。两份 YAML 的相关区域选择与这些数值一致。旧 YAML 的部分 `WVR_1tau0l0b_*` 名称不直接用作论文中的最终区域名称。
- jet 使用共同 baseline 集合，没有另一个 signal jet ID 工作点。区域中用于分类的 jet 有 resonant 250 GeV 或 non-resonant 50--250 GeV 要求；不能将这些阈值施加到所有计数用的 baseline jets。GN2v01 85% 用于 b-jet 子集。具体选哪个 jet、multiplicity 和 trigger matching 留在 CH7。
- 逐项确认前文已介绍 TightLH、Loose/Medium muon ID、Loose_VarRad、HighPtCaloOnly、Tight_VarRad、tau Loose/Medium/Tight RNN、Loose electron rejection、LooseBad、NNJVT FixedEffPt 和 GN2v01 85%。未新增未经原始资料确认的工作点效率或 isolation 数值公式。

版本边界：9 月 7 日与 9 月 8 日的相关 wrapper 和背景 YAML 快照逐字一致，但这不独立证明历史 ntuple 生产版本；如需追溯某批样本，应查该批的 MetadataTauX 和生产日志。另有 scale-factor 实现问题留待权重章节核查：当前 C++ 的 tau 权重组合含 Medium RNN ID/reconstruction 与 Loose electron-rejection SF，而 INT note 明确讨论 Tight 候选使用与 Medium tau ID 对应的 electron-rejection SF。这些名称不能与 Tight 事件选择混同。本次不改写权重实现，tau calibration 的分析约定仍以 INT note 为准。

## 博士论文的实际参考范围

库中七篇 phD 开头的论文都已查看相关段落。使用其解释层次和适合本分析的呈现方法，独立组织英文，不照搬句子或采用其他分析的数值工作点：

- `phD2020_yang.pdf`：PDF pp.45、50、57，track 步骤、muon 类型、tau-veto 的分析相关性。
- `phD2022_tateno.pdf`：PDF pp.41–42，track/PV 和 supercluster 的分步说明。
- `phD2022_oishi.pdf`：PDF pp.39–42，tracking、topocluster、particle flow 和分阶段 jet calibration。
- `phD2024_aoki.pdf`：PDF pp.62–65，对象重建层次、track/PV 解释。
- `phD2024_sugizaki.pdf`：PDF pp.71–72，electron 的信号机制、工作点和性能图的安排。
- `phD2024_zhang.pdf`：PDF pp.53–54、58，重建步骤、主题小标题、muon 类别和 isolation 解释。
- `phD2025_tanaka.pdf`：PDF pp.58–62，简短开头、分级对象要求及 jet calibration 列表。

不同论文的代际和定义不能混用。比如 electron seed clustering 有 sliding-window / supercluster 的区别，部分参考论文对 anti-kt 的描述也不够准确；本稿分别按公开 Run-2 supercluster 文献和 anti-kt 原始论文核实。

## 公开技术依据

BibTeX 保留 15 条正文实际使用的公开参考文献。主要用途如下：

- 1704.07983 §3：silicon cluster / space point、Kalman track finding、ambiguity resolution。
- ATL-PHYS-PUB-2015-026：vertex reconstruction。本分析的 PV 选择条件直接陈述，不引用本人的分析论文。
- 1908.00005 §4：supercluster；1902.04655 §6：electron likelihood；1908.00005 的 calibration / efficiency 部分：electron corrections。
- 2012.00578：muon reconstruction / identification / isolation；2212.07338：momentum calibration。
- ATL-PHYS-PUB-2022-044 §§4–6、8 和 Table 4：tau vertex、track RNN、ID RNN、electron rejection、TES。Table 4 的 Loose 1p/3p 为 85%/75%，未使用该文末 summary 中不一致的 3p 数字。ATL-PHYS-PUB-2019-033 补充 RNN 输入与机制。
- 1603.02934：topological clusters；1703.10485 §6：particle flow；0802.1189 §2：anti-kt；2007.02645 §§4–5：jet calibration。
- 2505.19689v2：GN2 transformer、辅助任务、四分类输出、discriminant、working-point 定义与校准。没有把 GN1 或 DL1r 的具体实现搬到本分析。
- 2402.05858v2：MET hard / track-soft terms、association map、soft-term response / resolution uncertainties。

GN2 的 untagged weight 公式是由互补概率给出的单 jet 说明，不将它声称为实际 ntuple 中 continuous flavour-tagging 权重的完整实现。

## 配图出处

五张图均来自公开 ATLAS 原始文献，图注含直接引用。没有使用其他博士论文独有的分析结果图。

- `track_parameters`：ATLAS, *Software and computing for Run 3 of the ATLAS experiment at the LHC*, EPJC 85 (2025) 234，DOI 10.1140/epjc/s10052-024-13701-w，Fig.16，PDF p.40。与 Aoki Fig.6.3 为同款示意图，直接从公开期刊论文裁取。图注将灰平面说明为参考 z=0 平面，正文与图中统一使用 phi；保留正文 z0 与相对于 PV 的 Delta z0 的区别。裁取坐标记录于 `tmp/ch6_track_figure/source.json`。
- `electron_superclusters`：1908.00005 Fig.3，PDF p.12，保留上方 electron 相关示意部分。
- `tau_identification`：ATL-PHYS-PUB-2022-044 Fig.7，PDF p.14，取左列两个 pT 面板并左右排列，分别为 1-prong 和 3-prong；未改变数据、轴或图例。
- `tau_energy_resolution`：同一公开文献 Fig.17，PDF p.31，保留上方两个 pT 面板；图注明确性能图使用 Medium ID。分析 signal 的 Tight ID 条件集中于对象定义节。
- `gn2_architecture`：2505.19689v2 Fig.1，PDF p.3。

保留裁取的 PDF 源图，并由其高分辨率渲染生成正文使用的 PNG。这样避免源 PDF 字体与论文模板字体合并产生的警告；图像内容不变。每个 section 最多两张图。

## 检查与交付

- `objects/` 中包含十个独立文件；`CH6.tex` 仅保留前言和十条 `\input`。整章展开的 TXT 与合并脚本已移至 `tmp/ch6_layout_before/`，后续直接编辑对象文件。
- 主论文前面已定义的 ID、MS 和 MET 记号直接复用，现有单位、过程和运动学宏保持一致。
- 对照 INT note 检查数值与工作点；独立检查完整正文、公式、标签和公开引用。
- 2026-09-10 阅读版为 19 页（正文 17 页、参考文献 2 页），5 张图、2 张表、15 条引用。track-parameter 示意图为 Fig.6.1；新增定义节为 §6.8、baseline 定义为 Table 6.2。已检查整章缩略图和新增内容的完整页面，且编译无未定义引用或 overfull box。2026-09-09 已检查全部 35 个现行 TeX/Bib 文件及重新编译的第六章和主论文 PDF，确认不存在本人的 INT note、上述分析论文或 TWiki 引用；本次新增正文没有引入这些引用。
- 正式 `Chapters/CH6_object_definition.tex` 与只读参考库未修改。
- 过程快照、段落清单、来源核查及编译记录位于 `tmp/ch6_rewrite_review/`。未调用独立 reader agents。

## 2026-09-11：electron isolation 工作点的数值要求

按用户要求，在 electron isolation 段中明确本文使用 Loose_VarRad 和 HighPtCaloOnly，并补充其主要阈值。INT note §5.2 和 TauX wrapper 确认工作点选择。公开 Athena `release/25.2.51` 的 `PhysicsAnalysis/AnalysisCommon/IsolationSelection/Root/IsolationSelectionTool.cxx`（253--266 行）确认：Loose_VarRad 的 track 和 calorimeter 上限为电子 pT 的 15% 与 20%，HighPtCaloOnly 的 calorimeter 上限为 max(0.015 pT, 3.5 GeV)。同版本 `IsolationConditionFormula.cxx` 确认公式自变量取候选电子的 pT。两份源码只读下载至 `tmp/ch6_sources/`。

原始公开文献 1908.00005 §8.1 / Table 2 支持这些阈值，继续使用 `ATLAS2019ElectronPerformance`。该文的 Loose track cone 名称为 varcone20，而上述软件版本的 Loose_VarRad 使用 `ptvarcone30_Nonprompt_All_MaxWeightTTVALooseCone_pt1000`；正文只补充已核对一致的数值比例，不将旧文献的 cone size 搬到当前工作点。baseline 与 signal 的叠加关系仍在对象定义节说明。
