"""Reproduce the Ch7 yield audit and MET scans from unmodified local YAML.

Run with system Python (matplotlib) and the locally installed YAML/PDF helpers:
PYTHONPATH=tmp/ch7_plot_deps:tmp/skill_validation_deps /usr/local/bin/python3 scripts/ch7/validate_yields_and_scan.py
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import argparse
import numpy as np
import yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
FIT = Path('/Users/zang/Desktop/fit_results')
OUT = ROOT / 'output/ch7/significance_validation'
FIG = ROOT / 'Figs/CH7/significance'
PAPER_FIT = FIT / 'TwoSided_HF0_3_HFSeperated_Renamed_BONLY/fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_5_23L0_6_alldecay_corrected'
SIG2500 = FIT / 'TwoSided_HF0_3_HFSeperated_Renamed_SPLUSB/fit_taunub_sys_1l_allVR_SPLUSB_MU2500_gU2_5_23L1_0_alldecay_corrected'
SIG3000 = FIT / 'TwoSided_HF0_3_HFSeperated_Renamed_SPLUSB/fit_taunub_sys_1l_allVR_SPLUSB_MU3000_gU2_5_23L1_0_alldecay_corrected'
SOURCES = {}

def read(path):
    SOURCES[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return yaml.safe_load(path.read_text())

def write_csv(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def z_asimov(s, b, relative=0.30, absolute=None):
    """The formula already in Ch7 / INT Eq. 6.1; no fit significance implied."""
    if b <= 0 or s < 0:
        return float('nan')
    if s == 0:
        return 0.0
    sigma = relative*b if absolute is None else absolute
    if sigma == 0:
        return math.sqrt(2*((s+b)*math.log1p(s/b)-s))
    v, n = sigma*sigma, s+b
    q = 2*(n*math.log(n*(b+v)/(b*b+n*v)) - b*b/v*math.log1p(v*s/(b*(b+v))))
    return math.sqrt(max(0, q))

# These are literal numbers from the paper auxiliary TeX tables, not a fit result.
PAPER_ROWS = [
    ('SR1b-Res', 'SR_1tau0l1b_Res', 2.69, .83),
    ('SR1b-NonRes', 'SR_1tau0l1b_NonRes', 1.88, .71),
    ('CRW-Res', '0#tau1l0b, Resonance WCR', 462, 22),
    ('CRW-NonRes', '0#tau1l0b, Non-Resonance WCR', 872, 30),
    ('CRTop-Res', '1#tau1l1b, Resonance topCR', 63.0, 7.9),
    ('CRTop-NonRes', '1#tau1l1b, Non-Resonance topCR', 468, 22),
    ('VRb-Res', '0#tau1l1b, Resonance 0tauVR', 34.7, 9.3),
    ('VRb-NonRes', '0#tau1l1b, Non-Resonance 0tauVR', 40.7, 12.0),
    ('SR0b-Res', '1#tau0l0b, Resonance WVR', 36.4, 7.3),
    ('SR0b-NonRes', '1#tau0l0b, Non-Resonance WVR', 38.3, 9.9),
    ('VRTop-Res', '1#tau0l2b, Resonance topVR', 13.0, 3.9),
    ('VRTop-NonRes', '1#tau0l2b, Non-Resonance topVR', 30.1, 8.1),
]

def audit():
    post = {x['Region']: x['Samples'] for x in read(PAPER_FIT/'Tables/Table_postfit_nosigs.yaml')}
    pre = {x['Region']: x['Samples'] for x in read(PAPER_FIT/'Tables/Table_prefit.yaml')}
    checks, background = [], []
    for name, key, paper_b, paper_err in PAPER_ROWS:
        total = next(x for x in post[key] if x.get('Sample') == 'Total')
        checks.append(dict(region=name, paper_B=paper_b, yaml_B=total['Yield'],
                           difference=total['Yield']-paper_b, paper_error=paper_err, yaml_error=total['Error']))
        for st, rows in [('prefit', pre[key]), ('postfit', post[key])]:
            for x in rows:
                sample = x.get('Sample', '')
                if sample and sample != 'Total' and not sample.startswith('MU'):
                    background.append(dict(region=name, stage=st, process=sample, yield_value=x['Yield'], error=x['Error']))
    write_csv(OUT/'paper_postfit_check.csv', checks)
    write_csv(OUT/'background_components.csv', background)
    yields = []
    for name, fit, mass, g, beta in [('SR1b-Res', PAPER_FIT, 1500, 1.5, .6),
                                   ('SR1b-NonRes', SIG2500, 2500, 2.5, 1.0),
                                   ('SR1b-NonRes', SIG3000, 3000, 2.5, 1.0)]:
        topo = name.split('-')[1]
        d = read(fit/f'Plots/SR_1tau0l1b_{topo}_met_prefit.yaml')
        reference = read(PAPER_FIT/f'Plots/SR_1tau0l1b_{topo}_met_prefit.yaml')
        # S+B directory is used only for a pre-fit signal, never post-fit B.
        assert np.allclose(d['Total'][0]['Yield'], reference['Total'][0]['Yield'], rtol=0, atol=1e-12)
        s = sum(d['Samples'][0]['Yield']); b = sum(reference['Total'][0]['Yield'])
        yields.append(dict(region=name, mass_GeV=mass, gU=g, betaL23=beta, S=s, B=b,
                           sigma_b=.3*b, Z=z_asimov(s,b), Z_absolute_sigma_0p3=z_asimov(s,b,absolute=.3)))
    write_csv(OUT/'validated_prefit_yields.csv', yields)
    write_csv(OUT/'int_note_Z_check.csv', [dict(region=reg, S=s, B=b, note_Z=zn,
              Z_relative_30percent=z_asimov(s,b), Z_absolute_sigma_0p3=z_asimov(s,b,absolute=.3))
              for reg,s,b,zn in [('SR1b-Res',4.2,2.4,2.2),('SR1b-NonRes',6.6,2.1,3.3)]])
    return checks, yields

# RGB values extracted from the actual paper SR1b-NonRes MET PDF.
COLOURS = {'Z+jets':(.580078,.642578,.634766), 'single t':(.724609,.673828,.439209),
           'ttbar':(.247070,.564453,.855469), 'Diboson':(1,.662109,.0549011),
           'W+jets':(1,.800781,1)}
LABELS = {'Z+jets':r'$Z$+jets', 'single t':r'single $t$', 'ttbar':r'$t\bar{t}$',
          'Diboson':'Diboson', 'W+jets':r'$W$+jets'}
SIGNAL_COLOURS = {'Res':'#ed232a', 'NonRes':(.513672,.176514,.712891)}
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],
    'font.size':12, 'axes.labelsize':14, 'legend.fontsize':10.5, 'xtick.direction':'in',
    'ytick.direction':'in','xtick.top':True,'ytick.right':True,'axes.linewidth':1.1,
    'mathtext.fontset':'stixsans','pdf.fonttype':42,'savefig.facecolor':'white'})

def group(name):
    if name.startswith('MU'): return 'signal'
    if name == 'ttbar': return 'ttbar'
    if name == 'SingleTop': return 'single t'
    if name.startswith('Z'): return 'Z+jets'
    if name.startswith('W'): return 'W+jets'
    if name == 'Diboson': return 'Diboson'
    raise ValueError(name)

def scan_input(topo):
    point = 'MU1500_gU1_5_23L0_6' if topo == 'Res' else 'MU2500_gU2_5_23L1_0'
    old = 'sch' if topo == 'Res' else 'tch'
    fit = FIT/f'fit_taunub_nom_1l_allVR_BONLY_{point}_alldecay_corrected_N_minus_1'
    path = fit/f'Plots/SR_1tau0l1b_{old}_met_N_minus_1_met_prefit.yaml'
    d = read(path)
    edges = np.array(d['Figure'][0]['BinEdges'], float)
    start = list(edges).index(200)
    groups = {key:np.zeros(len(edges)-1) for key in [*COLOURS, 'signal']}
    for sample in d['Samples']:
        groups[group(sample['Name'])] += np.array(sample['Yield'],float)
    total = np.array(d['Total'][0]['Yield'],float)
    assert np.allclose(sum(groups[k] for k in COLOURS),total,rtol=1e-12,atol=1e-14)
    # No rebinning, reweighting, normalisation, interpolation, or new clipping.
    # Bins below the separately retained trigger baseline are not plotted.
    edges = edges[start:]; groups={k:v[start:] for k,v in groups.items()}; total=total[start:]
    up=np.array(d['Total'][0]['UncertaintyUp'],float)[start:]
    down=np.array(d['Total'][0]['UncertaintyDown'],float)[start:]
    s=np.cumsum(groups['signal'][::-1])[::-1];b=np.cumsum(total[::-1])[::-1]
    z=np.array([z_asimov(si,bi) for si,bi in zip(s,b)])
    nominal=200 if topo=='Res' else 400
    rows=[dict(region='SR1b-'+topo,threshold_GeV=x,S=si,B=bi,sigma_b=.3*bi,Z=zi,
               passes_B_gt_2=bool(bi>2),nominal_cut=bool(x==nominal)) for x,si,bi,zi in zip(edges[:-1],s,b,z)]
    write_csv(OUT/f'SR1b_{topo}_met_scan.csv',rows)
    exact=read(fit/f'Plots/SR_1tau0l1b_{old}_met_prefit.yaml')
    nominal_i=list(edges).index(nominal)
    assert math.isclose(s[nominal_i],sum(exact['Samples'][0]['Yield']),rel_tol=1e-12)
    return dict(topo=topo,point=point,path=str(path),edges=edges,groups=groups,b=total,up=up,down=down,
                thresholds=edges[:-1],s_tail=s,b_tail=b,z=z,nominal=nominal,nominal_i=nominal_i,
                single_bin_B=sum(exact['Total'][0]['Yield']))

def labels(ax,topo):
    ax.text(.035,.955,r'$\sqrt{s}=13$ TeV, 140 fb$^{-1}$',transform=ax.transAxes,va='top',fontsize=12)
    ax.text(.035,.885,'SR1b-'+topo,transform=ax.transAxes,va='top',fontsize=12)

def curve(ax,d,legend=True):
    x,z,b=d['thresholds'],d['z'],d['b_tail'];colour=SIGNAL_COLOURS[d['topo']]
    ax.plot(x,z,ls='--',lw=1.5,color=colour)
    valid=b>2
    ax.plot(x[valid],z[valid],'-o',ms=4,lw=1.8,color=colour)
    ax.plot(x[~valid],z[~valid],linestyle='none',marker='o',ms=4,mfc='white',mec=colour)
    i=d['nominal_i'];ax.plot(x[i],z[i],marker='s',ms=6,color=colour,linestyle='none')
    ax.axvline(d['nominal'],color='.35',ls=':',lw=1,ymax=.68 if legend else 1)
    ax.set_xlim(200,1600);ax.set_ylim(0,max(z)*1.2)
    ax.set_xticks(np.arange(200,1601,200));ax.set_ylabel(r'$Z$')
    ax.minorticks_on()
    if legend:
        mass='1.5' if d['topo']=='Res' else '2.5'
        ax.legend(handles=[Line2D([],[],color=colour,lw=1.8,label=r'$U_1$ ('+mass+' TeV)'),
                  Line2D([],[],color=colour,marker='o',label=r'$B>2$'),
                  Line2D([],[],color=colour,ls='--',marker='o',mfc='white',label=r'$B\leq2$ (excluded)'),
                  Line2D([],[],color='.35',ls=':',label='Selected threshold')],frameon=False,loc='upper right')

def save(fig,name,paper_geometry=False):
    # A fixed page is needed to preserve the paper's title positions in points.
    bbox=None if paper_geometry else 'tight'
    pdf=FIG/f'{name}.pending.pdf';png=FIG/f'{name}.pending.png'
    fig.savefig(pdf,bbox_inches=bbox)
    fig.savefig(png,dpi=160,bbox_inches=bbox)
    pdf.replace(FIG/f'{name}.pdf');png.replace(FIG/f'{name}.png')
    plt.close(fig)

def plot_scans(ds):
    fig,axes=plt.subplots(1,2,figsize=(12.4,4.7))
    for ax,d in zip(axes,ds):
        curve(ax,d)
        ax.set_ylim(0,max(d['z'])*1.55)
        labels(ax,d['topo'])
        ax.set_xlabel(r'$E_{\mathrm{T}}^{\mathrm{miss}}$ threshold [GeV]')
        ax.text(.96,.64,r'$\sigma_b=0.30b$',transform=ax.transAxes,ha='right',fontsize=11)
    fig.subplots_adjust(wspace=.23,bottom=.16)
    save(fig,'SR1b_met_significance_scan')

def plot_distribution(d):
    # Paper: figures/Aux/post_fit_plots/SR1b_NonRes_met.pdf, 567 x 407 pt.
    # Axis frame coordinates come from the ROOT plot; title coordinates and
    # font sizes were read directly from the PDF text operators.
    fw,fh=567.,407.
    fig=plt.figure(figsize=(fw/72,fh/72))
    ax=fig.add_axes([59.5/fw,114/fh,486.25/fw,274.5/fh])
    lower=fig.add_axes([59.5/fw,49.25/fh,486.25/fw,64.75/fh],sharex=ax)
    edges=d['edges']; bottom=np.zeros(len(edges)-1)
    for key in COLOURS:
        values=d['groups'][key]
        patches=ax.bar(edges[:-1],values,width=np.diff(edges),bottom=bottom,align='edge',
                       color=COLOURS[key],edgecolor='black',linewidth=.65)
        assert np.allclose([p.get_height() for p in patches],values,rtol=0,atol=1e-15)
        bottom+=values
    assert np.allclose(bottom,d['b'],rtol=1e-12,atol=1e-14)
    ax.stairs(d['b']+d['up'],edges,baseline=d['b']+d['down'],fill=True,
              facecolor='none',edgecolor=(.399902,.399902,1),hatch='////',linewidth=0,zorder=4)
    colour=SIGNAL_COLOURS[d['topo']]
    ax.stairs(d['groups']['signal'],edges,linestyle=':',lw=2.5,color=colour,zorder=5)
    ax.set_yscale('log');ax.set_ylim(.001,300)
    ax.set_ylabel('Events / 200 GeV',fontsize=15.5,ha='right',va='baseline',rotation_mode='anchor')
    ax.yaxis.set_label_coords(23.1254/fw,388.5/fh,transform=fig.transFigure)
    ax.minorticks_on();ax.tick_params(labelbottom=False)
    ax.tick_params(axis='y',labelsize=14.232,pad=3)
    fig.text(76.9199/fw,361.098/fh,r'$\sqrt{s}=13$ TeV, 140 fb$^{-1}$',fontsize=14.232,va='baseline')
    fig.text(76.9199/fw,341.86793/fh,'SR1b-'+d['topo'],fontsize=14.232,va='baseline')
    mass='1.5' if d['topo']=='Res' else '2.5'
    handles=[Line2D([],[],color=colour,ls=':',lw=2.5,label=r'$U_1$ ('+mass+' TeV)')]
    handles += [Patch(facecolor=COLOURS[k],edgecolor='black',label=LABELS[k]) for k in ['W+jets','Diboson','ttbar','Z+jets','single t']]
    handles += [Patch(facecolor='none',edgecolor=(.399902,.399902,1),hatch='////',label='Uncertainty')]
    ax.legend(handles=handles,ncol=2,frameon=False,loc='upper right',fontsize=14.232,columnspacing=.8,handlelength=1.1)
    curve(lower,d,legend=False)
    lower.set_ylabel(r'Significance $Z$',fontsize=14.2587,ha='center',va='baseline',rotation_mode='anchor')
    lower.yaxis.set_label_coords(23.1254/fw,81.625/fh,transform=fig.transFigure)
    lower.tick_params(axis='both',labelsize=14.2587,pad=3)
    # Match ROOT's four text runs for the right-aligned MET title, including
    # independently sized E, T, miss and unit text, instead of a centred xlabel.
    fig.text(435.765/fw,10.47114/fh,'E',fontsize=23.75,fontstyle='italic',va='baseline')
    fig.text(455.1974/fw,3.1977/fh,'T',fontsize=17.5,va='baseline')
    fig.text(455.1974/fw,20.0934/fh,'miss',fontsize=17.5,va='baseline')
    fig.text(490.6771/fw,9.9711/fh,' [GeV]',fontsize=21.25,va='baseline')
    lower.text(.96,.92,r'$\sigma_b=0.30b$',transform=lower.transAxes,ha='right',va='top',fontsize=10)
    # The abscissa in this panel is the lower MET threshold, not a per-bin score.
    lower.text(.96,.69,r'Dashed: $B\leq2$',transform=lower.transAxes,ha='right',va='top',fontsize=9)
    save(fig,'SR1b_'+d['topo']+'_met_with_significance',paper_geometry=True)

def audit_figure_integrals(ds):
    bins,summary,processes=[],[],[]
    for d in ds:
        path=Path(d['path'])
        n1=read(path)
        sr=read(path.with_name(path.name.replace('_met_N_minus_1_met_','_met_')))
        paper=read(PAPER_FIT/f"Plots/SR_1tau0l1b_{d['topo']}_met_prefit.yaml")
        for i,(lo,hi) in enumerate(zip(d['edges'][:-1],d['edges'][1:])):
            vals={k:float(d['groups'][k][i]) for k in COLOURS}
            bins.append(dict(region=d['topo'],low_GeV=lo,high_GeV=hi,**vals,
                             stack_sum=sum(vals.values()),yaml_total=float(d['b'][i]),
                             difference=sum(vals.values())-float(d['b'][i])))
        b=float(d['b_tail'][d['nominal_i']]);ref=sum(sr['Total'][0]['Yield'])
        p_ref=sum(paper['Total'][0]['Yield'])
        summary.append(dict(region=d['topo'],nominal_threshold=d['nominal'],
                            all_displayed_bins_B=float(sum(d['b'])),SR_range_bins_B=b,
                            same_batch_SR_yaml_B=ref,difference=b-ref,relative_difference_percent=100*(b/ref-1),
                            paper_matched_SR_yaml_B=p_ref,paper_difference_percent=100*(b/p_ref-1)))
        start=n1['Figure'][0]['BinEdges'].index(d['nominal'])
        sr_samples={s['Name']:sum(map(float,s['Yield'])) for s in sr['Samples']}
        for s in n1['Samples']:
            if s['Name'].startswith('MU'):continue
            value=sum(map(float,s['Yield'][start:]));reference=sr_samples[s['Name']]
            processes.append(dict(region=d['topo'],process=s['Name'],Nminus1_SR_range_B=value,
                                  same_batch_SR_B=reference,difference=value-reference))
    write_csv(OUT/'fig73_bin_backgrounds.csv',bins)
    write_csv(OUT/'fig73_integral_check.csv',summary)
    write_csv(OUT/'fig73_process_differences.csv',processes)
    return summary

def prepare_helvetica():
    # This Matplotlib version cannot subset a macOS TTC for a Type-42 PDF.
    # Extract its existing faces unchanged to temporary TTFs; no font glyphs
    # or system files are modified, and the generated PDFs embed the faces.
    from fontTools.ttLib import TTCollection
    collection=Path('/System/Library/Fonts/Helvetica.ttc')
    cache=ROOT/'tmp/ch7_fonts';cache.mkdir(exist_ok=True)
    font_manager.fontManager.ttflist=[f for f in font_manager.fontManager.ttflist if Path(f.fname)!=collection]
    for i,font in enumerate(TTCollection(str(collection)).fonts):
        dest=cache/f'Helvetica-{i}.ttf'
        if not dest.exists():font.save(str(dest))
        font_manager.fontManager.addfont(str(dest))
    font_manager.fontManager._findfont_cached.cache_clear()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--distributions-only',action='store_true',help='Do not regenerate the standalone scan plot.')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);FIG.mkdir(parents=True,exist_ok=True)
    checks, yields=audit()
    ds=[scan_input(t) for t in ['Res','NonRes']]
    if not args.distributions_only:plot_scans(ds)
    integral_checks=audit_figure_integrals(ds)
    prepare_helvetica()
    with plt.rc_context({'font.sans-serif':['Helvetica'],'mathtext.fontset':'custom',
                         'mathtext.rm':'Helvetica','mathtext.it':'Helvetica:italic','mathtext.bf':'Helvetica:bold'}):
        for d in ds:plot_distribution(d)
    manifest={'inputs_sha256':SOURCES,'method':'Cumulative sum above native MET bin boundaries; sigma_b=0.30*b; pure BSM; no data plotted; no bin rescaling.',
              'scan_diagnostics':[{k:d[k] for k in ['topo','point','path','nominal','single_bin_B']}|
                  {'scan_S_at_nominal':float(d['s_tail'][d['nominal_i']]),'scan_B_at_nominal':float(d['b_tail'][d['nominal_i']]),
                   'scan_Z_at_nominal':float(d['z'][d['nominal_i']]),
                   'best_allowed_threshold':float(d['thresholds'][np.argmax(np.where(d['b_tail']>2,d['z'],-np.inf))]),
                   'numerical_bins_unchanged':True} for d in ds]}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'validated_yields':yields,'scan_diagnostics':manifest['scan_diagnostics'],
                      'figure_7_3_integrals':integral_checks},indent=2))

if __name__=='__main__':
    main()
