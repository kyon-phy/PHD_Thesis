exec(open('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/meetings/build_notes.py').read())
def N(g):return '[['+notes[g]+']]'
def P(g,p,label=None):return link(d['selected'][g],p,label or f'原报告 p.{p}')
def topic(name,body):write(name,front('meeting-topic','curated')+'---\n\n# '+name.replace('会议专题_','')+'\n\n[[会议资料索引]] · [[会议资料_分析演进时间线]]\n\n'+body+'\n')

topic('会议专题_对象校准与framework演进',fr'''这条路线解决“哪个object/WP/SF是何时开始用的”以及“framework比较是否完成”。完整object definition和overlap removal仍应以现行TopCPToolKit入口与内部说明为准；会议记录提供设定变更的原因。

## framework和输入样本

- **2022-11**：{N('TauX_tec_meeting')}介绍xTAUFramework编译、Grid提交、变量组与channel扩展（p2–6）。这是旧链的运行资料。
- **2023-11**：{N('analysis_meeting_231128')} p4记录AnalysisTop将迁移到TopCPToolKit，并完成General Ntuple 2生产。这里的“GN2”指ntuple层级，与后来的GN2 b-tagging不是同一概念。
- **2024-02**：{N('analysis_meeting_240206')} p13–21同sample cross-check尚有约20%event差异，需查OR或额外preselection；raw与weighted结果都有差异，不能简单归因于normalisation。
- **2024-04**：{N('analysis_meeting_240430')} p15–20在匹配object definition后确认xTAU与GFW1一致，开始以AnalysisTop/GFW1处理flat ntuples。该结果只支持当时匹配后的对照，不能保证所有后续版本相同。
- **2025-01**：{N('TauX_weekly_250115')} p2–8验证TopCPToolKit→FastFrames的systematic propagation；部分tau/muon/jet variation不动，属于调试问题，不能当零uncertainty。
- **2025-06**：{N('analysis_meeting_0617')} p5记录p5855→p6490、GN2v00→GN2v01，加入b-tag、electron(R21)及global-SLT efficiency SF。R22 electron SF当时还未就绪。

## tau ID与electron veto

1. 早期以RNN tau working points比较fake rejection；{N('analysis_meeting_231128')} p12和p22把Zll+tau中tau-pT偏移定位至RNN ID，说明tau选择会改变fake composition。
2. {N('EB_meeting_251103')} p12与{N('unblinding_request_251205')} p10解释保留RNN而未转GNTau：Run-2-only、hard pT/MET后fake背景很小、recommendation时间线。
3. **2025-12-12尚未定案**：tight RNN+eVeto对应的SF未提供。报告当时是在baseline loose-RNN+eVeto上加tight RNN，并讨论以tight-RNN/no-eVeto SF替代；e-fake贡献至多约3%，true-tau ELEOLR variation约1–2%。{P('TauX_weekly_251212',12)} {P('TauX_weekly_251212',20)}
4. **2026-01明确建议**：TauCP同意以medium-RNN+loose-eVeto的SF代替缺少的对应组合。选择仍是tight RNN，而不是把signal tau ID放松到medium。{P('EB_meeting_260109',2)} {P('EB_meeting_260109',16)}
5. **2026-04完整汇报**：明确写signal tau为tight RNN+loose eVeto，并沿用上述SF安排。{P('Higgs_260407',9)}

此处要区分**实际选择WP**与**用于校正的SF来源WP**。精确到代码时，还应区分tau-ID SF、electron-veto SF、truth-fake类型和各自NP；会议简写不能替代对应工具的配置。

## electron、muon与trigger

- {N('analysis_meeting_230418')} p17是早期Run-2 trigger menu；{N('analysis_meeting_230801')} p8–9和{N('analysis_meeting_231010')} p12在Zμμ+tau控制样本检验MET turn-on。
- {N('analysis_meeting_0415')} p20为TopCR转用single-lepton trigger的直接动机：要进入低MET region。
- {N('EB_meeting_251103')} p6记录R22 electron efficiency与F-tag更新，以及muon从loose到tight isolation。
- {N('unblinding_request_251205')} p11记Muon CP建议pT>300 GeV使用HighPt；分析暂保留medium，理由包含已有production、muon NP对POI影响低，以及合并e/μ CR后更稳定。这是具体分析的讨论记录，不能当通用muon recommendation。

## 仍要回代码核对的内容

会议不提供完整、逐行可执行的OR顺序，也不能仅凭“objects definition”图知道baseline和signal decorators的作用域。遇到“τ–jet OR”“muon isolation变化”“trigger matching/efficiency”等问题，先用会议定位版本，再查Python配置、C++选择及最终fit输入；不要从一个旧slide推断最新实现。
''')

