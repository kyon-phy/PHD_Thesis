from pathlib import Path
v=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search/01_分析项目')
refs=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references')
cache=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/analysis')
S=f'''\n## 来源与使用范围\n\n- **[P] 公开 paper**：[arXiv:2606.02067v1](https://arxiv.org/abs/2606.02067v1)，CERN-EP-2026-136；[本地 PDF](<{cache}/arXiv_2606.02067v1.pdf>)。2026-06-01 提交，PDF 封面日期 2026-06-02，42 页。\n- **[D] 内部 paper draft**：[ATL-COM-PHYS-2026-015.pdf](<{refs}/ATL-COM-PHYS-2026-015.pdf>)；2026-05-26，Draft 3.3，35 页。\n- **[N] Internal note**：[ANA_EXOT_2025_06_INT1.pdf](<{refs}/ANA_EXOT_2025_06_INT1.pdf>)；2026-04-20，166 页。封面写 Draft 0.5，但 changelog 已包含 v0.9；用日期、章节及页码识别内容。\n\n本页页码均指 **PDF 文件从 1 开始的物理页码**。公开结论以 [P] 为准；内部补充逐项标注 [N]，不自动视为公开 paper 已采用。文件路径仅用于本地查阅，内部资料没有上传。代码实施及提交配置另行核对；已发现差异集中于 [[分析版本差异与待核实事项]]。\n'''
def write(name,text,status='已核对主要文献'):
 head=f'''---\ntype: analysis-reference\nupdated: 2026-09-07\nstatus: {status}\ntags: [ATLAS, U1, taunub, 分析项目]\n---\n\n# {name}\n\n'''
 (v/f'{name}.md').write_text(head+text+S)
