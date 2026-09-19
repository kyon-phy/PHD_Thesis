# Top-quark background 术语统一

检查范围：`Chapters/` 下 32 个 LaTeX 文件（含附录和被包含文件），另检查摘要、致谢和导言区。相关统称共修改 23 处，涉及 3 个文件：

- `Chapters/CH8_Background_estimation.tex`：18 处。
- `Chapters/CH7_event_selection.tex`：3 处。
- `Chapters/object_definition/object_definition.tex`：2 处；该旧版对象定义文件当前未被主文档包含。

计数包含标题的方括号和花括号参数各一次。逐行增删见 `changes.diff`；其中仅记录本任务的修改，不包含同时发生的其他章节编辑。

## 术语与保留项

- `top background` → `top-quark background`。
- 表示合并背景的 `top-quark production`、`top-quark contribution`、`top prediction` 等统一采用 `top-quark background`。
- `The combined $\ttbar$ and single-top contribution` → `The top-quark background contribution`；该句明确指合并贡献。
- 分别讨论 `$\ttbar$` 和 single-top 的生成、衰变、比例和产额的内容保留；第七章 cutflow 中独立的过程列保留。第五章全文与本任务开始时一致。
- CRTop/VRTop 名称、宏、标签、图片路径和所有物理数值未因本任务改变。

## 修改的 LaTeX 命令

```latex
\section[Top-quark background estimation]{Top-quark background estimation}
\subsection[Top-quark background validation without a light lepton]{Top-quark background validation without a light lepton}
```

两条命令均只在原有标题文字中加入 `background`。方括号指定目录及相关导航使用的短标题，花括号指定正文标题；两处同步修改。章节层级和标签保持不变。渲染检查确认标题能正常放入版心。

编译发现并修正第八章首段的两处原有 LaTeX 问题：

```latex
\ref{CH7} → \ref{chapter:event_selection}
\tau → $\tau$
```

第一处使用第七章实际存在的标签，使引用显示正确章节号；第二处仅针对 `meaning that the ... lepton` 中的裸 `\tau`，添加数学模式定界符，消除 `Missing $ inserted` 编译错误。不涉及全局修改 `\tau`。

没有修改字号、行距、浮动体参数、表格列格式或图片尺寸。

## 验证

整篇论文经 pdfLaTeX、BibTeX、两次 pdfLaTeX 编译成功。该次构建生成 150 页。无未定义引用或 overfull 警告；原有模板、书签及参考文献 underfull 警告仍存在。已查看表 8.1 和两个修改标题所在页面，未见溢出或重叠。全章节未检出遗留的独立统称 `top background`。

验证用 PDF：`build/thesis.pdf`。旧的第八章独立预览未在本任务中覆盖。