topic('会议专题_信号模型与favoredregion演进',fr'''这条路线重点保存favored-region的**计算口径演进**，并区分signal reweighting、模型预测与数据给出的exclusion limit。不能把三者都当作一条“limit”。

## signal sample为什么换过

- 2022年kickoff与初次ICEPP使用单CV1 scenario的1.5/20 TeV truth samples复现理论cutflow：{N('Taux_kickoff')}、{N('analysis_meeting_221101')}。它们不是最终detector-level U1参数网格。
- 2025年1–3月发现hard-b SR主要选择resonance，跨mass重加权和βR33重加权无法可靠重现相应分布：{N('analysis_meeting_250128')} p19；{N('TauX_weekly_250307')} p3；{N('LPX_weekly_250331')} p12–13。因此申请独立mass/right-handed samples。
- 2025年10–11月进一步查明internal weights没有正确随coupling改变width，影响resonant yield。用M(b,τ)与truth b-pT作额外correction，PMG仍倾向直接生成参数点：{N('TauX_weekly_251031')} p2–14；{N('EB_meeting_251103')} p8–10。
- 2026年2月报告使用new signals，靠近limit补充网格，并用`griddata`在$(m_U,g_U,\beta_L^{{23}})$三维作linear interpolation：{N('EB_meeting_260213')} p8–9。精确插值自变量、孔洞/凸包外处理与最后画图算法，需查实际scripts。

## 2025年早期favored band：由原论文带做近似缩放

2025-03-07的backup p23写，以固定质量和$\beta_L^{{33}}=1$，把$g_U^2\beta_L^{{23}}\beta_L^{{33}}$看作常数来画带。1.5 TeV的上下边界锚点分别是

$$g_U^2\beta_L^{{23}}\beta_L^{{33}}=2.2^2\times0.2\times1,$$
$$g_U^2\beta_L^{{23}}\beta_L^{{33}}=0.93^2\times0.2\times1.$$

p27另给2.5 TeV上边界$3.6^2\times0.2\times1$。这几项已对原PDF图像核对。{P('TauX_weekly_250307',23)} {P('TauX_weekly_250307',27)}

这些是**旧图的换算参数**，不是最新低能fit输入。该报告同时提醒mass reweighting问题；p22/p23的ττ comparison也包含粗略cross-section scaling假设。因此不应用它直接复现最终favored region或断言其它分析的完整二维排除。

## 2025年11月：显式保留CKM项

EB报告p4给出在固定mass与$\beta_L^{{33}}=1$下相关组合$g_U^2[1+(V_{{cs}}/V_{{cb}})\beta_L^{{23}}]$；大βL23与小gU的区域是τν相对ττ的互补目标。{P('EB_meeting_251103',4)}

相较仅用$g_U^2\beta_L^{{23}}$，括号里的常数1代表不能任意丢掉的另一项；当β较小时尤其不能直接沿用旧缩放。这个专题记录slides的表达，模型及matching推导须与理论论文对照。

## 2026年2月：固定slice直接由CLLc计算

实际标题为**AJ tau meeting 2026-02-12**的`EB_meeting_260213_v1.pdf` p2明确给出（已视觉核对）：

$$C_{{LL}}^c=\frac{{g_U^2v^2}}{{4M_U^2}}\left(1+\frac{{V_{{cs}}}}{{V_{{cb}}}}\beta_L^{{23}}\right)=0.051\pm0.027.$$

该页把误差称为**1σ**；原论文图对$\beta_L^{{23}}\in[0.06,0.16]$扫描后形成包络，旧的转换继承该包络。新图固定β或mass后逐slice计算，所以比旧图窄。{P('AJ_tau_260212',2)} {P('AJ_tau_260212',3)}

从该式直接整理，定义$K=1+(V_{{cs}}/V_{{cb}})\beta_L^{{23}}$，当$K>0$、coupling取正时，

$$g_U(C;M_U,\beta_L^{{23}})=\frac{{2M_U}}{{v}}\sqrt{{\frac{{C}}{{K}}}}.$$

选择$n\sigma$带时，把$C_-=C_0-n\sigma_C$与$C_+=C_0+n\sigma_C$分别代入；若下界非正，就没有由该正coupling模型给出的正实数下边界，不能对负数开根。**这段是对报告公式的代数整理，不是对现行绘图script的实现审计。**

### 尚需核对的带宽定义

第二天的真正EB报告`EB_meeting_260213.pdf` p3–4写**within 2σ**，p5仍显示$0.051\pm0.027$。若把前一天的0.027视为1σ，2σ下界将跨零，因此1σ与2σ不能只换标签而沿用同一轮廓。应确认最终script中的`n_sigma`、best-fit输入和legend；在确认前保留这项来源差异。{P('EB_meeting_260213',3)} {P('EB_meeting_260213',5)}

相关会议：{N('AJ_tau_260212')}；{N('EB_meeting_260213')}。目录里的`_v1.pdf`不是这两份会议的版本顺序证据。
''')

