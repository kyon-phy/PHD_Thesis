# Iguro 论文中的变量用途与 Chapter 7 写作依据

核对日期：2026-09-16。本文是作者笔记，不是 thesis 正文。

主要来源：Endo, Iguro, Kitahara, Takeuchi and Watanabe, “Non-resonant new physics search at the LHC for the b → c τ ν anomalies”, JHEP 02 (2022) 106, arXiv:2111.04748v3。

- [公开全文](https://arxiv.org/html/2111.04748v3)
- 本地原文：/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/2111.04748v3.pdf
- BibTeX key：Endo2022NonResonant。
- 页码以下均指文章印刷页码；PDF 页码比它大 1。

## 1. mT：高能尾部的搜索灵敏度

依据：引言 Eq. (2)，印刷第 3 页；Section 4.2 末段，第 14 页；Section 5，第 29 页。

论文用 mT 研究高-pT τν 事件。在其统计分析和模型设定下，mT > 1 TeV 比 0.7 < mT < 1 TeV 对新物理更敏感；结论讨论在更大数据量下进一步提高门槛，通过减少 SM 背景改善灵敏度。

Chapter 7 的简短理由应是：mT 探测 τν 末态的高能尾部，该区域对非共振 LQ 贡献敏感。中微子纵向动量无法测量是一般重建理由，不是这篇论文明确提出的搜索动机；不要把它作为 Iguro 的原文解释。mT 也不是非共振 LQ 的重建质量，不能等同于 M_U 或传播子的动量转移 t。

论文中的 1/2 TeV 是其研究区间/展望，不能据此替换本分析 200/600 GeV 的最终 mT cut。

## 2. tau pT：选择高能 tau

依据：Section 3 的 cut a-1，印刷第 6 页；引言的 high-pT 搜索语境。

论文要求恰好一个 tau-tagged jet，pT ≥ 200 GeV、|eta| ≤ 2.1。这个 cut 选择研究所关注的 energetic tau final state。论文在这条 cut 后没有给出独立的背景抑制机制或量化改善，不能把更具体的解释说成其原文结论。

Thesis 中“信号分布延伸到较高 pT，而 SM 的主要贡献位于低 pT”是结合高能搜索逻辑及本分析 INT Chapter 6 分布/cutflow 的物理解释。|eta| 条件是论文的对象接受度要求，不应作为本分析新的 optimisation variable。

## 3. MET：抑制共振 W 贡献

依据：Section 3 的 cut a-3，印刷第 6 页。

论文明确将 MET ≥ 200 GeV 与抑制 resonant W contribution 联系起来。这是信号/背景运动学理由，不是该论文提出的触发器平台理由。

本分析 preselection 中 MET > 200 GeV 的 trigger-plateau 解释来自本分析的 trigger study；与上述物理作用可以同时成立，但来源不同。高 MET 不意味着所有 on-shell W 都被消除。

## 4. tau–MET azimuth 与 pT balance：back-to-back、平衡的 tauν 拓扑

依据：Section 3 的 cut a-4，第 6 页；Section 4.1，第 12 页；Section 3.2，第 9 页。

论文同时施加 Delta phi(tau, MET) ≥ 2.4 和 0.7 ≤ pT(tau)/MET ≤ 1.3，选择近似 back-to-back 且横向动量平衡的事件，以进一步抑制 SM 背景。Section 4.1 指出 back-to-back 条件对 top 相关背景有效；Section 3.2 明确提醒该条件也抑制 s-channel LQ production。

因此 SR1b 的解释应说明：角度下限有助于选择非共振拓扑并减少 top 背景，但强 back-to-back cut 会损失共振信号。本分析分别扫描 NonRes 的角度下限和 Res 的角度上限；最终值按 INT/paper，而不是直接采用 2.4。

论文的 back-to-back cutflow 是角度与 balance 的联合要求，不能把整步的数值抑制率单独归给 Delta phi。本分析没有采用该 pT balance cut，故只把它保存在研究笔记中。

## 5. b-tag multiplicity：减少 inclusive W+jets

依据：引言，第 2 页；Section 3 的 cut b-1，第 6 页；Sections 3.1、4.1，第 7、12 页。

论文通过新增一个 b-tag 将 tauν 搜索变为 tauν+b 搜索。对于 SM 子过程 gu → b tau nu 和 gc → b tau nu，振幅分别含小 CKM 元素 V_ub、V_cb；没有真实 b jet 的 tauν+jets 背景则需要 mistag 才能进入该类事件。

这个论证针对这些子过程和该研究的非共振选择，不能扩展为“所有 W+b 产生机制都由 V_cb/V_ub 抑制”。尤其不能忽略本分析中另外的重味产生机制或把论文的背景比例当成本分析的结果。

论文的 pT(b) ≥ 20 GeV 是选取 b jet 的最低要求，并没有定义本分析的 250 GeV Res/NonRes 分界。

## 6. additional-jet multiplicity：抑制 top decays

依据：Section 3 的 cut b-2，第 6 页。

论文明确限制 light-flavoured jets 的数量，以减少 top-decay backgrounds。写作中的物理解释是 top 衰变可产生额外 jets，因此上限有利于保留 jet 数较少的信号拓扑。

记号必须区分：论文在此用 N_j 表示 light-flavoured jets；本论文 N_j 包含 b-tagged jets，所以对应的扫描量是 N_j − N_b。其 N_j ≤ 2 不能直接替换本分析 NonRes/Res 的非 b-tag jet 上限 1/3。

## 7. 其他提出的变量：保留研究思路，不加入当前 SR

- Electron/muon veto：Section 3 cut a-2 明确列出 veto。选取 single-tau final state 是合理解释，但论文没有在该条为某个具体背景提供单独抑制结论；不额外添加未验证的 cut 理由或对象定义。
- Tau charge：引言和 Section 5 讨论选择负电 tau。W 背景受 proton valence quarks 影响，正负电率不对称；所研究的信号初态不来自 valence quarks，正负电率近似相等。这是进一步减少背景的研究思路，当前分析没有施加 charge-sign selection。
- Modified pseudorapidities eta'_tau = sgn(eta_b) eta_tau 和 eta'_b = sgn(eta_tau) eta_b：Section 4.5 Eq. (19)、Figs. 7–8 利用 tau 与 b 的相关方向，区分不同 Lorentz/flavour structures 的 LQ models。
- Delta phi(b,tau) 和 Delta phi(b,MET)：Section 4.5、Fig. 9 同样用于研究不同 LQ models 的角分布差别。这与已用于 selection 的 Delta phi(tau,MET) 不是同一变量；不要加入当前 scan table。

## 8. SR1b 中来自本分析的变量

- pT(b) = 250 GeV 的 Res/NonRes 分界：来自 INT Chapter 6 与最终分析 paper。用于区分高-pT 的共振衰变 jet 与通常较软的非共振辐射 jet。
- m_btau：来自本分析的共振 SR 研究，用于选择 U1 → b tau。衰变中微子使信号质量分布下移、展宽，重建分辨率进一步造成 smearing；采用宽的下限而不是窄的 mass window。
- m_jtau：0b region 没有 b-tagged jet，改用 leading jet 与 tau 构造质量；可以探测 U1 → s tau 拓扑，但不意味着每个 SR0b 信号事件都在 j tau 中有 resonance。
- 这些质量变量与具体分界不是 Iguro 的非共振 cuts；不能把整套 SR1b/SR0b 优化都归给该文。

## 9. 本次写作约定

7.1.1 保留定义和一句 mT 搜索动机；各变量的 discrimination 放在 optimisation，每段 2–3 句，先变量，再说明 SM/信号的运动学或拓扑差异。已经在 object definition 介绍的对象直接使用。引用公开 Iguro 论文，INT 与最终分析 paper 只记作者侧来源；冲突时以最终分析 paper 为准。
