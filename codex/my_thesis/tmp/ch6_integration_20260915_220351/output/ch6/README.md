# CH6 分节草稿

- `CH6.tex`：章节入口，仅保留前言和九条 `\input`。
- `objects/tracks.tex`：Tracks。
- `objects/primary_vertex.tex`：Primary vertex。
- `objects/electrons.tex`：Electrons。
- `objects/muons.tex`：Muons。
- `objects/taus.tex`：Hadronic tau leptons。
- `objects/jets.tex`：Jets。
- `objects/btagging.tex`：Jet flavour tagging。
- `objects/overlap_removal.tex`：Overlap removal。
- `objects/met.tex`：Missing transverse momentum。
- `CH6_references.bib`：本章公开参考文献。
- `CH6_source_notes.md`：来源、版本取舍和配图出处。

直接编辑对应的 `objects/*.tex`，编译时会自动读入。例如 `CH6.tex` 中：

```latex
\input{output/ch6/objects/muons}
\input{output/ch6/objects/met}
```

使用 `\input` 可保持各节连续排版，避免 `\include` 自动分页。无需执行合并脚本。

编译阅读版：

```bash
/Library/TeX/texbin/latexmk -pdf -cd- -interaction=nonstopmode -halt-on-error -outdir=output/ch6/build output/ch6/CH6_preview.tex
```

本次交付的阅读版位于 `output/pdf/CH6_draft.pdf`。正式的 `Chapters/CH6_object_definition.tex` 尚未替换。
