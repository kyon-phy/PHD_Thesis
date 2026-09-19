from pathlib import Path
import shutil,hashlib,json
root=Path.cwd()
source=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/figures')
out=root/'Figs/CH8'; texdir=root/'Chapters/background_estimation'
texdir.mkdir(exist_ok=True); out.mkdir(exist_ok=True)
manifest=[]
def asset(rel,target):
 s=source/rel; d=out/target
 assert s.is_file(),s
 shutil.copy2(s,d)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 assert sha(s)==sha(d)
 manifest.append(dict(source=str(s),target=str(d),sha256=sha(d),operation='byte-identical copy'))
 return 'Figs/CH8/'+target

def fig(label,short,caption,panels):
 lines=['\\begin{figure}[p]','    \\centering']
 for i,(path,subcap) in enumerate(panels):
  lines += ['    \\begin{subfigure}{0.49\\linewidth}',f'        \\includegraphics[width=\\linewidth]{{{path}}}',f'        \\caption[]{{{subcap}}}','    \\end{subfigure}'+('\\hfill' if i%2==0 and i+1<len(panels) else '\\par\\medskip')]
 lines += [f'    \\caption[{short}]{{{caption}}}',f'    \\label{{{label}}}','\\end{figure}','']
 return '\n'.join(lines)
for fam in ['wcr','topcr']:
 text=[]
 for cat in ['Res','NonRes']:
  panels=[]
  for var in (['jet_pT','met','mT'] if fam=='wcr' else ['bjet_pT','met','mT']):
   for lep,folder,leptex in [('ele','e','e'),('mu','mu',r'\mu')]:
    group='WCR' if fam=='wcr' else 'TopCR'
    count='0tau1'+folder+'0b' if fam=='wcr' else '1tau1'+folder
    rel=f'DataMC_Comparison/{group}/{count}/'+('resonance_plots' if cat=='Res' else 'nonresonance_plots')+f'/{group}_{lep}_{cat}_{var}.pdf'
    p=asset(rel,f'{group}_{lep}_{cat}_{var}.pdf')
    vartex={'jet_pT':r'\pT^{j_1}','bjet_pT':r'\pT^b','met':r'\met','mT':r'm_{\mathrm{T}}^\ell' if fam=='wcr' else r'\mT'}[var]
    panels.append((p,f'${vartex}$, ${leptex}$ channel'))
  group='CRW' if fam=='wcr' else 'CRTop'
  caption=f'Pre-fit $N-1$ distributions in {group}-{cat}, with the electron channel in the left column and the muon channel in the right column. The stacked prediction contains all simulated backgrounds. The lower panels show data divided by the total prediction, and the hatched bands show the statistical uncertainty in that prediction. Arrows indicate the selection boundaries. The last bin includes the overflow.'
  text.append(fig(f'fig:ch8_{fam}_{cat.lower()}',f'Pre-fit N-1 distributions in {group}-{cat}',caption,panels))
 (texdir/f'figures_{fam}.tex').write_text('\n'.join(text))
for fam in ['vrw','vrtop']:
 text=[]
 for cat,oldcat in [('Res','sch'),('NonRes','tch')]:
  if fam=='vrw':
   vars=[('met',r'\met'),('mT',r'm_{\mathrm{T}}^\ell'),('lep_pT',r'\pT^\ell'),('b_pT',r'\pT^b'),('Mlb' if cat=='Res' else 'DPhi',r'm_{b\ell}' if cat=='Res' else r'\DphiLepMet'),('nbjets',r'N_b')]
   name='VR0tau';folder='VR0tau';group='VRW'
  else:
   vars=[('met',r'\met'),('mT',r'\mT'),('tau_pT',r'\pT^\tau'),('bjet_pT',r'\pT^b'),('InvM' if cat=='Res' else 'DPhi',r'm_{b\tau}' if cat=='Res' else r'\DphiTauMet'),('nbjets',r'N_b')]
   name='TopVR';folder='TopVR';group='VRTop'
  panels=[]
  for v,title in vars:
   rel=f'DataMC_Comparison/{folder}/{name}_{oldcat}_{v}.pdf'
   p=asset(rel,f'{group}_{cat}_{v}.pdf'); panels.append((p,'$'+title+'$'))
  caption=f'Pre-fit $N-1$ distributions in {group}-{cat}. '+('The electron and muon channels are combined. ' if fam=='vrw' else '')+'The lower panels show data divided by the total simulated background. The hatched bands represent the statistical uncertainty in the prediction. The last bin includes the overflow. '+('The original plot labels $0\\tau$VR denote $\\VRb$.' if fam=='vrw' else 'The leading tagged jet is used for the jet-dependent variables.')
  text.append(fig(f'fig:ch8_{fam}_{cat.lower()}',f'Pre-fit N-1 distributions in {group}-{cat}',caption,panels))
 (texdir/f'figures_{fam}.tex').write_text('\n'.join(text))
