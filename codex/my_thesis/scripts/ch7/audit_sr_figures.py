"""Read-only numerical/provenance audit for CH7 Figures 7.3 and 7.4.

Uses nominal (not _orig) TH1 objects, grouped as in the plotting config.
The ROOT uncertainty graph is compared to the exported YAML independently.
The old note's raster panels are not treated as exact numerical sources.
"""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
import uproot
import yaml
from restyle_eps import SOURCE, ROOT, TEXT, drawing_signature, without_signal_path, signal_path_span
from prepare_bsm_signals import merge_to_edges

FIT = SOURCE.parent
OLD = FIT.parent / 'fit_taunub_nom_1l_allVR_BONLY_MU1500_gU1_5_23L0_6_alldecay_corrected_N_minus_1'
OLD2500 = FIT.parent / 'fit_taunub_nom_1l_allVR_BONLY_MU2500_gU2_5_23L1_0_alldecay_corrected_N_minus_1'
NOTE = ROOT.parents[2] / 'internal_notes/ANA_EXOT_2025_06_INT1/figures/SR_Optimization'
OUT = ROOT / 'output/ch7/figure_audit'
SUFFIX = {'InvM':'InvM','met':'met','mT':'mT','tau_pT':'tau_pT',
          'nlightjets':'nLightJets','dphi':'dphi_taumet'}
GROUPS = {'W+jets':['Wjets'], 'Diboson':['Diboson'], '#it{t#bar{t}}':['ttbar'],
          'single #it{t}':['SingleTop'], 'Z+jets':['Zll','Znunu','Ztautau']}


def read_yaml(path):
    y = yaml.safe_load(path.read_text())
    for s in y['Samples']:
        s['Yield'] = np.asarray(s['Yield'], float)
    return y


def top_geometry(eps, exclude_signal=False):
    start = re.search(r'1 1 1 c 1945 1098\s+238 456 bf', eps).start()
    # New restyling places x labels immediately after the protected top pad.
    end = eps.index('\nblack[ ] 0 sd 3 lw\ngsave 0 259 t', start)
    body=eps[start:end]
    return drawing_signature(without_signal_path(body) if exclude_signal else body)


def path_heights(path, edges):
    """Read the horizontal step heights from a ROOT EPS histogram path."""
    tokens = path.split()
    stack=[]
    segments=[]
    x=y=0
    for token in tokens:
        try:
            stack.append(float(token))
            continue
        except ValueError:
            pass
        if token=='m':
            x,y=stack[-2:];stack=[]
        elif token=='X':
            dx=stack.pop();segments.append((x,x+dx,y));x+=dx
        elif token=='Y':
            y+=stack.pop()
        else:
            raise ValueError(token)
    mids=238+1945*((np.asarray(edges[:-1])+edges[1:])/2-edges[0])/(edges[-1]-edges[0])
    return np.asarray([next(y for x0,x1,y in segments if x0<=mid<=x1) for mid in mids])


def verify_eps_heights(eps, y, bsm_values):
    """Verify actual EPS positions against YAML, allowing ROOT integer rounding."""
    edges=y['Figure'][0]['BinEdges']
    end=eps.index('\nblack[ ] 0 sd 3 lw\ngsave 0 259 t')
    body=eps[:end]
    start,stop=signal_path_span(body)
    checks={'signal':(body[start:stop],bsm_values)}
    colours={'W+jets':'1 0.8 1','Diboson':'1 0.662745 0.054902',
             '#it{t#bar{t}}':'0.247059 0.564706 0.854902',
             'single #it{t}':'0.72549 0.67451 0.439216','Z+jets':'0.580392 0.643137 0.635294'}
    running=np.zeros(len(edges)-1)
    byname={s['Name']:s['Yield'] for s in y['Samples']}
    for name in reversed(list(colours)):
        running=running+byname[name]
        c=re.escape(colours[name]).replace(r'\ ',r'\s+')
        matches=list(re.finditer(c+r'\s+c\s+(\d+\s+\d+\s+m[\d.\sXYm-]+)\s+f',body))
        assert matches, name
        # ROOT can emit an empty baseline polygon before the coloured stack.
        match=max(matches,key=lambda m:len(m[1]))
        checks[name]=(match[1],running.copy())
    deviations={}
    for name,(path,values) in checks.items():
        actual=path_heights(path,edges)
        expected=456+366*np.log10(np.clip(values,0.1,100)/0.1)
        deviation=float(np.max(np.abs(actual-expected)))
        assert deviation<=1.1,(name,deviation)
        deviations[name]=deviation
    return deviations


