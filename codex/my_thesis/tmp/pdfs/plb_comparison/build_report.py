from pathlib import Path
import re
import json
import textwrap

BASE = Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis')
TMP = BASE / 'tmp/pdfs/plb_comparison'
OUT = BASE / 'output/plb_comments'
OUT.mkdir(parents=True, exist_ok=True)

def read(name):
    text = (TMP / f'{name}.txt').read_text()
    text = re.sub(r'===== PAGE \d+ =====', '', text)
    return re.sub(r'\s+', ' ', text).strip()

J, S = read('Jiaqi'), read('Stergios')

# Identifiers below are assigned for this comparison, in the PDFs' order.
# Each response and manuscript excerpt is copied from the supplied PDFs.
items = [
 dict(id='R1-01', title='Introduction：SM suppression 的适用范围', jp='1', sp='1–2', start='In the SM, the production of a tvau system', ja='→ We meant', sa='You are right,', cut='Old text:', js='明确给出替换文字', ss='明确修改', change='主要润色', delta='保留你对 gq → Wb → taunub 和 Vub/Vcb suppression 的解释，改成正式回复。正文替换基本沿用你已写出的两句，不能算 Stergios 新增的物理说明。', where='Section 1 Introduction'),
 dict(id='R1-02', title='βL13：生成时保留，Eq. (1) 中略去', jp='1', sp='2', start='Signal model footnote.', ja='-> No,', sa='The $\\beta_L^{13}$ parameter', cut='SK –', js='给出解释，未写脚注替换稿', ss='建议修改', change='回复澄清；新增脚注', delta='回复明确说 included in the generation of the signal samples。实质新增在脚注：注明 in the signal generation、to Eq. (1)、approximately 5% 和 neglected there，消除“是否设为零”的歧义。', where='Section 3，signal-model footnote'),
 dict(id='R1-03', title='τhad 为什么没有 muon veto', jp='1', sp='2', start='Why is there no muon veto', ja='→ the probability', sa='The probability for a muon', cut=None, js='仅回复', ss='仅回复', change='主要润色', delta='改进 misidentified、electron-veto RNN 和 τhad 的写法；保留你的原理由，没有正文修改文字。', where='Section 5'),
 dict(id='R1-04', title='定义 calorimeter-tagged muon', jp='1–2', sp='2', start='Define a calorimeter-tagged muon before', ja='→ Will define', sa='We have adjusted', cut='Revised text:', js='明确给出新增定义', ss='明确修改', change='落实表述；轻微润色', delta='把 Will define 改成 We have adjusted。括号定义沿用你的文字，在 calorimeter energy deposit 前加了 a。', where='Section 5，overlap removal'),
 dict(id='R1-05', title='Jet–muon overlap removal 的条件', jp='2', sp='2–3', start='Why is for an electron only', ja='→Not all jets', sa='Not all jets', cut='Revised text:', js='明确给出替换文字', ss='明确修改', change='主要润色', delta='回复把不明确的 not many associated tracks 写成 at most two associated tracks；该精确条件及 ghost association 已在你的正文建议中。正文沿用你的建议，并修正 ΔR 的拼写。', where='Section 5，overlap removal'),
 dict(id='R1-06', title='删除重复的 ETmiss 定义', jp='2', sp='3', start='ETmiss is redefined here', ja='Will remove', sa='We have removed', cut='“The magnitude', js='明确要求删除', ss='明确修改', change='落实表述', delta='把 Will remove 改成 We have removed，并用红色删除线标出原句。', where='Section 5，missing transverse momentum'),
 dict(id='R1-07', title='Cuts 的物理动机与 optimisation criterion', jp='2', sp='3', start='In general it could use some more motivation', ja='-> The jet multiplicity', sa='The upper bounds', cut='SK –', js='回复已有动机和优化方法，未给正文替换稿', ss='建议修改', change='回复细化；新增正文', delta='回复明确 upper bounds、resonant production、total background。另写两段可加入正文的文字，可选其一或两者。注意回复仍用 expected significance，而建议正文用 expected exclusion sensitivity，定稿前需统一实际优化指标。', where='Section 6 Event selection'),
 dict(id='R1-08', title='SR0b-Res 的 jet 是否是 b-quark proxy；是否用最高 GN2', jp='2', sp='4', start='For the m_jthad the light jet', ja='→ The light jet', sa='The leading jet', cut='SK:', js='仅回复', ss='明确未加正文', change='限定对象；主要润色', delta='把 light jet in SR0b 更准确地改成 leading jet in SR0b-Res，保留 sτ、分支宽度比例以及 3.8% → 74% 的论据。SK 明说没有为这一题加入正文。', where='Section 6 的 SR0b-Res；SK 曾考虑 Section 4'),
 dict(id='R1-09', title='Top 的 fully leptonic 成分及 single-top/ttbar 外推', jp='2–3', sp='4', start='Why are we only considering fully leptonic', ja='→ We studied', sa='We studied', cut=None, js='仅回复', ss='仅回复', change='主要润色', delta='把 large missing ET requirement 写得更明确，保留 SR/CR ratio 在 MC statistical uncertainties 内一致的结论。没有新增正文，也没有明确回答是否单独设置 ratio uncertainty。', where='Section 7 Background estimation'),
 dict(id='R1-10', title='交换 W+jets 与 top 的叙述顺序', jp='3', sp='4', start='I would swap ttbar and W-jets', ja=None, sa='We kept the same ordering', cut=None, js='这一题没有回复', ss='明确保持顺序', change='新增完整回复', delta='你原稿空缺。Stergios 新增回复，说明保留 W+jets 在前、top 在后的顺序，全文和 summary plot 保持一致，没有接受 referee 的交换建议。', where='Section 7 及 summary plot'),
 dict(id='R1-11', title='W→τν 多一个 neutrino 对外推的影响', jp='3', sp='4', start='For the W+jets section,', ja='→ We have confirmed', sa='Indeed there is', cut=None, js='仅回复', ss='仅回复', change='补充说明', delta='新增对 extra neutrino 的直接承认，并把验证区说明为 low-mass/low-mT W→τν region。外推验证、data/MC 一致的主结论来自你的回复。', where='Section 7，W+jets'),
 dict(id='R1-12', title='30% W+HF/W+LF uncertainty 的依据', jp='3', sp='5', start='30% uncertainty on W+HF', ja='→ As shown', sa='As shown', cut=None, js='仅回复', ss='仅回复', change='主要润色', delta='保留前人研究最大偏差、统计主导和 Res/NonRes decorrelation 的论据。将 based on 改成 to cover，没有给正文改写；相关 decorrelation 正文另见 R1-17。', where='Section 8 Systematic uncertainties'),
 dict(id='R1-13', title='Z→νν fake-τ 方法及 100% uncertainty', jp='3', sp='5', start='For the Z->nunu background,', ja='→ The contribution', sa='The contribution from', cut=None, js='仅回复', ss='仅回复', change='补充量化依据', delta='保留 fake background 很小、100% uncertainty 对结果影响小于 1%。新增说明 100% 应覆盖 fake study 中高至 60% 的差异，使 uncertainty 的选择有直接依据。', where='Section 8，fake-τ uncertainty'),
 dict(id='R1-14', title='Res/NonRes normalisation 解关联及 W factors 差异', jp='3', sp='5', start='Motivate why you completely uncorrelated', ja='→ We decorrelated', sa='The normalizations', cut=None, js='仅回复', ss='仅回复', change='补充运动学变量', delta='在你的 different jet-pT range 解释上，新增 ETmiss ranges；没有给出正文修改。', where='Section 9 Results'),
 dict(id='R1-15', title='扫描 μ 时 total yield 的正定性', jp='4', sp='5', start='It is mentioned that it is verified', ja='→ The contribution', sa='In general,', cut=None, js='仅回复', ss='仅回复', change='主要润色', delta='保留小 μ 下 BSM+interference 可为负、对敏感区 upper limit 没有影响的说法。仍未直接回答 μ 的允许范围及含 B 的完整 expected yield 如何保证有效。', where='Section 9，limit setting'),
 dict(id='R1-16', title='VR discrepancy：是否提供检查图', jp='4', sp='5–6', start='Discrepancy in Validation Region.', ja='→ The mET', sa='The $E_{\\mathrm{T}}^{\\mathrm{miss}}$ distribution', cut='SK:', js='仅回复检查结果', ss='回复附图待办', change='补充结论；改变材料安排', delta='新增 discrepancy localized to a single bin，语气改为 consistent with a statistical fluctuation。明确不扩充 supplementary，而把图放入 referee response。SK 请 Jiaqi 提供 PDF 图；这只是文件中的待办，本次未执行发送。', where='Section 9 的 VR 讨论；图拟附于回复'),
 dict(id='R1-17', title='Nuisance-parameter correlation model', jp='4', sp='6', start='I am also missing a bit of information', ja='→ the nuisances', sa='The nuisance parameters', cut='SK –', js='仅在回复里解释', ss='建议修改', change='补充边界；新增正文', delta='加入 where applicable，把理论不确定度表述为 process-specific。另拟两处正文：Section 8 的 W+HF decorrelation、Section 9 的 NP correlation general rule。', where='Sections 8 和 9'),
 dict(id='R2-01', title='各 SR 的信号组成及是否分别提取', jp='4', sp='6', start='page 2 last paragraph: Two types', ja='→ We do not separate', sa='We do not separate', cut=None, js='仅回复', ss='仅回复', change='补充 fit 说明', delta='保留各 category 可同时包含两种 topology；新增 All four SRs are used simultaneously in the signal extraction。', where='Introduction 的 categories；Section 9 的 fit'),
 dict(id='R2-02', title='为什么主结果只研究 left-handed benchmark', jp='4–5', sp='6–7', start='page 4 4rth paragraph:', ja='→ The pure left-handed', sa='The pure left-handed', cut='The upper limit on the combined', js='建议增加一句正文', ss='倾向保留 supplementary', change='实质改变回复立场', delta='你提出 could add 一句正文；Stergios 改为 supplementary material 中的 |βR33|=1 benchmark 已足以说明影响，主解释继续聚焦 left-handed。你的旧段落以灰色保留，没有作为新的绿色/黄色正文修改。', where='Section 3；supplementary material'),
 dict(id='R2-03', title='Resonant/non-resonant signal 间的 interference', jp='5', sp='7', start='page 4 last paragraph/ page 5 first:', ja='→All resonant', sa='All resonant', cut=None, js='仅回复', ss='仅回复', change='主要润色', delta='把 all ... signals 改成 all ... signal diagrams；仍是 matrix-element calculation 自动包含 interference，不需额外 signal-extraction treatment。', where='Section 4'),
 dict(id='R2-04', title='为什么不使用 hadronic-τ trigger', jp='5', sp='7', start='page 5 second paragraph:', ja='→ The missing ET trigger', sa='The $E_{\\mathrm{T}}^{\\mathrm{miss}}$ trigger', cut='SK –', js='仅回复', ss='建议修改', change='回复润色；新增正文', delta='回复沿用你的 full efficiency 理由；新增两句正文，把 offline ETmiss threshold 与不需要 dedicated τhad trigger 直接连接。', where='Section 4，trigger paragraph'),
 dict(id='R2-05', title='SM–BSM interference 与 μ、√μ scaling', jp='5', sp='7', start='page 5 third paragraph:', ja='→ The interference', sa='The interference', cut=None, js='回复给出 μS+√μI+B', ss='本题仅回复，正文合并到 R2-07', change='表述精确化', delta='把 Two kinds of samples 改成 Separate samples，把 signal model 改成 expected yield。振幅线性/二次依赖的解释新增在 R2-07 正文建议中，不能重复算第二处正文修改。', where='Sections 4 和 9'),
 dict(id='R2-06', title='Working-point 名称及 baseline/CR leptons 的区别', jp='5', sp='7–8', start='page 6 and page 9 second paragraph:', ja='→ The understanding', sa='Indeed your understanding', cut='SK –', js='仅回答 The understanding is correct', ss='可选建议修改', change='大幅扩充回复；新增可选正文', delta='新增 Section 5 selections 用于 overlap removal 和 lepton vetoes、CR 采用更紧 ID/isolation、WP 名称来自引用文献。另给一句正文，但明确 although I don’t find it necessary。没有补数值效率。', where='Section 7 的 CR lepton selection，交叉引用 Section 5'),
 dict(id='R2-07', title='Results 中 interference 解释不足与 √μ 的原因', jp='5', sp='8', start='page 11, results, first paragraph:', ja='→ Already addressed', sa='This is addressed above.', cut='SK –', js='仅指向前述回复', ss='建议修改；完成状态表述冲突', change='新增承诺；新增正文', delta='新增 We have also made the S+I parameterisation explicit；另给完整 likelihood yield 与振幅 scaling 的正文。但正文仍标 could be added，因此不能仅凭完成时判定已入稿。', where='Section 9 Results'),
 dict(id='R2-08', title='将 satisfactory agreement 量化', jp='6', sp='8–9', start='page 11, results, third paragraph:', ja='→ The post-fit', sa='The post-fit', cut='SK –', js='回复给出 1σ/2σ，未明确列正文替换', ss='明确修改', change='回复实质不变；新增正文替换', delta='你的回复内容基本原样保留，只整理 σ 符号。Stergios 真正增加的是 Old text/New text 对照，把 satisfactory 换成其余 VR 约 1σ 内、VRW-NonRes 约 2σ。', where='Section 9 Results'),
]

