# CH6 分节草稿

- `CH6_draft.tex`：保留已确认的前言，通过 `\input` 整合九个 section，也是预览使用的章节入口。
- `sections/01_tracks.tex`：Tracks。
- `sections/02_primary_vertex.tex`：Primary vertex。
- `sections/03_electrons.tex`：Electrons。
- `sections/04_muons.tex`：Muons。
- `sections/05_hadronic_taus.tex`：Hadronic tau leptons。
- `sections/06_jets.tex`：Jets。
- `sections/07_flavour_tagging.tex`：Jet flavour tagging。
- `sections/08_overlap_removal.tex`：Overlap removal。
- `sections/09_missing_momentum.tex`：Missing transverse momentum。
- `CH6.txt`：展开全部 section 后的完整 LaTeX 文本，便于整章阅读、复制和编辑。
- `CH6_references.bib`：本章公开参考文献。
- `CH6_source_notes.md`：来源、版本取舍和配图出处。

建议逐节修改 `sections/*.tex`，修改后在项目根目录运行：

```bash
python3 output/ch6/assemble_ch6.py
```

此命令会用分节源文件重新生成 `CH6.txt`。直接编辑 `CH6.txt` 的内容不会自动同步回分节文件，因此重新生成前需要将这些修改放回对应 section。

编译阅读版：

```bash
/Library/TeX/texbin/latexmk -pdf -cd- -interaction=nonstopmode -halt-on-error -outdir=output/ch6/build output/ch6/CH6_preview.tex
```

本次交付的阅读版位于 `output/pdf/CH6_draft.pdf`。正式的 `Chapters/CH6_object_definition.tex` 尚未替换。
