from pathlib import Path
from pypdf import PdfReader
import xml.etree.ElementTree as ET,zipfile,re,json,hashlib
src=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/presentation');out=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/meetings')
import logging
logging.getLogger("pypdf").setLevel(logging.ERROR)
records=[]
for p in sorted(src.rglob('*')):
 if p.suffix.lower() not in ['.pdf','.pptx'] or p.name.startswith('~$'):continue
 d=dict(name=p.name,path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pages=[],metadata={})
 try:
  if p.suffix=='.pdf':
   pdf=PdfReader(p)
   d['metadata']={str(k):str(v) for k,v in (pdf.metadata or {}).items()}
   d['pages']=[{'page':i+1,'text':pg.extract_text() or ''} for i,pg in enumerate(pdf.pages)]
  else:
   with zipfile.ZipFile(p) as z:
    for s in sorted([s for s in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',s)],key=lambda s:int(re.search(r'slide(\d+)',s).group(1))):
     tree=ET.fromstring(z.read(s));page=int(re.search(r'slide(\d+)',s).group(1));text='\n'.join(t.text or '' for t in tree.iter() if t.tag.endswith('}t')).encode('utf-8','replace').decode('utf-8')
     notes='';nf=f'ppt/notesSlides/notesSlide{page}.xml'
     if nf in z.namelist():notes='\n'.join(t.text or '' for t in ET.fromstring(z.read(nf)).iter() if t.tag.endswith('}t')).encode('utf-8','replace').decode('utf-8')
     d['pages'].append({'page':page,'text':text,'notes':notes,'hidden':tree.attrib.get('show')=='0'})
    if 'docProps/core.xml' in z.namelist():d['metadata']={v.tag.split('}')[-1]:v.text for v in ET.fromstring(z.read('docProps/core.xml'))}
 except Exception as e:d['error']=str(e)
 records.append(d)
 (out/(p.name+'.txt')).write_text('\n\n'.join(f"### PAGE {x['page']}\n{x['text']}\nNOTES: {x.get('notes','')}" for x in d['pages']).encode('utf-8','replace').decode('utf-8'))
(out/'records.json').write_text(json.dumps(records,ensure_ascii=True,indent=2))
print(f'{len(records)} files {sum(len(r["pages"]) for r in records)} pages')
print([r['name'] for r in records if 'error' in r])
