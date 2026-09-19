# CH6 草稿的来源与待确认项

2026-09-08。正文按当前 `Chapters/CH6_object_definition.tex` 的九节顺序起草，使用英式科学英语。草稿单独保存在本目录，尚未替换正式章节。`CH6_references.bib` 是本稿新增引用，`CH6_preview.tex` 用现有 thesis class 和 preamble 生成阅读版。

## 来源如何使用

- **分析定义与技术约定**：`../references/ANA_EXOT_2025_06_INT1.pdf`，2026-04-20，PDF 第 23–26 页，§5.2–5.7 和 Tables 5.1–5.5。封面 Draft 0.5 与 changelog v0.9 不一致，因此以日期和位置识别版本。用它确定 baseline/signal object、各 working point、校准、tau eVeto SF 约定。
- **taunub 正文**：[arXiv:2606.02067v1](https://arxiv.org/abs/2606.02067v1)，PDF 第 6–7 页 §5、第 9 页 §7。已对照本地公开 PDF 和 2026-05-26 的 ATL-COM-PHYS-2026-015 Draft 3.3；网络页面确认公开文件目前列为 v1。用它核对对象选择、PV、公开 OR 顺序及控制区轻子定义。
- **Obsidian 整理**：读取了“文献中的对象定义与预选”“分析版本差异与待核实事项”“DAOD处理与Object定义”“Overlap removal与MET实现”，以及“高能物理博士论文写作框架”和 Sugizaki/Aoki/Zhang 三篇总结。进一步阅读三篇原论文对应的标准对象与 track/vertex 段落，仅采用共同的解释层次：探测器信号 → 重建 → identification/calibration → 本分析定义。没有沿用其中某一篇的句式或分析工作点。
- **τ 的详细技术依据**：ATL-PHYS-PUB-2022-044，§4（production vertex、track classifier）、§5（tau RNN）、§6（electron rejection）、§8（TES），并参考 ATL-PHYS-PUB-2019-033 的 RNN 原理。CDS 全文下载遇到访问限制后，从 INSPIRE 的 CDS 文档镜像取得并核对了完整原文。工作点数字另核对了 ATLAS 官方网页上的 Table 4。
- **其他背景原理**：追踪 1704.07983；电子 1902.04655、1908.00005；μ 2012.00578、2212.07338；topocluster 1603.02934；particle flow 1703.10485；anti-kt 0802.1189；JES 2007.02645；GN2 2505.19689v2；MET 2402.05858v2。均阅读了相应技术内容，BibTeX 的期刊和 DOI 已核对。

## 需要保留的几个物理区别

1. **τ production vertex 与 decay vertex**：taunub paper 的简述容易被读成从核心 tracks 直接重建 decay vertex。标准 TJVA 选择的是 τ 的 production vertex，三轨迹 secondary vertex 才描述 decay position。正文已按官方重建文献区分。
2. **τ 工作点效率**：Table 6.1 使用 2022-044 Table 4 的 Loose 85%/75%、Medium 75%/60%、Tight 60%/45%（1p/3p）。该 note 的末尾 summary 对 Loose 3p 出现 85% 的不一致写法，本稿采用定义表，且明确这些不是完整事件接受率。
3. **eVeto SF**：INT note §5.4 明确 Tight tau-ID 使用 Medium tau-ID 对应的 eVeto SF。正文保留这一分析约定，并说明选择仍为 Tight tau-ID + Loose eVeto。没有将其表述为一般 ATLAS 通用规则，也没有自行量化其结果影响。
4. **GN2 与 GN1**：依据 GN2 正式技术论文，正文称 GN2 为 transformer-based tagger，解释 track-origin 和 vertex-grouping 辅助任务。没有把 GN1 的具体网络结构直接搬给 GN2。
5. **85% 与 0b**：85% 是模拟 ttbar 参考样本上的 inclusive working point，不是高-pT U1 b-jet 的恒定效率。untagged 权重公式是从互补概率推导的概念说明，不声称生产使用简单逐 jet 二分类权重；当前快照保存 Continuous flavour-tagging 校准。
6. **MET**：正文区分分析 OR 和 MET association map，区分 central analysis jets 与 MET jet term。`Tight` MET WP、tau-ID `Tight`、以及具体 high-pT signal thresholds 是不同层级的要求。没有把正式 SR surviving objects 当成 MET 的全部输入。

## OR 的版本核对仍需完成

正文的 Table 6.2 **明确标为公开论文报告的顺序**，并在 caption 标记版本问题。以下尚不能仅靠当前代码认定为发布时 production 的事实。

- **electron–electron**：INT note §5.7 额外列出共享 track 时删低-pT electron；公开 paper 未列；当前 OverlapAnalysisConfig 默认没有启用这一独立步骤。未将它无条件加入正文表。
- **muon–jet**：公开 paper 写 ΔRy<0.4 且最多 2 tracks 时删 jet；INT note 写少于 3 tracks 且 ghost-associated。已读取的 AnalysisBase 25.2.51 默认实现是少于 3 条 `NumTrkPt500` tracks，且满足 **ghost association 或 ΔRy<0.2**，随后在 0.4 外锥删除与 surviving jet 重叠的 muon。三种表述不能直接当成逐字等价。若最终以生产代码为准，应将正文第 7 行替换成已核实的实现，并在正文定义 ghost association。
- **tau-specific muon rejection**：INT note Table 5.3 提到非 calo-tagged、pT>2 GeV 的 muon。它和 general OR 中 baseline muon 的 pT>10 GeV 条件不同。本稿未声称两者完全相同，也未将 2 GeV 阈值当作通用 baseline 定义。仍应以 production tau tool 和 metadata 确认。

这些差异已用 Obsidian 的源码指引核对本地 `obsidian_build/code/defaults` 中的 OverlapAnalysisConfig.py、OverlapRemovalTool.cxx 和 MuJetOverlapTool.cxx。当前 checkout 的 release 与 INT note §5.1 的 25.2.51 一致，但仍不构成完整 production provenance。后续需要对应 ntuple 的 `metadataTauX`、生产配置和日志。草稿没有改动任何分析代码。

## 与现有论文衔接

CH4 当前把 ΔR 定义为 eta–phi，并笼统说用于 OR。CH6 已用 ΔRy 明确 rapidity–phi 距离，以免把二者混用。合入时建议只调整 CH4 那一句适用范围。CH7/CH8/CH9 当前多数仍是框架，本稿仅引用其既有 chapter labels，没有填入未经核对的 region thresholds 或背景估计方法。

NNJVT 的具体有效 pT/eta 范围和 MET jet selection 的完整数值未从其他年份的性能论文移植。本稿保留本分析的 working point 名称与物理目的，后续若需要逐项复现表，再从 production 所用 CP calibration/config 补齐。

本目录附带可编辑的 LaTeX、独立 BibTeX 和预览入口。正式合入时，把 `CH6_draft.tex` 内容放入现有 CH6，并将新增文献合并到 `References/references.bib`；本次没有执行这一步。

## 阅读版检查与编译

阅读版为 `output/pdf/CH6_draft.pdf`，16 页（正文 14 页、参考文献 2 页），含 9 节、2 张表和 16 条引用。已检查所有页面的渲染，两个表格置于相关概念说明之后；最终编译无未定义引用、无 overfull box。外部章节与 CH4 公式编号从当前主论文 aux 导入，仅供独立预览。正式章节内容与主 bibliography 未改动。

从论文项目根目录编译：

```bash
/Library/TeX/texbin/latexmk -pdf -cd- -interaction=nonstopmode -halt-on-error -outdir=output/ch6/build output/ch6/CH6_preview.tex
cp output/ch6/build/CH6_preview.pdf output/pdf/CH6_draft.pdf
```
