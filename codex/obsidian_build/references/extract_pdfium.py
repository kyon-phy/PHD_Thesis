from pathlib import Path
import pypdfium2 as p
import json
src=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references')
out=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/references')
for file in src.rglob('*.pdf'):
    doc=p.PdfDocument(file)
    pages=[page.get_textpage().get_text_range().replace('\r\n','\n') for page in doc]
    stem=file.stem+'.pdfium'
    (out/(stem+'.json')).write_text(json.dumps(pages,ensure_ascii=False))
    (out/(stem+'.txt')).write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{text}' for i,text in enumerate(pages)))
    print(file.name,len(pages),flush=True)
