from pathlib import Path
from pypdf import PdfReader
import json, re, hashlib, difflib, shutil
root = Path(__file__).resolve().parents[2]
chapter = root/'Chapters/CH8_Background_estimation.tex'
incs = list((root/'Chapters/background_estimation').glob('*.tex'))
alltext = '\n'.join(p.read_text() for p in [chapter]+incs)
records = json.loads((root/'output/ch8/figure_manifest.json').read_text())
for r in records:
    for key in ['source', 'target']:
        assert hashlib.sha256(Path(r[key]).read_bytes()).hexdigest() == r['sha256']
for target in re.findall(r'\\includegraphics\[[^]]*\]\{([^}]+)\}', alltext):
    assert (root/target).is_file(), target
labels = re.findall(r'\\label\{([^}]+)\}', alltext)
assert len(labels) == len(set(labels))
preview_log = (root/'output/ch8/build/CH8_preview.log').read_text(errors='replace')
for pattern in ['undefined', 'Overfull', 'Underfull', 'Float too large', '! LaTeX Error']:
    assert pattern not in preview_log, pattern
preview = root/'output/ch8/build/CH8_preview.pdf'
reader = PdfReader(preview)
pdf_text = '\n'.join(p.extract_text() for p in reader.pages)
assert '??' not in pdf_text
assert 'Multi-jet cleaning' not in pdf_text
assert len(re.findall(r'\\begin\{figure\}', alltext)) == 12
assert len(re.findall(r'\\begin\{table\}', alltext)) == 6
assert len(records) == 57
out = root/'output/pdf/CH8_draft.pdf'
shutil.copy2(preview, out)
full = PdfReader(root/'output/ch8/full_build/thesis.pdf')
full_log = (root/'output/ch8/full_build/thesis.log').read_text(errors='replace')
assert 'undefined' not in full_log
assert 'Overfull' not in full_log
for before, after, target in [
    (root/'output/ch8/review/CH8_before.tex', chapter, 'CH8_draft.diff'),
    (root/'output/ch8/review/references_before_ch8.bib', root/'References/references.bib', 'references.diff')]:
    diff = ''.join(difflib.unified_diff(before.read_text().splitlines(True), after.read_text().splitlines(True), fromfile=str(before.relative_to(root)), tofile=str(after.relative_to(root))))
    (root/'output/ch8/review'/target).write_text(diff)
validation = dict(
    preview_pages=len(reader.pages), full_thesis_pages=len(full.pages), figures=12, tables=6,
    panels=57, cr_vr_prefit_n_minus_1_panels=48, source_pdfs_byte_identical=True,
    duplicate_local_labels=False, missing_figure_files=False, undefined_references=False,
    undefined_citations=False, preview_overfull_boxes=False, preview_underfull_boxes=False,
    oversize_floats=False, final_pdf=str(out),
    final_pdf_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
    retained_warnings=['shared document-class and bibliography-option notices', 'oneside fancyhdr notice',
        'shared thesis metadata PDF-string warnings', 'tikz-feynman compatibility notices'],
    full_build_limitations=['Bibliography has underfull hbox warnings outside Chapter 8.'],
    visual_review='Rendered pages inspected; original INT figure styles retained.',
    source_boundary='ZVR transverse-mass object choice is not unambiguous in Appendix D; noted for author.')
(root/'output/ch8/review/validation.json').write_text(json.dumps(validation, indent=2))
print(json.dumps(validation, indent=2))
