import json,pathlib,subprocess,hashlib,datetime
b=pathlib.Path('/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes')
rel=pathlib.Path('/cvmfs/atlas.cern.ch/repo/sw/software/25.2/AnalysisBase/25.2.51/InstallArea/x86_64-el9-gcc13-opt')
t=b/'TRExFitter/TRExFitter'
files=[rel/'python/AsgAnalysisAlgorithms/OverlapAnalysisConfig.py',rel/'python/AsgAnalysisAlgorithms/MetAnalysisConfig.py',rel/'python/TauAnalysisAlgorithms/TauAnalysisConfig.py',rel/'python/MuonAnalysisAlgorithms/MuonAnalysisConfig.py',t/'jobSchema.config',t/'version.txt',t/'README.md']
files+=list((t/'Root').glob('*Config*cc'))+list((t/'Root').glob('*Limit*cc'))
out={'files':[],'scripts':[]}
for p in files:
 if p.exists():
  bb=p.read_bytes();out['files'].append({'path':str(p),'text':bb.decode(errors='replace'),'sha256':hashlib.sha256(bb).hexdigest()})
for p in sorted((b/'run/scripts').glob('*')):
 if not p.is_file() or p.suffix not in ['.py','.sh']:continue
 r={'name':p.name,'path':str(p)}
 for key,args in [('first_git',['log','--follow','--diff-filter=A','--format=%aI|%cI|%h|%s','--',str(p.relative_to(b))]),('last_git',['log','-1','--format=%aI|%cI|%h|%s','--',str(p.relative_to(b))]),('stat',['status','--short','--',str(p.relative_to(b))])]:
  q=subprocess.run(['git','-C',str(b)]+args,text=True,capture_output=True);r[key]=q.stdout.strip()
 r['stat_birth']=subprocess.run(['stat','-c','%w',str(p)],text=True,capture_output=True).stdout.strip()
 out['scripts'].append(r)
print(json.dumps(out))
