from pathlib import Path

VAULT=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search')
SRC='/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references'
CACHE='/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build'

def write(folder,name,body,status='已核对来源，按所列版本',tags='[analysis, reference]'):
    path=VAULT/folder/(name+'.md');path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'---\ntype: knowledge-note\nupdated: 2026-09-07\nstatus: "{status}"\ntags: {tags}\n---\n\n# {name}\n\n'+body.replace('{SRC}',SRC).replace('{CACHE}',CACHE).strip()+'\n')

write('10_理论与动机','理论文献导航与版本边界',r'''
这组资料解释本分析为什么搜索 $\tau+E_T^{\rm miss}+\mathrm{jets}/b\text{-jets}$，以及 collider 参数如何与 $b\to c\tau\nu$ 联系。数字和 favoured region 都属于相应论文使用的数据版本，不自动代表 2026 年的世界平均。

## 按问题检索

- 为什么在 mono-tau 上增加一个 $b$-jet：[[Iguro等2022_taunub搜索动机]]。
- 本分析 $\beta_L^{23}$、$\beta_L^{33}$、$\beta_R^{33}$ 和 CKM 的意义：[[U1耦合与低能匹配速查]]。
- $U_1$ 的 vector Lagrangian、Yang–Mills/minimal convention、伴随 $Z'$ 和 coloron：[[Baker等2019_High-pT与U1模型]]。
- 为什么不能随意丢弃 right-handed coupling；哪些 flavour 限制依赖 UV completion：[[Cornella等2019_U1与flavour结构]]。
- 2023 版 low-energy fit、$\tau\tau$ 互补性、benchmark：[[Aebischer等2023_低高能联合约束]]。
- 画图脚本中的 $C_{LL}$ band 到底来自什么：[[Favoured-region理论输入与区间含义]]。

## 本地原始文献

1. [2111.04748v3.pdf](<{SRC}/2111.04748v3.pdf>)：Endo、Iguro、Kitahara、Takeuchi、Watanabe，JHEP 02 (2022) 106。[arXiv正式记录](https://arxiv.org/abs/2111.04748)。
2. [1901.10480v3.pdf](<{SRC}/1901.10480v3.pdf>)：Baker、Fuentes-Martín、Isidori、König，EPJC 79 (2019) 334。[arXiv正式记录](https://arxiv.org/abs/1901.10480)。
3. [1903.11517v2.pdf](<{SRC}/1903.11517v2.pdf>)：Cornella、Fuentes-Martín、Isidori，JHEP 07 (2019) 168。[arXiv正式记录](https://arxiv.org/abs/1903.11517)。
4. [2210.13422v3.pdf](<{SRC}/2210.13422v3.pdf>)：Aebischer、Isidori、Pesut、Stefanek、Wilsch，2023-06-12 的 v3。[arXiv正式记录](https://arxiv.org/abs/2210.13422)。

各笔记的“PDF 第 N 页”均为从封面起算的物理页码，非印刷页码。四篇论文的年代、假设和符号不同；引用时优先跟随本分析实际 Lagrangian，再做显式映射。
''',tags='[theory, motivation, index]')

