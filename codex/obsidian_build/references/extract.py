from pathlib import Path
from pypdf import PdfReader
import json
src=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references')
out=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/references')
for file in src.rglob('*.pdf'):
    reader=PdfReader(file)
    pages=[page.extract_text() or '' for page in reader.pages]
    stem=file.stem
    (out/(stem+'.json')).write_text(json.dumps(pages,ensure_ascii=False))
    (out/(stem+'.txt')).write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{text}' for i,text in enumerate(pages)))
    print(file.name,len(pages))
