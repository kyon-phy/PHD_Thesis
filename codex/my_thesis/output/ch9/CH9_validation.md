# 第九章草稿验证

日期：2026-09-19。

## 交付内容

- 正文：`Chapters/CH9_Systematics_uncertainties.tex`，约 4,200 词，正文 12 页。
- 独立预览：`output/ch9/build/CH9_preview.pdf`，14 页（正文 12 页、参考文献 2 页）。
- 整篇编译：`output/ch9/full_build/thesis.pdf`，162 页；第九章在 PDF 第 127–138 页，对应正文页码 111–122。
- 来源与冲突记录：`output/ch9/CH9_source_notes.md`。
- 逐行差异：`output/ch9/CH9_Systematics_uncertainties.diff`、`output/ch9/references.diff`；修改前文件保存在 `output/ch9/before/`。

## 内容与引用检查

- 章节顺序沿用 INT note；发生冲突时依照本次要求采用 paper > INT > Obsidian。具体取舍及实现边界均记录在来源说明中。
- 正文共引用 26 项公开来源，所有 bibliography keys 均存在；本次新增 12 项 bib entries。
- 18 个外部 labels 引用已有章节内容；独立预览仅导入这些 labels，参考文献独立编号。
- 6 个编号公式和 1 张数值表；表中的数值为 INT 的 SR1b transfer-factor variations，明确标示为 symmetrisation 前的结果。
- 未修改 CH5、CH6、Obsidian vault 或参考资料。
- Tau Tight/Medium SF 与最终生产版本的对应关系，以及 signal/interference 的逐点 uncertainty 配置仍需最终产物确认；未声称已完成该项生产复现。

## 编译检查

使用本机 TeX Live 2025 的 `latexmk`/pdfLaTeX，两个目标均完成编译，返回成功。

```sh
/Library/TeX/texbin/latexmk -norc -pdf -cd- -interaction=nonstopmode -halt-on-error -synctex=1 -outdir=output/ch9/full_build thesis.tex
/Library/TeX/texbin/latexmk -norc -pdf -cd- -interaction=nonstopmode -halt-on-error -synctex=1 -outdir=output/ch9/build output/ch9/CH9_preview.tex
```

最终两份 `.log` 均无未定义 citation/reference、重复 label 或 overfull box。独立预览无 underfull box；整篇有 3 条既有 bibliography underfull hbox，均位于 NNJVT calibration-file URL 对应的段落。

仍有项目模板产生的非致命警告：class 路径名称、bibliography option conflict、已有 PDF metadata/标题的数学 token、pdfLaTeX 下 TikZ-Feynman 的 LuaTeX/compat 提示；独立预览还有 `oneside` 下 fancyhdr 偶数页选项提示。整篇还提示未生成 `thesis.nls`。本次未为消除这些已有警告修改全局模板。

完整编译输出：`output/ch9/compile.log`、`output/ch9/preview_compile.log`。

## 视觉检查

独立预览全部页面已渲染检查；最终表格分页与参考文献布局调整后，又复查第 11–14 页。表格与后续说明连续排列，公式、caption 和参考文献均无裁切或重叠。另检查整篇 PDF 中第九章表格页的双面页眉与布局。

这是来源核对、静态检查、编译和视觉检查的记录；没有执行或声称执行独立 reader-agent 审稿，也没有重新生成分析的 systematic variations。
