from pathlib import Path
import re,json
base=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search')
folders=['10_理论与动机','20_Trigger','50_Systematics','70_博士论文写作']
allnotes=list(base.rglob('*.md')); stems={p.stem for p in allnotes}; owned=[p for d in folders for p in (base/d).glob('*.md')]
problems=[]
for p in owned:
 s=p.read_text()
 for key in ['type:','updated: 2026-09-07','status:','tags:']:
  if key not in s.split('---',2)[1]:problems.append([p.name,'frontmatter',key])
 for m in re.finditer(r'\]\(<([^>]+)>\)',s):
  dest=m[1]
  if dest.startswith('/') and not Path(dest.split('#')[0]).exists():problems.append([p.name,'missing local file',dest])
 for target in re.findall(r'\[\[([^]|#]+)',s):
  if target not in stems:problems.append([p.name,'missing wikilink',target])
 if '{SRC}' in s or '{CACHE}' in s:problems.append([p.name,'unresolved template'])
 if '\\\\' in s:problems.append([p.name,'double backslash'])
print(json.dumps({'notes':len(owned),'characters':sum(len(p.read_text()) for p in owned),'problems':problems},ensure_ascii=False,indent=2))
