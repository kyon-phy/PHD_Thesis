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

## 2026-09-11：各对象节中的分析工作点

按用户最终明确的范围，本轮只在各对象的介绍处保留 identification/isolation working point 及 baseline/signal 对应关系的补充。后面的对象定义节继续汇总原有的完整选择条件。

- 再次核对 INT note §§5.2--5.8 / Tables 5.1--5.5，以及本分析论文 arXiv:2606.02067v1 的对象定义和单轻子区域说明。electron 使用 TightLH，baseline 使用 Loose_VarRad，signal 额外要求 HighPtCaloOnly；muon 使用 Loose / Loose_VarRad，signal 额外要求 Medium / Tight_VarRad；tau 使用 Loose RNN，signal 额外要求 Tight，二者都保留 Loose electron rejection。
- 已撤回本轮增加的非 WP 内容：electron calorimeter quality 说明、tau 的 prong/电荷选择与低 pT muon rejection 的具体阈值，以及 PV 轨迹数和 pT 要求。原来已有的说明和对象定义表保留。
- 已撤回新增的 inside-out combined 条目和关于本分析接受 IO/ST/CT 的断言，保留用户原有的 combined-muon 使用说明并修正措辞。公开文献的工作点定义与配置快照只能支持有条件的类别推断，尚未直接核对实际生产版本或样本中的类别组成。Muon calibration 的非 WP 改写也已还原。
- jets 已写明 particle-flow anti-kt R=0.4、LooseBad、NNJVT FixedEffPt；flavour tagging 已写明 GN2v01 85%；MET 已写明 track soft term 和 Tight operating point，因此保留原文。没有为通用 tracks 杜撰一个全分析共用的独立 track-quality working point。

以上分析自身选择条件不附自引，内部来源仅记录于此。此次为多处局部补充，没有启动独立读者或全章审阅。

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

## 2026-09-11：WP 选择句后的具体条件

用户进一步要求：每处先用短句说明分析选择，再简述 WP 本身的条件及物理区别。此次增补限于 WP 定义，没有新增独立的事件选择。实际 WP 选择继续以 INT note §§5.2--5.8 / Tables 5.1--5.5 和已有配置核查为依据。

- Electron TightLH：1902.04655 §6.3 支持随 et/eta 变化的 likelihood 阈值、最内层 pixel hit 要求及失效层例外，以及 et > 150 GeV 时采用 Medium likelihood 阈值并增加 E/p < 10 和第一层 EM shower-width 条件。Electron isolation 已有具体上限，保留。
- Muon ID：2012.00578 §§5.1.1--5.1.2 支持 precision station 的至少三个 MDT/CSC hits 定义、Medium 的两站要求及中心区域例外、q/p significance < 7，以及 Loose 在 |eta| < 0.1 额外接受 CT/ST。正文明确 combined candidates 在两种 WP 下共享上述主要质量条件，不能把 q/p < 7 描述成 Medium 相对 Loose 的新增 cut。这里描述的是标准 WP 定义，没有推断分析样本中的 IO/ST/CT 组成。
- Muon isolation：2012.00578 §5.2 / Table 2 与公开 Athena release/25.2.51 的 `IsolationSelectionTool.cxx` 168--175 行均支持 Loose_VarRad 的 track/calo 上限 15%/30% 和 Tight_VarRad 的 4%/15%。保留 variable track cone，补充 calorimeter cone 0.2。
- Tau：ATL-PHYS-PUB-2022-044 的 RNN identification 说明和 Table 4 支持逐渐提高分数阈值及既有目标效率；electron-rejection 部分支持分别针对 1-prong/3-prong 的 RNN 分数条件。没有从性能曲线臆定 Loose eVeto 的具体效率。
- Jets：LooseBad 的单层能量比例 > 99%、|eta| < 2 拒绝条件由公开 Athena release/25.2.51 的 `JetCleaningTool.cxx` 258 行确认；对应公开 jet-cleaning 文献为 ATLAS-CONF-2015-029。`NNJvtSelectionTool.cxx` 13、52、58 行确认 FixedEffPt 配置及按 jet pT/eta 取 score 阈值；`JetVertexNNTagger.cxx` 确认基于顶点关联的轨迹变量。正文为 NNJVT cut 直接引用固定版本的公开源码，没有将旧 JVT 阈值当作 NNJVT 阈值。
- GN2v01：2505.19689v2 支持由模拟 ttbar 样本中 b-jet 效率定义固定分数阈值。保留本分析的 85% 选择和信号样本效率可能不同的解释。
- MET Tight：2402.05858 的 WP 表和公开 Athena release/25.2.51 的 `METMaker.cxx` 109--110、160--163、711--716 行均支持 central 20 GeV、forward 30 GeV、分界 |eta| = 2.5 和接受度 4.5。旧论文使用的 JVT 数值没有移植到当前 NNJVT。这里只补充 MET WP 自身的 jet 条件，不改变区域 jet 选择。

源码下载保存在 `tmp/ch6_sources/`，仅用于定义核查，不构成实际生产软件版本的证明。六个对象文件修改前的快照在 `tmp/wp_conditions_before_20260911/`。