topic('会议专题_区域背景与WHF演进',fr'''最终tau+MET+jets分析是在数年背景检验与region优化后形成的。这里保存“为什么从一个region移到另一个region”以及W+heavy-flavour误差的变化；不从历史cut表拼接一套新配置。

## 从fake tau背景检查到双拓扑SR

- **2023**：以Zμμ+tau检查Zνν+jet-fake tau，修复MC权重、double counting和MC20a归一问题，再加入Zee提升统计。见{N('analysis_meeting_230606')}、{N('analysis_meeting_230801')}、{N('analysis_meeting_231010')}、{N('analysis_meeting_231128')}。
- **2024春**：利用fake MET与jet方向关联建立minΔφ及MET/jet-pT清理；Wτν VR高jet-pT处的data/MC差异继续调查。{N('analysis_meeting_240430')} p7–14。
- **2024夏秋**：高mT Wτν MC统计不足，向Weak Boson申请约十倍tail统计；随后MET-filtered Wτν生产与validation改善optimisation。{N('Weak_Boson_240716')} p11；{N('TauX_weekly_241101')} p5–12。TopCR基于dileptonic ttbar，见{N('analysis_meeting_240827')} p16–23。
- **2024末至2025初**：为压V+jets加hard-b，发现选中resonant signal；另建soft-b/high-mT/τ–MET back-to-back的non-resonant SR。{N('analysis_meeting_241112')} p12–18；{N('analysis_meeting_250128')} p19；{N('TauX_weekly_250226')} p6–9。
- **2025春**：WCR逐步固定为0τ1e/μ0b；TopCR为1τ1e/μ+b。验证分别检查l→τ与0b→1b外推。{N('analysis_meeting_0415')} p7–20；{N('TauX_weekly_250516')} p6–12。

## non-resonant 0tau1l1b VR的偏差

2025年7月nominal-only fit后，偏差约3σ，集中在MET400–450 GeV；松/紧cut后降至约1.5σ，未表现为宽范围shape失配。7月11日与7月21日的e/μ显著性也不同，需保持各自production/selection语境。{P('TauX_weekly_250711',13)} {P('LPX_weekly_250721',19)}

加入experimental/theory uncertainties后，8月报告约2.5σ，9月改进逐process transfer-factor估计后为1.8σ。并非“数据被修复”，而是背景模型与误差描述发生变化。{P('TauX_weekly_250822',17)} {P('TauX_weekly_250905',9)}

12月–1月专门比较三种WCR选择：原0τ0b、0τ1b及combined。原方案保留较高统计的0τ0b约束，HF/LF外推由NP覆盖；加入0τ1b主要让VR本身约束HF/LF，且将失去独立validation的灵活性。最终1月选择保留原WCR。{P('TauX_weekly_251212',11)} {P('EB_meeting_260109',15)}

## W+HF/LF uncertainty：20%怎样变成30%

- **2025-08-22** p6：认为W+b/c fraction影响b-veto CR→b-tag SR/VR外推，初设20%。这是HF composition/modelling，而非b-tag efficiency校准误差。{P('TauX_weekly_250822',6)}
- **2025-11-19**：比较10%、20%、30%的fit/limit，见{N('TauX_weekly_251119')} slides10–13。
- **2025-12-05** p27：在1.5 TeV benchmark下significance分别2.156、2.105、2.034，差别有限；p31测试Res/NonRes decorrelation，p32提出20%，尚待解盲前最后决定。{P('unblinding_request_251205',27)} {P('unblinding_request_251205',31)}
- **2025-12-23** p19与**2026-01-09** p16：明确20%，并按Res/NonRes decorrelate/专家讨论达成共识。{P('analysis_meeting_1223',19)} {P('EB_meeting_260109',16)}
- **2026-04-07** p13：报告明确“30% is applied in the end”，所以用户记忆的30%有较晚会议支持。该页没有给出30%的外部实验证据或理论推导；文献依据仍须从systematics参考文献与analysis note追溯。{P('Higgs_260407',13)}

**会议记录证明采用值与选择过程，并不能单独证明“W+HF在所有相关phase space都有30%的理论误差”。** 若要写论文中的依据，应把reference测量/生成器比较、0b→1b extrapolation、实际NP实现连接起来。早期sensitivity中“assume30%systematics”是总体误差简化，不能用作W+HF专属reference。

## 其它误差与新版0b

Zνν+fake tau的assigned uncertainty从2025-12-05的50%增至2026-04-07的100%；后者还给Diboson/Z+jets 30%。这几个NP与W+HF并非同一个误差。{P('unblinding_request_251205',19)} {P('Higgs_260407',13)}

2026年PAM指出大βL23下1τ0b WVR有signal contamination；3月转为0b SR。3月11日比较重新optimise与直接沿用旧VRW cut，最终报告偏好沿用，以免解盲后重新调整cut、延长validation。4月完整汇报明确同时有SR0b/SR1b。{P('Paper_approval_260303',31)} {P('TauX_weekly_260311',13)} {P('Higgs_260407',12)}

这使旧的“WVR1tau验证l→τ外推”和“1b interference可忽略”都必须带历史限定；0b成为signal category后，region职责发生变化。
''')

