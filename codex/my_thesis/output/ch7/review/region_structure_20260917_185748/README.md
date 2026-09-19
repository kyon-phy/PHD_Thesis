# Chapter 7：SR1b 结构调整

## 内容与核对

- 7.2.1 保留 scan variables 和 optimisation criterion，随后展示 significance scan 及 MET distribution with significance。
- 7.2.2 和 7.2.3 分别介绍 SR1b-Res、SR1b-NonRes：selection → background composition → signal/background yield、Z 和 baseline-relative efficiency → cutflow → loose N−1 distributions。
- 原 interference 讨论移入 Appendix D，并根据 internal note 的 interference study 补充质量、耦合和灵敏度范围，避免将 5–10% 泛化到所有参数点。
- Res 和 NonRes 的约 12% 和 6% 来自原 cutflow 的 4.2/35.2 和 6.6/111.0；它们与以全部生成信号为分母的 acceptance times efficiency 分开说明。
- 背景比例统一为 pre-fit：Res 的 W+jets/diboson/ttbar/single-top 约为 64%/16%/8%/5%；NonRes 的 W+jets/ttbar/Ztautau/diboson 约为 69%/16%/8%/5%。计算输入为 `output/ch7/significance_validation/background_components.csv`。
- 原 pre-fit S/B/Z 汇总表逐字保留；拆分后的两张 cutflow 表逐项保留原数值。19 个被引用图文件的 SHA-256 均未改变，四个移动的 figure 环境也逐字保留。
- 本次改动范围之外的正文与操作前备份一致，仅更新 SR0b 对 Aε 定义的交叉引用。已复查本轮改写文字的被动语态、简单用词、符号和首次定义偏好。

## LaTeX 命令及版面变化

### 小节标题

删除以下两个旧标题及原 efficiency label：

```latex
\subsection{Interference and signal efficiency}
\label{subsec:ch7_efficiency}
\subsection{Selected regions and background composition}
```

改为分别对应两个 SR 的标题：

```latex
\subsection[SR1b-Res definition]{$\bTagSR$-$\Res$ definition}
\label{subsec:ch7_sr1b_res}
\subsection[SR1b-NonRes definition]{$\bTagSR$-$\NonRes$ definition}
\label{subsec:ch7_sr1b_nonres}
```

`\subsection` 自动生成 7.2.2/7.2.3；方括号中的纯文本用于目录等短标题，花括号中的宏用于正文标题。`\label` 不产生可见文字，供自动编号引用使用。原 SR0b 中的 `\ref{subsec:ch7_efficiency}` 改为 `\ref{subsec:ch7_sr1b_res}`，指向已移动的 Aε 定义。

### Cutflow 表格

```latex
% 原合并表
\begin{tabular}{lrrlrr}
\multicolumn{3}{c}{Resonant} & \multicolumn{3}{c}{Non-resonant} \\
% 两张独立表各使用
\begin{tabular}{lrr}
```

`lrrlrr` 的两个三列区块拆为各自的 `lrr`：selection 左对齐，S 和 B 右对齐。移除 `\multicolumn{3}{c}` 的跨列组标题，因为各表的 caption 和所在小节已标明 SR。两表仍使用 `\begin{table}[htbp]`、`\centering`、`\small` 和 booktabs 横线；`htbp` 允许当前位置、页顶、页底或浮动页，字号与原表一致。Caption 分别标明各自 benchmark，label 改为 `tab:ch7_cutflow_res` 和 `tab:ch7_cutflow_nonres`，正文引用同步更新。

### 图表顺序

```latex
\clearpage
```

在两个 SR 小节之前各新增一次：先排出等待中的浮动图表，再开始新页，从而使 significance 图位于分别介绍 SR 之前，Res 图位于 NonRes 小节之前。四个 figure 环境仅移动位置，原 `[htbp]`/`[p]` 参数、图片尺寸、caption 和文件均保留。原 SR0b 前的 `\clearpage` 保留。预览中 pre-fit 汇总表位于独立浮动页。

### 干涉附录

新增 `Chapters/Appendix/Appendix4.tex`：

```latex
\chapter{Signal--SM interference}
\label{app:signal_interference_study}
\section{Contribution to the selected signal yield}
\section{Effect of the kinematic requirements}
```

`\chapter` 在 appendices 环境内自动编号为 D；两个 `\section` 显示为 D.1 和 D.2。新的 label 供正文引用，替换原无效的 `app:Interference study` 引用。双连字符 `--` 在标题中显示为 en dash。

```latex
% thesis.tex
\include{Chapters/Appendix/Appendix4}
% output/ch7/CH7_preview.tex
\input{Chapters/Appendix/Appendix4}
```

`\include` 将附录纳入主论文，并按现有章节方式维护独立辅助文件及分页；`\input` 将同一源文件直接纳入 Chapter 7 预览。没有新增或重新定义物理公式。

## 验证

Chapter 7 预览已编译为 22 页，更新至 `output/pdf/CH7_draft.pdf`。已检查移动后的 significance 图、两个 SR 定义页、两组 loose N−1 图、pre-fit 汇总表及 Appendix D 的渲染。最终编译日志没有未解析引用、重复 label 或 overfull/underfull box；仍存在原模板的 bibliography、fancyhdr、hyperref 和 TikZ-Feynman 提示。本轮未重新编译完整 thesis.pdf。

操作前源文件位于 `before/`；最终逐行差异见本目录 `.diff` 文件，数值、文件哈希和范围检查见 `verification.json`。
