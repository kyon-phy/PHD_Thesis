# CH6 重写稿：来源与取舍

2026-09-09。从 Tracks 起重写九节；前言按用户已确认的版本逐字保留。按 reconstruction → identification → isolation → calibration 安排适用的主题，以编号列表描述顺序步骤，以项目列表呈现并列输入或要求。

## 分析定义

以下内容以只读参考库 `../references/ANA_EXOT_2025_06_INT1.pdf` 的 2026-04-20 版本为准：

- §5.2 / Table 5.1：electron baseline pT > 10 GeV、|eta| < 2.47、过渡区排除、TightLH、Loose_VarRad、impact parameters；signal 额外 HighPtCaloOnly。
- §5.3 / Table 5.2：muon baseline pT > 10 GeV、|eta| < 2.5、Loose、Loose_VarRad；signal 额外 Medium、Tight_VarRad。保留 combined momentum 校准含义，不在正文列配置字符串。
- §5.4 / Table 5.3：tau baseline pT > 20 GeV、1/3 tracks、单位电荷、Loose RNN / Loose eVeto；signal Tight RNN、SR pT > 200 GeV。对照后续区域表，其他区域阈值留在 CH7。低 pT muon rejection 的 2 GeV、非 calo-tagged 条件保留，并与 baseline-muon OR 分开。
- §5.4：Tight tau-ID 候选使用 Medium tau-ID 对应的 electron-rejection scale factor，正文仅陈述本分析的实际约定。未复述内部协商过程，也未声称影响可以忽略。尚无已核实的公开资料专门给出这一 scale-factor 约定，因此不附一个实际不支持该约定的公开引用。
- §5.5 / Table 5.4：EMPFlow anti-kt R=0.4、pT > 20 GeV、|eta| < 2.5、LooseBad、NNJVT FixedEffPt、GN2v01 85%；保留 JetArea → Residual → EtaJES → GSC → Insitu 的校准含义，最后一步仅用于数据。未套用其他论文中的旧 JVT 数值阈值。
- §5.6 / Table 5.5：track soft term、Tight MET 工作点。结合已核对的 TopCPTool / FastFrames 输入配置，保留轻子工作点、MET 自身 jet 选择、共享信号处理和读入已计算 MET 的区别。
- §5.7：OR 采用完整十步顺序，包括 electron–electron shared-track rejection，以及 NumTrack < 3 AND ghost association 的 jet–muon 条件。此前正文按公开论文写的不同版本已替换。
- §5.8：PV 至少两条 tracks，选最高 sum(pT²)。500 MeV 的 vertex-track 阈值由公开 taunub 论文 §5 交叉核对。

这些内部来源仅作为研究记录。正文和 BibTeX 中均不引用 INT note 或 TWiki。

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
- ATL-PHYS-PUB-2015-026：vertex finding / fitting；2606.02067v1 §5：公开分析对象与 PV 描述。
- 1908.00005 §4：supercluster；1902.04655 §6：electron likelihood；1908.00005 的 calibration / efficiency 部分：electron corrections。
- 2012.00578：muon reconstruction / identification / isolation；2212.07338：momentum calibration。
- ATL-PHYS-PUB-2022-044 §§4–6、8 和 Table 4：tau vertex、track RNN、ID RNN、electron rejection、TES。Table 4 的 Loose 1p/3p 为 85%/75%，未使用该文末 summary 中不一致的 3p 数字。ATL-PHYS-PUB-2019-033 补充 RNN 输入与机制。
- 1603.02934：topological clusters；1703.10485 §6：particle flow；0802.1189 §2：anti-kt；2007.02645 §§4–5：jet calibration。
- 2505.19689v2：GN2 transformer、辅助任务、四分类输出、discriminant、working-point 定义与校准。没有把 GN1 或 DL1r 的具体实现搬到本分析。
- 2402.05858v2：MET hard / track-soft terms、association map、soft-term response / resolution uncertainties。

GN2 的 untagged weight 公式是由互补概率给出的单 jet 说明，不将它声称为实际 ntuple 中 continuous flavour-tagging 权重的完整实现。

## 配图出处

四张图均来自上述公开 ATLAS 原始文献，图注含直接引用。没有使用其他博士论文独有的分析结果图。

- `electron_superclusters`：1908.00005 Fig.3，PDF p.12，保留上方 electron 相关示意部分。
- `tau_identification`：ATL-PHYS-PUB-2022-044 Fig.7，PDF p.14，取左列两个 pT 面板并左右排列，分别为 1-prong 和 3-prong；未改变数据、轴或图例。
- `tau_energy_resolution`：同一公开文献 Fig.17，PDF p.31，保留上方两个 pT 面板；图注明确性能图使用 Medium ID，分析 signal 使用 Tight ID。
- `gn2_architecture`：2505.19689v2 Fig.1，PDF p.3。

保留裁取的 PDF 源图，并由其高分辨率渲染生成正文使用的 PNG。这样避免源 PDF 字体与论文模板字体合并产生的警告；图像内容不变。每个 section 最多两张图。

## 检查与交付

- `sections/` 中包含九个 section 文件；`CH6_draft.tex` 为输入入口；`CH6.txt` 为全部展开的 LaTeX 文本。
- 主论文前面已定义的 ID、MS 和 MET 记号直接复用，现有单位、过程和运动学宏保持一致。
- 对照 INT note 检查数值与工作点；独立检查完整正文、公式、标签和公开引用。
- 阅读版为 18 页（正文 16 页、参考文献 2 页），4 张图、1 张表、15 条引用。已检查所有页面的排版，并放大检查配图。
- 正式 `Chapters/CH6_object_definition.tex` 与只读参考库未修改。
- 过程快照、段落清单、来源核查及编译记录位于 `tmp/ch6_rewrite_review/`。未调用独立 reader agents。