write('10_理论与动机','U1耦合与低能匹配速查',r'''
## 模型与物理含义

本分析的 vector leptoquark 为 $U_1\sim(3,1,2/3)$，依次表示 $SU(3)_C$、$SU(2)_L$、$U(1)_Y$ quantum numbers。它通过同一个 weak-doublet current 连接 down-type quark–charged lepton 和 up-type quark–neutrino。

采用 down-quark、charged-lepton mass basis：

$$
\mathcal L_{\rm int}=\frac{g_U}{\sqrt2}U_{1\mu}\left[\beta_L^{i\alpha}\bar q_L^i\gamma^\mu\ell_L^\alpha+\beta_R^{i\alpha}\bar d_R^i\gamma^\mu e_R^\alpha\right]+\mathrm{h.c.},\qquad q_L^i=\binom{V_{ji}^*u_L^j}{d_L^i}.
$$

这里 $i$ 为 quark generation，$\alpha$ 为 lepton generation。$\beta_L^{33}$ 给 $b_L\tau_L$，$\beta_L^{23}$ 给 $s_L\tau_L$，$\beta_R^{33}$ 给 $b_R\tau_R$；$g_U$ 决定整体强度。本分析通常固定 $\beta_L^{33}=1$。由于 conjugate doublet 中的 CKM 变为 $V_{ji}$，$c_L\nu_\tau$ coupling 为

$$
h_{c\nu}=\frac{g_U}{\sqrt2}(V_{cd}\beta_L^{13}+V_{cs}\beta_L^{23}+V_{cb}\beta_L^{33}).
$$

这解释了为何 $\beta_L^{23}$ 即使小于 1 也很重要：它乘的是 $V_{cs}$，而第三代项乘较小的 $V_{cb}$。来源：[internal note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF 第20页 Eq.(4.1)；[Cornella 2019](<{SRC}/1903.11517v2.pdf>) PDF 第3–4页 Eqs.(2.1)–(2.5)。

## 与低能 Wilson coefficient 的映射

定义 $C_{V_L}$ 为相对 SM 的额外 left-handed vector amplitude；SM 对应 $C_{V_L}=0$。令 $C_U=g_U^2v^2/(4M_U^2)$，则 tree-level matching 给出

$$
C_{V_L}=\frac{C_U}{V_{cb}}(V\beta_L)_{23}(\beta_L^{33})^*,\qquad
C_{S_R}=-2\frac{C_U}{V_{cb}}(V\beta_L)_{23}(\beta_R^{33})^*.
$$

$C_{S_R}$ 这里乘 $(\bar c_L b_R)(\bar\tau_R\nu_L)$；不同文献也记为 $C_{S_1}$，不可只按字母比较。在 $\beta_L^{13}=0,\beta_L^{33}=1$、实 coupling 情形：

$$
C_{V_L}=\frac{g_U^2v^2}{4M_U^2}\left(1+\frac{V_{cs}}{V_{cb}}\beta_L^{23}\right).
$$

这些是将 [Iguro等论文](<{SRC}/2111.04748v3.pdf>) PDF 第5页 Eq.(6) 的 $h=g_U\beta/\sqrt2$ 代入所得的本分析符号映射；也与 [2210.13422v3](<{SRC}/2210.13422v3.pdf>) PDF 第4页 Eqs.(23)–(25) 一致。后者的 $C_{LR}^c$ 不含 scalar operator 前的 $-2$，所以 $C_{S_R}=-2C_{LR}^c$。

## 从低能走向 collider

纯 LH 且 light-lepton channel 不变时，$R(D^{(*)})/R(D^{(*)})_{\rm SM}=|1+C_{V_L}|^2$。有 RH coupling 时出现 scalar contribution，$R(D)$ 和 $R(D^*)$ 对它的灵敏度不同，且 scalar coefficient 需要从 matching scale 演化到 $m_b$。不能仅以 $|\beta_R^{33}|$ 表示低能预测：相对符号和 phase 有影响。[2210.13422v3](<{SRC}/2210.13422v3.pdf>) PDF 第4–5页 Eqs.(30)–(35)。

高能 $\tau\nu$ 过程连接两个 coupling vertex；on-shell production、off-shell propagator、width、PDF 和 cuts 共同决定 rate。低能 amplitude 的简单 $g_U^2/M_U^2$ 比例不能直接当作所有 collider selected yields 的缩放。更大的 $\beta_L^{23}$ 同时提高 $s\tau$ final state 的重要性，因此 0b region 是有真实 signal 的类别。参见 [本分析paper draft](<{SRC}/ATL-COM-PHYS-2026-015.pdf>) PDF 第3–5页 §3。
''',tags='[theory, U1, CKM, Wilson-coefficient]')