topic('会议专题_interference与toyfit演进',fr'''低统计limits与SM–LQ interference是两个有关联但不同的问题：toy ensembles用于检查统计推断；interference改变signal expectation及其POI dependence。负interference不等于negative fitted signal-strength范围。

## interference的区域依赖

- 无日期{N('LQ_taunub')}用CKM结构说明τν+jets与τν+b可能有不同interference大小；只适合作为图示入口。
- {N('status_report_240426')} slide2询问negative interference会否产生deficit；当时是问题，没有结论。
- 2025末的研究主要针对**1b-only**：resonant SR一般<5%，non-resonant某些点可至40%，但主要有敏感度点一般<5%。{P('unblinding_request_251205',30)}
- 2026-02-13的新sample check认为1b limit含/不含interference差别<1%。{P('EB_meeting_260213',6)}
- 2026-03-03加入0b提议时，报告指出其interference可达BSM的30–50%；3月11日聚焦near-limit点得到约20%，测试点的S+I未负。这些不是同一参数集合的普遍上界。{P('Paper_approval_260303',32)} {P('TauX_weekly_260311',6)} {P('TauX_weekly_260311',12)}

## fit里的μ有两种记号

2025-11-19 slide16及12月unblinding p30用amplitude scale：interference乘μ、BSM乘μ²。2025-12-12 p22转述signal-strength记号：BSM乘μ、interference乘√μ。两者可以通过变量替换一致，不能把图上同名μ直接互用。{P('TauX_weekly_251119',16)} {P('TauX_weekly_251212',22)}

2026-04-07 p14明确写（已视觉核对）：

$$N(\mu)=\mu S+\sqrt{{\mu}}I+B=(\mu-\sqrt{{\mu}})S+\sqrt{{\mu}}(S+I)+B,$$

POI为$\sqrt{{\mu}}$。等价令$a=\sqrt{{\mu}}$，则$N(a)=a^2S+aI+B$。{P('Higgs_260407',14)}

这里$S$为nominal BSM contribution，$I$为interference，$B$为SM背景。重写用到$S$及$S+I$两个模板，但代数重写本身不保证任意扫描a下总期望都为正：当$0<a<1$时$a^2-a<0$。应查实际NormFactor表达式、POI范围及完整期望检查。3月11日“S+I非负”的结论仅针对展示的near-limit points。

## toy配置按日期追踪

- **2025-11至12月**：SR少于10个事件，因此计划用toys验证/替换asymptotic限值。{P('AJ_monthly_20251127',26)} {P('unblinding_request_251205',32)}
- **2026-02-12/13**：新signals、full systematics；3000 toys、15 steps，scan min/max从asymptotic −2σ/+2σ limits再减/加2。尚未理解expected band问题。{P('AJ_tau_260212',2)} {P('EB_meeting_260213',2)} {P('EB_meeting_260213',10)}
- **2026-02-27及03-02**：报告将异常归因于mu_hat允许[-15,15]，改mu_hat>0后更新。新的scan min=0，max=$2\mu_{{+2\sigma,\rm Asy}}-\mu_{{+1\sigma,\rm Asy}}$，15 steps，10k toys。{P('TauX_weekly_260227',2)} {P('EB_meeting_260302',4)}
- **2026-03-03 PAM**：p27注明circulation期间将exclusion更新为toy结果。{P('Paper_approval_260303',27)}
- **2026-03-11**：0b+1b快速study只包括少数leading systematics；不能把其limits当最终全systematics结果。{P('TauX_weekly_260311',15)}
- **2026-04-07**：正文p14、p17–18为含interference的combined结果；backup p32仍保留上述toy扫描设置。最终正式提交文件的名称、选项与实际执行参数需从run config和提交script核对。

## 不能从旧backup取当前结论

4月报告p64仍保留“interference可忽略”，p37仍讨论是否增加0b；但正文p12和p14已经明确0b+1b与计入interference。PAM p59也属于旧1b研究。检索时先确认页在主报告还是backup，再核对对应region和模型。
''')