panels=[]
for name,sub in [('WCR_emuRatio_Data','Leading-jet $\\pT$ in data'),('WCR_emuRatio_MC','Leading-jet $\\pT$ in simulation'),('WCR_evenweight_e','Event weights in the electron simulation'),('WCR_evenweight_mu','Event weights in the muon simulation')]:
 panels.append((asset(f'appendix/CRstudy/{name}.pdf',name+'.pdf'),sub))
(texdir/'figures_emu.tex').write_text(fig('fig:ch8_emu_comparison','Electron--muon comparison in CRW-NonRes',r'Electron--muon consistency checks in $\CRW$-$\NonRes$. In (a) and (b), red and blue denote the electron and muon channels, and the lower panels show their ratio. Panels (c) and (d) show the simulated event weights against leading-jet $\pT$. The marked high-weight muon event illustrates the statistical effect discussed in the text.',panels))
p=asset('appendix/ZVR/ZVR_pTtau.pdf','ZVR_pTtau.pdf')
(texdir/'figures_fake.tex').write_text('\n'.join([
 '\\begin{figure}[htbp]\n    \\centering\n    \\includegraphics[width=0.80\\linewidth]{'+p+'}\n    \\caption[Pre-fit tau momentum distribution in the ZVR]{Pre-fit $N-1$ distribution of $\\pT^\\tau$ in the ZVR. The red arrow indicates the $100~\\GeV$ threshold. The lower panel compares data with the total simulation. The high-$\\pT^\\tau$ prediction exceeds the observed yield.}\n    \\label{fig:ch8_zvr_pt}\n\\end{figure}\n',
 fig('fig:ch8_zvr_rnn','Tau-identification RNN distributions in the ZVR',r'The $\tau$-identification RNN score in $Z$+jets-enriched samples with (a) $\pT^\tau>20~\GeV$ and (b) $\pT^\tau>100~\GeV$. Looser $\tau$ identification and a relaxed transverse-mass requirement are used to compare the low- and high-score regions. These selections differ from the nominal ZVR.',[(asset('appendix/ZVR/ZVR_1tau20GeV_score.pdf','ZVR_1tau20GeV_score.pdf'),r'$\pT^\tau>20~\GeV$'),(asset('appendix/ZVR/ZVR_1tau100GeV_score.pdf','ZVR_1tau100GeV_score.pdf'),r'$\pT^\tau>100~\GeV$')])]))
panels=[(asset('appendix/VRstudy/met_VR0tau.pdf','VRW_NonRes_fine_met.pdf'),r'$\met$ with its threshold removed'),(asset('appendix/VRstudy/lep0_pt_VR0tau_met4250_450.pdf','VRW_NonRes_local_lep_pt.pdf'),r'$\pT^\ell$ for $425<\met<450~\GeV$')]
(texdir/'figures_vr_study.tex').write_text(fig('fig:ch8_vrw_met_study','Localised excess in VRW-NonRes',r'Diagnostic pre-fit distributions for the excess in $\VRb$-$\NonRes$. The finer $\met$ binning in (a) resolves the interval $425<\met<450~\GeV$. Panel (b) shows the lepton $\pT$ within that interval. The lower panels show data divided by the simulated prediction.',panels))
(root/'output/ch8/figure_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Copied',len(manifest),'source PDFs unchanged; generated',len(list(texdir.glob('*.tex'))),'figure include files.')
