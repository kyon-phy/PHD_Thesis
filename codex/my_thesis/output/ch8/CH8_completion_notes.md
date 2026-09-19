# 第八章草稿完成说明

## 内容

第八章已由空提纲写成完整 LaTeX 草稿：背景约束策略、W+jets、top、fake-tau、nominal VRs 和 supplementary 1τ0l1b study。共 12 组图、57 张源图和 6 张表。

- 删除独立 Multi-jet cleaning 节；对象、变量、trigger 与 multijet cut 改用前文章节引用。
- 插入 48 张 CR/VR pre-fit N−1 子图，保留数据点、误差、选区箭头和 Data/Bkg 面板。CR 左右列分别为 e、μ。
- 纳入 Appendix D 的 ZVR 和 RNN 验证、Appendix F 的 e/μ difference、Appendix G 的局部 VR excess，以及 Appendix M 的 1τ0l1b 检查。
- 采用 paper 的约 70% CRW purity、30% W+HF/LF 不确定度及 Res/NonRes 去相关、up to 60% ZVR yield differences。今后冲突遵循用户明确确认的 paper 优先规则。
- 将 review 回复中 extra-neutrino extrapolation、inclusive top composition、single-top/ttbar ratio check 和 fake 方法选择的理由融入对应段落。

## 文件

主稿：`Chapters/CH8_Background_estimation.tex`。
图环境：`Chapters/background_estimation/figures_*.tex`，由主稿直接 input。
原图副本：`Figs/CH8/`。
独立预览入口：`output/ch8/CH8_preview.tex`。
具体来源和仍需代码确认的 ZVR mT 定义：`CH8_source_notes.md`。
逐行增删：`review/CH8_draft.diff` 与 `review/references.diff`。

## 排版命令逐项说明

### 章节和交叉引用

原来的

    \chapter{Background Estimation Strategy}

改为

    \chapter{Background Estimation}

显示章名改为 Background Estimation；原 `\label{chapter:background_estimation}` 保留，前文对第八章的引用继续有效。

删除

    \section{Multi-jet cleaning}

不再产生该小节标题和编号。`\section{VRs}` 改为 `\section{Validation regions}`；`\section{$\ttbar$ estimation}` 改为 `\section[Top-quark estimation]{Top-quark estimation}`，以涵盖共用归一化的 ttbar 与 single-top。其他空节被相应正文填充。

新增 `\subsection{...}` 为 WCR definition、pre-fit comparison、e/μ study 和各个 VR study 自动编号。带数学符号的标题使用 `\section[纯文本标题]{显示标题}` / `\subsection[纯文本标题]{显示标题}`，方括号提供目录和书签文本。

`\label{...}` 为图、表和小节定义唯一引用；`\ref{...}` 自动显示编号。`\input{Chapters/background_estimation/figures_wcr}` 等七条 input 在当前位置插入图环境，便于独立编辑图注。

### 图组

六图组采用：

    \begin{figure}[p]
    \centering
    \begin{subfigure}{0.47\linewidth}
        \includegraphics[width=\linewidth]{Figs/CH8/...pdf}
        \caption[]{...}
    \end{subfigure}\hfill
    ...
    \end{subfigure}\par\medskip
    \caption[短标题]{完整图注}
    \label{fig:ch8_...}
    \end{figure}

- `[p]` 允许专用浮动图页。`\centering` 居中。
- `subfigure` 宽度为正文行宽的 47%，两列排布；`includegraphics[width=\linewidth]` 在各子图中等比例填满宽度。调整显示尺寸，不修改图内 histogram。
- `\hfill` 分配左右图间隔；`\par\medskip` 在每两图后换行并增加适度行距。
- 子图 `\caption[]{...}` 产生 (a) 等标号；空方括号避免子图独立进入图目录。
- 主 `\caption[短标题]{完整图注}` 将简短名称用于图目录，保留完整图注中的区域、pre-fit 状态和误差定义。
- ZVR 的单图使用 `width=0.80\linewidth`。ZVR 图使用 `[!htbp]`：允许当前位置、页顶、页底或浮动页，`!` 放宽浮动比例限制，便于相邻诊断图共页。
- 局部 VR 研究的两图组使用 `[htbp]`，允许与解释文字共页。