write('分析项目主页',r'''这个独立项目记录 **ATLAS EXOT-2025-06：Run 2 的 $\tau_{\rm had}+E_{\rm T}^{\rm miss}+\mathrm{jets}$ / $b$-jets 的 $U_1$ vector leptoquark 搜索**。项目内部常称 `taunub`，但正式结果包含 **0b 与 1b 两类 signal regions**，不能把 0b 当成单纯的 b-tag inefficiency 控制样本。

## 按问题查找

- 数据、MC 和总体设计：[[分析总览与数据模拟样本]]。
- coupling、flavour basis、CKM、signal generation、interference：[[U1信号模型与生成及干涉]]。
- 文献中的 baseline / signal object、MET、overlap removal：[[文献中的对象定义与预选]]。
- SR / CR / VR、阈值、变量及旧命名：[[分析区域与选择变量]]。
- $W$ / top 的 normalisation、fake tau 和验证：[[背景估计与验证逻辑]]。
- likelihood、$\mu$ / $\sqrt\mu$、toy CLs、最终数值：[[统计分析与结果解释]]。
- 旧结论、未采用优化、文献矛盾和复现缺口：[[分析版本差异与待核实事项]]。

## 分析逻辑

```mermaid
flowchart LR
 A["b → c τ ν / R(D*) 动机"] --> B["U1 的 bτ 与 cν 耦合"]
 B --> C["resonant 与 non-resonant 过程"]
 C --> D["高 pT tau + 大 MET + jets"]
 D --> E["0b / 1b × Res / NonRes 四个 SR"]
 F["W 与 top 四个 CR"] --> G["背景归一化与系统误差"]
 G --> E
 G --> H["四个 VR 检查外推"]
 E --> I["signal + interference + background 的 toy CLs"]
 I --> J["mU1、gU、beta23 的限制"]
```

[P] §1、§6–9；[N] §12 说明 0b 加入最终 fit 的历史。

## 使用顺序

描述已发布分析，先读本项目的 [P] 结论和 selection，再用 [N] 查技术理由与历史检查。修改或复现分析，则必须继续查实际 framework 和正式提交 config；本项目不把“内部笔记写过”当作“当前代码执行了”。发表资料的进展应按日期与 [[分析版本差异与待核实事项]] 对照。

截至本次核对，arXiv 页面仅列 v1，状态为 submitted to Physics Letters B；不能把本地 ATL-COM draft 误称为 arXiv 版本，也不能把“已提交”写成“已接收”。
''')
write('分析总览与数据模拟样本',r'''## 搜索对象和为什么做

本分析用 ATLAS Run 2 的 $pp$ 数据寻找 $U_1$ 对 $\tau\nu(+b)$ 末态的贡献，同时覆盖 single resonant production 与 non-resonant $t$-channel exchange。$b\to c\tau\nu$ 需要 $b\tau$ 与 $c\nu$ 两个 coupling；此前 $\tau\tau(+b)$ 搜索较侧重 $b\tau$，本末态补充对较大 $\beta_L^{23}$ 的敏感性。0b 可以接收 $s\tau$ 等信号过程，本身具有物理意义。[P] PDF pp.2–5，§1、§3。

数据为 **2015–2018、$\sqrt{s}=13$ TeV、$140\ \mathrm{fb}^{-1}$**。每 bunch crossing 的 pile-up 约 8–70，平均 34。采用数据质量合格时段；luminosity uncertainty 为 **0.83%**。这些数值是本分析采用值，不代表后来全部 ATLAS 数据。[P] pp.5、7、9，§4、§5、§8。

## 从事件到 fit 的处理层次

1. **DAOD_PHYS → TopCPToolKit**：CP calibrations、objects、overlap removal、MET、event preselection，写 intermediate ntuples。
2. **FastFrames**：更具体的 SR / CR / VR selection、weights、histograms / lightweight trees。
3. **TRExFitter**：histogram 输入、背景约束、signal plus interference、统计推断。

[N] p.23 §5.1 记录当时的 `TopCPToolKit 2.17.1`、`AnalysisBase 25.2.51`、data derivation `p6479`、MC `p6490`。该页不是软件环境的自动探测结果，复现时仍须对照 release 与 git commit。

## Signal simulation

- **152 个独立参数点**：$1.5\le m_{U_1}\le3.0$ TeV，$0.5\le g_U\le3.0$，$0\le\beta_L^{23}\le2.2$，纯 left-handed，$|\beta_R^{33}|=0$。
- hard process：MadGraph5_aMC@NLO **3.3.1**，LO QCD、five-flavour scheme，$\tau\nu+$ 最多两个 partons，NNPDF3.0nlo。
- parton shower / hadronisation：Pythia **8.308**，A14 tune；shower / UE 使用 NNPDF2.3lo。
- CKKW-L：`ktDurham = 15 GeV`，`D = 0.4`；ME 包括相关 resonant 与 non-resonant diagrams。
- signal–SM interference：逐参数点单独生成，并与对应 signal 合并用于解释。
- signal calorimeter simulation：AtlFast3；相关 detector-response 差异另有 uncertainty。

[P] pp.5–6 §4、Table 1；生成历史、coherent diagrams 和 weighting 限制见 [[U1信号模型与生成及干涉]]。

## Background simulation

| Process | Nominal generator / accuracy | PS、PDF、tune |
|---|---|---|
| $W\to\tau\nu,\ell\nu$ + jets | Sherpa 2.2.11；ME NLO 到 2 partons、LO 到 5 partons | Sherpa PS / MEPS@NLO；NNPDF3.0nnlo；Sherpa default |
| $Z\to\nu\nu,\ell\ell$ + jets | Sherpa 2.2.11 | 同上 |
| $Z\to\tau\tau$ + jets | Sherpa 2.2.14 | 同上 |
| $t\bar t$、single-$t$ | Powheg Box v2，NLO | Pythia 8.230；NNPDF3.0nlo；A14 |
| Diboson | Sherpa 2.2.2，NLO；只纳入 fully leptonic modes | Sherpa；NNPDF3.0nnlo；Sherpa default |

此处 $\ell=e,\mu$；diboson 的 fully leptonic decay 定义还包括 $\tau$。$t\bar t$ 以 NNLO+NNLL inclusive cross-section 归一化；single-top 包括 $s$、$t$、$Wt$，本分析以 $Wt$ 贡献为主。除 Sherpa 外，heavy-hadron decays 用 EvtGen。[P] pp.5–6，§4、Table 1。

[N] p.21 §4.2 的实施补充：

- $W\to\tau\nu$ 专门 high-$E_T^{\rm miss}$ / high-$p_T^\tau$ filter 样本 **DSID 700543–700544**，用于改善 MC statistics；与 nominal Sherpa 2.2.11 配置相同，但不按 B/C/L filters 分开。
- nominal $W\to\tau\nu$ 样本仍用于部分 lepton-trigger CR；不能任意用 high-MET-filter 样本替换所有区域。
- 通过大 MET / $m_T$ 后，top 中 dileptonic $t\bar t$ 占比超过 95%，使用 dilepton-filtered sample。

以上 DSID 和 filter 是内部版本实施记录；正式 sample 清单、filter efficiency、sum of weights、cross-section metadata 要从运行配置核对。

## Detector simulation 与 pile-up

Background 经过 Geant4 full detector simulation；signal 使用 AtlFast3 的 fast calorimeter response。pile-up overlay 混合 Epos 2.0.1.4（Epos LHC tune）与 Pythia 8.308（A3、NNPDF2.3lo）。Pythia component 包含高-$p_T$ jet、prompt photon 或 b-hadron decay lepton 等 filtered events；Epos 覆盖其余。先保持不同 jet-$p_T$ 区域平滑衔接，再 reweight 到数据 pile-up 分布。[P] p.6 §4。

## Trigger 概览

SR 使用 **lowest-unprescaled MET triggers**；CR 使用 **single-electron / single-muon triggers**。paper 仅给典型 HLT threshold：MET 110 GeV、single leptons 26 GeV，各 period 的 chain 并不相同。offline cuts 与 trigger thresholds 不是同一概念。[P] p.5 §4、pp.8–9 §6–7。内部 note 明确最后 **没有采用 tau trigger**，[N] p.27 §5.8。
''')
write('U1信号模型与生成及干涉',r'''## 本分析的参数约定

$U_1$ 是 vector leptoquark，gauge representation 为 $(3,1,2/3)$。模型采用 down-type quark mass basis：

$$q_L^i=\begin{pmatrix}V_{ji}^{*}u_L^j\\d_L^i\end{pmatrix},\qquad
\mathcal L\supset\frac{g_U}{\sqrt2}U_1^\mu\left(\beta_L^{ij}\bar q_L^i\gamma_\mu\ell_L^j+\beta_R^{ij}\bar d_R^i\gamma_\mu e_R^j\right)+\mathrm{h.c.}.$$

非零 flavour entries 设为 $\beta_L^{13},\beta_L^{23},\beta_L^{33},\beta_R^{33}$；取 $\beta_L^{33}=1$，以 $g_U$ 表示整体 coupling。公开结果 **仅解释 $|\beta_R^{33}|=0$**。Gauge-boson coupling 参数采用 $\kappa=\tilde\kappa=0$，即本篇 convention 的 **Yang–Mills** scenario。[P] pp.3–4 §3；[D] p.4；[N] p.20 Eq.(4.1)。

$\beta_L^{13}=(V_{td}^{*}/V_{ts}^{*})\beta_L^{23}$ 是 paper footnote 的 convention；paper 近似标成 $\sim0.2\beta_L^{23}$。实际数值包括 CKM 的符号 / phase，不能仅凭“0.2 倍”重新搭 UFO。[P] p.4 footnote 2；本页公式与 footnote 已对 PDF 图像核对。

由上式展开，$c\nu_\tau$ vertex 的 coefficient 与

$$\lambda_{c\nu_\tau}=\frac{g_U}{\sqrt2}\left(V_{cd}\beta_L^{13}+V_{cs}\beta_L^{23}+V_{cb}\beta_L^{33}\right)$$

成正比；这是对已给 Lagrangian 的代数展开，**不是新增 model assumption**。$b\tau$、$s\tau$ 左手 coupling 分别为 $g_U\beta_L^{33}/\sqrt2$、$g_U\beta_L^{23}/\sqrt2$。因此 $\beta_L^{23}=0$ 也不意味着 $c\nu$ vertex 为零：仍有 $V_{cb}\beta_L^{33}$。

## 与低能 $b\to c\tau\nu$ 的联系

忽略较小的 $\beta_L^{13}$ 项时，公开 paper Eq.(1) 给出

$$C_{LL}^{c}\sim\frac{g_U^2v^2}{4m_{U_1}^2}\left(1+\frac{V_{cs}}{V_{cb}}\beta_L^{23}\right).$$

这个式子说明 $V_{cs}\beta_L^{23}$ 相对于 $V_{cb}\beta_L^{33}$ 的增强为何重要。只固定 $\beta_L^{23}\sim0.1$ 会限制 phenomenological coverage；$B$ mixing、tau LFU 等额外约束受 UV completion 和其他 states 影响，不能把某个 UV fit 的 $\beta_L^{23}$ 区间直接当成所有 $U_1$ 理论的硬界。[P] p.4 §3。

favoured band 的 paper 来源是 **Aebischer et al., arXiv:2210.13422**（paper Ref.[35]），先以其 $C_{LL}^{c}$ 约束为依据，再用 Eq.(1) 映射到较大 $\beta_L^{23}$；不是在每个新 $\beta_L^{23}$ 点重新执行完整 flavour global fit。[P] p.12 §9、pp.15–16 Figures 5–6。实际常数、1σ / 2σ edges、插值算法须继续查 plotting scripts。

## Resonant / non-resonant 与 0b

- **Resonant**：on-shell LQ 衰变给出 hard quark + tau，$m_{b\tau}$ 或 $m_{j\tau}$ 提供可见质量 proxy。tau 自带不可见 neutrino，故 proxy 不等于精确 LQ mass。
- **Non-resonant**：$t$-channel exchange 造成高-$m_T$ 的 $\tau\nu$ 系统，associated jet 往往更软。
- $m_{U_1}$ 增大时，on-shell production 受高-$x$ parton luminosity 抑制，non-resonant 更重要。
- $\beta_L^{23}$ 增大同时改变 production flavours、width 和 branching fractions，增加不含 reconstructed b-jet 的 signal；不能仅以固定 template 乘 $g_U^4(\beta_L^{23})^2$ 精确覆盖全部 resonant 参数空间。[P] pp.2–5，§1、§3。

[N] pp.103–104 §12.1 的特定 truth study 在 $(m,g_U,\beta_L^{23})=(1.5\ \mathrm{TeV},1.5,0.6)$ 发现 SR0b-Res leading truth jet 约 30% 为 $s$、60% 为 $c$；$s$ 例子对应 $U_1\to s\tau$，$c$ 部分可来自 $c\nu$ resonance。此比例只针对该点和该 truth selection；**不可普遍写成“所有 0b 都是 $s\tau$”**。

## Generation 与旧 reweighting 的适用范围

最终 152 点来自独立 signal generation，细节见 [[分析总览与数据模拟样本]]。[N] pp.20–21 §4.1 进一步记录：`bsm`、`inf`、`bi` 对应 pure BSM、interference、BSM+interference（不含 pure SM）的生成命名；note 用 `NP == 2`、`NP2 == 2`、`NP2 > 0` 描述其 coupling-order selections。精确 MadGraph syntax 应查实际 process card。

完整 ME coherent 地包含相关 diagrams；Res / NonRes 是 **event categories**，不等价于生成时完全可分离的互不干涉 process samples。内部 note 还指出某些 masses 可以包含 $U_1U_1\to b\tau c\nu$ diagrams；不要把最终 signal sample 简化成一张 illustrative single-production diagram。[N] p.20 §4.1。

[N] pp.130–133 Appendix A.2 是 **早期 internal-weight scan 验证**：以 $(g_U,\beta_L^{23})=(1,0.2)$ baseline reweight，部分参数点不能同时重现 cross-section 与 kinematics；曾采用 truth leading-jet $p_T$ 和 $m_{b\tau}$ 的二维附加 correction。它解释了为什么后来重做独立样本，不应被抄成当前所有 signal 点必须执行的 nominal reweight。

## Interference 与 fit 参数

按固定 signal parameter point，区域期望写为

$$N_r(\mu)=B_r+\mu S_r+\sqrt\mu\,I_r,$$

其中 $I_r$ 可以为负。Amplitude 乘 $\sqrt\mu$ 导致 pure BSM yield 乘 $\mu$、与 SM 的 interference 乘 $\sqrt\mu$。[N] p.73 Eq.(10.1)；[P] p.11 §9。

1b 中 SM 对 associated b 的贡献有 CKM suppression，exclusion-sensitive 区域的 interference 较小；0b 必须纳入。公开 paper 给出的代表量级为 1.5 TeV 时约 pure BSM 的 **20% destructive**，高 mass 约 **30–40%**。[P] p.11。不能把该数值理解为每个小 coupling 网格点的统一比例，也不能把“目标 coupling 范围的总 signal 正”推广成任意 $\mu$ 下 $\mu S+\sqrt\mu I$ 都正。

Internal note §12.3 用 $x=\sqrt\mu$ 做 POI，再转成 $\mu=x^2$；不对称误差必须分别平方两端转换，不能简单将 $\sigma_x$ 平方当 $\sigma_\mu$。[N] p.106 Eq.(12.1)。正式 config 的 `mu` 命名是否实际代表 $x$，以 implementation 笔记为准。

## 右手与 $\tau\tau$ contamination

[N] p.115 §12.5 记录右手 interpretation 因缺少完整 interference samples 仍需决策；[P] p.4 明确最后只做纯 LH interpretation。早期 $|\beta_R^{33}|=1$ visible-cross-section plots 不能作为最终公开 LH coupling limits 的一部分。

[N] p.107 §12.4、pp.113–114 Tables 12.1–12.3 用有限 $\tau\tau$ samples 加 cross-section rescaling 估计额外 contamination：1b 约 35%、0b 约 5%，对 coupling limits 的可能改善约 2–5%。这是内部 sensitivity cross-check，既不是完整逐点 $\tau\tau$ simulation，也不能据此给 nominal yields 自动乘常数。
''')
write('文献中的对象定义与预选',r'''## Baseline 与分析 object 的区别

Baseline objects 用于计数、overlap removal、MET；SR 中真正要求的 signal object 通常更严格。下面按 [N] §5 和 [P] §5–7 整理；阈值并不意味着所有 surviving object 都用来定义 SR。当前代码的容器、selection decoration 和 working point 要继续对照 framework。

| Object | Baseline 文献定义 | 分析中更严格要求 |
|---|---|---|
| electron | $p_T>10$ GeV；$|\eta|<2.47$，排除 $1.37<|\eta|<1.52$；TightLH；Loose_VarRad；$|d_0|/\sigma(d_0)<5$、$|z_0\sin\theta|<0.5$ mm | CR signal e：HighPtCaloOnly isolation；WCR $p_T>200$ GeV；TopCR $p_T>28$ GeV（note） |
| muon | $p_T>10$ GeV；$|\eta|<2.5$；Loose ID + Loose_VarRad；$|d_0|/\sigma(d_0)<3$、$|z_0\sin\theta|<0.5$ mm | CR signal mu：Medium ID + Tight_VarRad；WCR $p_T>200$ GeV；TopCR $p_T>28$ GeV（note） |
| tau | anti-$k_t$, $R=0.4$ calorimeter seed；$p_T>20$ GeV；$|\eta|<2.5$，排除 transition；1 或 3 tracks，$|Q|=1$；Loose RNN tau-ID + Loose RNN eVeto | Tight RNN tau-ID；SR $p_T>200$ GeV；TopCR / TopVR 的 tau $p_T>100$ GeV |
| small-$R$ jet | anti-$k_t$, $R=0.4$，EMPFlow；$p_T>20$ GeV，$|\eta|<2.5$；LooseBad cleaning；NNJVT FixedEffPt | 用指定 leading jet / b-jet 做 Res / NonRes 分类 |
| b-jet | GN2v01、FixedCutBEff 85% | multiplicity 和所用 b-jet 的 $p_T$ 由 region 决定 |

[P] pp.6–7 §5、p.9 §7；[N] pp.23–25 Tables 5.1–5.4、p.38 Table 7.1、p.39 Table 7.2。impact parameter 表使用 [N] 的绝对值形式；公开正文省略了 $d_0$ 的绝对值记号，不能据此写成只剔除正侧尾。

## Calibrations 和特殊约定

[N] pp.23–26 记录的具体版本：

- electron energy model：`es2023_R22_Run2_v1`；electron efficiency map `2015_2025/rel22.2/2025_Run2Rel22_Recommendation_v3/map0.txt`，当时有 local checkout 手动配置。
- muon：`correctData_CB`。
- tau：MVA TES；**Tight RNN ID 没有对应 eVeto SF 时，经 Tau CP 讨论使用 Medium RNN 的 eVeto SF**。这是一项分析处理约定，不是 Tight tau-ID 本身变成 Medium。
- jets：CalibArea `00-04-83`；`PreRec_R22_PFlow_ResPU_EtaJES_GSC_February23_230215.config`；data `JetArea_Residual_EtaJES_GSC_Insitu`，MC 去掉 `Insitu`。
- GN2v01 CDI：`MC20_2025-06-17_GN2v01_v4.root`；note 说 ntuple 中多个 b-efficiency WP 可用，但 nominal 是 85%。

## MET

$$\vec p_T^{\,\rm miss}=-\left(\sum_{\text{selected hard objects}}\vec p_T+\sum_{\text{PV soft tracks}}\vec p_T\right).$$

Track soft term 只纳入与 PV 相容、又未归入 selected hard objects 的 tracks。$E_T^{\rm miss}=|\vec p_T^{\,\rm miss}|$。[P] p.7 §5。

[N] p.26 Table 5.5：METMaker / METUtilities，TST，MET operating point **Tight**，`METUtilities/R22_PreRecs`，`TrackSoftTerms-pflow_Dec24.config`。**MET Tight 与 Tight tau-ID 是不同配置。**

## Overlap removal：按顺序执行

[N] p.26 §5.7 比 paper 提供多一行 electron–electron；以下保留 note 的顺序，并在存在差异时注明。

1. 共享 track 的两个 electrons，剔除较低 $p_T$ 的 electron（仅 [N] 表明确列出）。
2. tau 距 electron $\Delta R<0.2$：剔除 tau。
3. tau 距 muon $\Delta R<0.2$：剔除 tau。
4. calo-tagged muon 与 electron 共享 ID track：剔除 muon。
5. electron 与 muon 共享 ID track：剔除 electron。
6. jet 距 electron $\Delta R<0.2$：剔除 jet；paper 明确写 closest jet。
7. electron 距 surviving jet $\Delta R<0.4$：剔除 electron。
8. jet–muon：[N] 写 `NumTrack < 3` 且 **ghost-associated**；[P] 写 $\Delta R<0.4$ 且 **最多 2 tracks** 时剔除 jet。两种 matching 描述需查 CP-tool implementation，不能直接视为同义。
9. muon 距 surviving jet $\Delta R<0.4$：剔除 muon。
10. jet 距 tau $\Delta R<0.2$：剔除 jet。

[N] p.26 说明默认 $\Delta R$ 用 **rapidity**；[P] p.3 footnote 1 也定义 $\sqrt{(\Delta y)^2+(\Delta\phi)^2}$。tau-specific muon rejection 在 [N] p.25 Table 5.3 还说明 muon $p_T>2$ GeV、非 calo-tagged；它不应被自动等同为 baseline muon $p_T>10$ GeV 的一般 OR。

## Event preselection

- GRL / detector data-quality；PV 至少两条关联 tracks；以 $\sum p_T^2$ 最大的 vertex 作为 PV，paper 指 track $p_T>500$ MeV。
- 至少 1 jet。
- QCD / fake-MET cleaning 用“或”逻辑：

$$\min_j\Delta\phi(j,\vec p_T^{\rm miss})>0.4\quad\mathbf{OR}\quad\frac{E_T^{\rm miss}}{p_T^{j_{\min\Delta\phi}}}>6.$$

这里第二项的分母是与 MET **最接近方位角的 jet**，不是必然 leading jet。只有 small angle 与 small ratio 同时出现时才 reject；误写成 AND 会改变 acceptance。[P] p.7 §5；[N] p.38 Table 7.1、Appendix C pp.135–137。

[N] p.27 中 intermediate-ntuple preselection 的 TopCR lepton $p_T>150$ GeV 与 p.39 最终 TopCR $p_T>28$ GeV 不一致；当前实际 skim 以代码为准，详见 [[分析版本差异与待核实事项]]。Trigger flags 在 note 所述 TopCPToolKit 阶段保存，不显式要求通过 trigger；最终使用 chain 在 FastFrames 层另判定。
''')
write('分析区域与选择变量',r'''## 四个 SR 的最终定义

共同条件：满足 [[文献中的对象定义与预选]]；通过 lowest-unprescaled **MET trigger**；**恰好一只 tau**、Tight RNN ID、$p_T^\tau>200$ GeV；**没有额外 electron / muon**。jet 的 baseline threshold 是 20 GeV。

| Selection | SR0b-Res | SR1b-Res | SR0b-NonRes | SR1b-NonRes |
|---|---:|---:|---:|---:|
| $N_b$ | 0 | 1 | 0 | 1 |
| 用于分类的 jet | leading jet | 唯一 b-jet | leading jet | 唯一 b-jet |
| 该 jet 的 $p_T$ | $>250$ GeV | $>250$ GeV | $50<p_T<250$ GeV | $50<p_T<250$ GeV |
| $E_T^{\rm miss}$ | $>200$ GeV | $>200$ GeV | $>400$ GeV | $>400$ GeV |
| $m_T(\tau,\mathrm{MET})$ | $>200$ GeV | $>200$ GeV | $>600$ GeV | $>600$ GeV |
| 可见 invariant mass | $m_{j\tau}>800$ GeV | $m_{b\tau}>800$ GeV | 无 | 无 |
| $\Delta\phi(\tau,\mathrm{MET})$ | 无额外要求 | 无额外要求 | $>1.2$ | $>1.2$ |
| jet multiplicity | $1\le N_j\le4$ | $1\le N_j\le4$ | $1\le N_j\le2$ | $1\le N_j\le2$ |

[P] p.8 §6、Table 2；表与 PDF 图像核对。公开正文用 strict $50<p_T<250$，同页表写 `[50,250]`；边界是否取等号需查代码。1b 分类别误用 leading **inclusive** jet：paper 指 b-jet。

### 变量为什么有效

$$m_T=\sqrt{2p_T^\tau E_T^{\rm miss}\,[1-\cos\Delta\phi(\tau,\vec p_T^{\rm miss})]}.$$

这个常用 massless transverse-mass 形式解释 tau 与 MET 的 high-scale 特征，实际 branch 的定义需查代码。Res 用 hard jet 与大 visible mass 接近 resonant topology；NonRes 用 high $m_T$ / MET 选出高能 scattering，并限制 jet multiplicity 以压低 top。paper 说明优化时要求 expected background 的 MC statistical uncertainty 小于 30%。[P] p.8 §6；[N] §6 pp.28–36 给出旧 1b 优化细节。

0b 是真实 signal category。特别在大 $\beta_L^{23}$ 时，$s$ / $c$ flavours 也能贡献；参见 [[U1信号模型与生成及干涉]]。

## CR：用于 likelihood 中约束 backgrounds

### CRW-Res / CRW-NonRes

- $(N_\tau,N_\ell,N_b)=(0,1,0)$，$\ell=e,\mu$。
- 以 signal electron / muon 替代 SR0b 的 tau，并用 lepton 计算 $m_T$、$m_{j\ell}$、$\Delta\phi$；$p_T^\ell>200$ GeV。
- 其余 Res / NonRes 的 MET、jet、mass、$m_T$、jet multiplicity cuts 与 SR0b 相同。
- 使用 single-lepton trigger。其原因之一：MET trigger 的在线计算未纳入 muon，直接套用会对 muon CR 产生不同 bias。[N] p.38 §7.1。
- b-veto 抑制 top，提高 $W\to\ell\nu$ purity 与 event count；$\lambda_W^{\rm Res}$ 和 $\lambda_W^{\rm NonRes}$ 分别由两个区约束。

[P] p.9 §7；[N] p.38 Table 7.1。公开 paper 概括 W purity 约 70%；旧 note 区分 Res 约 70%、NonRes 约 90%，不把两个版本的精度描述混写成精确测量。

### CRTop-Res / CRTop-NonRes

- $(N_\tau,N_\ell)=(1,1)$，$N_b\ge1$；最高 $p_T$ b-jet 作为 proxy。
- single-lepton trigger，额外 lepton $p_T>28$ GeV（[N] Table 7.2）。
- 放宽为 $p_T^\tau>100$ GeV、MET $>100$ GeV、$m_T>100$ GeV；取消 $m_{b\tau}$ cut。
- Res / NonRes 仍由 b-jet $p_T>250$ / $50<p_T<250$ GeV 区分；jet multiplicity 分别 ≤4 / ≤2；NonRes 仍要求 $\Delta\phi(\tau,\mathrm{MET})>1.2$。
- top purity 约 90%；$t\bar t$ 与 single-top 共用该 topology 的 top normalisation。

[P] p.9 §7；[N] pp.38–39、Table 7.2。

## VR：检验外推，不参与 nominal background-only fit

**VRW-Res / VRW-NonRes**：$(N_\tau,N_\ell,N_b)=(0,1,1)$。从 WCR 的 0b 改成 1b，检验 b-veto → b-tagged transfer；kinematics 用 e / mu。paper 的 $m_{b\ell}$ 及选用的 b-jet 说明见 p.13 Figure 3，但旧 note Table 7.1 对 WCR / VR 共用“leading jet”的表述需结合代码解读。[P] p.9；[N] p.40 §7.3.1。

**VRTop-Res / VRTop-NonRes**：$(N_\tau,N_\ell,N_b)=(1,0,2)$，检验 top 从额外 lepton CR 到 light-lepton-veto tau sample 的外推。[P] p.9。paper 仅概括“放宽 kinematics”，**没有完整列出数值**。内部 [N] p.41 Table 7.4 给出：

| 旧 note 的 TopVR1tau selection | Res | NonRes |
|---|---:|---:|
| MET trigger / $p_T^\tau$ | MET trigger / $>100$ GeV | MET trigger / $>100$ GeV |
| MET | $>200$ GeV | $>200$ GeV |
| $m_T$ | $>100$ GeV | $>200$ GeV |
| $m_{b\tau}$ | $>400$ GeV | 无 |
| leading b-jet $p_T$ | $>250$ GeV | $[50,250]$ GeV |
| $N_j$ | ≤4 | ≤2 |
| $\Delta\phi(\tau,\mathrm{MET})$ | 无额外要求 | $>1.2$ |

这些值先保留为 **内部文献记录**，由正式配置核对后才能作为复现值；不要将 TopCR 的 100 GeV MET、no-mass-cut 自动复制到 TopVR。

## 旧命名如何对应最终区域

| Internal note 早期名称 | 最终 paper 名称 | 主要 multiplicities |
|---|---|---|
| SR / SR-Res / SR-NonRes | SR1b-Res / SR1b-NonRes | 1 tau, 0 lepton, 1b |
| WVR1tau / WVR-Res / WVR-NonRes | SR0b-Res / SR0b-NonRes | 1 tau, 0 lepton, 0b |
| VR0tau | VRW-Res / VRW-NonRes | 0 tau, 1 lepton, 1b |
| TopVR1tau | VRTop-Res / VRTop-NonRes | 1 tau, 0 lepton, 2b |
| WCR | CRW | 0 tau, 1 lepton, 0b |
| TopCR | CRTop | 1 tau, 1 lepton, ≥1b |

[N] p.103 §12：发现旧 WVR 的大-$\beta_L^{23}$ signal contamination 后，在 PAM 同意把它们纳入 fit，成为 0b SR，cuts 不变。因此代码中含 `WVR` 的 histogram 名仍可能在 final config 中被定义成 `SIGNAL` region。

## 没有采用的 SR0b optimisation

[N] Appendix N pp.164–166 尝试将 SR0b-Res 的 MET 提至 600 GeV，预计改善 low-mass sensitivity、减小 interference。最终因 unblinding 与分析进度等考虑 **没有纳入 nominal**；公开 Table 2 仍是 200 GeV。该 study 的优化点不是新的正式 selection。
''')
write('背景估计与验证逻辑',r'''## 主方法

本分析以 **MC prediction + CR data 约束主要背景 normalisation** 为主；fake-tau component 也由 MC 估计，并由专门数据样本赋予保守 uncertainty。因此它既不是完全 data-driven background，也不是直接使用未约束的 MC normalization。[P] pp.8–11 §7–9。

- $W\to\tau\nu+$jets：SR 主背景；CRW 中用 $W\to e\nu/\mu\nu$ 的大统计量约束。
- top：主要 $t\bar t$ 和 $Wt$，通过包含额外 e / mu 的 CRTop 约束。
- $Z\to\nu\nu+$jet faking tau：次要背景，MC + 专门 $Z\to\ell\ell$ validation。
- diboson、$Z\to\tau\tau$、少量 $W\to\ell\nu$ / $Z\to\ell\ell$：MC。
- multijet：经 fake-MET cleaning 与高能 selection 后可忽略；不能把 preselection 前也说成可忽略。

## WCR 约束什么，不能约束什么

CRW 采用 e / mu、0b、与 SR 相近 kinematics 来给 $W$ 总体 normalization 提供数据约束；transfer 到 SR 必须依赖 simulation 的 e/mu → tau acceptance，以及 0b → 1b 的 flavour / tagging modelling。由于 WCR b-veto，**它不能单独测定 W+HF / W+LF ratio**。因此 final paper 对 1b regions 的 HF/LF transfer 赋予 **30%** uncertainty。[P] p.10 §8。

需要避免三种混淆：

1. 30% 不是 $W+$jets 全体 inclusive cross-section 的统一 uncertainty。
2. 30% 不是 CR 拟合出的 $\lambda_W$ 的误差。
3. HF production modelling 与 b-tagging calibration 是不同来源，即使都影响 0b / 1b migration。

[N] Appendix J p.151 曾比较 10% / 20% / 30%，当时正文仍残留“nominal 20%”；最终 paper 是 30%。note 还说明 HF/LF ratio 随 $p_T$ 变化，因此 Res / NonRes 采用 decorrelated NPs。是否同样适用于每个当前 histogram、样本 flavour split 和 sample 名，以正式 fit config 核对。

[P] 对 30% 引用四项公开资料：ATL-PHYS-PUB-2017-006；arXiv:2112.09588；arXiv:2403.15093；arXiv:2410.19611（[D] PDF p.24，Refs.[87–90]）。这些引用提供 modelling / comparison 的依据；**不能在未读原文前声称任一文献直接给出本 analysis 的精确 30% prescription**。完整证据链见系统误差主题笔记。

## 为什么有 Res / NonRes 两个 W normalisations

两个 regions 覆盖不同 jet-$p_T$ kinematics。内部 note p.74 §10.2 把两者 normalization difference 与 jet-$p_T$ slope 联系起来，故不能简单要求两个 $\lambda_W$ 相同。最终 B-only fit 得到：

- $\lambda_W^{\rm Res}=1.21\pm0.11$；
- $\lambda_W^{\rm NonRes}=0.89\pm0.08$。

这些是 model-dependent post-fit correction factors，不是新的 W cross-section measurement。[P] p.11 §9。

## Top 的 transfer

CRTop 要求 tau + 一只额外 light lepton，选出 semileptonic / dileptonic decay topology；SR 则无 extra light lepton。通过 simulation 把 CR 的 normalization 转到 SR，单独由 VRTop 检查此 extrapolation。Res / NonRes 分别有一个 $\lambda_t$，每个同时作用于 $t\bar t$ 和 single-top：

- $\lambda_t^{\rm Res}=0.76\pm0.16$；
- $\lambda_t^{\rm NonRes}=0.81\pm0.16$。

[P] pp.9、11。TopCR 为增加 event yield 放宽 MET、tau-$p_T$、$m_T$、$m_{b\tau}$；故 CR 与 SR 的 modelling systematics 和相关性非常重要，不能将“90% purity”误读为“无需 extrapolation uncertainty”。

## Fake tau：Z validation study

$Z\to\ell\ell+$tau candidate 样本用来检查 simulation 的 jet→tau fake probability。选择 $m_{\ell\ell}$ 接近 Z mass、0b、looser kinematics；用 $|\vec p_T^{\,\ell\ell}+\vec p_T^{\,\rm miss}|$ 模拟 invisible Z 的 recoil。它检查与 SR $Z\to\nu\nu+$fake tau 相近的 jet/tau 体系，但不是直接在 SR 中计数。[N] p.138 Appendix D、Table D.1。

公开 paper 给出 Z+fake-tau purity **>90%**，总体 yield 可有 **至多约 60%** data/MC discrepancy；kinematic shapes 基本可用。由于 SR 中此分量较小，assign **100% normalisation uncertainty**。[P] p.10 §8。内部 note 还记录 116 data events 以及 high-$p_T$ 约 50% overestimate；这些是具体旧检查结果，不能将 50% 与 final 60% 当成同一数字。

## VR 的结论与局限

CR-fit normalization 与 nuisances 外推至四个 VR：VRW 检查 0b→1b，VRTop 检查 tau+lepton→tau-only。公开 paper 指 VRW-NonRes 约 2σ deviation；检查 detector pathology 与较低 / 较高 MET 邻近区域后，没有发现明确 modelling defect，因而与 statistical fluctuation 相容。[P] p.11 §9；[N] pp.144–146 Appendix G。

[N] pp.156–162 Appendix L 比较了三种 WCR 方案：nominal 0tau0b；把 0tau1b VR 改作 CR；两者同时 fit。第二种 statistics 太少，使 $\lambda_W$ uncertainty 约增加 7–8 倍；方案间结果总体相容。这说明 nominal 选择的统计与验证权衡，**不意味着所有方案都同时参与最终 likelihood**。

旧 WVR1tau 因发现大-$\beta_L^{23}$ signal contamination 已变成 SR0b。因此“有六个 VR”及“WVR1tau 只验证 tau transfer”的说法属于早期设计，最终四 SR / 四 CR / 四 VR 见 [[分析区域与选择变量]]。
''')
write('统计分析与结果解释',r'''## Likelihood 的组成

每个区域提供一个 event count；同时约束 signal strength、background normalisations 与 nuisance parameters。按最终四 SR / 四 CR 的版本，期望可以写成

$$\nu_r(\mu,\boldsymbol\lambda,\boldsymbol\theta)=\mu S_r(\boldsymbol\theta)+\sqrt\mu I_r(\boldsymbol\theta)+\lambda_W^{a(r)}W_r(\boldsymbol\theta)+\lambda_t^{a(r)}T_r(\boldsymbol\theta)+O_r(\boldsymbol\theta),$$

$$\mathcal L=\prod_{r\in\mathrm{fit}}\mathrm{Pois}(n_r\mid\nu_r)\prod_k C_k(\theta_k).$$

$a(r)$ 指 Res / NonRes；$T$ 合并 top pair 与 single-top normalization，$O$ 是其他背景。$\boldsymbol\lambda=\{\lambda_W^{\rm Res},\lambda_W^{\rm NonRes},\lambda_t^{\rm Res},\lambda_t^{\rm NonRes}\}$ 是四个 free normalisation parameters；$C_k$ 可为 Gaussian、log-normal 或 Poisson constraints。有限 MC sample size 以 Beeston–Barlow lite、每 bin 一个 dedicated parameter 处理。[P] p.11 §9；[N] p.73 Eqs.(10.1–10.2)。

以上是描述实际结构的通用写法，不宣称所有 NP 独立或所有 constraints 都 Gaussian。同一个 NP 作用于多个 samples / regions 才体现 correlation；明确 decorrelated 的参数需以 config 为准。

## 三类输出要分清

1. **Background-only fit**：只 fit 四个 single-bin CR，固定 $\mu=0$。再把 post-fit prediction 外推到 SR / VR，作 data/MC comparison。SR 数据没有反向拉动此 background-only prediction。
2. **Signal-plus-background fit**：四 CR + 四 SR 同时 fit；包括 $\mu S+\sqrt\mu I$。旧 note §10 仍写四 CR + 二 SR，是加入 0b 之前的版本。
3. **Limit evaluation**：在每个 model parameter point 用 CLs 求 $\mu$ 的上限，再找该点 nominal prediction（$\mu=1$）是否被排除，拼接 coupling exclusion contours。最终 test-statistic 分布由 pseudo-experiments 得到。

[P] pp.11–12 §9；[N] p.105 §12.3。

Internal note p.74 §10.1 说明是 **single-bin counting fit**，shape components 被 dropped，并设置 1% normalisation pruning。公开 paper 提到 shape / normalisation variations，不能据此宣称最终把图中的 multi-bin $m_T$ 或 $m_{j\tau}$ spectra 全部放入 fit。检查实际 histogram rebin 和 nominal submission config 才能确定实现。

## $\mu$ 与 $\sqrt\mu$ 不是 coupling 本身

Fixed parameter point 下 signal amplitude 的 scale 可以选 $x=\sqrt\mu$，则 yield 为 $x^2S+xI$。note §12.3 采用此 POI，绘图及 report 再转回 $\mu=x^2$。参数名 `mu` 不保证它在代码里就是 yield multiplier；这是复现时必须查 `Expression` / `NormFactor` 的地方。

把某一 template 的 $\mu$ 限制近似换成 $g_U$ 时，$g_U^4$ scaling 仅在适当 non-resonant approximation 下有简单意义。Final model scan 还包括 width、branching fractions、flavour composition 和 interference，不能无条件使用 $g_U^{95}=g_U^{\rm ref}(\mu^{95})^{1/4}$ 重造所有 contours。见 [[U1信号模型与生成及干涉]]。

## Toy 与 asymptotic

最终 paper 明确 **CLs + pseudo-experiments**。[P] p.12。Internal note p.99 §11.4 记录过 **10,000 toys、15 个 scan steps / parameter point**，最小 $\mu=0$，最大 scan range 根据 asymptotic +2σ expected limit 调整。这些是 note 阶段的数值；正式 toy config 可采用不同 settings，不能仅由此恢复提交命令。

Pseudo-experiments 与 Asimov dataset 要分开：前者涉及随机数据实现 / test-statistic distributions，后者是无 statistical fluctuation 的期望 dataset。note 中的 Asimov sensitivity / ranking 与最终 toy limit 是不同计算。

## 最终 background-only SR yields

| Region | Observed data | Post-fit background |
|---|---:|---:|
| SR0b-Res | 33 | $36.4\pm7.3$ |
| SR0b-NonRes | 45 | $38.3\pm9.9$ |
| SR1b-Res | 3 | $2.69\pm0.83$ |
| SR1b-NonRes | 2 | $1.88\pm0.71$ |

[P] p.11 §9；pp.12–14 Figures 2–4。误差为 paper 报告的 combined prediction uncertainty；这些背景来自 **CR-only B-only fit 外推**。总体没有显著 excess。

W / top best-fit normalisations 见 [[背景估计与验证逻辑]]。Paper 中 N−1 distributions 是在去掉被画变量 cut 后展示 signal / background 的检验图，不等于 signal-region 最终 count，也不等于 fit 用了该 shape。

## 公布的 coupling limits

纯 LH、Yang–Mills scenario 下，95% CL 的 $g_U$ 上限例子：

| $m_{U_1}$ | $\beta_L^{23}$ | Observed | Expected |
|---|---:|---:|---:|
| 1.5 TeV | 1.0 | 1.13 | 1.11 |
| 1.5 TeV | 2.2 | 0.52 | 0.53 |
| 2.5 TeV | 1.0 | 2.30 | 2.19 |
| 2.5 TeV | 2.2 | 1.22 | 1.18 |

[P] p.12 §9，Figures 5–6 pp.15–16。这些 fixed-$\beta$ coupling limits 不是 mass limits，也不是 model-independent cross-section limits。当前结果覆盖 mass scan 1.5–3.0 TeV、较大 $\beta_L^{23}$ 的部分 flavour-motivated region；不能写成“排除了 $R(D^{(*)})$ anomaly 的全部 U1 解释”。

## Uncertainty impact 的读法

[P] pp.11–12 描述最终 ranking：利用 fit covariance、post-fit uncertainties 与 POI–NP correlation 估计 impact。TES 是主要 systematic，典型对 $\mu$ impact 约 10%；W+HF / W+LF 次之，约 5–10%。这些 **对 POI 的 impact** 不等于 input uncertainty 的百分数；W+HF input 是 30%，两者没有矛盾。

[N] p.74 还保留通过固定 NP 在 post-fit ±1σ、重新 fit 的传统 ranking 描述；不同 ranking construction 不应在方法章节拼接成同一种实现。对代码里的 decorrelation、pruning、Gaussian / log-normal、MC-stat 的细节，以 config 和实际 TRExFitter 版本核对。

## Favoured band 与 exclusion band

$B$-anomaly favoured 1σ / 2σ 阴影表示低能 fit 偏好的 region；expected limit 的 ±1σ / ±2σ band 表示 collider exclusion 在 background hypothesis 下的 expected fluctuations。两套 band 的统计含义、输入以及颜色约定不同。[P] p.12、Figures 5–6。低能 band 从 Ref.[35] arXiv:2210.13422 的 $C_{LL}^{c}$ 约束通过 Eq.(1) 映射；具体绘图实现应查 scripts 笔记。
''')
write('分析版本差异与待核实事项',r'''这页用于避免从不同阶段的 note、paper、slides 和代码各取一段，拼出一个实际不存在的分析版本。这里只列有具体证据的问题，后续代码确认后补充结果，不删除历史来源。

## 文献身份与默认优先级

| 文献 | 可确认的身份 | 使用方式 |
|---|---|---|
| ANA-EXOT-2025-06-INT1 | 2026-04-20；166 页；封面 Draft 0.5，changelog 到 v0.9 | 技术过程与 checks；较晚 §12 可覆盖较早 §10–11 |
| ATL-COM-PHYS-2026-015 | 2026-05-26；Draft 3.3；35 页 | 接近最终的内部 paper，但包含附录 / draft cross-reference 残留 |
| arXiv:2606.02067v1 | CERN-EP-2026-136；2026-06-01 submission，封面 06-02；42 页 | 最终公开结论；截至本次官方页只列 v1，submitted to PLB |

公开 paper 的 §3–9 与本地 05-26 draft 的主要模型、cuts、yields、limits 本次已逐段核对，数值相同；不能据此宣称整个文件完全相同。公开 PDF 已把 draft 的 Figure 8 / 9 交叉引用改为 Figure 3 / 4 等。

## 已解决：应采用哪个版本

- **2 SR → 4 SR**：[N] p.73 §10.1 / §11 是早期 SR1b-only；p.103 §12 将旧 WVR1tau 两区加入 fit 成为 SR0b。最终 [P] p.11 是四 CR + 四 SR。
- **Interference 可忽略 → 0b 必须计入**：[N] Appendix I pp.149–150 主要针对早期 1b；p.105 §12.2 更新为 0b 明显 destructive interference。最终 [P] p.11 包含 $\sqrt\mu I$。
- **W+HF 20% → 30%**：[N] p.151 Appendix J 保留 old nominal 20% 与 10/20/30% test；最终 [P] p.10 是 30%。
- **旧 WVR → 新 SR0b**：旧 WVR1tau 不是最终 VRW；最终 VRW 是旧 VR0tau。详见 [[分析区域与选择变量]]。
- **SR0b-Res MET 600 GeV 未采用**：[N] pp.164–166 Appendix N 是 test；最终 [P] p.8 Table 2 为 200 GeV。
- **最终 interpretation 只有 LH**：[N] p.115 右手解释仍有 options；[P] p.4 明确 $|\beta_R^{33}|=0$。不能把旧 right-handed cross-section plot 作为最终 result。
- **独立 signal samples 替代早期 weights scan**：[N] Appendix A pp.130–133 为 reweighting issue；[N] pp.20–21 和 [P] p.5 的正式描述是 152 独立点。旧 correction 不自动等于当前 `noWeights` / nominal 处理。
- **CLs 与 CLs+b**：[N] p.4 changelog 说明 v0.1 已从旧 CLs+b 转为 CLs；final [P] p.12 为 CLs + toys。历史图必须保留它实际采用的方法标签。

## 需要代码确认的具体差异

1. **TopCR intermediate skim lepton threshold**：[N] p.27 写 $p_T^\ell>150$ GeV，但 p.39 Table 7.2 写最终 TopCR $>28$ GeV。若 skim 真为 150，28 GeV 的 final cut 不能恢复被 skim 丢掉的事件。须检查 TopCPToolKit selection block、实际生成时的 ntuple metadata / cutflow。
2. **Jet–muon OR matching**：[N] p.26 写 `<3 tracks + ghost-associated`；[P] p.7 写 `$\Delta R<0.4$ + at most 2 tracks`。须查 OR CP-tool defaults 和 flags，二者不能仅靠文字视作完全等价。
3. **Electron–electron OR**：[N] p.26 明确 lower-$p_T$ shared-track rejection；[P] p.7 未列。须确认代码是否 enabled。
4. **Tau-specific muon overlap**：[N] p.25 指非 calo-tagged、$p_T>2$ GeV muon；general baseline muon 为 $>10$ GeV。须确认 tau tool 与 generic OR 各自实际 input。
5. **VRTop 数值**：[P] p.9 未列完整阈值；[N] p.41 Table 7.4 是 MET 200 / 200、$m_T$ 100 / 200、Res $m_{b\tau}>400$ GeV，与 TopCR 不同。正式 FastFrames regions 必须核对。
6. **VRW 的分类 jet**：旧 [N] p.38 共用表写 leading jet；paper 1b SR 用 b-jet，VRW plot 用 $m_{b\ell}$。是否 VRW 的 category boundary 用 leading inclusive jet 还是 leading b-jet，查代码。
7. **50 / 250 GeV 边界**：公开 Table 2 写 `[50,250]`，正文写 strict interval。代码中的 `>` / `>=` / `<` / `<=` 是复现依据。
8. **POI 与 toy settings**：[N] p.106 表明 $x=\sqrt\mu$；p.99 写 10k toys / 15 steps，p.74 写 1% pruning；但正式 config 可能变化。需查表达式、允许范围、scan max、seed、toy 数、MC-stat 和 correlations。
9. **NP impact 方法**：[N] p.74 是 fixed-NP refit；[P] pp.11–12 为 covariance-based linear impact，须查当时 TRExFitter option 和 plotting source。
10. **W+HF NP 的样本与区域作用范围**：paper 是 0b CR→1b transfer，note p.151 选择 Res / NonRes decorrelation；正式 config 中的 region list、sample list、30% magnitude、对 VR 是否施加仍需逐条核对。

## Internal study 的适用范围

- **$\tau\tau$ contamination**：[N] p.107 §12.4 的 1b 约 35%、0b 约 5% 来自有限 samples / rescaling；改善 $g_U$ limit 约 2–5%。没有证据表明 final nominal 已逐点加入完整 $\tau\tau$ contribution。
- **小 coupling 下 interference**：[N] Figure 12.6 p.106、Table 12.4 p.116 存在很大的 negative ratios；公开 paper “total signal positive”不能脱离所解释的参数范围使用，也不能推广到所有 $\mu$ / $x$ 的 scan domain。
- **右手 sample 数量笔误**：[N] p.21 说“5 points”却列 1.5、2、2.5、3、4、5 TeV 六个 masses。以实际 DSID inventory 确认，不在资料库凭猜测删掉其中一个。
- **$\beta_L^{13}$ 近似**：公开 p.4 footnote 给复杂 CKM ratio，同时写 $\sim0.2\beta_L^{23}$。实际 generator 必须保持 CKM convention；不要用正实 0.2 自动替换。

## 后续补充资料的最小清单

为了把本资料库推进到可复现状态，优先记录：正式运行 git commit / release；DSID 和 cross-section / filter / sum-of-weights map；使用的 YAML / config 完整副本与校验值；toy submission 参数；signal grid 和 interference availability；favoured-band input fit 的具体 numbers、version 及脚本常数。上述中代码可读取的部分由 framework / script 笔记补齐，不能因为 paper 未详述就当成不存在。
''')
print('\n'.join(str(p) for p in sorted(v.glob('*.md'))))