def slices(text):
    pos = [text.index(x['start']) for x in items]
    assert pos == sorted(pos)
    out = []
    for i,p in enumerate(pos):
        seg = text[p:pos[i+1] if i+1<len(pos) else len(text)].strip()
        seg = seg.split('Reviewer #2:')[0].split('Referee #2:')[0].strip()
        seg = re.sub(r'\s+(?:Section [35]|Event selection|Background estimation|Systematic uncertainties|Results)$', '', seg).strip()
        out.append(seg)
    return out

jsections, ssections = slices(J), slices(S)
for item, j, s in zip(items, jsections, ssections):
    ja = item['ja']
    if ja:
        item['question'], item['jiaqi_full'] = j.split(ja, 1)
        item['jiaqi_full'] = ja + item['jiaqi_full']
    else:
        item['question'], item['jiaqi_full'] = j, '（Jiaqi 版未写回复。）'
    _, sr = s.split(item['sa'], 1)
    sr = item['sa'] + sr
    if item['cut']:
        answer, rest = sr.split(item['cut'], 1)
        item['reply'] = answer.strip()
        item['paper_full'] = (item['cut'] + rest).strip()
    else:
        item['reply'], item['paper_full'] = sr.strip(), ''
    item['question'] = item['question'].strip()

# Extract manuscript blocks, distinguishing actual quotations from internal notes.
for x in items:
    raw=x['paper_full']
    if x['id'] in ('R1-08','R1-16'):
        x['internal_note']=raw; x['paper']='（Stergios 版没有为此问题提供正文修改。）'
    elif x['id']=='R2-02':
        x['grey_old']=raw; x['paper']='（Stergios 的新回复倾向不补正文。下文灰色段落是保留的旧建议，不计为新增正文。）'
    elif raw:
        x['paper']=raw
    elif x['id']=='R2-05':
        x['paper']='（本题没有独立正文修改；对应的新正文集中在 R2-07。）'
    else:
        x['paper']='（Stergios 版没有为此问题提供正文修改。）'