topic('会议专题_解盲审批与版本边界',fr'''这条路线记录分析对外汇报与内部决定的时间顺序。会议标题“approval”“unblinding request”只说明本次议题；只有内容明确记录通过/签署时，才记为已批准。

## 决策路线

- **2025-03-07/31**：与PC讨论Run-2-only和partial Run-3可行性，仍未完全一致。{N('TauX_weekly_250307')} p5–10；{N('LPX_weekly_250331')} p14/p16。
- **2025-04-15**：记录已同意Run-2-only、另建Glance并继续与Tau+X合作；对发表进度和结果强度有要求。{P('analysis_meeting_0415',3)}
- **2025-09-08**：LPX正式请求EB，同时仍列NP相关性、signal correction等待办。{P('LPX_weekly_250908',26)} {P('LPX_weekly_250908',27)}
- **2025-11-03**：首次EB；核心信号weight/width与calibration更新已集中讨论。{N('EB_meeting_251103')}。
- **2025-12-05**：unblinding request。W+HF值、new samples与toys尚未全部完成，不能把当天记为已解盲。{P('unblinding_request_251205',32)}
- **2026-01-09**：第二次EB落实WCR策略、tau SF与20%HF；{N('EB_meeting_260109')} p16。
- **2026-01-14**：报告本周一获unblind approval，展示1b SR的3/2事件。按日历推定周一为1月12日，但签署具体时间应查审批记录。{P('TauX_weekly_260114',2)} {P('TauX_weekly_260114',4)}
- **2026-01-19/22**：LPX和EXTO展示解盲与初始limits，新直接生成signals和toys仍更新中。{N('LPX_weekly_260119')}、{N('EXTO_approval_260122')}。
- **2026-02-24/27**：ATLAS weekly short talk；2月27日报告论文已circulated to ATLAS，准备PAM。{N('LQ_taunub_ATLAS_weekly')}；{P('TauX_weekly_260227',2)}
- **2026-03-03**：PAM提出0b signal contamination与是否加入SR。{N('Paper_approval_260303')} p31–33。
- **2026-03-06文件**：报告“PAM passed”，0b+1b敏感度改善并需第二轮circulation。{P('TauX_weekly_260306',2)}
- **2026-03-11**：记录在PAM与PC同意增加原WVR为SR，并倾向保留原cut。{P('TauX_weekly_260311',4)} {P('TauX_weekly_260311',13)}
- **2026-04-07**：完整0b+1b汇报，准备第二轮ATLAS circulation，目标LHCP2026。{P('Higgs_260407',19)}

## 已发现的日期、内容与版本冲突

1. **`EB_meeting_260213_v1.pdf`**封面/正文是2026-02-12 AJ tau meeting；无v1后缀的是2026-02-13 EB。必须分两组。
2. **`LPX_weekly_260119.pdf`**封面和页脚写2025，但引用2025年12月request与2026年1月9日EB；按文件名与事件顺序归2026。
3. **`TauX_weekly_260306.pptx`**封面沿用2026-02-27，但p2已记3月3日PAM通过；按文件名暂记3月6日，实际发表日待Indico确认。
4. **`AJ_monthly_20251127.pptx`**封面/正文写11月28日；按封面日期归档。
5. **`TauX_weekly_250516_v2.pdf`**封面写5月15日、正文与文件名5月16日。
6. **`status_report_240208.pptx`**封面2月9日、文件名2月8日、页脚常为2月6日；保留三者。
7. **`analysis_meeting_0617.pdf`**封面6月17日、页脚6月12日；按封面。
8. **`Higgs_260407.pdf`**p14仍写SR blinded，p16实际已解盲；p16后两项背景预测误标SR1b，右侧明确列SR0b观测33/45。p37/p64旧backup与当前正文不一致。
9. **favored band σ**：2月12日AJ报告0.051±0.027为1σ，2月13日EB部分页称2σ。见[[会议专题_信号模型与favoredregion演进]]，不能靠改legend解决。
10. **早期物理措辞**：2022 kickoff/ICEPP写“LFV observed”，与LFU anomaly动机不一致；不抄入知识库的事实陈述。

## 本库的版本规则

优先同一会议编号最高的PDF便于引用实际页码，保留所有PPTX与其它PDF入口；遇到封面/正文实为另一个会议时拆组。正文与backup分别理解，已被后续明确决定覆盖的设定保留为历史。PDF/PPTX页数差异与exact duplicate的SHA见[[会议资料_原始文件清单]]。本库没有把文件mtime或Office metadata当发表日期。
''')

