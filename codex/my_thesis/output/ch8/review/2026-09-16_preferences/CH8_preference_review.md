# 第八章 writing preferences 执行核查

核查日期：2026-09-16。对象为当前第八章全部 29 个正文段落、6 张表及七份 figure include 中的图注。此轮为 review-only；以下替换均为建议，未写回正文或重新生成 PDF。

## 结论

上一轮没有完整落实写作偏好。主要遗漏是：实验步骤的被动语态与主题位置、局部主语/指代、重复限定、已有 LaTeX 宏，以及一处分号。它们应与物理错误区分：被动语态是用户明确的行文偏好，不是主动句在科学上错误。

依据为当前 [academic-writing-pipeline skill](/Users/zang/.codex/skills/academic-writing-pipeline/SKILL.md:64) 与 [thesis-writing skill](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/.agents/skills/atlas-u1-thesis-writing/SKILL.md)。前者明确要求：

> Prefer passive constructions when describing physical and experimental facts or procedures, where natural and scientifically accurate.

该规则还有两个必要条件：维持段落话题连续性；保留自然、准确的物理因果关系。因此不使用“被动句比例”判断是否合格，也不建议把全部主动句机械改成被动句。

## 1. 主语与条件没有正确对应

位置：[第 206 行](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/Chapters/CH8_Background_estimation.tex:206)。

原句：

```latex
The jet multiplicity satisfies $1\leq N_j\leq3$ and $\pT^\tau>100~\GeV$.
```

句法上，jet multiplicity 同时支配了两个条件，但第二项是 tau 的动量条件。这比一般风格偏好更需要修正。

建议：

```latex
Events are required to satisfy $1\leq N_j\leq3$ and $\pT^\tau>100~\GeV$.
```

中文回核：事件须满足 jet 数目和 tau 动量两个要求；没有改变阈值或增加选择。

## 2. 不确定度的指代不够清楚

位置：[第 228–229 行](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/Chapters/CH8_Background_estimation.tex:228)。

前一句以 `because this background is small` 结束，随后 `It describes the fake-tau modelling ...` 的 `It` 实际指 additional uncertainty，容易被误读为 background 或 change。建议只将句首 `It` 改为 `This additional uncertainty`，保留后半句对 genuine-tau uncertainties 的区分。

这里重复 uncertainty 是为了消除歧义，不违背“先行词清楚时优先代词”的偏好。

## 3. 实验步骤没有充分采用自然的被动表达

以下为明确值得调整的例子。位置均指当前主稿。

### 第 13 行：拟合输入

```latex
% Original
Each region contributes its total event count to a simultaneous fit.
% Suggested
The total event count in each CR is used in a simultaneous fit.
```

将实际拟合输入放在句首，仍然是每个 CR 的总计数。

### 第 186 行：top yield 的约束

```latex
% Original
The fit constrains the combined top-quark yield, while the relative $\ttbar$ and single-top contributions are predicted separately in each region.
% Suggested
The combined top-quark yield is constrained by the fit, while the relative $\ttbar$ and single-top contributions are predicted separately in each region.
```

主语回到本节正在讨论的背景产额，保持总量约束与相对组成的区别。

### 第 208 行：trigger 选择

```latex
% Original
The muon channel uses the $\met$ trigger, whereas the electron channel uses a single-electron trigger.
% Suggested
In the muon channel, events are selected using the $\met$ trigger, whereas a single-electron trigger is used in the electron channel.
```

表达具体的事件选择步骤，保留两个 lepton channel 的差别。

### 第 352 行：post-fit 产额

```latex
% Original
The CR fit then predicts $25.4\pm1.5$ and $8.0\pm1.7$ background events, compared with 24 and 9 observed events.
% Suggested
Background yields of $25.4\pm1.5$ and $8.0\pm1.7$ events are predicted after the CR fit, compared with 24 and 9 observed events.
```

把比较对象放在句首，数值、顺序及 pre-/post-fit 属性保持不变。

第 54、61、155–157、204、216、245、284、324 行也包含可按段落语境调整的程序性主动表达，但没有必要逐句改成相同句式。尤其应保留合理的主动因果句，例如第 65 行关于 tau 衰变中微子改变可见动量和 missing momentum 的解释，以及第 134 行关于高权重 MC 事件改变 yield 的说明。

## 4. 两处 section 开头的主题还可以更准确

### Top-quark estimation，第 146 行

本节主题是 top 背景估计，当前以 CRTop regions 为主语。建议把受约束的背景放在句首，同时采用被动表达：

```latex
The $\ttbar$ and single-top backgrounds are constrained in the $\CRTop$ regions, which require one $\tau$ and an additional electron or muon.
```

### Fake-tau estimation，第 195 行

当前以整个 selected SM background 开始，到后半句才出现 fake contribution。建议：

```latex
The fake-$\tau$ contribution is small because the selected SM background is dominated by events containing a genuine hadronically decaying $\tau$.
```

这只是主题顺序调整，仍然保留“真 tau 背景占主导，因此 fake 很小”的因果关系。其余小节开头大体能够直接引出所讨论的对象，无需统一重写。

## 5. 部分限定说明重复，带有解释写作取舍的语气

