# 第八章：来源、取舍与待确认项

## 使用的版本

- INT reference PDF：`../references/ANA_EXOT_2025_06_INT1.pdf`，印刷日期 20 April 2026。正文第 7、8、10 章及 Appendix D、F、G、M。
- 可编辑 INT 源文件（只读使用）：`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/sections/`。其中 BG_Estimation.tex、DataMC_Comparison.tex、Appendices/ZVR.tex、CRstudy.tex、VRstudy.tex、1tau0l1b_VR_Study.tex。
- Paper：`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/paper_draft/ANA-EXOT-2025-06-PAPER/sections/background.tex` 与 results.tex。
- Journal 回复：`../references/Taunub Journal review.pdf`，第 3–4 页。
- ATLAS circulation 回复：`../references/Taunub ATLAS circulation comments.pdf`，第 6–7、26、28–29、34–35、39–40 页。
- 三篇参考 thesis 仅用于共同的说明深度：先定义约束和转移，再以独立区域检查假设。未沿用其具体方法、文字或特殊结构。

以上分析文件和回复只用于事实核对，不在论文正文或图注中自引。

## 章节对应关系

- 8.1：INT 第 7/10 章、paper background/results，以及 circulation 关于 MC 归一化、单 bin 计数和其余背景在不确定度内变化的回复。保留四个归一化参数，不展开第十章的 likelihood。
- 8.2：INT WCR 定义与 N−1 图、Appendix F 的 e/μ 比较。1.25±0.09、1.08±0.08、1.00±0.09、0.80±0.08 是 data/total MC，并非拟合 W 因子。电子 80–100 GeV 波动、约 30 权重的单个 muon MC 事件按来源限定，不将来源中猜测的 pile-up 解释写成结论。
- W→τν 额外中微子：Journal 第 3 页回答用低质量 W→τν 区域验证。正文说明模拟保留 τ 衰变导致的 visible pT 和 MET 变化，并交叉引用 8.5.4，不假设重建分布相同。
- 8.3：INT TopCR 和 paper 定义。Journal 第 3 页补充 inclusive top 样本、大 MET 导致双轻子衰变占主导、single-top/ttbar 比率在 SR/CR 之间于 MC 统计误差内一致。没有由此虚构独立 ratio nuisance，也未将 inclusive 样本说成只生成双轻子衰变。
- 8.4：Appendix D 的 116 events、约 90% Z purity、high-pT 过预测及 paper 的至多 60% 总产额差异、RNN 比较以及 100% 额外不确定度。Journal 第 3 页和 circulation 第 39 页补充不用 fake-factor 方法的敏感度理由。
- 8.5：INT VR 定义和第 8 章 pre-fit 图。Appendix G 的 MET 425–450 GeV 局部超出、相邻 threshold 检查、12 事件的 e/μ 和位置检查。paper 的“约 2 sigma”描述与 INT 最终约 2.3 sigma 为不同精度的表述，不拼接早期 2.84/2.5 sigma 阶段。
- 8.5.4：Appendix M 的 400<m_btau<800 GeV / 500<mT<600 GeV、放松阈值、2%/7% signal contamination、25.4±1.5 对 24、8.0±1.7 对 9。明确这些为 CR-only background fit 外推的 post-fit 产额；原研究未增加 mass-interval modelling uncertainty，不能当成对 SR uncertainty 的新测量。

## 取舍及来源边界