write('10_理论与动机','Iguro等2022_taunub搜索动机',r'''
原文：[2111.04748v3.pdf](<{SRC}/2111.04748v3.pdf>)；[arXiv](https://arxiv.org/abs/2111.04748)。作者为 Motoi Endo、Syuhei Iguro、Teppei Kitahara、Michihisa Takeuchi、Ryoutaro Watanabe。它是本分析 $\tau\nu+b$ non-resonant search 的直接 phenomenological motivation，但不是 ATLAS 正式 object definition 或最终灵敏度的来源。

## 主要论证

1. $R(D^{(*)})$ 测量比较 $b\to c\tau\nu$ 与 light-lepton mode，部分 hadronic/experimental uncertainty 在 ratio 中抵消。NP contribution 可写成 vector/scalar/tensor effective operators。LHC 的 hard $\tau\nu$ final state 用 crossing-related interaction 测试这些 coupling。（PDF 第2–5页，§1–2，Eqs.(1),(4)–(6)）
2. 增加 $b$-tag 会损失一部分 signal，但能强烈抑制来自 light-flavour jets 的 $W/Z+$jets background。本文选择较严格的 $b$-tag 工作点，使用 $\epsilon_b=0.6$、$\epsilon_c=1/27$、$\epsilon_j=1/1300$；因而不能把其 background composition 原样用于本分析的 85% WP。（PDF 第8页，Eq.(12)）
3. 比较 mono-tau 的 cut a 与加 $b$-jet 的 cut b，本文模拟中总 background 降低约两个数量级，signal 损失较小，因此 Wilson-coefficient reach 改善。摘要所称“约40%”是本文特定模拟和比较的 sensitivity 结果。（PDF 第12–16页，Tables 1–6）
4. TeV-scale LQ 的 propagator 不能普遍用 contact interaction 代替。低能 $q^2\ll M_{LQ}^2$ 的 EFT 在 flavour physics 很好，但 LHC tail 可有 $|q^2|\sim M_{LQ}^2$；有限质量使预期 reach 弱于 EFT limit。（PDF 第3–5页，§1–2；第16页 Tables 5–6）

## U1 部分怎么用

- §2.1（PDF 第5–6页）给出 $h_L,h_R$ current 和 matching。映射到本分析前必须保留 $g_U/\sqrt2$：见 [[U1耦合与低能匹配速查]]。
- §4.4.3（PDF 第22–26页）比较 pure-LH/single-$U_1$ 和 $U(2)$-$U_1$ scenarios，并显示 coupling ratio 如何改变 mono-tau 与 $\tau\nu+b$ 的互补性。
- Figure 4（PDF 第23页）在 $M_{LQ}$–coupling product 平面比较 expected sensitivity 和 flavour-favoured bands；Figure 5（PDF 第24页）在两 coupling 平面展示 $\tau\tau$ 约束的互补性。
- Table 6（PDF 第16页）适合检索 expected reach 的尺度依赖。Figure 6（PDF 第25页）用于理解 RH phase：相位的正负不是误差条。

## 版本和使用边界

文中使用的 flavour solution，例如 $C_{V_1}\simeq0.09$，是 2021–2022 分析输入（PDF 第5、22页），不等于当前脚本中的 favoured region。本文的 tau tagging 为 simplified detector treatment，且 b-tag mistag 很严格；ATLAS 使用 data-calibrated ID、独立 CR/VR 和 signal simulation。写本分析 motivation 时借用物理逻辑，数值和 selection 则以本分析代码与 note 为准。
''',tags='[theory, Iguro, motivation, taunub]')