## 2026-09-11：WP 的 efficiency 和 rejection 数值

按用户要求，为能够明确量化的 WP 补充效率和背景 rejection。数值为所引文献的指定样本性能，不是本分析的总信号效率。分析 WP 仍按 INT note §§5.2--5.8 和相关分析论文对象定义核对，没有变更选择。本文使用的 rejection factor 为背景通过率的倒数。

- **Electron ID：**新增原始公开性能论文 2308.13362v2（JHEP 05 (2024) 162），Table 1 / PDF p.29。在 20 < et < 50 GeV 的模拟样本中，Tight 的 reconstructed Z→ee signal efficiency 为 78.59%，inclusive QCD reconstructed-electron background efficiency 为 0.455%。正文取约 79%、0.46% 和 rejection ≈ 220（100/0.455）。这是 ID 相对重建候选的效率，不能误写成原始 jet 到 electron 的总 rejection。没有沿用旧论文相对 Loose 的 3.5 或 5 倍提升来充当绝对 rejection。
- **Electron isolation：**2308.13362v2 Table 2 的 Loose_VarRad 使用 varcone30，和已有软件核对一致。Fig.18 / PDF p.33 的 2018 Z→ee 数据、Medium ID 条件下，Loose_VarRad 在 50 < et < 500 GeV 效率 >99%，HighPtCaloOnly 在 100 < et < 500 GeV 约 90--95%。这些是分别测量的单项隔离效率，不是本分析 TightLH + 两项 isolation 叠加后的总效率。该文没有给出可直接用于这两项 WP 的背景 rejection 数值，未推断或补造。
- **Muon ID：**2012.00578v2 Table 1 / PDF p.15，20 < pT < 100 GeV、|eta| < 2.5 的 ttbar 模拟中，相对 truth-matched ID tracks 的 Loose/Medium prompt-muon reconstruction+ID efficiencies 为 99%/97%，light-hadron misidentification rates 为 0.25%/0.17%。正文 rejection 取约 400/600。此处量化标准 WP 的完整接受度，不是仅对 combined 类别的效率。
- **Muon isolation：**采用公开性能图 MUON-2024-01 Fig.03（2024-05-24），其标签明确为 Loose_VarRad/Tight_VarRad。图中约 95%/86% 的 prompt-muon efficiencies 对应 non-prompt rejection ≈20/60。条件为 13/13.6 TeV 的 ttbar 模拟、Medium ID、vertex association、pT > 10 GeV、|eta| < 2.5；正文明确这些条件。图页的 vertex-association 公式存在排版问题，正文只保留物理条件名称，没有复制问题公式。2012.00578 Table 3 使用在 pT > 50 GeV 固定 R=0.2 的版本，不能把其高 pT 性能直接用于 VarRad，因此未采用该表数值。
- **Tau ID：**ATL-PHYS-PUB-2022-044 Table 4 保留既有效率。新增 rejection 来自 Fig.6 / PDF p.13 的 13 TeV、pT ≥20 GeV、dijet background ROC，按 Loose/Medium/Tight 顺序，1-prong 约 15/25/50，3-prong 约 90/230/600。表中和 caption 均注明近似值与运动学依赖；没有把 Fig.8 不同 pT 或 pile-up bin 的 rejection 当作同一组 inclusive 数值。
- **Tau electron veto：**同文 Fig.12 / PDF p.22，Loose 的 1-prong/3-prong efficiency 标记位于 95%/98%，对应 electron rejection 约 300/80，使用 γ*→ττ signal 和 Z→ee background 模拟。按该图的 Loose 标记读值，没有将文中“95% 时 rejection 300/200”的泛用性能点同时当作两个 prong 的 Loose WP。
- **GN2v01 85%：**2505.19689v2 Fig.4 / PDF p.7 的 Run-2 校准后点，20 < jet pT < 250 GeV、|eta| < 2.5、含至少一个 reconstructed electron/muon 的 ttbar 模拟加数据校准，light-jet/c-jet rejection 约 70/6。没有将 Fig.2 的 13.6 TeV 未校准曲线值与 Run-2 校准后数值混合。
- **LooseBad：**ATLAS-CONF-2015-029 的公开摘要给出 collision-jet efficiency >99.5%（pT >20 GeV）和 >99.9%（pT >100 GeV）。没有找到在同一明确背景定义下可直接采用的单一 rejection 数值。
- **NNJVT FixedEffPt：**搜索到 ATLAS triple-Higgs paper 2411.02040 报告 NNJVT hard-scatter efficiency 88--99%（20 < pT <60 GeV，Z→μμ+jets，mean pile-up 33.7），但该段没有明确 WP 名称，也没有完整配套 rejection，暂未把它当作 FixedEffPt 的定量定义写入正文。另一个公开论文为 FixedEffPt 引用的 1510.03823 是旧 JVT，不能替代 NNJVT 的性能数据。
- **MET Tight：**为 MET 输入 jet 的选择方案，2402.05858 用 response、resolution 和具体 event selections 的效率评价其性能；没有将某一事件级效率写成通用的对象 WP efficiency/rejection。

