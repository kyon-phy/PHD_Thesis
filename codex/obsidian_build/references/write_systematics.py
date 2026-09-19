from write_notes import write

write('50_Systematics','Systematics来源与分析实现总览',r'''
本分析把 uncertainties 分成 experimental calibration/efficiency、MC modelling、analysis-specific background estimate 和有限 MC statistics。大背景的 normalization 由 CR fit 决定，理论 uncertainties 主要作用于 CR→SR/VR transfer；因此 inclusive cross-section uncertainty 与 transfer uncertainty 不能混为一谈。

- W+HF/LF 30%的证据、20%→30%历史、Toy配置：[[Wjets_HF约30percent的依据与适用边界]]。
- Theory variation、transfer factor、smoothing、relaxed selection：[[Theory_systematics与transfer-factor处理]]。
- Tau/JES/JER/FTAG/lepton/MET/luminosity：[[Experimental_systematics与校准来源]]。
- 缺少的 calibration/derivation 文件和需要确认的事项：[[Systematics待补资料清单]]。

## 证据优先级与版本

1. 实际执行值：[Toy正式配置快照](<{CACHE}/code/snapshot/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config>)。它证明 NP 叫什么、施加给谁、幅度多少；不独立证明物理来源。
2. 较新文字说明：[ATL-COM-PHYS-2026-015.pdf](<{SRC}/ATL-COM-PHYS-2026-015.pdf>)，2026-05-26 draft，PDF 第9–11页。
3. 推导与历史研究：[ANA_EXOT_2025_06_INT1.pdf](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>)，2026-04-20，PDF 第60–74页 §9，Appendices D、G、H、J、L。
4. CP/PMG 处方：`systematics/` 下的 TWiki snapshots；是2026-09-07导出的页面，内容包含较早 recommendation。Run-3更新不能自动替代本分析 Run-2/MC20 setup。

## 已保存参考各自提供什么

- [PmgWeakBosonProcesses](<{SRC}/systematics/PmgWeakBosonProcesses _ AtlasProtected _ TWiki.pdf>)：sample setup、scale/PDF/EW recipes、HF-tag normalization discrepancy。重点 PDF 第13–15页。
- [PmgTopProcesses](<{SRC}/systematics/PmgTopProcesses _ AtlasProtected _ TWiki.pdf>)：top matching、PS、ISR/FSR、hdamp、NNLO reweighting、recoil 和 DR/DS 等。重点 PDF 第2–5页。
- [JetUncertaintiesRel22](<{SRC}/systematics/JetUncertaintiesRel22 _ AtlasProtected _ TWiki.pdf>)：R22、MC20/AF3、CategoryReduction、FullJER 的正确配置与相关性。重点 PDF 第1–2、6–9页。
- [LuminosityForPhysics](<{SRC}/systematics/LuminosityForPhysics _ Atlas _ TWiki.pdf>)：full Run-2 final tag、0.83%及140 fb⁻¹书写方式。PDF 第4页。
- [WHF_uncertainty_study](<{SRC}/systematics/WHF_uncertainty_study.pdf>)：实际是 ATLAS VHbb/VHcc 论文2410.19611v2；flavour分类、不同 phase-space 的 fitted normalization。PDF 第17–18、21–22、26页。
- [s10052-021-09402-3](<{SRC}/s10052-021-09402-3.pdf>)：JES/JER测量方法及其 uncertainties；不是 LQ theory paper。§5–6，PDF 第5–32页。

本页的状态代表资料已核对到所列版本，不表示现行工作区每次提交都会自动与这些快照同步。
''',tags='[systematics, index, provenance]')