h=front('analysis-timeline','curated')+'---\n\n# 分析演进时间线\n\n[[会议资料索引]]\n\n'
entries=[
('2022-10至2023-01','从理论cutflow到可运行工具','Taux_kickoff','U1 truth sample复现，加入Tau+X，开发xTAU/R22并排查UFO、dijet权重。'),
('2023-04至2023-11','建立可信的背景比较','analysis_meeting_231128','扫描初步SR，修复MC权重/双计数/MC20a归一，检查MET trigger和tau ID，将Zee与Zμμ合并用于fake-tau modelling。'),
('2024-02至2024-05','多喷注清理与framework迁移','analysis_meeting_240430','利用jet–MET关联压制fake MET，在object definition匹配后确认xTAU与GFW一致，更新AF3 signal。'),
('2024-07至2024-11','改善高mT MC统计与TopCR','TauX_weekly_241101','申请/验证MET-filtered Wτν样本，建立dileptonic TopCR，hard-b优化带来新的signal-topology问题。'),
('2025-01至2025-03','Res与NonRes分离','TauX_weekly_250226','发现hard-b SR增强resonance，另建soft-b高mT SR；跨mass与RH重加权不可靠，扩大signal request。'),
('2025-04至2025-06','确立Run2范围与处理链','analysis_meeting_0617','Run-2-only与独立Glance确定；TopCPToolKit→FastFrames→TRExFitter、p6490/GN2v01及各SF逐步到位。'),
('2025-07至2025-09','VR偏差与systematics模型','TauX_weekly_250905','non-resonant 0τ1l1b VR局部约3σ偏差，经HF及逐process theory transfer-factor估计降至约1.8σ；正式请求EB。'),
('2025-10至2025-11','修正signal width与验证fit','EB_meeting_251103','new/old samples和production对照定位internal-weight width问题，额外truth correction，更新calibration及NP correlation验证。'),
('2025-12至2026-01','完成解盲前选择','EB_meeting_260109','测试WCR方案和tau eVeto SF，1月确定原0τ0b WCR、20%HF与替代SF；获准解盲后1b SR观测3/2事件。'),
('2026-02','更新favored band、signal网格和toys','AJ_tau_260212','按固定parameter slice直接用CLLc计算favored band；网格插值、新signals、RH解释与toy expected-band问题得到集中处理。'),
('2026-03','PAM后增加0b信号区','TauX_weekly_260311','从WVR signal contamination出发加入0b，计入较强interference；研究更紧MET但倾向保留旧VRW cut。'),
('2026-04-07','最新完整会议快照','Higgs_260407','0b+1b、interference fit与toy limits；W+HF30%、fake tau100%；0b观测33/45，准备第二轮circulation。')]
for date,title,g,desc in entries:h+=f'## {date}：{title}\n\n{desc} 入口：{N(g)}。\n\n'
h+='## 阅读原则\n\n该时间线记录发展路线，不能替代最新参数表。一个旧报告里的selection、signal sample、systematic size、POI记号与后来的不同，通常是版本变化；只有在同一配置和数据范围下仍冲突，才作为待解决的问题。日期错写与正文/backup冲突见[[会议专题_解盲审批与版本边界]]。\n'
write('会议资料_分析演进时间线',h)
print('wrote 5 topic routes + timeline')