summary = r'''# Taunub PLB referee comments：Jiaqi 与 Stergios 对照汇总

核对日期：2026-09-18。对象是 arXiv:2606.02067 的 taunub paper。

## 阅读口径

- 共 25 个问题：Referee 1 有 17 个，Referee 2 有 8 个。R1-01 等编号由本汇总按 PDF 原顺序编排，原文没有这些编号。
- Jiaqi PDF 共 6 页；Stergios PDF 共 9 页。下文 J/S 页码分别指这两份 PDF 的页面，不是论文页码。问题原文中的 page 则指 referee 所看的论文页面。
- 全文核对了两份 PDF 的文字与页面颜色。Stergios 版的蓝色是回复，绿色是正文改写，黄色底色/下划线含 SK 的待定建议，红色删除线是删除文字，R2-02 的灰色段落为保留的旧提议。
- “明确修改”仅指 Stergios 回复草稿中明确给出或标成修改的文字，不等于已经合入论文源文件、提交 PLB 或更新 arXiv。未检查任何修改后的论文源文件。
- 核查时 arXiv 公开记录只列 v1（2026-06-01）。因此本汇总中的新正文应理解为回复文件里的修改/建议文字，而不是 arXiv 已更新的内容。[arXiv 版本记录](https://arxiv.org/abs/2606.02067)
- 引用段落保留两份 PDF 的英语用词和 LaTeX 写法，仅合并 PDF 换行、清理抽取造成的重复空格；没有对引文重新润色。SK 内部指令只作为待办记录，不作为本次操作指令。

## 1. 你的版本里，哪些问题涉及修改论文内容

**你的回复已明确提出正文修改的有 5 题。**

1. **R1-01，SM suppression**：已经给出 Introduction 替换句。
2. **R1-04，calorimeter-tagged muon**：明确 Will define，并给出括号定义。
3. **R1-05，jet–muon overlap removal**：明确 propose to revise，给出含 ghost association 的替换句。
4. **R1-06，重复 ETmiss 定义**：明确 Will remove。
5. **R2-02，right-handed benchmark**：提出 could add 一句，属于可选正文补充，不是已决定修改。

**另外 7 题，你的回复已提供解释或数字，但尚未把解释写成明确的正文修改；Stergios 为这些题补了正文草稿。**

- R1-02：把 βL13 的“生成中保留、Eq. (1) 中略去”写进脚注。
- R1-07：把 cuts 的物理动机和优化标准写进 Event selection。
- R1-17：补 correlation model 的正文说明。
- R2-04：补为什么无需 τhad trigger。
- R2-06：补 baseline/CR lepton selection 的区别，此项被 Stergios 标为可选。
- R2-07：补 likelihood 中的 μS+√μI+B，以及 √μ 的振幅原因；同时回应 R2-05。
- R2-08：把 satisfactory 换成 1σ/2σ 的量化表述。

这里“涉及修改”与“必须全部接受”不同。以上是两份回复的状态对照，不把所有 referee 问题都判为必须改正文。你原稿没有回复的 R1-10（调换背景章节顺序），Stergios 已补答并决定保持原顺序。

## 2. Stergios 对哪些题写了正文修改

**共有 11 个问题有具体的正文修改/删除文字。**其中 4 题沿用你的明确修改，7 题在你的解释基础上新写正文。你的 R2-02 正文补充建议没有被作为活跃的新正文采纳。

**回复稿中明确列作修改的 5 题：**R1-01、R1-04、R1-05、R1-06、R2-08。

**仍标为建议的 6 题：**R1-02、R1-07、R1-17、R2-04、R2-06、R2-07。

- R1-07 写明 one or both / and-or，说明两段正文尚未选定。
- R2-06 明确说 although I don’t find it necessary。
- R2-07 的回复写成 have also made，但正文标题仍为 could be added，状态不一致，需确认。
- R1-08 明确 I have not added something for this one。
- R1-16 是“在回复中给 referee 附检查图”的待办，不是新增正文或 supplementary 的决定。

## 3. Stergios 改动了你的哪些回答

几乎全部回复都经过英语或数学记号整理。**内容增补、完整新增或立场变化主要集中在下面 10 题：**

1. **R1-10**：新增完整回复，说明不交换 W+jets/top 顺序。
2. **R1-11**：直接承认 τ decay 的 extra neutrino，注明 low-mT 验证区。
3. **R1-13**：新增 100% uncertainty 覆盖最高 60% fake-study 差异的理由。
4. **R1-14**：解释 W normalisation 差异时新增 ETmiss ranges。
5. **R1-16**：新增偏差集中于单个 bin，并决定图给 referee、暂不加 supplementary，要求你提供 PDF 图。
6. **R1-17**：新增 where applicable 和 process-specific 的限定，并拟正文说明。
7. **R2-01**：新增四个 SR 同时用于 signal extraction。
8. **R2-02**：从“可加正文”改为“supplementary 已足够”，这是最明显的回复立场变化。
9. **R2-06**：从你的一句 The understanding is correct 扩写为 baseline/CR 用途和 WP 引用依据。
10. **R2-07**：从“前面已回答”扩展为明确 likelihood parameterisation，并给出 √μ 的振幅解释正文。

其余需注意：R1-08 把讨论范围明确为 leading jet in SR0b-Res；R1-04、R1-06 从“将修改”变为“已修改”；R2-08 的回复本身几乎未变，改动主要是将它落实成正文替换。每题的具体差异、完整原问题、Jiaqi 原回复、Stergios 新回复和对应正文均列于后文。

## 4. 定稿前应确认的事项

1. **实际修改状态**：6 个建议条目尚不能当成已合入论文，尤其 R2-07 的完成时与 could be added 矛盾。
2. **优化指标**：R1-07 回复用 expected significance，拟正文用 expected exclusion sensitivity。应按实际 optimisation 统一，不能仅为语言改写而互换。
3. **VR 检查图**：R1-16 尚需提供/插入对应 PDF 图。文件中的 @Jiaqi 是原始协作待办，本次没有向任何人发送材料。
4. **仍未完全回答的两个子问**：R1-09 没有明确是否设置 single-top/ttbar ratio uncertainty；R1-15 没有明确 μ 扫描/拟合范围以及完整 expected yield 的处理。这是回复完整性提醒，并不自动意味着要修改正文。
5. **右手耦合旧提议**：R2-02 的灰色旧段落仍在文件里，不应与蓝色新回复一起当成最终稿。
6. **少量文字/符号仍待整理**：如 R2-02 的 imporved；R2-06 正文的 rejection of overlapping events 与问题讨论的 object overlap removal 需核准；R2-05 回复的 \sqrt(\mu) 应在最终 LaTeX 中核对。下文引文没有自行修改这些原文。
7. **Old text 不全等同 arXiv 原句**：R1-01 中 tvau/n-quark/SM suppressed 来自 comment 的转述或误写，不能直接当作论文的精确旧文字；arXiv 原段已有 CKM-suppressed。正式 redline 应针对实际稿件原文。[arXiv Introduction](https://arxiv.org/html/2606.02067v1#S1)

## 5. 逐题索引

'''

