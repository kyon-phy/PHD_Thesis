import urllib.request,json,concurrent.futures
from pathlib import Path
import pypdfium2 as pdfium
root=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/references')
def get(paper):
    url='https://arxiv.org/pdf/'+paper
    path=root/(paper+'.pdf')
    if not path.exists() or paper!='2005.09554':urllib.request.urlretrieve(url,path)
    doc=pdfium.PdfDocument(str(path)); pages=[]
    for page in doc:
        text=page.get_textpage();pages.append(text.get_text_range());text.close();page.close()
    doc.close()
    (root/(paper+'.pdfium.json')).write_text(json.dumps(pages,ensure_ascii=False))
    (root/(paper+'.pdfium.txt')).write_text('\n\n'.join('=== PDF PAGE %d ===\n%s'%(i+1,p) for i,p in enumerate(pages)))
    return [paper,len(pages),path.stat().st_size]
for paper in ['2005.09554','1909.00761','2004.13447']:print(get(paper),flush=True)
