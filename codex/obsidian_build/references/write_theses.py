from write_notes import write

books=[
dict(key='Aoki2024_博士论文结构与深度',file='phD2024_aoki.pdf',offset=2,toc='5–7',title='Takumi Aoki：slepton cascade decay，opposite-/same-sign three leptons',chapters=[
('1 Introduction',6,7,'快速定位SM未解问题、SUSY动机和本工作。'),
('2 Theoretical Backgrounds',8,29,'约22页，SM/gauge/EWSB较简明，重点发展MSSM mass spectrum、dark matter与muon g−2。'),
('3 SUSY Mass Hierarchy',30,42,'约13页，逐步筛选能同时满足g−2与dark matter的mass hierarchy，最终选择target benchmark。说明模型选择本身可以构成独立物理论证。'),
('4 Experimental Apparatus',43,52,'约10页，LHC/ATLAS、坐标、tracking、calorimeter、muon与TDAQ，提供理解三轻子的基础。'),
('5 Dataset and MC',53,59,'约7页，data quality/luminosity、MC总流程、background/signal样本及trigger。'),
('6 Object Reconstruction',60,69,'约10页，从detector signatures和低层objects到electron/muon/jets、OR、MET，结尾汇总analysis definition。'),
('7 Event Selection',70,80,'约11页，cleaning、preselection、SR优化、signal composition。'),
('8 Background Estimation',81,118,'约38页，是方法重点；WZ CR normalization、charge-flip SF、fake-factor测量及validation逐项展开。'),
('9 Systematic Uncertainties',119,123,'约5页，theory/experimental/data-driven三类及summary；背景方法自身误差在前章已有充分内容。'),
('10 Result',124,135,'约12页，三种fit目的、SR数据、model-dependent和model-independent结果。'),
('11 Discussion',136,141,'约6页，回到该search独特贡献、g−2、higgsino mass与future reach。'),
('12 Conclusion',142,142,'约1页结论；后续硬件和补充图放appendix。')],
samples='PDF第62页先解释low-level objects如何组合为physics objects；第83页先给背景估计总体策略及CR/VR角色，再分方法；第126页在统计公式前列出三类fit的推断目的。',
take='本篇最有用的是“从physics可行空间筛选到benchmark”的因果链，以及将背景中的独立技术问题分开讲清后再汇总。对U1可对应为coupling texture、CKM、flavour fit和collider final-state选择。',
limit='不能照搬约22页SUSY理论或38页fake/charge-flip内容；这些长度由本篇研究重点决定。硬件贡献置appendix也是本篇选择，并非所有博士论文必需。'),
dict(key='Sugizaki2024_博士论文结构与深度',file='phD2024_sugizaki.pdf',offset=11,toc='6–8',title='Kaito Sugizaki：compressed higgsino，low-momentum leptons',chapters=[
('1 Introduction and theory',1,32,'约32页，SM、SUSY、mass spectrum、既有约束和target/search strategy集成在一章；不是纯简短引言。'),
('2 Experimental Setup',33,48,'约16页，detectors与TDAQ，其中muon系统介绍较详细。'),
('3 Data and Simulated Samples',49,53,'约5页，data、trigger、signal/background MC、detector/pile-up simulation。'),
('4 Standard Object Reconstruction',54,64,'约11页，track/vertex/cluster到jet/lepton/OR/MET，为下一章专用低pT算法铺垫。'),
('5 Low-pT Lepton Track ID',65,85,'约21页核心技术：electron-track ID设计、变量和优化、data efficiency calibration；随后muon-track ID。'),
('6 Event Selection',86,99,'约14页，strategy、kinematic variables、parameterised neural network输入/训练/验证/使用及SR definition。'),
('7 Background Methodology',100,108,'约9页，fake-lepton-track data-driven与true-track MC、validation、CR/VR总表及SR预测。'),
('8 Systematic Uncertainties',109,114,'约6页，experimental/theory/analysis-specific，强调dominant non-closure。'),
('9 Statistical Analysis',115,118,'约4页，likelihood、hypothesis test、analysis fit configuration独立成章。'),
('10 Results',119,136,'约18页，background-only、model-dependent、model-independent fits。'),
('11 Discussion',137,145,'约9页，局部excess、与其它搜索比较、mass-parameter interpretation、未来实验。'),
('12 Conclusion',146,146,'约1页总结。'),
('13 Muon Trigger Contributions',147,151,'约5页，另列Run-3硬件/控制软件工作；appendices保存更多ID细节和signal资料。')],
samples='PDF第76页附近进入printed65的专用ID章；PDF第91页（printed80）示例解释data/MC输入变量差异如何导致SF偏离1；PDF第120页（printed109）明确fake-track non-closure主导，而小背景MC uncertainty仅占较小角色。',
take='最值得借鉴的是把“标准object定义”与“作者开发的新技术”分开：前者够用，后者从需求、算法、优化到data calibration闭环。U1若重点是tau calibration/高pT性能，可借这个层次；不能把算法名直接丢给读者。',
limit='PNN训练章与专用low-pT ID是本篇贡献；本分析cut-based计数若不使用这些技术，无需添加相同章节。'),
dict(key='Tanaka2025_博士论文结构与深度',file='phD2025_tanaka.pdf',offset=14,toc='9–13',title='Aoto Tanaka：VH production与H→bb测量',chapters=[
('1 Introduction',1,19,'约19页，Higgs/EFT背景、VH production/decay、既有测量、改进点、作者贡献与全文导航。'),
('2 LHC-ATLAS',20,32,'约13页，装置、TDAQ和control/operation。'),
('3 Data and Simulation',33,43,'约11页，先general MC chain再具体signal/background setup。'),
('4 Objects',44,58,'约15页；flavour tagging从物理特征、tagging scheme、calibration到保留MC统计，约8页为重心。'),
('5 Selection and Categorisation',59,73,'约15页，V/H candidates、background suppression、resolved/boosted与STXS categories。'),
('6 Jet Energy Corrections',74,78,'约5页，muon-in-jet、pT-dependent correction、kinematic fit、FSR recovery总览。'),
('7 FSR Recovery',79,96,'约18页专门贡献，从strategy到identification，再以mass resolution、purity、migration、sensitivity/STXS precision评估。'),
('8 Multivariate Discriminants',97,106,'约10页，SR/CR用途、输入、training、evaluation。'),
('9 Systematics',107,128,'约22页，experimental与modelling，并明确normalization、relative acceptance、shape三个层次。'),
('10 Diboson Modelling Improvement',129,150,'约22页核心技术；alternative models、uncertainty推导、mbb reweighting与CARL比较。'),
('11 Statistical Description',151,160,'约10页，一般profile likelihood→本分析fit model→fit validation。'),
('12 Results and Discussion',161,176,'约16页，先VZ cross-check，再VH strength与STXS，再解释误差和各项改进效果。'),
('13 Conclusion',177,179,'约3页结论；appendices自180页起，涵盖hardware、SMEFT、trigger和大量技术支持图。')],
samples='PDF第65页（printed51）把b/c/light的物理特征与tagger performance连接；第95页（printed81）说明FSR/ISR/pile-up labels的实际定义；第172页（printed158）给BDT rebinning criterion，展示实施规则如何与统计精度目标联系。',
take='适合学习“独立贡献写成可验证的方法章”：为什么做、怎样做、替代方案、closure/performance、对最终precision有什么影响。也适合参考systematic的normalization/acceptance/shape区分。',
limit='这是measurement论文，STXS和复杂MVA shape fit占比高；不能强迫U1单bin搜索采用同样篇幅。它的HF/LF组成与本分析单b-tag类别不同。'),
dict(key='Yang2020_博士论文结构与深度',file='phD2020_yang.pdf',offset=1,toc='3–7',title='Yi-Lin Yang：all-hadronic scalar-top search',chapters=[
('1 Introduction',7,9,'约3页，问题、target和search动机。'),
('2 Theory',10,21,'约12页，简要SM/gauge/EWSB、SUSY/MSSM、stop特性。'),
('3 LHC and ATLAS',22,37,'约16页，细分各detector technology及TDAQ。'),
('4 Samples and Reconstruction',38,58,'约21页，data/trigger、MC、objects；额外讨论VR track jets、flavour tagging、MET significance。'),
('5 DNN Top Taggers',59,73,'约15页专门技术，truth label、输入变量、network、calibration regions、SF/systematics和结果。'),
('6 Data Analysis and Results',74,119,'约46页把selection、background、uncertainty、statistics和results集中；6.4背景约15页，6.5误差4页，6.6统计5页，6.7结果10页。'),
('7 Discussion',120,128,'约9页，exclusion、reclustering方法对照、CMS及其它lepton channels比较。'),
('8 Conclusion',129,129,'约1页结论；reference和两个简短appendix随后。')],
samples='PDF第60页用boosted top的物理需求引出DNN tagger；第87页解释为何CR校正MC、为何CR需正交且接近SR；第106页从每region的Poisson期望进入statistical model。',
take='大章可包含完整analysis链，但需要清晰小节。新object/tagger的校准独立于search主线，便于区分性能研究与最终search。讨论章用明确方法对照说明新技术带来的收益。',
limit='这是2020年记录，luminosity、CP tool和tagger推荐可能旧；它的detector硬件库存式深度不是本分析必须达到的标准。'),
dict(key='Zhang2024_博士论文结构与深度',file='phD2024_zhang.pdf',offset=10,toc='7–9',title='Zhang：prompt dark photon / lepton-jet search',chapters=[
('1 Introduction',1,2,'约2页总览。'),
('2 Standard Model and Beyond',3,14,'约12页，QED/QCD/electroweak/Higgs及BSM背景。'),
('3 Dark Matter Search',15,26,'约12页，从dark-sector portals到vector/Higgs portal及benchmark。'),
('4 ATLAS and Standard Objects',27,54,'约28页；LHC、luminosity/pile-up、detector、MC、standard objects集中一章。'),
('5 Prompt Dark Photon Signatures',55,74,'约20页，signal kinematics、close-by isolation、merged EM clusters、lepton-jet reconstruction及trigger效率/matching。'),
('6 Event Selection',75,84,'约10页，SR definition、signal/background expectation与selection-variable checks。'),
('7 Background Estimation',85,98,'约14页，ABCD假设、选变量、构造plane、验证closure。'),
('8 Systematics',99,108,'约10页，标准实验误差、理论、专门non-closure。'),
('9 Results and Discussions',109,120,'约12页，likelihood、signal contamination、两类portal interpretation与future development。'),
('10 Conclusion',121,122,'约2页；references自123页起。')],
samples='PDF第65页明确specialised lepton-jet由standard objects构成；第95页先解释MC对特殊对象的不可靠性，再引出ABCD及validation；第119页将ABCD统计/系统误差、SR observed/predicted与后续likelihood连接。',
take='对于非标准object，先说明kinematics导致什么reconstruction困难，再讲customization、efficiency、trigger与背景方法。ABCD章不是只写公式，而要说明变量选择和closure。',
limit='dark photon portals和lepton-jet reconstruction的专门篇幅不适用于普通tau对象；可借论证层次，不借具体构造。'),
dict(key='Tateno2022_博士论文结构与深度',file='phD2022_tateno.pdf',offset=0,toc='5–6',title='Tateno：light-by-light / diphoton search with AFP',chapters=[
('1 Introduction',7,18,'约12页直接从light-by-light过程、AFP、新物理mediator、既有工作到目标；没有通用SM教科书式大章。'),
('2 Experimental Setup',19,36,'约18页，ATLAS概要、重点EM calorimeter与AFP，包括AFP calibration/performance。'),
('3 Data and MC Samples',37,48,'约12页，把data/signal MC与photon/proton reconstruction放一起，解释为何选特定2017 dataset。'),
('4 Event Selection',49,66,'约18页，acoplanarity、proton kinematics、matching和set operation逐步给mechanism/efficiency。'),
('5 Signal Modelling',67,78,'约12页，fit function、shape uncertainty、efficiency及yield。'),
('6 Background Modelling',79,98,'约20页，combinatorial background构造、data/MC validation、template uncertainty、smoothing和spurious signal。'),
('7 Systematics',99,108,'约10页，photon/proton对象、fit、theory uncertainty。'),
('8 Statistical Procedure and Results',109,122,'约14页，先模型与NP effect，再significance和limit。'),
('9 Discussion and Conclusion',123,126,'约4页，比较既有搜索、prospects和结论。')],
samples='PDF第7页直接从QED中light-by-light机制出发；第37页给AFP2017/2018数据可用性的具体原因；第79页先定义不同vertex的accidental matching及combinatorial background；第109页先构建statistical model再解释结果。',
take='本篇说明thesis自洽不等于必须完整重讲SM。装置篇幅跟测量关键性分配：AFP和EM重要，因此比普通子探测器更深入。signal/background shape modelling值得独立说明。',
limit='AFP、unbinned/shape modelling及spurious-signal检验属于其特定策略；本分析single-bin计数的重点不同。'),
dict(key='Oishi2022_博士论文结构与深度',file='phD2022_oishi.pdf',offset=0,toc='4–6',title='Reiyo Oishi：right-handed W与boosted right-handed neutrino search',chapters=[
('1 Introduction',7,25,'约19页，SM gauge/Higgs、neutrino mass、baryon asymmetry、RH neutrino与WR、既有约束、boosted topology策略。'),
('2 LHC-ATLAS',26,33,'约8页，较紧凑的detector/TDAQ背景。'),
('3 Dataset and MC',34,38,'约5页，data/trigger、general cross-section、signal/background samples。'),
('4 Objects',39,47,'约9页，track/vertex/cluster到jet、b-tag、leptons、OR、MET、large-R jet。'),
('5 Event Selection',48,61,'约14页，以SR1e/SR2e/SR2mu分解boosted topology与binning。'),
('6 Background Estimation',62,72,'约11页，三类SR的背景转移、W+jets和fake相关验证，并最终汇总。'),
('7 Statistical Analysis',73,79,'约7页，likelihood、hypothesis tests、experimental/theory/ad-hoc uncertainties。'),
('8 Extra VR Fit Results',80,89,'约10页，专门展示additional VR对W+jets/QCD/Z+jets模型的检验。'),
('9 Results',90,102,'约13页，background-only、model-independent、model-dependent、LHC与非LHC约束对照。'),
('10 Conclusion',103,103,'约1页；参考文献后续。')],
samples='PDF第48页由WR→lepton+boosted NR的kinematics解释objects角分离；第62页写出CR normalization→SR预测并明确依赖MC transfer modelling；第73页先说明三种fit目的。',
take='与U1方法最相关的是：把CR→SR transfer的假设写出来；把额外VR checks作为可复查证据，而不是只在结果中说agreement良好。',
limit='该PDF部分font的数学text extraction异常，章节和内容经另一PDF引擎复核；引用具体公式时需打开原PDF检查。旧版139fb−1/1.7%等不作为本分析现行输入。'),
dict(key='Mino_博士论文结构与深度',file='mino_dt.pdf',offset=0,toc='6–9',title='Yuya Mino：compressed higgsino，low-momentum mildly displaced tracks',chapters=[
('1 Introduction',13,16,'约4页，总问题、search缺口和贡献。'),
('2 Theoretical Background',17,33,'约17页，SM/MSSM、light higgsino、mass splitting、collider/non-collider constraints、target models。'),
('3 ATLAS Experiment',34,44,'约11页，装置基础和MET trigger；future upgrades简述。'),
('4 Data and MC',45,51,'约7页，general simulation后接signal/background配置和汇总。'),
('5 Event Reconstruction',52,62,'约11页，低层objects→physics objects→analysis selection汇总。'),
('6 Strategy and Selection',63,80,'约18页，trigger/cleaning、signal track definition、preselection与SR。'),
('7 Background Estimation',81,108,'约28页，tau-decay tracks半data-driven、QCD tracks全data-driven、各自CR/VR和联合validation。'),
('8 Systematics',109,114,'约6页，theory、experimental、data-driven及summary。'),
('9 Results',115,124,'约10页，background-only、model-independent、model-dependent结果。'),
('10 Discussion',125,133,'约9页，electroweakino mass、naturalness、其它techniques和未来prospects。'),
('11 Conclusion',134,135,'约2页；bibliography和众多appendices保存硬件、object补充、cutflow、background composition和auxiliary limits。')],
samples='PDF第52页将detector signature→low-level→physics objects串起来；第81页先描述各类background的来源再引入CR/VR角色；第109页明确theory variation可同时影响cross-section与shape。',
take='背景主要由不同track来源决定，先按物理起源拆分再为每部分选择估计方法，最后做combined closure。适合U1区分true tau与jet/electron fake tau，而不是只按generator名字列表。',
limit='部分标准object与完整cutflow放appendix有助于主线，但与本分析tau/FTAG相关的核心解释仍应留正文。')
]