write('50_Systematics','Wjets_HF约30percent的依据与适用边界',r'''
## 结论

本分析采用的30%是从 b-veto CR 将 W+jets normalization 外推到含 b-jet region 时，对 **HF/LF composition/relative normalization** 赋予的额外 uncertainty。HF = heavy flavour，LF = light flavour；用户最初写的“LH”在这里应理解为 LF。它不等于 inclusive W production cross-section 的30% uncertainty，也不等于 b-tagging efficiency uncertainty。

## 证据链一：PMG明确报告10–30%的差异

[PmgWeakBosonProcesses TWiki快照](<{SRC}/systematics/PmgWeakBosonProcesses _ AtlasProtected _ TWiki.pdf>) PDF 第15页，“Normalisation discrepancies due to heavy-flavour-tags”指出：要求一个或多个HF tag后，data和simulation的normalization可差10–30%；该现象不只限于一个 generator。该页引用 boson+jets PUB note §5 和 ongoing studies。

这是采用额外 composition allowance 的直接经验依据，但该句本身没有说“所有分析必须使用30% Gaussian prior”。最终幅度、sample选择、phase space、correlation仍是分析建模决定。

## 证据链二：本分析文字和正式Toy配置

[2026-05-26 paper draft](<{SRC}/ATL-COM-PHYS-2026-015.pdf>) PDF 第10页 lines298–301明确写：CRW使用b-veto，而SR含b-jet，因此对W+HF/W+LF ratio赋予30%，并引Refs.[87–90]。References在PDF第24页：

- [87] ATL-PHYS-PUB-2017-006，[CERN记录](https://cds.cern.ch/record/2261937)。
- [88] ATLAS V+jets modelling，arXiv:2112.09588，[正式记录](https://arxiv.org/abs/2112.09588)。
- [89] ATLAS Z+b/c measurement，arXiv:2403.15093，[全文](https://arxiv.org/html/2403.15093v2)。
- [90] ATLAS VHbb/VHcc，arXiv:2410.19611，即本地 `WHF_uncertainty_study.pdf`。

[Toy正式配置快照](<{CACHE}/code/snapshot/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config>) 第2932–2951行：

- `Wjets_HF_modeling_Res`：`OverallDown: -0.3`、`OverallUp: 0.3`，`Samples: W*`，`Regions: *1b*_Res*,*2b*_Res*`。
- `Wjets_HF_modeling_NonRes`：同样±0.3，`Regions: *1b*NonRes*,*2b*NonRes*`。
- 两个NP均为 `Type: OVERALL`、`Symmetrisation: TWOSIDED`。Res与NonRes是不同名称，故为分别建模的NP；0b region没有被这两项直接选中。

这里实现的是对含b-tag region的**全部 `W*` sample yield**额外variation，没有单独对truth-HF events逐事例重加权。物理上称HF/LF ratio uncertainty，代码上以tag-category transfer的overall modifier近似；两个层次应同时记载。

## 证据链三：WHF论文真正提供的量级

[WHF_uncertainty_study.pdf](<{SRC}/systematics/WHF_uncertainty_study.pdf>) PDF第26页Table4给post-fit W+jets normalization factors（errors含stat+syst）：

- $75<p_T^V<150$ GeV、≥3 jets：W+hf $1.30\pm0.07$，W+mf $1.16\pm0.04$，W+lf $1.07\pm0.05$。
- $150<p_T^V<250$ GeV、≥3 jets：W+hf $1.28\pm0.07$，W+lf $1.07\pm0.04$。
- $250<p_T^V<400$ GeV、≥3 jets：W+hf $1.46\pm0.12$，W+lf $1.10\pm0.04$。

前两项显示HF相对nominal有约30%的normalization偏差；第三项说明偏差也能大于30%。若只看HF/LF **相对**修正，三个central-value ratio分别约1.21、1.20、1.33（由上述fit值相除得到；不是论文给出的独立measurement，也不能忽略它们的correlation来计算error）。

该论文PDF第17页把`hf`定义为两jet flavours为bb或cc，`mf`为bl、cl、bc，`lf`为ll；本分析的单b-tag category与它不同。PDF第18页显示它按jet multiplicity和$p_T^V$浮动不同normalization；boosted region还有hf+mf共用因子，Table4高$p_T$数值甚至约1.5–2。因此这篇论文支持“flavour modelling需要独立约束、差异可达tens of percent”，**不能单独证明本分析所有极端相空间都被30%覆盖**。

另一个容易混淆的“30%”：PDF第18页说新增BDT使某个W+hf normalization factor的**uncertainty减少30%**，这是相对改善，不是赋予30% prior。

## 20%到30%的历史

[2026-04-20 internal note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) §9.2.1 PDF第67页仍写20%；AppendixJ第151–154页比较10/20/30%，并讨论Res/NonRes decorrelation。例子里的expected significance依次2.156、2.105、2.034，变化最大约5%；这是特定signal point，不能推广为所有mass/coupling。

[Higgs_260407.pdf](</Users/zang/Desktop/ICEPP/博士课题/leptoquark/presentation/Higgs_260407.pdf>) PDF第13页已经明确最终采用30%，同时列出Zνν+fake tau 100%和Diboson/Z+jets 30%。会议记录见 [[会议_2026-04-07_AJHiggs汇报0b加1b分析]]。这把30%的最终选择追溯到2026-04-07；April20 note第67页保留20%是文档同步问题，不能据PDF日期推断它在会议后重新回退为20%。

同一note第82页已称30%为leading uncertainty之一，也说明内部文字未完全同步。May26 paper与正式Toy配置一致使用30%，应作为当前这套设定的依据。AppendixL（第156页起）还比较0b CR、1b CR、二者联合的fit策略，解释为何低统计1b CR并非必然更优。

## 仍需补充的材料

PUB-2017-006全文未在本地references中；本次公开CERN入口返回bot-check，未声称已读其§5。建议保存PDF及PMG链接的HF专门studies。如要严谨论证30%在本分析phase space的覆盖性，还需本分析tag类别、jet multiplicity、$p_T$ dependence和CR/VR closure的验证记录。现有note/配置足以说明“为什么选择30%以及怎么施加”，不应写成外部论文直接测得的通用误差。
''',tags='[systematics, Wjets, heavy-flavour, evidence]')

