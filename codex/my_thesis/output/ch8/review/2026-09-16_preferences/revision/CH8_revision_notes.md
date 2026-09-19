# 第八章：按 writing preference 核查结果修改

2026-09-16。用户已授权将上一轮核查发现的问题写回原文。本轮按明确的八类问题进行局部修改，不重新开展章节结构或物理方法改写。

## 已落实的修改

- **主语与条件：** `The jet multiplicity satisfies ...` 改为 `Events are required to satisfy ...`，使 jet multiplicity 和 tau momentum 两个条件都由 events 支配。
- **指代：** `It describes the fake-...` 改为 `This additional uncertainty describes the fake-...`，明确它指额外不确定度。
- **程序性被动表达：** CR 总计数作为 fit input、combined top yield 的约束、ZVR trigger 选择及 supplementary VR 的 post-fit yield，均按核查建议修改。
- **节首主题：** top 节以待估计的 top backgrounds 为主语；fake 节以 fake contribution 为主语，保留原因果关系。
- **重复内容：** 删除 inclusive sample 解释收尾、fake 不设为零的重复句、VR 不进入拟合的重复句及 benchmark 范围的重复收尾，共四句。相应事实仍由附近正文或 strategy 明确表达。
- **宏：** 全章及相关图注统一使用已有的 `\mT`、`\wlnu`、`\wtaunu`、`\znunu`、`\zll`、`\wjets` 和 `\zjets`。
- **标点：** WCR/VRW 表注中的分号拆为句号。
- **图注：** 删除 ZVR tau momentum 图注末尾重复正文的 high-pT overprediction 解释。图中条件和阅读说明保留。

核查中标为“可按语境调整”的其他主动句没有机械改为被动句。关于额外中微子、b veto 和高权重 MC 事件的直接因果说明保持自然的主语连续性。

## 代表性的逐句变更

```latex
% Before
Each region contributes its total event count to a simultaneous fit.
% After
The total event count in each CR is used in a simultaneous fit.

% Before
The fit constrains the combined top-quark yield, while the relative $\ttbar$ and single-top contributions are predicted separately in each region.
% After
The combined top-quark yield is constrained by the fit, while the relative $\ttbar$ and single-top contributions are predicted separately in each region.
```

完整逐行删改见同目录的 `changes.diff`；修改前文本保存在上一层 `snapshot/`，原 PDF 保存在 `before/output/pdf/`。

## 修改的排版命令及显示效果

以下列出本轮所有命令层面的变化，不涉及新宏定义。

```latex
% Before -> After
$m_{\mathrm{T}}^\ell$ -> $\mT^\ell$
$W\to\ell\nu$      -> $\wlnu$
$W\to\tau\nu$      -> $\wtaunu$
$Z\to\nu\nu$       -> $\znunu$
$Z\to\ell\ell$     -> $\zll$
$W$+jets            -> $\wjets$
$Z$+jets            -> $\zjets$
```

- `\mT` 展开为 `m_{\mathrm{T}}`，保留 `^\ell` 上标，用于正文、选择表和 WCR/VRW 子图标题。
- 四个衰变过程宏分别展开为相同的粒子与轻子组合，使用 preamble 统一的 `\rightarrow`；它与原 `\to` 表示相同箭头。
- `\wjets`、`\zjets` 分别展开为 `W+\mathrm{jets}`、`Z+\mathrm{jets}`。`jets` 使用正体，加号采用数学模式的标准间距；可能带来轻微换行变化，但不改变过程含义。
- 上述宏已有 `\ensuremath` 与 `\xspace`，分别管理数学模式和文本后间距。preamble 本身未修改。

标题中同步使用上述宏：

```latex
\section[W+jets estimation]{$\wjets$ estimation}
\subsection[Validation with Z dilepton events]{Validation with $\zll$ events}
```

方括号内短标题保留原文，用于目录与导航；花括号内显示标题改用统一宏。章节级别和标签不变。

图注继续使用 `\caption[short title]{full caption}` 和 `\caption[]{...}`。本轮只缩短 ZVR 图的完整图注、替换相关图注中的宏，并将一处表注分号改成句号；短标题、子图编号和图注机制不变。

图尺寸、浮动位置、表格列格式、分页命令及全局字体/行距均沿用原设置。`scripts/ch8/prepare_source_figures.py` 同步更新了横质量宏与 ZVR 图注，避免将来重建 include 时恢复旧文本。独立预览使用的外部标签由最新整篇编译结果刷新，未更改 `\externaldocument` 命令。

## 验证

- 修改前后全部数值 token 的顺序一致；labels、交叉引用、citations 和图片路径保持一致。
- 正文四处重复句及不清楚的原句已移除，七类旧宏展开均已替换。
- 57 张原始图的 SHA-256 再次核对，数值和图形文件未修改。
- 本章预览与整篇集成编译均成功；预览 21 页，当前整篇 146 页。无本章未定义引用、overfull/underfull box 或过大浮动图警告。
- 共用模板提示和整篇参考文献中的既有 underfull box 警告仍存在。
- 最新渲染页面的检查结果补充在同目录 `checks.json`。

原有 ZVR transverse-mass 对象定义及未取回全文的原始参考文献问题仍按 source notes 保留，没有通过行文修改补造事实。
