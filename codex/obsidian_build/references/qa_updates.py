from pathlib import Path
base=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search')
build=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/references')
old='FTAG主要是b、c、light三个truth flavour的efficiency/mistag SF，note使用Loose eigenvector reduction，列`FT_EFF_Eigen_B_[0–84]`、C `[0–55]`、Light `[0–41]`（第63页）。这测量tagger response；W+HF/LF variation则改变physics flavour composition，二者不是重复项。'
new='''FTAG主要是b、c、light三个truth flavour的efficiency/mistag SF。**版本差异：** internal note第63页写Loose eigenvector reduction，列`FT_EFF_Eigen_B_[0–84]`、C `[0–55]`、Light `[0–41]`；但本次读取的[TopCP入口快照](<{CACHE}/code/snapshot/TopCP/TauX_Gnt1makerAlg/python/TauX_Gnt1NtupleMaker.py>)第282–296行，对`Continuous` event SF显式设置B/C/Light三者为 **Medium**，tagger为`GN2v01`，MC20 calibration为`MC20_2025-06-17_GN2v01_v4.root`。因此不能把note的Loose/counts当成当前代码产物的确定NP数量；需以对应生产版本、实际输出branches和fit输入核实。85% analysis WP及其他输出WP见 [[DAOD处理与Object定义]]。

FTAG SF测量tagger response；W+HF/LF variation则改变physics flavour composition，二者不是重复项。'''
old2='- **FTAG calibration**：本分析实际tagger、85%WP、Loose eigenvector reduction、high-$p_T$ extrapolation的CP推荐/uncertainty map。paper引用的公开b/c/light效率论文提供方法，未替代当前版本配置。'
new2='- **FTAG calibration与版本对应**：补充GN2v01、85%WP、`MC20_2025-06-17_GN2v01_v4.root`和high-$p_T$ extrapolation的CP推荐/uncertainty map。TopCP入口对Continuous event SF显式设置B/C/Light均为Medium，而internal note第63页写Loose；需确认正式fit样本对应哪次生产及实际NP数，见 [[Experimental_systematics与校准来源]]。paper引用的公开b/c/light效率论文提供方法，未替代当前版本配置。'
old3='同一note第82页已称30%为leading uncertainty之一，说明该版本内部文字未完全同步。May26 paper与正式Toy配置一致使用30%，应作为当前这套设定的依据。AppendixL（第156页起）还比较0b CR、1b CR、二者联合的fit策略，解释为何低统计1b CR并非必然更优。'
new3='''[Higgs_260407.pdf](</Users/zang/Desktop/ICEPP/博士课题/leptoquark/presentation/Higgs_260407.pdf>) PDF第13页已经明确最终采用30%，同时列出Zνν+fake tau 100%和Diboson/Z+jets 30%。会议记录见 [[会议_2026-04-07_AJHiggs汇报0b加1b分析]]。这把30%的最终选择追溯到2026-04-07；April20 note第67页保留20%是文档同步问题，不能据PDF日期推断它在会议后重新回退为20%。

同一note第82页已称30%为leading uncertainty之一，也说明内部文字未完全同步。May26 paper与正式Toy配置一致使用30%，应作为当前这套设定的依据。AppendixL（第156页起）还比较0b CR、1b CR、二者联合的fit策略，解释为何低统计1b CR并非必然更优。'''
for path in [build/'write_systematics.py', *(base/'50_Systematics').glob('*.md')]:
    text=path.read_text()
    for a,b in [(old,new),(old2,new2),(old3,new3)]:
        if path.suffix=='.md': b=b.replace('{CACHE}',str(build.parent))
        text=text.replace(a,b)
    path.write_text(text)
# Clarify the verified code path and line provenance without changing numerical assumptions.
p=base/'10_理论与动机/Favoured-region理论输入与区间含义.md'
t=p.read_text().replace(' 的实际 cache 路径如有变动应从代码资料索引检索；原位置是',' 第1788–1791行给出实际启用的区间；原位置是')
p.write_text(t)
