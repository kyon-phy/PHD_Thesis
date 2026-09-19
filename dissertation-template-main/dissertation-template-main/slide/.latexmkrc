#!usr/bin/env perl
$latex = 'lualatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$pdflatex = 'lualatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$bibtex = 'bibtex %O %S';
$makeindex = 'mendex %O -o %D %S';
$max_repeat = 10;
$out_dir = 'cache';
$aux_dir = 'cache';
$pdf_mode = 1;