本轮新增资料保存在 `tmp/ch6_sources/electron_eff_run2.pdf`、`muon_plit_public.html`、`muon_varrad_roc.pdf`；查阅页面的渲染图位于 `tmp/wp_efficiency_figures/`。修改前的对象文件保存在 `tmp/wp_efficiencies_before_20260911/`。用户并行删除的 electron ID 具体 hit/high-et 条件未恢复。

验证：CH6_preview 使用 MacTeX/latexmk 编译通过，20 页，没有未定义引用或 overfull box。扩展后的 tau 表及受影响段落已渲染检查。首次编译发现用户正在编辑的 calibration 句中 `\Zee` 宏未定义，仅将其拼写改为项目已定义的 `\zee`，保留其余文字。

### 后续精简（用户最新要求）

正文的 WP 性能说明已压缩为近似效率，删除本轮 rejection 数值和详细 benchmark 条件，tau 表恢复为只列效率。Electron ID 取整为约 80%，electron isolation 保留“high et”限定，tau electron veto 保留 prong 区别。完整来源、定义和适用范围仍保存在上面的核查记录中。此前已接受的 WP 条件和方法解释保留。

### 2026-09-11：NNJVT FixedEffPt 的 score 与目标效率

已直接读取公开 calibration JSON `JetPileupTag/NNJvt/2022-03-22/NNJVT.Cuts.FixedEffPt.Offline.Nonprompt_All_MaxW.json`，正文使用 `ATLASNNJVTFixedEffPt` 引用。这补足了此前仅凭其他分析论文未能确定 FixedEffPt 数值的问题。公开 Athena release/25.2.51 的 `NNJvtSelectionTool.h` 指定上述目录，`.cxx` 将 FixedEffPt 映射到该文件，选择条件为 score 严格大于相应 cut。

资料库 TopCP wrapper `JvtExtraFlagConfig.py` 为选择和效率工具均设置 `MaxPtForJvt = 60*GeV`。结合本分析 jet pT > 20 GeV、|eta| < 2.5，适用 JSON 的前四个 pT bin，score 阈值最小 0.07、最大 0.75，`ptbin_eff` 为 0.88、0.92、0.96、0.98。正文给出阈值范围 0.07--0.75 和目标 hard-scatter jet 效率 88--98%，不是单一固定阈值或本分析信号样本的实测效率。第五个 bin 从约 62.04 GeV 开始，其 99.5% 目标和最低 0.05 阈值未纳入本分析所用范围。原始 JSON 与工具头文件保存在 `tmp/ch6_sources/`。

### 2026-09-11：tau electron rejection 的动机及 muon rejection 核对

- ATL-PHYS-PUB-2022-044 §6（PDF p.16）明确说明电子可被误识别为 tau，尤其与 one-prong 候选的探测器特征相似。正文在 Loose electron-rejection WP 之前补充窄簇射及关联轨迹造成混淆的原因，原有 WP 条件和近似效率保留。
- 已确认 tau--muon overlap removal：本分析论文 §5 明确列出该步骤；资料库 TopCP 的 `TauX_Gnt1NtupleMaker.py:438--450` 为所用 WP 集合接入 tau 与 muon 容器；`defaults/OverlapAnalysisConfig.py:77` 默认启用 `doTauMuOR`，398--406 行配置 `TauMuORT` 及 DR=0.2；`OverlapRemovalTool.cxx:108` 对 taus、muons 按此顺序调用，重叠时移除 tau。现有 defaults 使用 rapidity 距离，与正文 overlap-removal 节的定义一致。tau identification 中的泛称已改为对该 overlap-removal 步骤的明确交叉引用。
- 需区分已确认的 overlap removal 和额外低-pT veto：INT note Table 5.3（PDF p.25）另写有 pT(mu)>2 GeV、排除 calorimeter-tagged muons 的要求；但本次查看的 `tau_selection_loose_eleid.conf` 未列出独立 muon-veto cut，TopCP 快照也未直接展示该额外步骤。因此“2 GeV 且非 calo-tagged 的独立 veto 已在生产中确认”不能由当前代码证据推出。它也可能在其他重建或生产阶段实施，不能据未找到就断言未使用。对象定义表及 overlap-removal 节已有的额外低-pT 条件仍仅依据 INT note，本轮未改动这些未被选中的段落；若需确认实际生产，应继续核对对应批次的配置或元数据。

### 2026-09-11：按用户要求补充 Loose electron-rejection efficiency

重新查看 ATL-PHYS-PUB-2022-044 Figure 12（PDF p.22）：Loose eVeto 的 one-prong / three-prong 标记分别约为 tau efficiency 95% / 98%，electron rejection factor 300 / 80。该图定义 rejection factor 为背景通过率的倒数。正文按用户所问的 rejection efficiency 写被拒绝的比例，即 1 - 1/R，分别约 99.7% / 98.8%，不把 rejection factor 直接写成百分数。数值由图中的近似 rejection factor 换算，原图使用 Z→ee 电子背景与 γ*→ττ 真 tau 模拟，并非对所有电子或任意分析样本的普适精确效率。正文仅补这一简短数值说明，未扩展其他 WP。
