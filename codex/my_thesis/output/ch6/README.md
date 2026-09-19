# 第六章源文件与预览

正文已整合到正式论文目录：

- `Chapters/CH6_object_definition.tex`：章节入口，已由 `thesis.tex` 引用。
- `Chapters/object_definition/*.tex`：可编辑的 object 正文；`met.tex` 包含 MET 和对象定义汇总表。
- `Chapters/object_definition/object_definition.tex`：原有的未启用定义文件，仍未参与编译。
- `Figs/CH6/`：当前正文使用的三张图。
- `References/references.bib`：主论文及各局部预览使用的参考文献库。

`output/ch6/CH6.tex` 和 `output/ch6/objects/*.tex` 只保留转发入口。后续请编辑上面的 `Chapters/` 源文件。
`CH6_source_notes.md` 保留来源和历史记录；`CH6_references.bib` 与 `figures/` 保留原始素材副本。

从论文根目录编译 MET 局部预览：

```bash
/Library/TeX/texbin/latexmk -norc -pdf -cd- -interaction=nonstopmode -halt-on-error -synctex=1 -outdir=output/ch6/build output/ch6/MET_preview.tex
```

输出为 `output/ch6/build/MET_preview.pdf`。
需要整章预览时，将命令中的 `MET_preview.tex` 换为 `CH6_preview.tex`；正文会直接从 `Chapters/` 读取。