for b in books:
    lines=[f'本地来源：[{b["file"]}](<{{SRC}}/{b["file"]}>)。主题：{b["title"]}。',
           f'目录定位：PDF第{b["toc"]}页。下列范围按目录相邻章起点估算，包含图表和章末空白，不代表纯文字长度。印刷页码与PDF物理页码分别列出，PDF从封面起算。',
           '## 章节内容与大致深度']
    for name,start,end,desc in b['chapters']:
        lines.append(f'- **{name}**：印刷第{start}–{end}页；PDF第{start+b["offset"]}–{end+b["offset"]}页。{desc}')
    lines.extend(['## 正文抽查所见',b['samples'],'## 对本分析写作的借鉴',b['take'],'## 不宜直接照搬',b['limit'],
                  '返回：[[高能物理博士论文写作框架]]。本笔记是阅读/结构总结，不是对原论文全部物理结论的逐式审稿，也不作为其旧实验数字的现行引用。'])
    write('70_博士论文写作',b['key'],'\n\n'.join(lines),tags='[thesis, reading, structure]')

links='\n'.join(f'- [[{b["key"]}]]：{b["title"]}。' for b in books)
write('70_博士论文写作','高能物理博士论文写作框架',r'''
这份笔记综合本地8篇博士论文的目录与代表性正文，形成适合实验高能物理search/measurement的写作框架。它是可供选择的经验总结，不是项目skill或强制审批规则；笔记内容以中文说明，专业术语保留英语。

## 从8篇论文能稳定看到的共同骨架

读者需要先理解研究问题和目标模型，再理解装置与数据如何测到final state，随后理解event selection、background prediction、uncertainty、statistical inference，最后判断结果的物理意义。章节可以拆开或合并：Yang把analysis链集中在大章，Tanaka独立讨论统计及多项方法，Tateno直接从目标过程而非通用SM课程开始。相同的是解释链，而不是章数。

这组论文大体把detector与standard objects各用约8–20页，MC/data通常约5–11页；也有Zhang将detector/MC/objects合并约28页、Yang将samples/reconstruction合并约21页的安排。篇幅数字是目录观察，不是配额。共同特点是新方法或主要背景问题比一般背景占更多空间，例如Aoki的charge-flip/fake、Sugizaki的low-pT ID、Tanaka的FSR与diboson modelling、Mino的track background。

## 一个可执行的章节方案

### 1. 研究问题与总体路线

先说明物理问题、现有实验缺口、为何选择当前final state，以及本研究提供什么信息。结尾给全文路线和作者贡献。简短引言可约2–4页；若把理论一并放入则会长很多，因此不要只按“Introduction”这个标题比较深度。

### 2. 与本研究直接相关的理论

需要足够定义粒子、coupling、symmetry、benchmark和observables。对U1，主线可为LFU与R(D(*))→低能effective interaction→U1 representation/current→flavour basis与CKM→LH/RH contributions→collider resonant/non-resonant production→与tau-tau/直接搜索互补性。

每个重要equation都回答“为何引入、符号是什么、哪一项决定后果”。SM gauge/Higgs背景只发展到这条主线需要的程度；Tateno证明不必为了thesis完整性重写一套SM教材。详细UV构造可作为带假设的补充，不能把completion-dependent约束包装成模型无关实验事实。

### 3. 装置、数据与simulation

按测量功能介绍ATLAS：charged-track curvature、EM/hadronic energy、muon measurement、trigger和luminosity。更细的technology描述用于解释性能差异。随后先讲PDF、hard process、shower、hadronisation/decays、detector simulation、reconstruction、weights之间的关系，再列generator表；表应保留version、PDF、tune、accuracy和特殊过滤/overlap。

本分析应使读者理解Run-2 dataset、GRL、MET与single-lepton trigger的分工、AF3/full simulation、signal BSM/interference样本，以及simulation如何转换为event yields。

### 4. Physics objects

从track/vertex/cluster到tau、jet、b-tag、electron/muon、MET。每类按“真实粒子特征→detector signature→reconstruction/ID/calibration→本分析definition”发展。先说明物理机制，再给working point或软件名。tau和FTAG是本分析重点，应比只用于veto的object更深入。OR需列顺序和物理理由；MET解释hard objects与soft term如何避免double counting。

### 5. Analysis strategy、selections与categories

先通过signal diagrams/kinematics解释resonant/non-resonant及0b/1b分类，再给selection表和优化。每个不显然的cut要有target background或sensitivity理由。展示cutflow、signal composition、acceptance和相关性；不要仅罗列阈值。特别说明large beta23产生的s-tau使0b具有真实signal，而非只来自b-tag inefficiency。

### 6. Background estimation与validation

先讲物理来源与relative importance，再选择MC、CR-normalised MC、data-driven等方法。对W/top说明CR富集、与SR的替换关系、transfer factor、共享normalization/correlation；对fake tau说明fake object的来源及验证。VR检验哪一个假设、与SR距离多远、signal contamination是否可忽略，应直接写出。只有“data/MC agreement good”不够复查。

### 7. Uncertainties

分开experimental response、theory modelling、background-method/non-closure和MC statistics。每项记“来源→如何variation→哪些samples/regions→normalization/shape/transfer effect→correlation”。重心放在影响最大的项与本分析特有假设。HF/LF30%适合说明其经验依据、0b→1b外推及Res/NonRes decorrelation，而不是孤立一个数字。

### 8. Statistical inference

从要检验或测量的量开始：region Poisson counts→signal/background expectation→signal strength→nuisance constraints→CR信息与correlation→profiling/test statistic→background-only/model-dependent/model-independent fit→p-value/CLs/expected vs observed→implementation。

若有BSM–SM interference，明确yield中如何随parameter变化，不能只把它叫“另一个正的signal sample”。Asimov、toy与asymptotic的角色分清。通用统计方法和本分析fit config可以分节，这在Sugizaki/Tanaka的组织中很清楚。

### 9. Results、interpretation与discussion

先给CR/VR及SR prediction和data，再给fit结果、NP pulls/constraints及限值；说明plot中读者该看到什么。对U1 parameter scan应注明mass/coupling/chirality/width假设，favoured region注明fit version和confidence含义。最后回到研究动机：约束了哪一类解释、与其它channels如何互补、剩余空间来自什么局限、未来数据/方法可改变什么。

Discussion不应只是重复exclusion number。Aoki/Mino把结果回接g−2/naturalness，Tanaka量化每项方法改进对precision的作用，Yang比较tagger与reclustering；U1可比较tau-nu/tau-tau对不同coupling的覆盖。

### 10. Appendices

放完整sample/DSID列表、全量cutflow、次要object细节、大量validation plots、每个signal point的结果、硬件贡献或长推导。正文保留论证成立所必需的验证和定义；appendix承担可复现性，不能成为隐藏关键假设的地方。

## 写作时的自检

- 本章读完，读者能说出为什么下一章必要。
- 新term第一次用到时已有足够解释，后续不反复定义。
- 实验事实、模型assumption、analysis choice、个人判断分别清楚。
- 图表回答一个问题；正文说明机制和后果，而不是复述坐标轴。
- 专业名词与公式保留必要精确度，句子由物理问题推动。
- 学习参考论文的解释方式和层次，独立重建自己的论证，不复制原文句式。
- 用自己analysis的最新config、note、paper定数值；旧thesis仅供解释深度参考。

## 8篇逐篇阅读卡

{LINKS}
'''.replace('{LINKS}',links),tags='[thesis, writing, framework, index]')

print('Wrote eight thesis reading notes and synthesis')
