# 第七章 draft 完成说明

## 正文与 appendix

- **7.1**：先介绍分析变量及其物理作用，再解释 multijet suppression，最后用表格总结 optimisation 的 common preselection。
- **7.2**：沿用 Iguro/Endo 等人的高-mT、b-tag 和 jet multiplicity 逻辑，写出 SR1b 扫描变量表、significance 定义、signal efficiency 的分母、两个 benchmark 的保留率和最终选择，并插入 paper 中的两个 SR1b distribution。
- **7.3**：交叉引用第 3 章 beta_L23 与 s-tau coupling 的讨论，解释 SR0b、leading-jet 替代和总 jet multiplicity，插入两个 SR0b distribution，最后以一张表总结四个 SR。
- **Appendix B**：填充已有的 multijet study 占位文件，介绍模拟样本、二维 cut、rejection scan、96.4% signal retention 和残余 multijet 的证据边界，使用三张 INT 图。
- **Appendix C**：新建 SR0b optimisation appendix，收录 MET scan、600/400 GeV 最优点和约 20% 的 benchmark significance 改善。依照用户确认，正文保留 MET > 200 GeV 的理由是与 SR1b 对齐。

全部新增/删除行见 `review/CH7_draft.diff`。原有第七章只包含 chapter 和三个 section 标题，这些标题均已保留。Appendix B 删除的只有两条 TODO 注释。没有删除已写好的物理段落。

## 图表与排版命令说明

以下列出新增命令的实际写法及显示效果。同类命令在多处出现时合并说明，完整出现位置见 diff。

### 文档结构

```latex
\subsection{Analysis variables}
\subsection{Multijet suppression}
\subsection{Common preselection}
\subsection{Scan variables and optimisation criterion}
\subsection{Signal efficiency and selected regions}
\chapter{Zero-b-jet signal-region optimisation}
\include{Chapters/Appendix/Appendix3}
```

`\subsection` 在保留的 7.1/7.2 下生成编号小节。Appendix B 中的 `\section` 生成 B.1--B.4。新 `\chapter` 生成 Appendix C 的标题和编号。`thesis.tex` 新增的 `\include` 在独立页面开始 Appendix C，并生成单独的辅助文件。

### 变量解释与公式

```latex
\begin{itemize}
    \item \textbf{The transverse mass $\mT$} ...
\end{itemize}
\begin{equation} ... \label{eq:ch7_mt} \end{equation}
\begin{align} ... \nonumber\\ ... \end{align}
```

`itemize`/`\item` 将各变量分成条目，`\textbf` 使变量名成为醒目的开头。`equation` 显示带编号的单个公式。`align` 用 `&` 对齐两项定义或 significance 公式的两行；`\\` 换行，`\nonumber` 取消中间一行的重复编号。`\frac`、`\sqrt` 和自动伸缩括号分别排出分式、根号与适合公式高度的括号。`\text{...}` 在数学式中以直立文字显示 `or`/`and` 和 efficiency 分母。

`\label` 建立公式、图、表和章节的引用目标；`\ref` 按当前编号引用。`\cite` 使用已有 Iguro/Endo key 和新增的公开 significance reference，不写死参考文献编号。既有的 `\met`、`\mT`、`\pT`、`\MU`、`\SR`、`\bVetoSR` 等宏继续保留原定义。

### 表格

```latex
\begin{table}[htbp]
    \centering
    \small
    \begin{tabular}{lcccc}
        \toprule
        & \multicolumn{2}{c}{Resonant}
        & \multicolumn{2}{c}{Non-resonant} \\
        \midrule
        ...
        \bottomrule
    \end{tabular}
\end{table}
```

`table[htbp]` 允许表格放在当前位置、页顶、页底或浮动页。`\centering` 居中。较宽的 scan/SR/Appendix C 表使用局部 `\small`，不改变正文大小。`tabular` 的 `l` 表示左对齐、`c` 表示居中，分别采用 `ll`、`lcc`、`lccc` 或 `lcccc` 配合两至五列。`\multicolumn{2}{c}` 合并两个居中列，`{4}{c}` 合并四列共享的条件。`\toprule`、`\midrule`、`\bottomrule` 绘制表顶、表头分隔和表底横线。`&` 分列，`\\` 结束一行。

### 图片与图注