- **第 152 行** `This explains the dominant modes identified above without restricting the prediction to those modes.` 前两句已经明确 inclusive samples 和大 MET 对衰变组成的影响，建议删除这句收尾说明。
- **第 198 行** `It is retained in the prediction rather than set to zero.` 紧接着第 199 行已经说明 nominal yield 来自 simulation，后文又给出额外 100% uncertainty。建议删除第 198 行，保留估计方法和不确定度。
- **第 240 行** VR observations 不进入约束，已在第 25 行说明。可以删除该重复句，同时保留第 239 行新增的 pre-fit/post-fit 用途区分。
- **第 297 行** `... for the stated benchmarks rather than for arbitrary signal couplings.` 第 295–296 行已将具体 benchmark 与对应 contamination 紧密连接。建议删除这句额外的防御性限定，保留 benchmark 本身。

不建议删掉真正约束结论范围的内容：第 100 行 raw data/MC 不等于 fitted W normalisation、第 197 行 fake 份额的适用范围，以及第 354 行 supplementary study 未加入额外 mass-window uncertainty，均有必要。表格与解释段中适度重复关键数值也不自动算冗余。

## 6. 已有 LaTeX 宏没有统一沿用

当前 [preamble](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/Preamble/preamble.tex:219) 已定义对应宏；主稿和部分子图标题仍手写展开。建议的等义替换为：

- `m_{\mathrm{T}}^\ell` → `\mT^\ell`，如第 61、84 行及 WCR/VRW 子图标题。
- `W\to\ell\nu` → `\wlnu`，如第 54 行。
- `W\to\tau\nu` → `\wtaunu`，如第 67 行。
- `Z\to\nu\nu` → `\znunu`，如第 196、211、226 行。
- `Z\to\ell\ell` → `\zll`，如第 199、201 行。
- 常见过程 `$W$+jets`、`$Z$+jets` 也应检查是否统一使用既有 `\wjets`、`\zjets`，而非在本章另写展开。

这些宏定义通过 `\ensuremath` 支持数学模式，`\xspace` 处理文本后间距；它们集中管理同一物理符号的排版。建议不会改动物理量、上标或数值，也不需要新增宏。此轮未执行替换，未更改版面命令。

## 7. 一处分号遗漏

位置：[第 74 行表注](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/Chapters/CH8_Background_estimation.tex:74)。

```latex
% Original ending
... the tagged jet in $\VRb$; its momentum is denoted by $\pT^J$.
% Suggested ending
... the tagged jet in $\VRb$. Its momentum is denoted by $\pT^J$.
```

草稿中的 `80--100` 等数值区间和 `Electron--muon` 等关系标记不按“避免 prose dash”的规则机械删除。

## 8. 图注的解释性收尾可以缩短

[figures_fake.tex 第 4 行](/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/Chapters/background_estimation/figures_fake.tex:4) 的末句 `The high-... prediction exceeds the observed yield.` 重复主稿第 218 行的图形解读。依据本地写作指南“图注描述、主要解释留在正文”的规则，可删去图注末句，保留图中变量、N−1、阈值和 ratio panel 的说明。这是次要精简项，不是图注不完整。

## 已执行的偏好与不应误报的项目

- 未检出 `account for`、`approach`、`exploit`、`subsequently`、`associate with`、`relative to` 或独立单词 `content` 的禁用表达。
- 使用 British English，例如 normalisation、modelling、flavour、favours、localised。
- 主图均使用 `\caption[short title]{full caption}`，短标题没有 citation；子图 `\caption[]{...}` 不单独加入图目录。
- 正文没有自引 INT、对应 leptoquark paper 或 review replies。三条公开原始文献在同一处引用，没有近邻重复 citation。
- CR/VR 的缩写没有在前文完成定义，此章展开可以保留；SR 和 RNN 已在前文定义，本章未重新展开。
- N−1、对象定义、SR 选择和 multijet suppression 使用前文交叉引用。第七章 fake 组成在本章保留一行提示是为了引出 ZVR 方法，不需要再增加相同机制的说明。
- 29 个段落中没有连续多句机械地以 `It` 起头，也没有 `itemize`；后者的 bold-label 主语规则不适用。
- 当前正文采用 paper 的 CRW purity 约 70% 和 W HF/LF uncertainty 30%；Res/NonRes 去相关在 journal reply 中明确说明。skill 中仍写 INT priority 的旧句子被用户本轮更高优先级的指令覆盖，不应当以该旧句判定草稿执行错误。

## 原有记录中的边界

- 前次数值、图片和编译验证不能代表这次行文偏好核查已经完成。现有来源记录有助于追溯取舍，但不能代替逐段语言检查。
- 图样式仍保留 INT 原样，尚未统一为 paper 的配色和标签；这是上一轮已披露的图形工作，不在本次只读语言核查中改动。
- Appendix D 的 ZVR transverse-mass 对象定义、未取回全文的 ATL-PHYS-PUB-2017-006，仍保留在原有 source notes。此轮没有将它们报告为已解决。

## 验证范围

本轮覆盖全部正文段落、表内文字和图注，并核对前文章节中的定义、preamble 宏及 paper 对已决定冲突的表述。没有重新运行模拟、拟合、数值分析、PDF 编译或独立 reader review；这些不是此次语言偏好核查完成的前提。全部正文建议保持原数值和物理条件，未对原来的来源核对作全面重新认证。

与本报告同目录的 `review_manifest.json` 保存当前文本快照、逐段论证用途、来源检查、问题位置及最终文件 hash 验证。
