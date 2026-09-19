from pathlib import Path
root=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search/20_Trigger')
cache=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/references')
s=r'''---
type: knowledge-note
updated: 2026-09-07
status: "公开原文已核对；Run-2性能背景，不替代本分析效率验证"
tags: [trigger, performance, MET, electron, muon]
---

# Run2_trigger性能论文与效率含义

本分析paper draft的Refs.[37–39]分别引用下列三篇ATLAS公开性能论文。本次从arXiv下载到独立cache，未改动原references。所有页码为PDF物理页码；下列version已从封面核对。

## MET：为何从mht走向pufit

[2005.09554v2公开记录](https://arxiv.org/abs/2005.09554)、[本地PDF](<{CACHE}/2005.09554.pdf>)，v2为2021-01-06，JHEP 08 (2020) 080。

- **mht**取经pile-up/JES校准的online jets的负横向动量和；**pufit**将topoclusters分成η–φ patches，从低能patch估计pile-up，再拟合其对高能patch的贡献。约束是pile-up横向总动量约为零、空间分布近似均匀。细节在§3.4–3.5（第7页）、Appendix A（第24–25页）。
- 第17页Table2明确：2017的pufit还隐含`cell MET > 50 GeV`，名称未完整显示；2018的xe65/70也是cell条件。表中各chain的luminosity有重叠，**不能相加**。
- 第3、8页说明online MET仅用calorimeter，性能论文的offline比较也排除muon可见动量。故不能直接拿它的曲线与包含muon的另一MET定义对照。
- 第21–22页§5.7讨论data/MC SF。offline MET>200 GeV常把选取放在>99%的plateau，但SF仍依赖offline definition及event topology，**不存在通用于所有分析的MET-trigger SF**。本分析200/400 GeV的实际效率应以自己的CR验证为依据。

## Electron：efficiency相对于哪个offline selection

[1909.00761v2公开记录](https://arxiv.org/abs/1909.00761)、[本地PDF](<{CACHE}/1909.00761.pdf>)，v2为2020-02-10，EPJC 80 (2020) 47。

第13–14页§7.2用Z→ee tag-and-probe：tag满足严格条件并匹配触发，probe测量目标trigger的通过率并扣除背景。定义是 $\epsilon_{\rm trig}=N_{\rm trig}/N_{\rm offline}$，总效率还要乘offline reconstruction/ID/isolation效率；SF为data/MC之比。不同offline WP对应不同效率，不能只抄“electron trigger efficiency”。

第24–28页§10.3解释24/26 GeV低阈值链与60、120/140 GeV非isolated/looser-ID链的互补。第28页将inefficiency拆到HLT步骤，online/offline ID差异会保留在plateau中。对本分析CRW的高-pT electron，应保留实际OR、offline ID/isolation、匹配和推荐SF版本；论文的性能图不能替代这些配置。

## Muon：plateau不意味着绝对100%

[2004.13447v2公开记录](https://arxiv.org/abs/2004.13447)、[本地PDF](<{CACHE}/2004.13447.pdf>)，v2为2021-01-08，JINST 15 (2020) P09015。

第12页Table1：`mu26_ivarmedium`要求isolation，`mu50`无isolation；`mu60_0eta105_msonly`仅覆盖barrel并仅用MS reconstruction。第15–18页§8.3以Z→μμ tag-and-probe为主，高-pT另用W+jets和top验证。

第21–24页§10.1显示full-chain efficiency受L1 acceptance/response限制；HLT相对L1接近1，不代表full-chain接近1。摘要的barrel约68%、endcap约85%是对应研究定义的整体表现，不能当本分析每个event的常数权重。第24页Table3给不同年份、高-pT样本和detector region的SF，支持保留year/η/φ依赖及实际CP calibration。CRW要求muon pT>200 GeV仍需处理trigger SF及其uncertainty。

## 与本分析资料的连接

- 历史chain/period来源：[[Run2_MET_trigger逐年推荐与检查]]、[[Run2_单轻子trigger与控制区]]。
- 本分析的独立trigger sample、200/400 GeV验证：[[Trigger导航与本分析使用逻辑]]。
- 实际ntuple selection与SF：[[DAOD处理与Object定义]]、[[Experimental_systematics与校准来源]]。
'''.replace('{CACHE}',str(cache))
(root/'Run2_trigger性能论文与效率含义.md').write_text(s)
p=root/'Trigger导航与本分析使用逻辑.md'
t=p.read_text().replace('- 各年 MET chain、period、L1 seed 与 luminosity tradeoff：','- MET算法、单轻子tag-and-probe及plateau/SF含义的公开论文：[[Run2_trigger性能论文与效率含义]]。\n- 各年 MET chain、period、L1 seed 与 luminosity tradeoff：')
p.write_text(t)
p=root/'Run2_MET_trigger逐年推荐与检查.md'
t=p.read_text().replace('pufit 为 pile-up mitigation algorithm；其完整数学机制应引用 MET-trigger performance paper。','pufit 为 pile-up mitigation algorithm；数学机制及2017隐含的cell MET>50 GeV条件见 [[Run2_trigger性能论文与效率含义]]。')
p.write_text(t)