write('10_理论与动机','Baker等2019_High-pT与U1模型',r'''
原文：[1901.10480v3.pdf](<{SRC}/1901.10480v3.pdf>)；[arXiv](https://arxiv.org/abs/1901.10480)。本地 v3 为 2019-04-16 版本。

## 这篇文献回答的问题

$U_1$ 是 massive vector，写一个 phenomenological interaction 并不足以说明 UV consistency。本文先解释 gauge/composite completion 中 $U_1$ 常与 neutral $Z'$ 和 colour-octet $G'$ 一起出现，再构建足够一般的 high-$p_T$ Lagrangian，比较 pair production、$\tau\tau$、$\tau\nu$、LFV 和 $t\bar t$ constraints。各通道针对不同 coupling，不能把一个质量下限当作所有 $U_1$ realization 的通用下限。

## 阅读定位

- PDF 第2–4页 §2：gauge algebra closure 及 $SU(4)$、额外 vector states 的动机。适合支持一句到一段 UV 背景；本分析不需要完整照搬群论推导。
- PDF 第5页 §3 Eq.(9)：$U_1$ kinetic、mass、gauge 和 fermion interactions；Eq.(12)：down-aligned doublet；Eq.(13)：flavour texture。
- PDF 第6页 Table 1：不同 high-$p_T$ final states 对应的 constraint 来源。这里列的是早期 Run-2 数据，是文献当年的 input。
- §4：不同 collider channel 的 reinterpretation；检索对本分析直接有用的 $\tau\nu$ 与 $\tau\tau$ dependence，不把其它 mediator 的贡献无条件加进本分析 signal。

## Convention 必须保留

本文 gluon term 写作 $-ig_s(1-\kappa_U)U^\dagger_\mu T^aU_\nu G^{a\mu\nu}$。这一写法中 Yang–Mills/gauge case 是 $\kappa_U=0$，minimal-coupling case 是 $\kappa_U=1$。换成直接用 $\kappa$ 乘 field-strength 的论文，0/1 标签会改变。应先核对 equation，再引用 benchmark 名称。（PDF 第5页 Eq.(9) 及其下段）

本分析采用相同形式，但 flavour assumptions 的 scan 范围可更宽。该论文由 $U(2)$-type assumptions motivated 的 hierarchy 不是直接实验测量；尤其不能把它当成 $\beta_L^{23}$ 必須很小的 model-independent limit。
''',tags='[theory, U1, high-pT, convention]')

write('10_理论与动机','Cornella等2019_U1与flavour结构',r'''
原文：[1903.11517v2.pdf](<{SRC}/1903.11517v2.pdf>)；[arXiv](https://arxiv.org/abs/1903.11517)。v2 为 2019-07-25，目标是当时 charged-和 neutral-current B anomalies 的联合解释。

## 核心内容

这篇文献把 $U_1$ simplified model 与具体 flavour non-universal UV completion 分开处理。前者用于 tree-level 或对 UV 不敏感的 observables；后者用于需要其它新态参与才能可靠计算的 loop effects，特别是 $\Delta F=2$。因此引用 $B_s$ mixing constraint 时，需要同时说出 completion 假设，而不能只写一个 standalone $U_1$ mass/coupling bound。

PDF 第3页 Eqs.(2.1)–(2.4) 建立 current、basis 和 texture，固定 $\beta_L^{b\tau}=1$。第4页 Eq.(2.5) 将 mediator 积分掉，定义 $C_U=g_U^2v^2/(4M_U^2)$。$b\to c\tau\nu$ amplitude 有 $1+(V_{cs}/V_{cb})\beta_L^{s\tau}+(V_{cd}/V_{cb})\beta_L^{d\tau}$，这正是不能省略 CKM contribution 的来源。

## Right-handed coupling 的作用

规范量子数允许 $\beta_R^{b\tau}$；令它为零是一种 benchmark choice，非 gauge symmetry 的强制结果。它引入 scalar operator，影响 $R(D)$、$R(D^*)$ 和 $B_c\to\tau\nu$ 的程度不同。第4页 Eqs.(2.6)–(2.8) 给出直观近似及 scalar running factor。该近似是 expansion，不能在任意大 coupling 区域代替完整预测。

## 怎样用于本分析

- 解释 coupling matrix 与 down-mass basis：PDF 第3–4页。
- 解释 RH 不能只看绝对值：PDF 第4页 $R(D^{(*)})$ formulae。
- 解释小 $\beta_L^{s\tau}$ 的来源：PDF 第4页明确把 $|\beta_L^{s\tau}|\le0.25$ 作为该 fit 的先验/assumption，并说仅 low-energy data 对它约束弱；不是观测直接给出的硬上限。
- 查完整 UV/flavour discussion：§3（PDF 第12页起，具体 subsection 以原目录为准），适合检索 $ΔF=2$、vector-like fermions、4321 completion。

文中 2019 年 anomaly significances、global-fit benchmark 和当时 $b\to s\ell\ell$ 情况只作为历史背景。当前论文动机应分别更新 charged-current 与 neutral-current 的实验状态。
''',tags='[theory, flavour, U1, UV]')

