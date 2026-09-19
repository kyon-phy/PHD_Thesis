from pathlib import Path
import json,shutil,datetime,hashlib
V=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search')
B=Path(__file__).parent/'code'
S=V/'90_来源与维护/代码快照/2026-09-07'
S.mkdir(parents=True,exist_ok=True)
snap=json.loads((B/'remote_snapshot.json').read_text())
manifest=[]
for item in snap['files']:
 p=S/item['relative'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(item['text'])
 manifest.append({k:v for k,v in item.items() if k!='text'})
for p in (B/'defaults').glob('*'):
 if p.read_text().lstrip().startswith('<!DOCTYPE'):continue
 target=S/'CP与TREx默认实现'/p.name;target.parent.mkdir(exist_ok=True);shutil.copy2(p,target)
(S/'代码来源清单.json').write_text(json.dumps({'collected_utc':snap['collected_utc'],'files':manifest},ensure_ascii=False,indent=2))
shutil.copy2(B/'details.json',B/'details_archive.json')
(S/'脚本时间与Git记录.json').write_text(json.dumps(json.loads((B/'details.json').read_text())['scripts'],ensure_ascii=False,indent=2))
def note(folder,name,body,tags):
 p=V/folder/(name+'.md');p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('---\ntype: technical-note\nupdated: 2026-09-07\nstatus: 已核对代码快照\ntags: ['+tags+']\n---\n\n# '+name+'\n\n'+body.strip()+'\n')
note('30_Objects与DAOD','DAOD处理与Object定义',r'''
本页描述 **2026-09-07 读取的入口代码**。它有 Run 2/Run 3 共用分支；本分析论文使用 Run 2。当前 checkout 的代码、ntuple 生产时的代码和公开论文描述是三个需要对应的版本，不能仅凭目录中的 v02/v04/v05 名称证明相同。

入口：`/afs/cern.ch/work/z/zang/LQanalysis/GFW1_TopCPTool/v02/taux_gnt1makeralg/TauX_GFw1_TopCPToolkit/source/TauX_Gnt1makerAlg/python/TauX_Gnt1NtupleMaker.py`。本地副本在 `90_来源与维护/代码快照/2026-09-07/TopCP/TauX_Gnt1makerAlg/python/`；下文行号均指此快照。

## 处理顺序

`makeRecoConfiguration()` 建立 ConfigSequence：event cleaning / GRL → generator weights与CutBookkeepers → PRW → calibration与多个object WP → 组合用于OR/MET的WP → MET → track decorations → overlap removal → triggers / matching / SF → object thinning → event skimming → truth与ttbar NNLO weights → metadata → `reco` tree。`fullConfigure()` 最后解析依赖并生成算法。

这不是把所有声明的WP同时施加到最终SR。多数WP只是保留 selection/SF branches，供下游选择。[[Overlap removal与MET实现]] 解释真正用来消除重复对象的组合；[[FastFrames处理流程与Histogram]] 解释 ntuple 到 histogram 的第二次选择。

## Electron

- 自定义 `TauX_ElectronAnalysisConfig.py` 做calibration，入口开启 crack veto，`minPt=5e3` MeV，PHYSLITE不重新calibrate（L139–148）。
- OR用 `TightLH + Loose_VarRad`。此外保存 TightLH 与 Tight_VarRad / HighPtCaloOnly / 两种TightTrackOnly的组合、LooseBLayerLH NonIso及若干DNN WP。DNN条目不计算SF（L150–184）。
- `maxD0Significance=5`；reco、ID、iso correlation model均为 `TOTAL`。最终veto集合在FastFrames要求 pT>10 GeV；CR再要求 TightLH+HighPtCaloOnly，不能把后者当作所有electron的baseline定义。

## Muon

入口 calibration 要求 pT>5 GeV、|η|<2.5。OR用 `Loose + Loose_VarRad`，并保存Medium、Tight、HighPt、LowPtEfficiency等辅助WP。`maxD0Significance=3`。最终veto集合 pT>10 GeV；CR要求 `Medium + Tight_VarRad`（入口L203–243；FastFrames YAML L47–52及各CR selection）。

## Jet和b-tagging

- 容器 `AntiKt4EMPFlowJets`；启用 ghost muon association、NNJVT update、fJVT selection及efficiency。另存 Tight/Tighter fJVT decorations（L270–293附近）。存了fJVT不等于最终区域对每个jet都施加fJVT。
- ntuple显式PtEta selection pT>15 GeV、|η|<2.5；OR输入 `AnaJets.baselineJvt`。FastFrames分析jet集合改为pT>20 GeV、|η|<2.5。
- GN2v01保存85/77/70/65%固定WP及Continuous。Run 2 CDI为 `MC20_2025-06-17_GN2v01_v4.root`；Run 3另有MC23配置。Continuous event SF使用B/C/light的Medium eigenvector reduction；Wtaunu特殊DSID手动指定Sherpa2211，其他autoconfig。
- 本分析分类用 **85% WP**。`TauXFastFrame.cc` L107–119把Continuous bin≥3记为b jet；90/77/70/65%的计数虽然也定义，不能据此认为分析同时使用这些WP。

## Hadronic tau

入口保存 BaselineForFakes/Loose/Medium/Tight，RNN/GNTau、带/不带eVeto等多种组合。**OR和MET用LooseRNN + eVeto**，即当前仅有的tau `doOR=True`（L330–379）。旧PHYS p-tag/PHYSLITE可能跳过GNTau；GNTau branches存在不代表本分析改用了GNTau。

显式PtEta block写15 GeV，但25.2.51的 `tau_selection_loose_eleid.conf` 本身已经要求pT≥20 GeV、|η|落在[0,1.37]或[1.52,2.5]、|charge|=1、1或3 tracks、Loose RNN jet ID与Loose electron RNN veto。因此不能把15 GeV误报为经过Loose WP后的完整tau threshold。

FastFrames `wpSet0`后又要求 `LooseRNN_noElVeto` 与pT>20 GeV。这不会撤销此前由wpSet0/OR施加的eVeto。SR/TopCR再要求 `select_TightRNN_NOSYS()==1`。当前SF组合却是Medium RNN ID+reco，加Loose RNN true-tau及fake-tau eVeto SF（`TauXFastFrame.cc` L82）。这是必须连同TauCP建议/会议来源保留的分析约定，不能把“tight选择”写成“tight SF”。见[[会议资料索引]]中2026-01-09会议及[[系统误差总览与来源缺口]]（若标题更新，在50_Systematics检索tau SF）。

## Ntuple skimming

入口L531–568的三条保留路径，单位换算后为：

- `zerolep`：恰好1个pT>50 GeV tau；pT>5 GeV electron+muon数为0；MET≥150 GeV。
- `onelep`：恰好1个pT>50 GeV tau；pT>20 GeV light-lepton数为1；MET≥50 GeV。
- `zerotau`：pT>1 GeV tau数为0（实际仍受此前WP约束）；pT>150 GeV light-lepton数为1；MET≥150 GeV。

signal DSID设置 `forceNoFilter=True`，防止此筛选切掉重新加权所需事件；background/data保持event filter。`noFilter`参数用于trigger过滤，不能直接推断background/data的event skimming也被关掉。正式TopCR下游 pT(lepton)>28 GeV，**150 GeV属于zerotau路径，不是TopCR**。

## 输出与追溯

输出tree `reco`；prefix为 `el_ / mu_ / tau_ / jet_ / MET_wpSet0_`，系统变动使用 `%SYS%` / `NOSYS`命名。`metadataTauX` 存 `wp` 和 `WPSet_OR` YAML。这份metadata与实际production日志，是确认旧ntuple生产设定最直接的证据。当前文件头还含v5 TODO（eVeto修复、muon SF等）；TODO是开发记录，不应当作已应用的生产修复。

来源：入口L33–57、59–129、139–398、431–568、664–686；FastFrames YAML L1–57、176–345。完整路径与SHA-256见[[代码版本与资料来源]]。
''','objects, DAOD, TopCPToolkit')
note('30_Objects与DAOD','Overlap removal与MET实现',r'''
**当前配置只产生一个 `wpSet0`：electron TightLH_Loose_VarRad、muon Loose_Loose_VarRad、tau LooseRNN（带eVeto）**。由 `WorkingPointHelperTauX.py` 的Cartesian product生成；OR不是对所有保存的WP分别做一遍。

## 从入口追到CP默认实现

`TauX_Gnt1NtupleMaker.py` L438–451设置 `inputLabel=prewpSet0`、`outputLabel=passOR_wpSet0`、`addPreselection=True`，并指定三个lepton容器和 `AnaJets.baselineJvt`。没有改boostedLeptons、bJetLabel或各ΔR阈值，故需读取安装release默认值。

读取的build `CMakeCache.txt`指向 **AnalysisBase 25.2.51**。本页核对该release的 `AsgAnalysisAlgorithms/OverlapAnalysisConfig.py`，以及Athena `release/25.2.51` 的AssociationUtils C++。只知道入口里的 `makeConfig('OverlapRemoval')` 不足以推导下面的先后顺序。

## 有效执行顺序

1. **tau–electron、tau–muon**：先删与存活electron或muon距离小于0.2的tau。
2. **electron–muon**：共享ID track时通常删electron；若muon是CaloTagged，工具先删除与electron共享track的此类muon。默认不是简单的ΔR matching。
3. **electron–jet**：内圈0.2优先删jet；随后0.4外圈内仍与jet重叠的electron被删。bJetLabel为空，没有额外b-jet优先保护；boostedLeptons=False，没有sliding cone。
4. **muon–jet**：jet的 `NumTrkPt500` 在PV处少于3，且满足 **ghost association或内圈ΔR<0.2** 时删jet；之后对存活jet，用外圈0.4删除重叠muon。默认 `ApplyRelPt=False`，不能将定义但未启用的pT-ratio判据写进选择。
5. **tau–jet**：最后删距离存活tau小于0.2的jet。C++实际调用参数顺序为 `(jets, taus)`，因此删除jet而不是tau。

这些工具默认 `UseRapidity=True`，距离是 $\Delta R_y=\sqrt{(\Delta y)^2+(\Delta\phi)^2}$。若论文把ΔR统一定义成η，需要说明实现细节，不能悄悄认为完全相同。对象在更早步骤已被删除，后续步骤不会再次恢复。

**来源定位**：`OverlapAnalysisConfig.py` L24–29、L356–425；`OverlapRemovalTool.cxx` L98–120；`EleMuSharedTrkOverlapTool.cxx` L92–145；`EleJetOverlapTool.cxx` L29–50及125–175；`MuJetOverlapTool.cxx` L32–60、144–220；`MuJetGhostDRMatcher.h` L20–26。公开源码：[Athena release/25.2.51 AssociationUtils](https://gitlab.cern.ch/atlas/athena/-/tree/release/25.2.51/PhysicsAnalysis/AnalysisCommon/AssociationUtils)。本地副本见[[代码版本与资料来源]]。

## MET如何使用objects

入口L402–411对每个WPset建立 `OutMet_wpSet0`；electron/muon/tau选相应WP，jet传入整个 `AnaJets`，由MET maker自己的jet selection处理。不是把最终SR中剩余的objects直接矢量求和。

25.2.51 `MetAnalysisConfig.py` L16–49默认：`metWP=Tight`、`useJVT=True`、`useFJVT=False`、`setMuonJetEMScale=True`。所以在jet准备时计算fJVT decoration，并不意味着MET启用了fJVT。

MET使用 `MET_Core_AntiKt4EMPFlow` 和 `METAssoc_AntiKt4EMPFlow`，PFlow处理开启；MC加入METSystematicsTool。读取lepton/tau selection时显式 `excludeFrom={'or'}`（L99–106），通过association map自身处理信号重叠。MET block在入口OR block之前出现，与这一实现一致；不能断言它使用了完整的分析OR输出。

## 与文献比对时保留的边界

论文中的jet–tau 0.2与当前代码相符。Muon–jet的论文简述“0.4内少轨迹jet”比实际“ghost或0.2内圈→0.4外圈”的规则简略。以往production是否完全使用25.2.51，仍需 `metadataTauX`、生成日志和release记录串联核验。资料库保留当前实现与文献各自的事实，不据此改动分析代码。
''','objects, overlap-removal, MET')
note('40_Histogram与Fit','FastFrames处理流程与Histogram',r'''
用户提到的 `FastFrame.cc`，本checkout实际分析入口是 **`TauXFastFrame/Root/TauXFastFrame.cc`**，核心调度是 `FastFrames/Root/MainFrame.cc`。这两层分工不同：前者定义本分析的objects、flags、SF与变量；后者读取样本、传播systematics、应用regions、填histograms及输出。

## 输入到输出的链

```mermaid
flowchart LR
  A[DAOD] --> B[TopCPToolkit reco ntuple]
  B --> C[metadata: filelist / sumW / xsec]
  C --> D[TauXFastFrame objects与变量]
  D --> E[YAML region selections与weights]
  E --> F[各sample与systematic的ROOT histograms]
  F --> G[BSM和interference模板组合]
  G --> H[TRExFitter config与workspace]
  H --> I[Toy CLs与参数扫描]
```

基准YAML为 `taunub/config_taunub/config_taunub_plot_sys_1l_w_beamspot_v04.yml`。它读取 `input/filelist_v04.txt`、`input/sum_of_weights_v04.txt`、本地 `PMGxsecDB_mc16.txt`，tree=`reco`、class=`TauXFastFrame`，输出到 `run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04`（L1–40）。当前工作文件有未提交修改，完整证据见[[代码版本与资料来源]]。

## Object与变量

`TauXFastFrame.cc` L35–51把各 `presel_*` 与 `*_select_wpSet0_NOSYS`相与，再用 `TauXHelpers::add_*_vector()`建立分析objects。计数、排序后的b jet、MET、trigger flags和event SF随后通过 `systematicRedefine` / `systematicStringDefine`建立。返回值不足时变量常用-999 sentinel；region选择需先保证objects存在。

`flag_minDPhi` 的实际函数为：遍历**全部所选jets与taus**，找到与MET方位角最近的对象，要求最小Δφ≥0.4 **或** MET/pT(该对象)≥6；不是仅对leading jet，也不是“所有objects的MET/pT都大于6”（`TauXHelpers.cc` L92–112）。

本分析的Run 2 MET menu在 `TauXHelpers::getMETflag` L116–149，MC使用randomRunNumber，data用runNumber。2016/17/18还按run区间选择不同trigger。更多见20_Trigger。

## Event weight与normalisation

YAML默认event weight为：

$$w_\mathrm{evt}=w_\mathrm{MC}\,w_\mathrm{pileup}\,w_\mathrm{beamspot}\,SF_\tau SF_e SF_\mu SF_\mathrm{JVT} SF_\mathrm{btag}\,SF_\mathrm{SLT}.$$

具体branches：`weight_mc_NOSYS * weight_pileup_NOSYS * weight_beamspot * tauSF_NOSYS * elSF_NOSYS * muonSF_NOSYS * jetSF_NOSYS * weight_ftag_effSF_GN2v01_Continuous_NOSYS * globalTriggerEffSFSLT_wpSet0_NOSYS`。FastFrames再自动乘 $\mathcal L\sigma_\mathrm{effective}/\sum w$；effective xsec由metadata/PMG表解释filter efficiency和k-factor。不要在TREx再重复乘140 fb⁻¹。官方说明见[histogramming weights](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/documentation/histogramming/)，本地实现见 `MainFrame.cc`的weight metadata与total-weight构造。

`noWeights` 是样本命名中的分析约定，**不等于event weight=1**。本YAML中noWeights信号仍继承默认SF/normalisation。信号耦合reweighting是否开启，要看每个sample的event_weights、sumweights和输入DSID。

当前基础YAML同时定义 `ttbar`、分campaign ttbar和 `ttbar_NNLO_mc20*`用于比较；只有后者显式多乘 `weight_NNLO_3D_NOSYS`（L417–453）。正式Toy config读取名为 `ttbar.root` 的模板，不能仅因文件里有NNLO样本就证明fit读入的是NNLO模板。生产/重命名记录需要单独保留。

## Histogram命名和region名称

`regions`定义 selection、variable definition和binning；当前fit输入主变量 `met` 统一MeV→GeV，很多区域直接使用 `[0,2000]` 单bin。绘制N-minus-1图的其它config另有多bin，不能据其图形判断正式fit用了shape information。

输出定位例子：sample `Wjets` → `Wjets.root`；nominal目录 `NOSYS`；SR1b Res变量为 `NOSYS/met_SR_1tau0l1b_sch`。`sch/tch` 是代码中Res/NonRes的历史名称，不是严格按Feynman diagram划分生成事件。

**SR0b在ROOT中仍叫WVR**：正式Toy config将 `met_WVR_1tau0l0b_sch/tch`装入 `SR_1tau0l0b_Res/NonRes_met`，标记为SIGNAL。看histogram文件名中的WVR不能据此当作validation-only。

## Systematics如何进入histogram

YAML开启 `automatic_systematics: True`、`nominal_only: False`；CP ntuple中的变动及自动systematics映射用于替换相关objects、selection和weight。C++使用systematic-aware的define，避免仅重新加权而遗漏迁移。手动systematic可以覆盖自动同名定义；理论weight若需要不同sumW必须显式指定，不能默认认为每个variation都有自己的normalisation。[官方systematics说明](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/documentation/systematics/)

产生过的variation不一定最终入fit：TREx还执行sample/region筛选、combine、symmetrisation和pruning。见[[正式Toy配置与TRExFitter统计模型]]。

## 执行入口

在已设置好ROOT/FastFrames环境的CERN工作区运行，当前官方CLI为 `python3 FastFrames.py --config <yaml>`；本项目实际环境脚本与批处理命令见80_Scripts。这里保存的是方法说明，整理资料时没有运行生产histogram、提交fit jobs或改写ROOT输出。

FastFrames的[custom class](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/documentation/custom_classes/)与[TRExFitter integration](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/documentation/trexfitter_integration/)用于解释框架接口；`latest`为访问日2026-09-07的在线版本，分析实际checkout为 `48fe08ca37679344a93fad492aefdac428788930`，不要把在线新增功能自动归于本分析。
''','FastFrames, histogram, framework')
note('40_Histogram与Fit','正式Toy配置与TRExFitter统计模型',r'''
基准是用户指定的正式提交模板：

`/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_0b1bSR_Toy.config`

以下数值均从2026-09-07快照读取。模板示例信号为 `MU1500_gU1_5_23L0_2`；逐信号生成config可能改Job名、signal样本及scan range。模板中的ScanMax=3不能代表所有已提交任务。

## 实际拟合内容

- `ReadFrom: HIST`，`Lumi: 1`，显示标签140 fb⁻¹。FastFrames histograms已normalised；标签不参与数值运算。
- 4个SIGNAL区：SR1b / SR0b × Res / NonRes；4个CONTROL区：WCR / TopCR × Res / NonRes。另定义BVR和TopVR各两区为VALIDATION。
- `FitRegion: CRSR`，`FitType: SPLUSB`。VALIDATION可画预测，但不因此成为此fit的Poisson约束项。
- 每个区域 `Rebinning: 0,2000`，`MergeUnderOverFlow: True`。这份模板按区域单bin做计数fit；不是把MET连续分布做多bin shape fit。
- `BlindSRs / FitBlind / LimitBlind = False`。`POIAsimov=1`用于相应Asimov设置，不能把它解读成observed fit强制信号强度为1。

来源：config L5–80、L86–241。

## Interference与POI

POI是 $q=\sqrt\mu\ge0$，而不是名叫mu的线性信号系数。Combined样本模板是 $S+I$，其NormFactor为q；纯BSM样本模板是S，其factor为 $q^2-q$：

$$q(S+I)+(q^2-q)S+B=q^2S+qI+B=\mu S+\sqrt\mu I+B.$$

因此并没有把BSM重复相加。`Norm_BSM`在0<q<1时为负是此代数重写的一部分；需要检查的是完整Poisson期望是否有效。$I$可为负，不能把它当作独立非负background。

config L349–364：`sqrt_mu` Nominal1/Min0/Max3，`Expression: (sqrt_mu^2-sqrt_mu): sqrt_mu[1,0,3]`。结果ROOT中的upper-limit数值对应**实际POI q**；转成μ需平方。画q=1的排除等高线与μ=1边界相同，但不能因此把轴或数值解释随意互换。

## Background约束与correlation

4个free normalisation：`top_Norm_Res / top_Norm_NonRes`作用于ttbar与SingleTop；`Wjets_Norm_Res / Wjets_Norm_NonRes`作用于W*；均Nominal1、[0,3]。Res/NonRes独立；同一拓扑内跨所指定区域共享同名factor。

HF是额外的30%相对归一化不确定度：`Wjets_HF_modeling_Res`匹配 `*1b*_Res*,*2b*_Res*`，NonRes对应另外一个NP。作用Samples=`W*`、Type=OVERALL、TWOSIDED、OverallUp/Down=±0.3。**按b-tag区域的W预测施加，不是按truth HF label挑一个独立HF样本；0b区不直接加这项。** 把它解释成从WCR向b-tag区域转移时的HF/LF建模自由度更准确。来源config L2932–2951。

不同名称产生两个独立NP；`CorrelationThreshold:0.2`控制相关矩阵显示阈值，不把所有NP相关系数设置为0.2。

## 系统误差处理

`MCstatThreshold=0.01`；shape/norm pruning thresholds均0.01；`SmoothingOption=MAXVARIATION`，但所有区域 `SkipSmoothing=True`。不能只读全局项就说每个形状均已平滑。

信号PDF replicas通过STANDARDDEVIATION合成；scale variations及CP histo系统项随后配置。声明数量不等于最终自由NP数，需workspace/pruning日志确认。非W的OVERALL例子：Znunu/Zll fake tau100%，Zll/Ztautau30%，Diboson30%（L2901–2930）。各理论项的不对称幅度及参考缺口见50_Systematics。

## Toy limits

模板启用 `LimitType: TOYS`，每个scan point生成10000 S+B toys和10000 B-only toys；15个scan points，q从0到3。没有设置ToysSeed时，本地TRExFitter v1.2.1 `LimitToys.cc`默认1234。

本地实现使用 `FrequentistCalculator`、one-sided `ProfileLikelihoodTestStat`、`HypoTestInverter.UseCLs(true)`和95% CL；以fixed scan寻找upper limit。输出 `Limits/Toys.root`，`stats` tree含 `observedLimit`、`expectedLimit`及±1/2σ分位点。tree的每一行是一个scan point，upper limit值在这些行重复（`LimitToys.cc` L25–79、L127–177）。

`toy_config_maker.py --combined`从asymptotic的 `Limits/Asymptotics/myLimit.root`读预期分位点，设置q_min=0，q_max=q_(+2σ)+|q_(+2σ)−q_(+1σ)|，并要求至少1.1；无效数值时用50。此范围还写回q及Norm_BSM表达式。其变量名有mu，仍应按输入workspace的真实POI解释。更多使用方法见80_Scripts。

## 正式config与生产结果的区分

本页确认的是模板与实现。最终结果复现还需要：每个signal的生成config、输入histogram checksum、pruning/fit日志、Toys.root、相同软件环境。整理过程没有重新跑toys，因此不声称已复现limits。

在线[TRExFitter documentation](https://trexfitter-docs.web.cern.ch/trexfitter-docs/latest/)在本次无会话读取时跳转CERN SSO，正文未取得；上述语义通过本机CERN checkout的 `jobSchema.config / ConfigReader.cc / LimitToys.cc`交叉核对。本地版本 **v1.2.1，commit f0fb71a839c819721736d9491913e991f9799b13**，不冒充已读取在线latest的全部文档。
''','TRExFitter, toys, fit, interference')
note('80_Scripts','B-anomaly favoured region计算与绘图',r'''
主程序是 `run/scripts/draw_limits_mu.py`。本页区分两种完全不同的图层：**ATLAS数据给出的excluded contour**与**flavour fit给出的favoured band**。后者不是从本实验的Toy limits拟合出来的。

## 当前执行公式

`draw_limits_mu.py` L1788–1825使用 $\beta_L^{33}=1$、$\beta_R^{33}=0$ 的纯左手情形：

$$C_{LL}^{c}=\frac{g_U^2v^2}{4M_U^2}\left(1+\frac{V_{cs}}{V_{cb}}\beta_L^{23}\right).$$

实际常数 `v=246` GeV、`Vcs=0.97349`、`Vcb=0.04182`。函数的mass参数单位必须为GeV。CKM项中的1对应第三代耦合的Vcb贡献，不能用单纯 $g_U^2\beta_L^{23}/M_U^2$ 替代；尤其β23→0时该项仍在。

当前硬编码区间：1σ为 **[0.038,0.090]**，2σ为 **[0.018,0.110]**。代码注释还写 `0.051 ± 0.027`，但这不是执行时区间。下列inverse functions没有重新做flavour likelihood fit。

固定mass、横轴gU、纵轴β23：

$$\beta_{\min,\max}=\frac{4M_U^2 C_{\min,\max}/(g_U^2v^2)-1}{V_{cs}/V_{cb}}.$$

固定β23、横轴mass、纵轴gU：

$$g_{\min,\max}=\sqrt{\frac{4M_U^2 C_{\min,\max}}{v^2(1+V_{cs}\beta_L^{23}/V_{cb})}}.$$

`get_beta_limit_from_cLL`返回(lower,upper)，而`get_gU_limit_from_cLL`返回(high,low)，调用时需注意顺序。适用gU>0、mass>0、根号分母为正；当前物理扫描β23≥0满足后者。不要把公式外推为βR33≠0情形的完整favoured region。

## 阴影如何构造

`fill_between_curves()` L1853–1915在gU轴采样（默认100点），计算上下β边界，沿上界正向及下界反向拼成闭合TGraph，再填充。函数默认sigma=2，但真正展示哪条带由调用处sigma实参决定；图形axes会裁剪画布外的负β部分，程序并没有重新定义flavour likelihood。

`draw_gU_beta_limit_from_cLL()` L2123以后对固定β的mass–gU平面同样画上下界；两条边界都线性随mass变化，所以函数默认只需两端点。变量名 `mu slice`中的mu指MU质量，并非fit signal strength μ，阅读函数名要结合输入。

## 数值例子与来源边界

在M=1500 GeV、β23=0.2时，可用下面独立于ROOT的公式复算上下gU；这是检查单位和边界的办法，不是重做flavour fit：

```python
from math import sqrt
M, v, beta = 1500., 246., 0.2
r = 0.97349 / 0.04182
for label, bounds in [('1sigma',(0.038,0.090)), ('2sigma',(0.018,0.110))]:
    print(label, [sqrt(4*M*M*C/(v*v*(1+r*beta))) for C in bounds])
```

四个端点在本地 `2210.13422v3.pdf` 的PDF p5 Fig.1二维 $(C_{LL}^c,C_{LR}^c)$ contours与 $C_{LR}^c=0$ 横线的交点处有相符的图形依据；正文未列四个精确数。**目前尚未找到数值提取记录，不能确认是digitisation还是作者给的数据。二维置信等高线的切片，也不能自动叫作固定纯LH模型后重新profile的一参数1σ/2σ区间。** 需补该端点来源/提取说明，见[[待补资料与版本差异]]。

历史报告 `EB_meeting_260213_v1.pdf`实际为2026-02-12 AJ tau meeting，p2用0.051±0.027；2025-03-07报告还用更粗略gU²β23β33 scaling。当前文件保留 `get_gU_limit_for_b_anomalies()`和 `get_b_anomalies_production_limit()`等legacy函数，不能把这些未选用的路径混为现行band。参见[[会议资料索引]]与10_理论与动机。

## ATLAS exclusion图层的计算

1. `scan_input_dir_limits`从目录名解析(MU,gU,β23)，普通模式读 `Limits/Asymptotics/myLimit.root`；`--use_toy`读 `Limits/Toys.root`。对应stats branches不同（L560–738）。
2. `--unblind True`将dict名为 `exp` 的central字段改为observed limit；±1σ/2σ字段仍取expected。这是内部命名复用，不能把这些边带称为observed uncertainty。
3. 非AcceptanceEff模式先 `enforce_monotonic_limits()`，然后 `interpolate_function.build_full_grid_monotone(...,clip_max=99)`补扫描网格，再从2D histogram提取level=1等高线。该程序**会修改非单调点、插值和裁剪**，产图不是原始离散fit points的直接连线。最终图应保留raw limits及插值策略记录。
4. `get_first_contour_at_level()`只返回第一条contour；若出现不连通区域，应检查是否丢失其它分支。
5. Toy workspace的POI是q=√μ。程序读出值没有自动平方；level1的排除边界相同，但打印成“μ_exp”的数值仍需按q解释。

来源：主脚本L560–741、L741–832、L958–1052、L1788–1915、L2123–2155、L2870–2920；插值函数完整副本见[[代码版本与资料来源]]。

## 使用示例

在CERN的run/scripts目录、已加载ROOT/numpy/scipy环境后：

```bash
python3 draw_limits_mu.py \
  --input_dir '<逐信号fit结果父目录>' \
  --out_dir '<新的绘图输出目录>' \
  --sig noWeights \
  --use_toy \
  --unblind True
```

此处尖括号为需替换的路径。输出包括 `output_mu_contours.root`和mass/β切片图。只需要expected图则省略`--unblind True`。`--plot_option combined`是叠加已有contour图层的绘图选项，不会重新做统计combined fit。`--limit_path / --extra_path_1 / --extra_path_2`指定已有ROOT contour文件。

默认 `--sig alldecay`和默认limit_path带旧HF0_2名称；用当前noWeights Toy结果时应显式指定。脚本无独立“只画favoured band”的CLI；要仅做公式研究可调用上述纯函数，或用短小独立计算，不能假定运行main不需要ROOT与limit inputs。
''','scripts, flavour, favoured-region, U1')
note('90_来源与维护','代码版本与资料来源',r'''
采集日期2026-09-07；远程访问通过现有SSH `codex_lxplus`，只读分析代码、配置、git记录与文件stat。没有执行run/scripts中的生产/提交脚本。

## 本地可查的代码副本

`90_来源与维护/代码快照/2026-09-07/`保存351份原始文本文件：37个run/scripts Python/shell脚本、21个TauXFastFrame实现/头文件、85个FastFrames框架文件、195份taunub配置、13份TopCP入口与辅助Python文件。CP/AssociationUtils及TREx关键默认实现另存在 `CP与TREx默认实现`。

`代码来源清单.json`记录每份远程原始路径、relative path、size、mtime、ctime、birthtime和SHA-256，便于以后判断源码有无更新。副本是本次采集版本，不会自动与CERN同步。未复制ROOT样本、fit outputs、大型图目录或credentials。

## 版本标识

- taux_fastframes主仓库：`484a60cb439ab1c9fb4a1d201c5a6f20b130bc49`；有未提交修改，包括draw_limits_mu.py、eps_modifier.py和基础v04 YAML。
- FastFrames子仓库：`48fe08ca37679344a93fad492aefdac428788930`，也有工作树修改。
- TauX_Gnt1makerAlg：`29a77b4b82489a70d63d757f1798a8608955d7f6`。
- TopCP所在工作树：`fa924baff7a63489ef3d691d7ba71af500cac14d`；当前build AnalysisBase **25.2.51**。
- TRExFitter实际仓库位于 `TRExFitter/TRExFitter`，版本 **v1.2.1**，commit `f0fb71a839c819721736d9491913e991f9799b13`。外层TRExFitter目录不是同一个git repo。

实际文本checksum比单独commit更能标识本次读取的未提交状态。复现实验论文还需要当时production版本、input ntuple metadata和输出模板hash，当前checkout不能单独完成这条追溯链。

## 时间如何解释

AFS `stat`的birth time均不可得（`-`），Python亦未提供st_birthtime；**ctime是inode状态改变时间，不是创建时间**。37脚本中只有draw_limits_mu.py、eps_modifier.py、signal_yield_plotter.py有首次git加入记录：2026-05-17T23:51:09+02:00，commit c9a747b。其余脚本当前untracked，创建时间应写“未知”。

脚本笔记同时保留mtime用于比较新旧，但mtime可能因复制、touch或restore改变；首次Git加入时间也只能作为已存在的证据。完整记录在 `脚本时间与Git记录.json`，不能用本地副本的创建日期冒充原脚本创建日期。

## 在线资料

FastFrames官方latest的histogramming/systematics/custom classes/TREx integration/configuration/metadata页面已读取，访问日2026-09-07；工具语义需要结合本地checkout。TREx hosted documentation跳转CERN SSO，正文未取得，改以本地version/schema/ConfigReader/LimitToys核对。AssociationUtils取自官方Athena `release/25.2.51`源码和同release CVMFS安装。
''','sources, code, provenance')
print('wrote code notes and',len(manifest),'source snapshots')