write('50_Systematics','Theory_systematics与transfer-factor处理',r'''
## Transfer factor 的正确对象

对由CR约束的大背景，设 $T=N_{\rm SR}^{\rm MC}/N_{\rm CR}^{\rm MC}$。一个variation对预测的相对影响为

$$
\kappa_T=\frac{T_{\rm varied}}{T_{\rm nominal}}
=\frac{N_{\rm SR}^{\rm varied}/N_{\rm SR}^{\rm nominal}}{N_{\rm CR}^{\rm varied}/N_{\rm CR}^{\rm nominal}}.
$$

因此SR、CR同向同比变化可以抵消；若acceptance不同则保留残差。实现可写为 $N_{\rm SR}^{\rm pred}=\lambda\,N_{\rm SR}^{\rm nominal}\kappa_T(\theta)$，而CR为 $\lambda N_{\rm CR}^{\rm nominal}$。这里 $\lambda$ 是由data拟合的normalization，$\kappa_T$ 是相对修正。来源：[internal note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF第66–67页Eqs.(9.1)–(9.9)。该note Eq.(9.10)使用`TF`的写法容易将绝对transfer与相对modifier混淆；笔记以上式明确两者。

## W+jets

[note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF第67页 §9.2.1 与 [PMG WeakBoson](<{SRC}/systematics/PmgWeakBosonProcesses _ AtlasProtected _ TWiki.pdf>) 第13–15页：

- QCD scales：Sherpa internal weights的7-point variations，使用ME+PS coherent variation envelope。排除两种相反方向极端组合的7-point prescription需与实际weights确认。
- PDF及$\alpha_s$：按所用NNPDF Hessian prescription以及alternative central PDFs构造；PDF set名、LHAPDF编号和weight availability必须以production metadata核对。
- EW corrections：approximate NLO virtual EW weights；additive/multiplicative/exponentiated组合给scheme变化。本分析有额外EW correction项。
- HF/LF：单独的30% category transfer uncertainty，见 [[Wjets_HF约30percent的依据与适用边界]]。

[Toy配置](<{CACHE}/code/snapshot/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config>) 第2953行起用`OVERALL`理论NP：W QCD Res原始Down/Up为−0.17/+0.10，NonRes为−0.16/+0.14；EW为±0.04/±0.01。PDF+$\alpha_s$ Res原始字段为−0.001/−0.02，NonRes为−0.03/+0.03。这些是**symmetrisation之前的配置字段**，不能直接说全部是对称±X%；需结合TRExFitter `TWOSIDED`处理及fit输出读取最终effect。

## Top

[PMG Top](<{SRC}/systematics/PmgTopProcesses _ AtlasProtected _ TWiki.pdf>) PDF第4–5页与[note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) 第67–68页：

- NLO matching：nominal Powheg+Pythia8与`pthard=1` alternative，改变shower veto边界。
- Parton shower：Powheg+Pythia8对Powheg+Herwig7。
- QCD scales、ISR（A14 Var3c）、FSR、PDF：internal weights或dedicated variation sample。
- $h_{\rm damp}$：nominal $1.5m_t$对$3m_t$；PMG指出动态scale的$tW$也需考虑。
- Top-$p_T$：nominal NLO对NNLO reweighted prediction，物理上主要针对$t\bar t$。
- Recoil：recoil-to-colour对recoil-to-top；note讨论$t\bar t$。
- $t\bar t$–$tW$ interference：$tW$ DR对DS；这是top background内部的interference，与U1–SM interference不同。

Toy配置把多种派生top transfer NP应用于`ttbar,SingleTop`集合；不能根据名字推断每种generator variation原始作用于两个process。应保留“原始variation对象”与“合并Top prediction的最终modifier”两个层次。[同一Toy配置](<{CACHE}/code/snapshot/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config>) 第3019行起。

## Tail MC statistics、smoothing与relaxed region

[note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF第69页：先在对应CR把alternative sample归一至nominal，再比较resonance的$m_{b\tau}$或non-resonance的MET N−1分布；对ratio使用ROOT `353QH twice` smoothing，重加权nominal后积分得到SR/VR transfer effect。部分稀疏variation放宽jet multiplicity并要求 $N_b\ge1$，必要时再平滑。不是所有variation都同时使用两步。

该做法引入“looser region中的modelling difference可外推到tight SR”的假设；AppendixH（PDF第147–148页）记录验证。第68页关于b multiplicity的文字曾写成`>1b`，第69页说明为`≥1`，后者更清楚；复现应查实际script。

## Minor backgrounds与signal

Z→νν/ℓℓ中的fake tau：100% normalization uncertainty，对应note的Z+tau validation。Ztautau/Zll和Diboson：Toy中的30% overall。这些是analysis-specific conservative choices，不是inclusive cross-section precision。[note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) 第68页；[Toy配置](<{CACHE}/code/snapshot/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config>) 第2901–2930行。

Signal包含scale/PDF uncertainties（note第68页称量级约10–20%，取决于参数点）；不能把所有mass/coupling统一写成一个固定百分比。最终值与signal-specific配置/weight产物对应。
''',tags='[systematics, theory, transfer-factor, smoothing]')