write('10_理论与动机','Aebischer等2023_低高能联合约束',r'''
原文：[2210.13422v3.pdf](<{SRC}/2210.13422v3.pdf>)；[arXiv](https://arxiv.org/abs/2210.13422)。本文把更新的 low-energy charged-current fit 与 high-$p_T$ $\tau\tau$ search 联系起来。摘要中的“当前”指该 2023 年版本。

## 结构与关键定位

- §II.A（PDF 第2–4页）：flavour basis、$U(2)$ breaking、down alignment 与 minimal/non-minimal ansatz；说明不同 flavour observables 的关联来自哪些假设。
- §II.B（PDF 第4页）：Eqs.(23)–(25) 定义 $C_{LL}^c,C_{LR}^c$。本分析中 $C_{V_L}=C_{LL}^c$，scalar coefficient 通常为 $-2C_{LR}^c$。
- §III.A（PDF 第4–5页）：$R(D)$、$R(D^*)$、$R(\Lambda_c)$ 的输入及 coefficient dependence；Figure 1 是二维 low-energy fit。
- §III.B 与 Figures 2–3（PDF 第6–7页）：$\tau\tau$ 的 b-tag/b-veto collider constraints 和与 low-energy contour 的比较。$b\bar b\to\tau\tau$ 及初态 gluon splitting 解释伴随 b-jet 的作用。
- Appendix A（PDF 第8–9页）：可供未来 search 使用的 parameter benchmarks；Figure 4 是质量–coupling 平面。

## 可直接查的数字及其前提

Figure 1 的两系数被假设为实数、在 $\Lambda_{\rm UV}=1$ TeV 归一化；best fit 为 $(C_{LL}^c,C_{LR}^c)=(0.05,-0.02)$。Eq.(35) 在 QCD running approximation 下令 $C_{LL}^c(m_b)=C_{LL}^c(1\,\mathrm{TeV})$，scalar coefficient 则有约1.6的 running factor。它是二维最佳点，不能写成 pure-LH fit 的中心和误差。

Appendix A 给 pure-LH 时 $M_U/g_U\in[0.69,1.71]$ TeV，$|\beta_R|=1$ 时 $[0.92,2.19]$ TeV，均为文中 low-energy fit 的 90% CL preferred range。PDF 第9页明确：这些区间在 $\beta_L^{s\tau}\in[0.06,0.16]$、$\beta_L^{d\tau}=0$ 等假设下得到。不能将其原样套入本分析一直扫描至 $\beta_L^{23}\sim2$ 的参数平面。

## 对本分析最有用的结论

$\tau\tau$ 对第三代 coupling 很敏感；为了固定 low-energy effect，更小的 $s\tau$ coupling 通常要求更强的整体 coupling，因此更容易受该 channel 约束。$\tau\nu+\mathrm{jets}/b$ 对第二代耦合提供互补信息。比较不同 search 时同时记录 flavour assumptions、chirality、mass、width 和 perturbative treatment。

脚本里 $[0.038,0.090]$、$[0.018,0.110]$ 与 Figure 1 的 pure-LH 切片对应关系见 [[Favoured-region理论输入与区间含义]]。
''',tags='[theory, flavour-fit, U1, benchmark]')