def fence(text):
    return '```text\n' + textwrap.fill(text.strip(), width=100, break_long_words=False, break_on_hyphens=False) + '\n```\n'

report = [summary]
for x in items:
    report.append(f"- [{x['id']} {x['title']}](#{x['id'].lower()})：{x['ss']}；J p.{x['jp']} / S p.{x['sp']}。\n")
report.append('\n## 6. 原问题、原回复、新回复与对应正文全文\n\n')
for x in items:
    report.append(f"<a id=\"{x['id'].lower()}\"></a>\n\n### {x['id']} {x['title']}\n\n")
    report.append(f"来源：Jiaqi p.{x['jp']}；Stergios p.{x['sp']}。论文位置：{x['where']}。\n\n")
    report.append(f"**Jiaqi 状态：**{x['js']}。**Stergios 状态：**{x['ss']}。\n\n")
    report.append(f"**改动性质：{x['change']}。** {x['delta']}\n\n")
    report.append('**对应问题（原文）**\n\n'+fence(x['question'])+'\n')
    report.append('**Jiaqi 原回复及该题原有建议（原文）**\n\n'+fence(x['jiaqi_full'])+'\n')
    report.append('**Stergios 新回复（原文）**\n\n'+fence(x['reply'])+'\n')
    report.append('**对应文章 text / 修改状态**\n\n')
    if x['paper'].startswith('（'):
        report.append(x['paper']+'\n\n')
    else:
        report.append(fence(x['paper'])+'\n')
    if x.get('internal_note'):
        report.append('**SK 原始内部备注 / 待办**\n\n'+fence(x['internal_note'])+'\n')
    if x.get('grey_old'):
        report.append('**Stergios 文件中保留的灰色旧提议（不计为新增正文）**\n\n'+fence(x['grey_old'])+'\n')