```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}{0.49\linewidth}
        \includegraphics[width=\linewidth]{Figs/CH7/SR1b_Res_InvM.pdf}
        \caption{$\SR$-$\Res$: $m_{b\tau}$.}
    \end{subfigure}\hfill
    ...
    \caption[Discriminating-variable distributions in SR1b]{...}
\end{figure}
\includegraphics[width=0.70\linewidth]{Figs/CH7/QCD/rejection_scan.pdf}
```

`figure[htbp]` 与表格采用相同的浮动位置选项。两个 `subfigure` 各占当前行宽的 49%，内部 `width=\linewidth` 将原 PDF 等比缩放到该子图宽度，`\hfill` 分配中间的剩余空间。子图 `\caption` 产生 (a)/(b) 标识。主图 `\caption[short title]{full caption}` 分别控制 List of Figures 的短标题和正文完整图注。单幅 QCD scan 使用 `width=0.70\linewidth`，即正文行宽的 70%。所有原始图文件均未修改。

### 独立阅读版

```latex
\documentclass[a4paper,12pt,times,numbered,oneside,custombib]{Classes/PhDThesisPSnPDF}
\input{Preamble/preamble}
\input{thesis-info}
\hypersetup{pdftitle={Chapter 7: Event Selection and Supporting Studies},pdfauthor={Jiaqi Zang}}
\usepackage{xr-hyper}
\externaldocument[][nocite]{output/ch7/CH7_external_labels}[../../thesis.pdf]
\mainmatter
\setcounter{chapter}{6}
\input{Chapters/CH7_event_selection}
\begin{appendices}
\setcounter{chapter}{1}
\input{Chapters/Appendix/Appendix2}
\input{Chapters/Appendix/Appendix3}
\end{appendices}
\begin{spacing}{0.9}
\bibliographystyle{unsrtnat}
\bibliography{References/references}
\end{spacing}
```

预览沿用 A4、12 pt、Times 和数字文献编号；`oneside` 避免仅为单双页规则产生空白页。两个前置 `\input` 沿用论文设置和作者信息，`\hypersetup` 只设置 PDF 元数据。`xr-hyper` 和 `\externaldocument` 导入七个所需的外部标签，`[nocite]` 避免导入整篇的引用编号，最后的方括号给出外部链接目标。

`\mainmatter` 使用正文页码。第一个 `\setcounter{chapter}{6}` 使下一个 chapter 为 7。`appendices` 切换到字母编号，第二个 `\setcounter{chapter}{1}` 使下一个 appendix 为 B，后一个自然成为 C。`\input` 直接读入可编辑源文件，不维护另一份正文副本。`spacing{0.9}` 仅收紧 References 的行距，`unsrtnat` 按引用顺序编号，`\bibliography` 从现有 bibliography 中抽取实际引用项。现有连续行号设置继续生效。

## 编译与核验

独立预览命令：

```bash
/Library/TeX/texbin/latexmk -norc -pdf -cd- -interaction=nonstopmode -halt-on-error -synctex=1 -outdir=output/ch7/build output/ch7/CH7_preview.tex
```

`-norc` 不加载个人 latexmk 配置，`-pdf` 生成 PDF，`-cd-` 保持论文根目录作为工作目录，`-interaction=nonstopmode` 将诊断写入日志，`-halt-on-error` 遇到实际错误停止，`-synctex=1` 生成源文件定位信息，`-outdir` 将辅助文件集中在预览 build 目录。

整篇的首次独立 outdir 编译受到根目录旧 `.aux`/`.bbl` 干扰，未完成引用解析。随后从当前 full-build `.aux` 运行 BibTeX，并在本次编译进程中优先搜索当前输出目录，解决该问题。没有更改全局 TeX 配置或删除原有辅助文件。

最终结果：独立阅读版 15 页，包含第七章、Appendix B、Appendix C 和两条参考文献。独立预览和整篇编译均完成，没有未定义引用、未定义文献或 overfull/underfull box。共享 preamble 原有的 hyperref PDF-string 和 tikz-feynman 引擎/兼容性提示仍存在。

数值、标签、引用 key、七份图片的源/目标 SHA-256 一致性均已检查。最终 PDF 全页渲染结果已检查，Appendix C 的末段孤页已通过删去重复说明和缩短标题消除。记录见 `review/validation.json`。源码出处和仍有来源限制的内容见 `CH7_source_notes.md`。