write('10_理论与动机','Favoured-region理论输入与区间含义',r'''
## 已找到的理论关系

本分析 $\beta_L^{13}=0,\beta_L^{33}=1,\beta_R^{33}=0$ 的画图公式应为

$$
C_{LL}^c=\frac{g_U^2v^2}{4M_U^2}\left(1+\frac{V_{cs}}{V_{cb}}\beta_L^{23}\right),
\qquad
\beta_L^{23}=\frac{V_{cb}}{V_{cs}}\left(\frac{4M_U^2 C_{LL}^c}{g_U^2v^2}-1\right).
$$

这是 [2210.13422v3](<{SRC}/2210.13422v3.pdf>) PDF 第4页 Eq.(25) 在本分析 texture 下的表达式。使用 GeV 或 TeV 时 $M_U$ 和 $v$ 必须同单位。括号中的 1 是 $V_{cb}\beta_L^{33}$ 项；在较小 $\beta_L^{23}$ 下不能忽略。见 [[U1耦合与低能匹配速查]]。

## 当前代码值与文献图的关系

代码快照 [draw_limits_mu.py](<{CACHE}/code/snapshot/run/scripts/draw_limits_mu.py>) 的实际 cache 路径如有变动应从代码资料索引检索；原位置是 `/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/draw_limits_mu.py`。本次远程核对到实际启用区间为 $1\sigma:[0.038,0.090]$、$2\sigma:[0.018,0.110]$；注释中的 $0.051\pm0.027$ 并不产生这四个端点。

**图形对应已核对，精确提取来源待确认：** [2210.13422v3](<{SRC}/2210.13422v3.pdf>) PDF 第5页 Figure 1 的蓝色二维 low-energy fit 椭圆与 $C_{LR}^c=0$ 横线相交，视觉读数与上述区间相符。正文没有逐项列出这四个端点；目前不能证明代码就是从该图 digitisation 得到，不能把估读写成原文精确数值。

## 为什么需要区分统计含义

Figure 1 是两个 real Wilson coefficients 的 joint contour。取 $C_{LR}^c=0$ 的截线，保留的是原二维 fit 的等高线定义。重新在 pure-LH hypothesis 中做 one-parameter fit，其 best fit、$\Delta\chi^2$ reference 和 1σ/2σ thresholds 都可能不同；两种“favoured band”不应混用。也不能把二维 fit 的 $C_{LL}^c$ profile/marginal interval当作固定 $C_{LR}^c=0$ 的区间。

## 建议保存的 provenance

- 原始 fit 的 paper/version、Figure/Table/Eq.；若由图读数，保存 digitised points 或 extraction record。
- 使用哪些 observables、covariance 和 SM predictions；WC renormalisation scale。
- 这是 joint contour 的 slice，还是 fixed-model one-parameter confidence interval。
- $\beta_R$、$\beta_L^{13}$、CKM 和 $\beta_L^{33}$ convention。
- 画图源码中的 active numerical constants 与对应 git commit。

当前最需要补充的是四端点的提取或拟合记录，以及 $0.051\pm0.027$ 的具体出处；无需为了获得这些记录先更改现有代码。
''',status='公式已核对；数值端点与Fig.1图形对应，提取记录待补',tags='[theory, favoured-region, provenance, todo]')

write('20_Trigger','Trigger导航与本分析使用逻辑',r'''
本分析使用 full Run-2（2015–2018，13 TeV）数据。signal regions 用 $E_T^{\rm miss}$ trigger，含 electron/muon 的 control regions 用 single-lepton trigger。2026 paper draft 的“典型 threshold 为110 GeV / 26 GeV”是概述，不能替代 run-period chain selection。[paper draft](<{SRC}/ATL-COM-PHYS-2026-015.pdf>) PDF 第5页 §4、第8页 §6、第25页 Table 3。

- 各年 MET chain、period、L1 seed 与 luminosity tradeoff：[[Run2_MET_trigger逐年推荐与检查]]。
- Single-electron/muon chain 与 CR transfer：[[Run2_单轻子trigger与控制区]]。

## 选择 MET trigger 的原因

信号含 prompt neutrino 和 tau-decay neutrino，因此具有真实 $E_T^{\rm miss}$；高 offline threshold 可让 analysis operating point 进入 trigger plateau。trigger 的 online MET 与 offline calibrated MET 不同，名称中的 xe110 不是 offline 110 GeV cut。本分析 resonant/non-resonant selection 分别要求至少200/400 GeV，note 在 light-lepton control sample 中检查效率。[internal note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF 第28–29页 Eq.(6.2)、Fig.6.1。

效率定义为独立 electron trigger 选出的 CR sample 中，同时通过 MET trigger 的比例。这个验证依赖控制样本与 SR 的 hadronic recoil/online MET response 可比；尤其 muon 在 calorimeter 中可见能量较少，不能未经说明把含 muon 的 online MET 与 full offline MET 曲线混为一谈。

## 资料版本

`Atlas_LowestUnprescaled.pdf` 同时包含 Run-3 和 Run-2。PDF 第6页起出现2025年 menu；本分析重点是第49页起2018年、第60页起2017年、第70页起2016年、第77–78页2015年。不要取文件最前面的 current menu 作为本分析 trigger。

年度 MET 推荐另有独立PDF；文件名 `Atlas_RecommendedMetTriggers2017.pdf` 的第6页实际包含2018年 menu。读页码时从封面起算。

## 尚需从运行配置保留的信息

精确 trigger OR、run-number 切换、event-level trigger matching、MC efficiency SF、GRL/luminosity calculation 和 ntuple 分支必须最终与代码对应。TWiki 说明“推荐哪些”不等于代码证明“实际用了哪些”。本笔记记录的是来源内容；代码核对结果应与 framework 资料互相链接。
''',tags='[trigger, Run2, index]')