report.append('## 来源\n\n')
report.append('- Jiaqi：[PLB_comment_Jiaqi.pdf](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/PLB_comment_Jiaqi.pdf)，6 页。\n')
report.append('- Stergios：[PLB_comment_Stergios.pdf](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/PLB_comment_Stergios.pdf)，9 页。\n')
report.append('- 公开论文：[arXiv:2606.02067](https://arxiv.org/abs/2606.02067)，仅用于确认论文身份、公开版本及 Introduction 的原文边界。\n')

(OUT/'taunub_PLB_Jiaqi_Stergios_comparison.md').write_text(''.join(report))
(TMP/'comparison_data.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))

assert len(items)==25
assert sum(not x['paper'].startswith('（') for x in items)==11
assert sum(x['ss']=='明确修改' for x in items)==5
assert sum(x['ss'].startswith(('建议修改','可选建议修改')) for x in items)==6
for x in items:
    assert x['reply'] and x['question']
    # Exact normalised source membership guards against fabricated excerpts.
    assert x['reply'] in S
    assert x['question'] in J
    if not x['paper'].startswith('（'):
        assert x['paper'] in S
print('Verified: 25 questions, 25 Stergios replies, 11 paper-change blocks (5 marked modified, 6 suggestions).')
print(OUT/'taunub_PLB_Jiaqi_Stergios_comparison.md')