write('50_Systematics','Experimental_systematics与校准来源',r'''
来源入口：[internal note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF第60–65页 §9.1和NP表；[May26 paper draft](<{SRC}/ATL-COM-PHYS-2026-015.pdf>) PDF第9–10页。下列NP名字用于快速检索；它们是note中的清单，实际保留/裁剪/重命名以正式fit配置为准。

## Tau

TES包含in-situ measurement、detector modelling、physics list和model closure。检索前缀`TAUS_TRUEHADTAU_SME_TES_`，如`INSITUEXP`、`INSITUFIT`、`DETECTOR`、`PHYSICSLIST`、`MODEL_CLOSURE`。它们会改变tau kinematics，传播到MET和region acceptance。

Efficiency包含`RECO_TOTAL`、RNNID的1-/3-prong与$p_T$ bin项、truth tau的`ELEOLR_TOTAL`，以及truth electron的`TAUS_SF_EFF_ELERNN_STAT/SYST`。不要将“electron fake tau”的SF和true-tau SF混用。（note PDF第63页）

May26 draft第10页给tau TES通常<1% correction、absolute uncertainty<1.5%；Tight ID uncertainty对1-prong约5–8%、3-prong约6–11%。这些是该paper的概括，与某个高-$p_T$ bin的总yield impact不同；尤其要保留$p_T$与prong dependence。

## Jets、JER与MET

JES采用CategoryReduction；NP反映in-situ statistical/modelling、eta intercalibration、flavour composition/response、pile-up、punch-through和high-$p_T$ response。R22又有R21→R22 non-closure、vertexing和noise变化；AF3有FullSim差异项。note PDF第64页列出准确前缀。

[JES/JER性能论文](<{SRC}/s10052-021-09402-3.pdf>) 提供物理方法：MC calibration及pile-up correction（PDF第5–11页），dijet eta-intercalibration、Z/γ+jet balance、multijet balance及combination（第12–22页），systematics及correlation reduction（第23–26页），JER measurement与应用（第26–32页）。这是支持测量方法的公开来源；R22具体config由[TWiki](<{SRC}/systematics/JetUncertaintiesRel22 _ AtlasProtected _ TWiki.pdf>)提供。

TWiki PDF第2页给Run-2/MC20对应`AntiKt4EMPFlowJets`、CategoryReduction和FullJER；MCType必须正确标记MC20或AF3。PDF第7页强调FullJER应组合MC和(pseudo-)data smearing构造templates，而不是把两套NP独立传播。SimpleJER只smear MC，会改变某些anticorrelation，仅适合对JER不敏感的情形。源码/fit是否按这个recipe完成，应查framework和histogram notes。

MET的soft-track term独立有`MET_SoftTrk_Scale`、`ResoPara`、`ResoPerp`。hard-object variation同时传播到MET；因此soft-term uncertainty不是“全部MET uncertainty”。JVT/NNJvt efficiency及pile-up residual也需与JES区分。（note PDF第64页）

## Flavour tagging与light leptons

FTAG主要是b、c、light三个truth flavour的efficiency/mistag SF。**版本差异：** internal note第63页写Loose eigenvector reduction，列`FT_EFF_Eigen_B_[0–84]`、C `[0–55]`、Light `[0–41]`；但本次读取的[TopCP入口快照](<{CACHE}/code/snapshot/TopCP/TauX_Gnt1makerAlg/python/TauX_Gnt1NtupleMaker.py>)第282–296行，对`Continuous` event SF显式设置B/C/Light三者为 **Medium**，tagger为`GN2v01`，MC20 calibration为`MC20_2025-06-17_GN2v01_v4.root`。因此不能把note的Loose/counts当成当前代码产物的确定NP数量；需以对应生产版本、实际输出branches和fit输入核实。85% analysis WP及其他输出WP见 [[DAOD处理与Object定义]]。

FTAG SF测量tagger response；W+HF/LF variation则改变physics flavour composition，二者不是重复项。

Electron包含energy scale/resolution、reconstruction/ID/isolation/trigger SF；muon包含momentum calibration、sagitta、reconstruction/isolation/TTVA/trigger SF。note第65页给清单。第62页还记录manual electron SF map：`ElectronEfficiencyCorrection/2015_2025/rel22.2/2025_Run2Rel22_Recommendation_v3/map0.txt`。应在framework snapshot中固定这一版本，不能只引用“latest recommendation”。

## Luminosity与pile-up

[LuminosityForPhysics](<{SRC}/systematics/LuminosityForPhysics _ Atlas _ TWiki.pdf>) PDF第4页明确full Run-2 final tag `OflLumi-13TeV-011`，uncertainty0.83%，通常写140 fb⁻¹，带绝对误差写 $140.1\pm1.2$ fb⁻¹。1.7%是更早推荐；不能从旧thesis搬来。0.83%只直接适用于相应full Run-2 dataset，子集需重新确认。更新tag引起约+0.8%的整体luminosity shift，但不是逐年常数缩放。

`PRW_DATASF`变动pile-up reweighting。Luminosity校准、pile-up profile reweighting和detector response to pile-up属于不同环节，不能用一个NP笼统替代。（note第63页；luminosity TWiki第4页）
''',tags='[systematics, tau, JES, JER, calibration]')

