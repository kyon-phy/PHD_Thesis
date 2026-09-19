"""Read the requested noWeights_BSM curves from checksum-verified CERN inputs.

First reproduce the existing comb curve, using the existing bin edges and
MergeUnderOverFlow convention. Apply exactly that mapping to the requested
BSM benchmark, without rescaling or negative-bin correction.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import uproot
import yaml
from restyle_eps import ROOT, SOURCE

INPUT = ROOT / 'data/ch7/signal_noWeights_v3'
OUTPUT = ROOT / 'output/ch7/figure_audit/bsm_signal_bins.json'
SUFFIX = {'InvM': 'InvM', 'met': 'met', 'mT': 'mT', 'tau_pT': 'tau_pT',
          'nlightjets': 'nLightJets', 'dphi': 'dphi_taumet'}
POINTS = {'Res': 'MU1500_gU1_5_23L0_6', 'NonRes': 'MU2500_gU2_5_23L1_0'}
REFERENCE_POINTS = {'Res': 'MU1500_gU1_5_23L0_6', 'NonRes': 'MU3000_gU2_5_23L1_0'}


def merge_to_edges(values_with_flow, source_edges, target_edges):
    """Sum whole bins only, then fold the under/overflow into the end bins."""
    indices = []
    for edge in target_edges:
        matches = np.flatnonzero(np.isclose(source_edges, edge, atol=1e-10, rtol=0))
        assert len(matches) == 1, (source_edges, edge)
        indices.append(matches[0])
    assert all(j > i for i, j in zip(indices[:-1], indices[1:]))
    a = np.asarray(values_with_flow)
    values = np.array([a[i+1:j+1].sum() for i, j in zip(indices[:-1], indices[1:])])
    values[0] += a[:indices[0]+1].sum()
    values[-1] += a[indices[-1]+1:].sum()
    return values


def main():
    sources = {Path(s['local_path']).name: s
               for s in json.loads((INPUT / 'source_manifest.json').read_text())}
    for name, source in sources.items():
        assert hashlib.sha256((INPUT / name).read_bytes()).hexdigest() == source['sha256']
    records = []
    for cat, point in POINTS.items():
        reference = REFERENCE_POINTS[cat]
        files = {c: uproot.open(INPUT / f'{reference}_noWeights_{c}.root')
                 for c in ['BSM', 'inf', 'comb']}
        plotted_file = uproot.open(INPUT / f'{point}_noWeights_BSM.root')
        for var, suffix in SUFFIX.items():
            region = f'SR_1tau0l1b_loose_{cat}_{var}_N_minus_1'
            key = f'NOSYS/{suffix}_{region}'
            yp = SOURCE / f'{region}_{suffix}_prefit.yaml'
            y = yaml.safe_load(yp.read_text())
            edges = y['Figure'][0]['BinEdges']
            hists = {c: f[key] for c, f in files.items()}
            source_edges = hists['BSM'].axis().edges()
            for h in hists.values():
                np.testing.assert_allclose(h.axis().edges(), source_edges, atol=1e-12)
            values = {c: merge_to_edges(h.values(flow=True), source_edges, edges)
                      for c, h in hists.items()}
            variances = {c: merge_to_edges(h.variances(flow=True), source_edges, edges)
                         for c, h in hists.items()}
            original = np.asarray(y['Samples'][0]['Yield'], float)
            np.testing.assert_allclose(values['comb'], original, rtol=1e-12, atol=1e-12)
            raw_difference = (hists['comb'].values(flow=True)
                              - hists['BSM'].values(flow=True) - hists['inf'].values(flow=True))
            np.testing.assert_allclose(raw_difference, 0, atol=1e-12)
            np.testing.assert_allclose(variances['comb'], variances['BSM'] + variances['inf'],
                                       rtol=1e-12, atol=1e-12)
            plotted_hist = plotted_file[key]
            np.testing.assert_allclose(plotted_hist.axis().edges(), source_edges, atol=1e-12)
            plotted_values = merge_to_edges(plotted_hist.values(flow=True), source_edges, edges)
            plotted_variances = merge_to_edges(plotted_hist.variances(flow=True), source_edges, edges)
            assert np.all(plotted_values >= 0), (cat, var)
            records.append(dict(
                target=f'SR1b_{cat}_{var}', sample=f'{point}_noWeights_BSM',
                mass_TeV=float(point.split('_')[0][2:])/1000,
                source=sources[f'{point}_noWeights_BSM.root'], object=key,
                reference_point=reference,
                comparison_sources={c: sources[f'{reference}_noWeights_{c}.root']
                                    for c in ['BSM', 'comb', 'inf']},
                comparison_yaml=str(yp), edges=edges, source_edges=source_edges.tolist(),
                values={'BSM':plotted_values.tolist()},
                variances={'BSM':plotted_variances.tolist()},
                sums={'BSM':float(plotted_values.sum())},
                reference_values={c: v.tolist() for c, v in values.items()},
                reference_variances={c: v.tolist() for c, v in variances.items()},
                max_comb_yaml_difference=float(np.max(np.abs(values['comb'] - original))),
                max_raw_comb_minus_bsm_minus_inf=float(np.max(np.abs(raw_difference))),
                flow_handling='Fold underflow/overflow and excluded edge bins into first/last displayed bin',
                additional_signal_scale=1.0))
            print(f'{cat:6} {var:10} {point}_noWeights_BSM={plotted_values.sum():.9f}')
        for f in files.values():
            f.close()
        plotted_file.close()
    OUTPUT.write_text(json.dumps(records, indent=2))
    print('PASS: original reference comb curves reproduce YAML; requested BSM curves read without rescaling.')


if __name__ == '__main__':
    main()