1. 删除第八章 Multi-jet cleaning 空节。主章使用 Chapter 7 与 Appendix B 的已有解释，不重复 QCD cut 公式、对象 WP 或变量定义。
2. 旧 INT 的 WVR1tau (1τ0l0b) 在 circulation 后成为 SR0b。沿用用户先前已确定的 Chapter 7 SR0b，不再将它列作本章 nominal VR。VR0tau 采用当前宏名 `\\VRb`（显示 VRW）。
3. Fake 很少不等于零。Appendix D 的“10% 或更低”是 Z→νν+jets 占背景的份额，不是任意背景样本的 truth fake fraction。正文不将其变成全样本 fake fraction 的精密测量。
4. Journal 的“100% uncertainty 对 final result <1%”未给出对应 metric、benchmark 与扫描范围，正文只采用其与 circulation 一致的定性结论：测试中 50% 改至 100% 对最终结果影响不明显，不推广成所有参数点的严格 <1%。
5. Appendix D 的 high-pT 过预测与 paper 的 overall-yield difference 不是同一量。按用户最新决定，正文使用 paper 的“总产额至多相差 60%”，图形讨论只描述 high-pT 过预测，不将 60% 强加为高 pT 的精确 correction factor。
6. Appendix D 表 D.1 将 transverse mass 记作 mT(pT^l,MET)，未明确 dilepton 样本中的 l 指哪一个对象，也未明确其是否使用 recoil-restored MET。草稿仅保留“100 GeV transverse-mass threshold”，不擅自改成 mT(tau,MET_ll)。精确实现需代码确认。
7. Appendix M 首句误写 1τ0l0b，与标题、后续定义和研究用途冲突。采用明确的 1τ0l1b，不沿用笔误。
8. Appendix G 关于“six independent VRs”的全局概率既涉及旧 region scheme，公式也不适合直接并入现有四 VR 模型，因此未采用。保留可追溯的局部检查结果。
9. 当前 Chapter 6 将 object_definition.tex 的 input 注释掉，因此引用该章而不引用未编入正文的 sec:ch6_object_definition。

## 用户已确认的冲突规则

本任务中用户明确决定：今后 INT note 与 paper 冲突时，以 paper 为准。

- CRW 的两个区域均采用 paper 的约 70% purity，覆盖 INT 对 NonRes 的约 90% 表述。
- W+HF/LF uncertainty 采用 30%，在 Res/NonRes 间去相关，覆盖旧 INT Appendix G 中的 20%。
- Fake validation 的总体产额差异采用 paper 的 up to 60%，保留 Appendix D 的具体选区和诊断图。

## 原始公开文献

新增原始 BibTeX keys PMGR-2021-01、STDM-2018-43、HIGG-2020-20，沿用 paper 的 bibliographic identity。在线核对了 https://arxiv.org/pdf/2112.09588、https://arxiv.org/html/2403.15093v2、https://arxiv.org/html/2410.19611v2 的内容。它们支持 flavour modelling 和 kinematic dependence 的动机；30% 和去相关作为本分析选择单独陈述，不宣称这些文章直接测得本分析的 30%。

Paper 同句还引用 ATL-PHYS-PUB-2017-006。CDS 正文被访问验证页面拦截，ATLAS 镜像没有成功取回，本次未将未经正文检查的文献加入 manuscript。该条原始关联保留在此，Chapter 9 继续展开时应核对 Section 5。其余三条原始引用没有替换为不相关文献。

## 图片

57 张 PDF 从 INT 对应图路径逐字节复制，组成 12 个 figure 环境：CRW/CRTop 的 Res/NonRes 各一组六图（左右为 e/μ，纵向为 jet pT、MET、mT）；VRW/VRTop 各两组六图；e/μ 研究四图；ZVR 三图；局部 VR 检查两图。

`figure_manifest.json` 记录每张图的绝对来源、目标及 SHA-256。没有更改 histogram、数据点、误差、binning 或数值读数。草稿保留旧图内配色及区域名称，caption 对 VR0tau→VRW 作映射。

`/Users/zang/Desktop/fit_results/...fullRegion_v3_modified/Plots/` 有 paper 配色的后期 EPS，但抽查 CRW pre-fit N−1 数值与本章 INT snapshot 不同。没有将这些图与旧版 event counts 混合。若统一画图风格，需在保持本版数值的前提下重排原图或取得对应的可编辑直方图。

新插入的所有 CR/VR 诊断图均来自 INT pre-fit 部分。Appendix M 只提供可靠的 post-fit 产额，本章用表呈现，没有用 post-fit 图冒充该区域的 pre-fit N−1 图。