write('50_Systematics','Systematics待补资料清单',r'''
以下区分“有paper引用，但本地缺全文/具体CP处方”和“本分析赋值/实现缺推导记录”。不是说这些uncertainties没有合理来源。

## 最值得补充的reference

- **W+HF相关PUB与studies**：ATL-PHYS-PUB-2017-006 §5的原PDF、PMG第15页所链接HF studies。当前PMG快照已支持10–30%差异，正式Toy已证实采用30%；PUB全文本次CERN公开入口遇到bot-check。
- **Tau Run-2/R22 calibration**：RNN ID、TES、electron rejection、high-$p_T$ extrapolation完整CP推荐页、map/root文件版本及approval slides。note和paper已有引用/概要，但`references/systematics`没有专门tau CP PDF。特别需要检验当前RNNID高-$p_T$ bins与SF文件一致。
- **FTAG calibration与版本对应**：补充GN2v01、85%WP、`MC20_2025-06-17_GN2v01_v4.root`和high-$p_T$ extrapolation的CP推荐/uncertainty map。TopCP入口对Continuous event SF显式设置B/C/Light均为Medium，而internal note第63页写Loose；需确认正式fit样本对应哪次生产及实际NP数，见 [[Experimental_systematics与校准来源]]。paper引用的公开b/c/light效率论文提供方法，未替代当前版本配置。
- **Electron/muon/MET/JVT**：electron 2025 Run2Rel22 map、muon sagitta与trigger SF、MET soft-term、NNJvt推荐页。现有note列NP，但不足以重建每个variation来源。
- **FullJER template recipe**：JetUncertaintiesRel22第7页所链presentation的slides7–11及framework对应实施。当前TWiki已说明需要MC/(pseudo-)data组合；需要把具体算法文档与处理脚本存档。
- **PMG generic recipes**：`PmgSystematicUncertaintyRecipes`、实际PDF/alpha_s weight mapping及PMGSystematicsTool版本；已有weak-boson/top页是入口，不能单凭weight名字判断组合正确。

## 需要的是analysis记录，而非通用论文

- W+HF20%→30%的决定和Res/NonRes decorrelation记录；现有May26 paper与Toy配置一致，Apr20 note内部尚有20%/30%混用。
- `Zll_modeling`/`Diboson_modeling`统一30%的具体选择依据与validation。note写“conservative”，当前没有找到独立外部文献证明本分析每个region恰为30%。
- fake-tau100%：note AppendixD与paper有closure研究说明；建议保存最后版Z+tau验证plots、统计误差和样本设置。它是analysis-driven allowance，而不是从外部论文引用的universal fake rate error。
- 每个theory overall数值的原始yield、CR normalization、ratio、smoothing和relaxed-cut产物；general recipe只证明做法合理，不证明Toy里−17/+10%等数值。
- signal各mass/coupling的scale/PDF numerical results及是否同步传播到interference template。
- Favoured-region四端点的读图/fit记录：[[Favoured-region理论输入与区间含义]]。该项属于interpretation input，非detector systematic。

## 已可回答的问题

HF30%不是完全无出处：PMG快照第15页是直接经验来源，VHbb/VHcc Table4支持tens-of-percent且依phase-space变化，May26本分析paper明确选30%，Toy配置给出作用范围。当前主要缺“更深的完整证据归档和实施trace”，不应把所有项目都标成完全unknown。
''',status='待补文档；不阻断已验证结论',tags='[systematics, todo, sources]')

print('Wrote systematics notes')
