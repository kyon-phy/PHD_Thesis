from pathlib import Path
from collections import defaultdict
import hashlib,json,datetime,re
V=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search')
R=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references')
P=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/presentation')
M=V/'90_来源与维护'
def md(name,text):
 (M/(name+'.md')).write_text('---\ntype: index\nupdated: 2026-09-07\nstatus: 本次整理快照\ntags: [sources, index]\n---\n\n# '+name+'\n\n'+text+'\n')
sources=[]
for kind,paths in [('reference',R.rglob('*.pdf')),('meeting',P.iterdir())]:
 for p in sorted(paths):
  if not p.is_file() or p.suffix.lower() not in ['.pdf','.pptx'] or p.name.startswith('~$'):continue
  s=p.stat();sources.append({'kind':kind,'path':str(p),'size':s.st_size,'mtime_utc':datetime.datetime.fromtimestamp(s.st_mtime,datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(M/'原始文献与会议来源清单.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
nref=sum(s['kind']=='reference' for s in sources);nmeeting=sum(s['kind']=='meeting' for s in sources)
md('资料覆盖与来源索引',f'''本次盘点的本地来源包括 **{nref}份reference PDF** 和 **{nmeeting}份meeting PDF/PPTX**。同一报告的PDF/PPTX、v1/v2等文件分别登记，会议摘要按真实会议归组，不把文件数当成独立会议数。

## 对应最初10项任务

1. Trigger：20_Trigger，逐年MET menu、single-lepton control-region trigger及论文/性能来源。
2. Tau meetings：60_Meetings，按日期/真实会议身份归档，同时有对象、signal、fit等主题路线。
3. 其它meetings：同一分库收录ICEPP、LPX、EB、approval、Higgs等；173源文件归为63组，60个有日期组及3个辅助组。
4. 博士论文：70_博士论文写作，8篇逐篇章节内容/页数/深度卡，加一篇通用写作框架。
5. LQ理论：10_理论与动机，Iguro tau-nu-b motivation、U1 flavour结构/low-energy matching、高低能约束和favoured band。
6. 独立分析项目：01_分析项目，8篇串联本实验细节，内部note与公开arXiv版本分别标明。
7. DAOD objects/OR：30_Objects与DAOD，追踪指定入口、CP默认实现、WP、MET、OR顺序和skimming。
8. Histogram/fit：40_Histogram与Fit，FastFrames实际入口及指定Toy config、POI/interference、regions、toys、systematics/pruning。
9. Systematics：50_Systematics，HF30%证据链、experimental/theory来源、代码实现与待补资料。
10. Scripts：80_Scripts，37个Python/shell脚本逐项归类、时间证据、用法和输入输出，favoured-band另有独立专题。

## 来源存放位置

- 本地原始reference：`{R}`。原文件未修改。
- 本地原始meeting：`{P}`。原文件未修改；忽略Office临时锁文件`~$*`。
- 代码：CERN原路径逐份记录在 `代码快照/2026-09-07/代码来源清单.json`；351份主代码/配置副本加CP/TREx默认实现、24份脚本附属文本/备份。不是完整analysis checkout，也不含大型ROOT输出。
- `原始文献与会议来源清单.json`包含source path、size、mtime和SHA-256；它用于找到源文件及比较更新，不包含全文。
- 公开paper arXiv及补充性能论文的本次下载副本位于笔记所链接的`codex/obsidian_build`缓存；原始reference目录没有被替换。

## 阅读和验证深度

会议全部文件完成文本盘点，每组主读本有摘要和页码；涉及主要结论的公式/关键图页作了视觉核对。博士论文以目录和代表性正文判断解释深度，不宣称逐式审稿。文献图中的全部曲线没有逐点digitise。代码笔记为静态阅读结果，没有重新生产histograms、提交toys或复现final limits。

## 入口

[[00_资料库首页]] · [[全库目录]] · [[检索与更新说明]] · [[代码版本与资料来源]] · [[待补资料与版本差异]]
''')
groups=defaultdict(list)
for p in V.rglob('*.md'):
 if '代码快照' in p.parts or '.obsidian' in p.parts or p.name in ['Welcome.md','全库目录.md']:continue
 groups[p.parent.name if p.parent!=V else '00_首页'].append(p)
text=[]
for group,ps in sorted(groups.items()):
 text.extend(['## '+group,''])
 for p in sorted(ps):text.append('- [['+p.stem+']]')
 text.append('')
md('全库目录','按主题目录列出全部笔记。历史meeting卡片与现行分析说明并列保存，请注意每页status与来源日期。\n\n'+'\n'.join(text))
print(json.dumps({'reference_pdfs':nref,'meeting_sources':nmeeting,'notes':sum(len(ps) for ps in groups.values())+1,'groups':{g:len(ps) for g,ps in groups.items()}},ensure_ascii=False,indent=2))