`\clearpage` 放在图组结束、开始下一主题之前，输出尚未排出的图表，避免它们漂移到下一节。

### 表格

所有新增表采用：

    \begin{table}[htbp]
    \centering
    \small
    \caption{...}
    \label{tab:ch8_...}
    \begin{tabular}{...}
        \toprule
        ...
        \midrule
        ...
        \bottomrule
    \end{tabular}
    \end{table}

- `[htbp]` 允许标准浮动位置。`\small` 仅缩小当前表内字体，保证选择和数值列容纳在正文宽度内。
- `tabular{lcccl}` 用于区域用途表，`{lcc}` 用于 WCR/VRW 与 1τ0l1b 表，`{lrrrr}` 用于 e/μ 并列 CR counts，`{lcccc}` 用于 TopCR/TopVR，`{llrr}` 用于 VRW yields。`l/c/r` 分别为左/中/右对齐。
- `\multicolumn{2}{c}{...}` 等将相邻列合并并居中，表示共享条件或通道分组。
- `\toprule`、`\midrule`、`\bottomrule` 分别绘制顶线、分组线和底线；`\\` 结束表行。
- `---` 表示没有该项要求。质量区间使用明确上下限，且在列标题注明 GeV。

### 独立预览与引用

    \documentclass[a4paper,12pt,times,numbered,oneside,custombib]{Classes/PhDThesisPSnPDF}
    \usepackage{xr-hyper}
    \externaldocument[][nocite]{output/ch8/CH8_external_labels}[../ch8/full_build/thesis.pdf]
    \mainmatter
    \setcounter{chapter}{7}

沿用论文类、A4、12pt 和 Times。`oneside` 使预览不插入双面装订空白页。`xr-hyper` 和 `externaldocument` 读取当前整篇编译得到的前文章节标签；`[nocite]` 不导入其他章节的文献列表。`mainmatter` 使用正文页码；章计数先设为 7，使随后 `\chapter` 自动产生 Chapter 8。

    \begin{spacing}{0.9}
    \bibliographystyle{unsrtnat}
    \bibliography{References/references}
    \end{spacing}

预览末尾仅列本章引用的三篇原始公开文献。参考文献局部使用 0.9 行距，按出现顺序编号。整篇 thesis 的全局字体、行距和章节输入顺序未改。

正文新增 `\cite{PMGR-2021-01,STDM-2018-43,HIGG-2020-20}`，对应原始公开研究，不引用自己的 INT note、paper 或评审回复。

## 数值与编译验证

- 57 张目标 PDF 与 source SHA-256 一致，未改动原始分析图。
- 主稿、七份 figure include 的图引用、标签和所有图片路径均检查。
- 编译与渲染的最终结果记录在 `review/validation.json`。
- 原图包含其历史配色和区域标签，未将数值不一致的后期 paper-style EPS 混入本章。图注解释 VR0tau 与 VRW 的名称对应。
- ZVR 的横质量对象定义仍需核对实现代码，草稿没有补造定义。
- 最终独立预览共 21 页（含本章参考文献），整篇集成编译共 148 页。本章没有未定义交叉引用、缺失文献引用、overfull/underfull box 或过大浮动图警告；全部预览页面已渲染检查。
- 编译仍有共用模板的类选项、页眉、PDF 元数据和 TikZ-Feynman 提示；整篇参考文献中仍有本章之外的 underfull box 警告，未作为本章改写范围处理。

## 2026-09-16：写作偏好修订

已按后续核查落实被动语态、节首主题、主语/指代、四处重复句、已有宏、一处分号及 ZVR 图注精简。最新预览仍为 21 页，当前整篇编译为 146 页。全部数值、选择条件、图片路径及引用保留。

本轮逐行修改及每个变更命令的显示效果，见 `review/2026-09-16_preferences/revision/changes.diff` 和 `CH8_revision_notes.md`。