def main():
    raw_path = FIT/'Histograms'/ (FIT.name.removesuffix('_modified')+'_histos.root')
    raw = uproot.open(raw_path)
    records = []
    bsm_records={r['target']:r for r in json.loads((OUT/'bsm_signal_bins.json').read_text())}
    for cat in ['Res','NonRes']:
        for var, suffix in SUFFIX.items():
            region = f'SR_1tau0l1b_loose_{cat}_{var}_N_minus_1_{suffix}'
            yp = SOURCE/(region+'_prefit.yaml')
            y = read_yaml(yp)
            samples = raw[region].keys(recursive=False, cycle=False)
            signal = next(x for x in samples if x.startswith('MU'))
            edges = y['Figure'][0]['BinEdges']
            errors = {}
            for s in y['Samples']:
                names = [signal] if s['Name'].startswith('#it{U}') else GROUPS[s['Name']]
                hists = [raw[f'{region}/{n}/nominal/{region}_{n}'] for n in names]
                values = sum(h.values() for h in hists)
                for h in hists:
                    np.testing.assert_allclose(h.axis().edges(), edges, atol=1e-12)
                np.testing.assert_allclose(values, s['Yield'], atol=1e-12, rtol=1e-12)
                errors[s['Name']] = float(np.max(np.abs(values-s['Yield'])))
            total = sum(s['Yield'] for s in y['Samples'][1:])
            np.testing.assert_allclose(total,y['Total'][0]['Yield'],rtol=1e-12,atol=1e-12)
            graph_path = FIT/'Histograms'/(region+'.root')
            gf = uproot.open(graph_path)
            graph = next(gf[k] for k in gf.keys() if gf[k].classname=='TGraphAsymmErrors')
            np.testing.assert_allclose(graph.member('fY'),total,atol=1e-12)
            np.testing.assert_allclose(graph.member('fEYhigh'),y['Total'][0]['UncertaintyUp'],atol=1e-12)
            np.testing.assert_allclose(graph.member('fEYlow'),-np.asarray(y['Total'][0]['UncertaintyDown']),atol=1e-12)
            oldtag = 'sch' if cat=='Res' else 'tch'
            oldregion = f'SR_1tau0l1b_loose_{oldtag}_{var}_N_minus_1_{suffix}'
            # Note NonRes a-d: 2.5 TeV; e-f: 1.5 TeV, verified in note PDFs.
            oldbase = OLD2500 if cat=='NonRes' and var in list(SUFFIX)[:4] else OLD
            oldyp = oldbase/'Plots'/(oldregion+'_prefit.yaml')
            old = read_yaml(oldyp)
            note = NOTE/('resonance_plots' if cat=='Res' else 'nonresonance_plots')/(oldregion+'.pdf')
            oldpdf = oldbase/'Plots'/(oldregion+'.pdf')
            exact = note.read_bytes()==oldpdf.read_bytes()
            target = ROOT/'Figs/CH7'/f'SR1b_{cat}_{var}.eps'
            before = OUT/'before_bsm_signal'/target.name
            geometry_before=top_geometry(before.read_text(),exclude_signal=True)
            geometry_after=top_geometry(target.read_text(),exclude_signal=True)
            assert geometry_before==geometry_after
            bsm=bsm_records[target.stem]
            bsm_path=Path(bsm['source']['local_path'])
            assert hashlib.sha256(bsm_path.read_bytes()).hexdigest()==bsm['source']['sha256']
            with uproot.open(bsm_path) as bf:
                h=bf[bsm['object']]
                bsm_values=merge_to_edges(h.values(flow=True),h.axis().edges(),edges)
            np.testing.assert_allclose(bsm_values,bsm['values']['BSM'],atol=1e-12,rtol=1e-12)
            # Whole EPS comparison also protects all annotations and arrows.
            expected=without_signal_path(before.read_text())
            if cat=='NonRes':
                expected=expected.replace('3.0 TeV',f'{bsm["mass_TeV"]:.1f} TeV')
            assert expected == without_signal_path(target.read_text())
            eps_deviations=verify_eps_heights(target.read_text(),y,bsm_values)
            oldbg = np.asarray(old['Total'][0]['Yield'],float)
            oldsig = old['Samples'][0]['Yield']
            records.append(dict(
                panel=f'{cat}_{var}', eps_source=str(SOURCE/(region+'.eps')),
                yaml_source=str(yp), raw_root=str(raw_path), raw_region=region,
                original_comb_signal_object=f'{region}/{signal}/nominal/{region}_{signal}',
                signal_root=str(bsm_path),signal_object=bsm['object'],signal_sample=bsm['sample'],
                uncertainty_root=str(graph_path), uncertainty_object=graph.member('fName'),
                max_sample_root_yaml_difference=errors, all_root_yaml_checks_passed=True,
                background_drawing_sha256=geometry_after, background_and_uncertainty_geometry_unchanged=True,
                all_eps_except_signal_and_mass_label_unchanged=True,
                eps_max_coordinate_error=eps_deviations,
                eps_coordinate_tolerance=1.1,
                background=total.tolist(), signal=bsm_values.tolist(),
                previous_comb_signal=y['Samples'][0]['Yield'].tolist(),
                uncertainty=y['Total'][0]['UncertaintyUp'], edges=edges,
                background_sum=float(total.sum()), signal_sum=float(bsm_values.sum()),
                previous_comb_signal_sum=float(y['Samples'][0]['Yield'].sum()),
                note_pdf=str(note), comparison_yaml=str(oldyp),
                exact_note_pdf_match=exact,
                comparison_status='exact note PDF source' if exact else 'candidate for raster note panel; not exact provenance',
                old_signal_name=old['Samples'][0]['Name'], old_edges=old['Figure'][0]['BinEdges'],
                old_background=oldbg.tolist(), old_signal=oldsig.tolist(),
                old_uncertainty=old['Total'][0]['UncertaintyUp'],
                old_background_sum=float(oldbg.sum()),old_signal_sum=float(oldsig.sum()),
                old_background_components={s['Name']:float(s['Yield'].sum()) for s in old['Samples'][1:]},
                current_background_components={s['Name']:float(s['Yield'].sum()) for s in y['Samples'][1:]},
            ))
    (OUT/'verified_bins_and_provenance.json').write_text(json.dumps(records,indent=2))
    for r in records:
        print(r['panel'], 'BSM ROOT + background YAML + protected geometry PASS',
              f"B {r['old_background_sum']:.6f} -> {r['background_sum']:.6f}",
              f"S {r['old_signal_sum']:.6f} -> {r['signal_sum']:.6f}",
              'exact note source' if r['exact_note_pdf_match'] else 'raster: candidate only')


if __name__=='__main__':
    main()