write('20_Trigger','Run2_MET_trigger逐年推荐与检查',r'''
以下为历史 Run-2 TWiki 推荐，不自动代表本分析完整 run-dependent OR。PDF 页码从封面起算；源文件仅作只读证据。

## 2015

[RecommendedMetTriggers2015](<{SRC}/triggers/Atlas_RecommendedMetTriggers2015.pdf>) PDF 第2页列出 `HLT_xe70_mht`，覆盖 C2–C4、D3–D6、E、F、G、H、J。`HLT_xe70_tc_lcw` 与 `HLT_xe70` 也 unprescaled。文中说明当年测试 cell、topocluster、pile-up mitigation 等算法；比较结果中 topo-cluster algorithm 的 offline MET turn-on 更陡。存在 muon-corrected variants，不应误认为与默认 chain 完全相同。

## 2016

[RecommendedMetTriggers2016](<{SRC}/triggers/Atlas_RecommendedMetTriggers2016.pdf>) PDF 第2–3页：

- A、B–C、D1–D3：`HLT_xe90_mht_L1XE50`。
- D4–E3、F1、F2以后：`HLT_xe110_mht_L1XE50`。
- D4–F1 的 `HLT_xe100_mht_L1XE50` 大部分时间 unprescaled，但一些高 luminosity run 开始时例外；若使用需重算有效 luminosity。

MHT 是 trigger jets transverse-momentum vector sum 的负值；该页给的 jet calibration 是 EM + pile-up subtraction + JES。不能把 online jet sum 和 offline MET 的 soft term 等同。

## 2017

[RecommendedMetTriggers2017](<{SRC}/triggers/Atlas_RecommendedMetTriggers2017.pdf>) PDF 第2–5页提供三类 threshold/luminosity tradeoff：

- 低 threshold 且较小 luminosity loss 的 period组合：B 用 `HLT_xe90_pufit_L1XE50`；C 用 `HLT_xe100_pufit_L1XE55`；D1–D5 用 `HLT_xe110_pufit_L1XE55`；D6–K 用 `HLT_xe110_pufit_L1XE50`。
- 更低 L1 threshold 的替代方案，在 C、D1–D5 采用 L1XE50 variant，但部分 run 被 prescale。
- `HLT_xe110_pufit_L1XE55` 是为避免 period组合而给出的较高 threshold/full-luminosity 选项；应以实际 run/LB 数据核验有效性。

TWiki 对前两种方案给约270 pb⁻¹、900 pb⁻¹的相对 luminosity loss，仅为 indicative 数字（PDF 第5–6页）。这些是当时 menu 比较，不能直接从本分析140 fb⁻¹扣除。pufit 为 pile-up mitigation algorithm；其完整数学机制应引用 MET-trigger performance paper。

## 2018

同一 [2017文件](<{SRC}/triggers/Atlas_RecommendedMetTriggers2017.pdf>) PDF 第6页的2018表：

- B：`HLT_xe110_pufit_xe70_L1XE50` 或 `HLT_xe120_pufit_L1XE50`。
- C–J：表中有 `HLT_xe110_pufit_xe65_L1XE50`、`HLT_xe110_pufit_xe70_L1XE50`、`HLT_xe120_pufit_L1XE50`；xe65 chain 自 run 350067 起 unprescaled。
- K以后：列 xe65 与 xe70 variants。

复合 chain 中 xe110_pufit 和 xe65/70 是不同 online 条件的组合，不是把两个数取最小值。

## 对本分析的核对清单

1. 对 data 用真实 run number，对 MC 用与 pile-up/random-run assignment 一致的 period；记录实际选中的 chain OR。
2. 按 analysis GRL 和实际 trigger 查 effective luminosity；“lowest”不保证每个 LB 都 unprescaled。
3. 用 light-lepton reference trigger 验证200/400 GeV analysis thresholds 的效率和 residual data/MC difference；[internal note](<{SRC}/ANA_EXOT_2025_06_INT1.pdf>) PDF 第28–29页已有 Eq.(6.2)、Fig.6.1。
4. TWiki 多处要求检查 `HLT_noalg_L1J400` 是否有分析相空间事件未通过 MET trigger。该建议已在2015第2页、2016第3页、2017第6页保存；需由实际 validation 结果确认是否完成。
''',tags='[trigger, MET, Run2, TWiki]')

