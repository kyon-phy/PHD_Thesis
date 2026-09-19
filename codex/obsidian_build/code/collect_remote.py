import os,json,hashlib,subprocess,pathlib,datetime
base=pathlib.Path('/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes')
top=pathlib.Path('/afs/cern.ch/work/z/zang/LQanalysis/GFW1_TopCPTool/v02/taux_gnt1makeralg/TauX_GFw1_TopCPToolkit/source')
roots=[base/'run/scripts',base/'TauXFastFrame/Root',base/'TauXFastFrame/TauXFastFrame',base/'FastFrames/Root',base/'FastFrames/python',base/'FastFrames/FastFrames',base/'taunub/TRXconfig',base/'taunub/config_taunub',top/'TauX_Gnt1makerAlg/python']
ext={'.py','.sh','.cc','.cxx','.h','.hpp','.yml','.yaml','.config','.md'}
out={'collected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[],'repos':[]}
for root in roots:
 for dp,dn,fn in os.walk(root):
  dn[:]=[d for d in dn if not d.startswith('.') and d not in ['__pycache__','build','install'] and not d.startswith(('plots','processlog','signific'))]
  for f in sorted(fn):
   p=pathlib.Path(dp)/f
   if p.suffix not in ext: continue
   s=p.stat()
   if s.st_size>8_000_000: continue
   b=p.read_bytes()
   out['files'].append({'path':str(p),'relative':str(p.relative_to(base)) if p.is_relative_to(base) else 'TopCP/'+str(p.relative_to(top)), 'size':s.st_size,'mtime':s.st_mtime,'ctime':s.st_ctime,'birthtime':getattr(s,'st_birthtime',None),'sha256':hashlib.sha256(b).hexdigest(),'text':b.decode(errors='replace')})
for p in [base,base/'TauXFastFrame',base/'FastFrames',base/'TRExFitter',top/'TauX_Gnt1makerAlg',top/'TopCPToolkit']:
 d={'path':str(p)}
 for k,c in [('head',['git','-C',str(p),'rev-parse','HEAD']),('status',['git','-C',str(p),'status','--short']),('root',['git','-C',str(p),'rev-parse','--show-toplevel'])]:
  r=subprocess.run(c,text=True,capture_output=True); d[k]=r.stdout.strip() if r.returncode==0 else r.stderr.strip()
 out['repos'].append(d)
print(json.dumps(out))
