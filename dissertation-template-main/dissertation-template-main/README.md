# My Dissertation Template
- 博士論文の作成に使用したLaTeXファイルから骨組だけを抜き出したものです。
- フォーマットは東京大学大学院理学系研究科物理学専攻における令和6年12月博士（理学）申請のものになります。

## 構成と用途
```
.
├── README.md
├── abstract
│   └── main.tex
├── cover
│   └── cover.tex
├── fig
├── slide
│   └── main.tex
├── spine
│   └── spine.tex
├── src
│   ├── abstract.tex
│   ├── acknowledgements.tex
│   ├── appendix.tex
│   ├── conclusion.tex
│   ├── introduction.tex
│   ├── main.bib
│   └── main.tex
└── sty
    └── common.sty
```
- `src/`
    - `main.tex`を親ファイルとしてChapter毎に分割された本文の作成
- `sty/`
    - `\usepackage`の簡略化のための`sty`ファイルの格納
- `fig/`
    - 図の格納
- `abstract/`
    - 論文の内容の要旨の作成
- `cover/`
    - 製本用の表紙の作成
- `spine/`
    - 製本用の背表紙の作成
- `slide/`
    - 審査スライドの作成

## 免責
- 本テンプレートの使用によって生じた損害や不利益について、作成者は一切の責任を負いません。