write('20_Trigger','Run2_单轻子trigger与控制区',r'''
原始 menu 来源：[Atlas_LowestUnprescaled.pdf](<{SRC}/triggers/Atlas_LowestUnprescaled.pdf>)。本笔记列主要 single-lepton chain family，详细 OR、matching 与 SF 以本分析代码为准。

## Electron

- 2015（PDF 第77–78页）：`HLT_e24_lhmedium_L1EM20VH`、`HLT_e60_lhmedium`、`HLT_e120_lhloose`。24 GeV chain 的 L1 seed 选择与 prescale 有关；不能随意用 L1EM18VH variant 替代。
- 2016 A–D3（PDF 第70–71页）：主要低阈值为 `HLT_e24_lhtight_nod0_ivarloose`，另有 e60、e140、e300 high-$p_T$ chains。
- 2016 D4以后及2017（PDF 第71、61页）：低阈值改为 `HLT_e26_lhtight_nod0_ivarloose`，与 `HLT_e60_lhmedium_nod0`、`HLT_e140_lhloose_nod0` 等互补。
- 2018（PDF 第49页）：继续上述主要 family；`HLT_e26_lhtight_nod0` 自 run 349169 起 unprescaled。

run 298687 有 L1 autoprescaler 问题；TWiki 给出 e24 两条 chain 的 OR 用于恢复统计（PDF 第71页）。这是需要 run-dependent 处理的例子，不应把该 OR 无条件施加所有年份。

## Muon

- 2015（PDF 第78页）：`HLT_mu20_iloose_L1MU15`、`HLT_mu40`，另有 barrel MS-only高阈值链。
- 2016（PDF 第71–72页）：A 有 mu24 loose isolation family；B–D3 有 `HLT_mu24_ivarmedium`/`HLT_mu24_imedium` 与 mu50；D4–E 开始存在 mu26，mu24 会在高 luminosity 被 prescale；F以后 mu26 成为主要低阈值。
- 2017–2018（PDF 第61、49页）：`HLT_mu26_ivarmedium` 与 `HLT_mu50`，另有 `HLT_mu60_0eta105_msonly`。

## 为什么同一 lepton 类型需要多个 chain

低 threshold trigger 用较紧 ID/isolation 控制 rate；高 threshold chain 可放宽这些条件，补回高-$p_T$ signal 或 control sample 的效率。因此 OR 的 efficiency 不是单条 threshold 的阶跃函数，也不等于直接相加各条 efficiencies。

本分析 CRW/VRW 要求恰好一个 light lepton、无 tau；用 single-lepton trigger，$p_T^\ell>200$ GeV。electron 使用 HighPtCaloOnly isolation，muon 使用 Medium ID、Tight_VarRad isolation。[paper draft](<{SRC}/ATL-COM-PHYS-2026-015.pdf>) PDF 第25页 Table 3。CR 使用这些 leptons 替代 SR 中 tau，所以 trigger efficiency uncertainty 属于 CR→SR transfer 的一部分；不能因为离26 GeV阈值很远就把 plateau efficiency 假设为精确100%。
''',tags='[trigger, lepton, CR, Run2]')

if __name__=='__main__':
    print('Wrote theory and trigger notes')
