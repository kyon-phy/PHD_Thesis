# 第七章修订说明

## 修改结果

7.1 改为连续段落，保持 variables → multijet suppression → baseline 顺序；baseline 合并进 Table 7.3，删除单独 preselection 表和重复 WP 介绍。7.2 增加 cutflow、signal efficiency 和 interference 说明，Eq.7.5 改为单行 Z=平方根，删除原 Eq.7.6。SR1b 插入 12 张 loose N−1 图，SR0b 两张图同步更新，全部去除 data。两个类别均补充背景组成与具体过程。

7.3 加入 Chapter 12 的 s/c-jet 与 cν resonance 研究；MET=200 GeV 对齐 SR1b 的理由保留。7.4 新增 Tau-pair signal contamination，说明截面缩放的适用范围、额外信号因子和 coupling-limit 影响。Appendix B/C 同步更新。图片与单行公式偏好已存入 memory extension note。Favoured-region 计算已追加到 Obsidian 现有笔记。

本次逐行增删见 review/CH7_revision.diff，比较基准为上一份完整草稿。修订前版本保存在 review/revision_20260915_before/。

## 排版命令逐项说明

### 列表与公式

删除以下命令，取消项目符号、列表缩进和变量开头的加粗，改为普通段落：

    \begin{itemize}
    \item \textbf{...}
    \end{itemize}

可见质量定义由 align 改为单个 equation，用 \qquad 分隔同一行的两个定义，删除 & 对齐列。显示内容仍为两个四动量不变量。

Eq.7.5 由 align 改为 equation，删除 \nonumber\\ 强制换行，使用：

    Z = \sqrt{2\left[n\ln\!\left(\frac{n(b+\sigma_b^2)}{b^2+n\sigma_b^2}\right)-\frac{b^2}{\sigma_b^2}\ln\!\left(\frac{b^2+n\sigma_b^2}{b(b+\sigma_b^2)}\right)\right]},

\sqrt 对右侧开方；\left/\right 调整括号大小；\! 收紧 ln 后间距。原 eq:ch7_optimisation_significance 标签保留，编号仍为 7.5。删除原 relative-efficiency 的 equation 和 label，不再产生 Eq.7.6。Appendix B 用源公式的 \text{Rejection ratio} 替代 f_rej 名称，整式保持单行。

### 小节和分页

修改/新增：

    \subsection{Interference and signal efficiency}
    \subsection{Selected regions and background composition}
    \clearpage
    \section[b-veto signal region definition (SR0b)]{...}
    ...
    \clearpage
    \section{Tau-pair signal contamination}

subsection 提供 7.2 内的编号标题。clearpage 在进入 7.3/7.4 前输出待排图表并换页，避免图表进入下一 section 后才显示。新 section 生成 7.4。主章、appendix 引入、全局字体和行距命令未变。

### 表格

新增 cutflow 使用：

    \begin{table}[htbp]
    \centering
    \small
    \begin{tabular}{lrrlrr}
    \multicolumn{3}{c}{Resonant} & \multicolumn{3}{c}{Non-resonant} \\

htbp 允许当前位置、页顶、页底或浮动页；small 只缩小表内文字。lrrlrr 是两个“左对齐 cut + 右对齐 S/B”列组；multicolumn{3}{c} 合并每组三列居中放置标题。

Table 7.3 新增：

    \multicolumn{5}{c}{Baseline requirements} \\
    Trigger & \multicolumn{4}{c}{...} \\

第一行合并五列作 baseline 标题，共用条件合并后四列；midrule 分隔 baseline 与 SR。原 lcccc 格式保留。原独立 preselection 的 table、tabular{ll}、caption 和 label 删除，其条件并入 Table 7.3。

ττ 表采用 tabular{lcc}，region 左对齐，贡献与乘数居中。toprule/midrule/bottomrule 沿用现有表格横线；新增 caption/label 负责自动编号与交叉引用。

### 图片

SR1b 每组六图使用：

    \begin{figure}[p]
    \begin{subfigure}{0.49\linewidth}
    \includegraphics[width=\linewidth]{Figs/CH7/SR1b_Res_InvM.pdf}
    \caption{...}
    \end{subfigure}\hfill
    ...
    \end{subfigure}\par\medskip
    \caption[Loose N-1 distributions in SR1b-Res]{...}

[p] 将六子图放到浮动图页。每幅宽度为行宽 49%；includegraphics 等比缩放，不改变图内比例。hfill 分配两列间距，par/medskip 每两图换行并留适中间隔，形成两列三行。子图 caption 生成 (a)–(f)，主 caption 的方括号给图目录短标题，花括号给完整条件。SR0b 保留 [htbp] 两图结构，只替换 PDF 和图注。

### 图内 EPS/PDF 命令

- BoundingBox 改为 0 65 567 407，裁去下方 panel 和空白，图宽/纵轴映射不变。
- .25 .25 scale 保留。gsave 0 259 t ... grestore 仅平移原 x 轴标签，不作用于 histogram。
- sqrt(s) 和 region 分别按原行距平移；字符字体和间距保留。
- 删除 data markers/error bars、Data legend、ratio panel、ATLAS 状态行与旧 fit 注释。
- dphi/njet 纵轴改为 Events，移除错误 GeV 单位而不缩放 yield；phi 字符改为小写。
- QCD 用 PDF re W n 裁剪标签区、cm 平移原标签像素。原 Im1 图像字节不变，白色遮盖只在旧标签区。

### 预览

CH7_external_labels.aux 新增 Chapter 5、interference equation、Chapter 8 的标签记录。xr-hyper、externaldocument、章节计数、字体和行距命令均未变。

## 验证

当前章节预览共 19 页，包括 Chapter 7、Appendix B/C 和参考文献。MacTeX/latexmk 编译通过，无未定义引用、未定义文献或 overfull/underfull box。共享模板的 class、bibliography 选择、单面 fancyhdr、hyperref PDF-string 和 tikz-feynman 提示仍存在。

14 张 SR 图的受保护绘制指令 hash 一致；QCD 标签区域以外像素差为零。数值与图形验证见两个 figure manifest，最终渲染记录见 review/validation.json。本次重新验证章节预览，不将上次整篇 build 冒充为本次检查。

ττ 原表的 beta 标注不一致等来源边界见 CH7_source_notes.md。正文使用明确的 supplementary-fit 因子与适用范围，未补造缺失结果。
