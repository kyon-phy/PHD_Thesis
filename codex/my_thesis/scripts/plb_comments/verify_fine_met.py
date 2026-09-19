"""Check exported ROOT drawing objects against the untouched plotting inputs."""
from pathlib import Path
import ast
import hashlib
import json
import sys

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'tmp/pdfs/plb_reply_plot_search/python_packages'))
import numpy as np
import uproot

A = PROJECT / 'output/plb_comments/VRW_NonRes_fine_MET_archive'
P = A / 'original_lxatut'
R = 'VR_0tau1l1b_tch_met_N_minus_1_met'
source = uproot.open(P / 'fit_taunub_N_minus_1_histos.root')
plot_source = uproot.open(P / f'{R}.root')
band = plot_source[f'Graph_from_{R}_Dijet']
groups = {
    'ttbar': ['ttbar_dilep', 'ttZ'],
    'SingleTop': ['SingleTop_tch', 'SingleTop_sch', 'SingleTop_tW'],
    'Zjets': ['Zll', 'Znunu', 'Ztautau', 'Zjet_EWK'],
    'Wjets': ['Wlnu', 'Wtaunu_METTAU', 'Wtaunu_HF'],
    'Diboson': ['Diboson', 'Diboson_semiLep'],
    'Dijet': ['Dijet'],
}
def read(name):
    return source[f'{R}/{name}/nominal/{R}_{name}']

samples = {k: np.sum([read(s).values() for s in members], axis=0) for k, members in groups.items()}
total = np.sum(list(samples.values()), axis=0)
data = read('Data').values()
edges = read('Data').axis().edges()
assert np.array_equal(edges, np.arange(0, 1001, 25))
assert data.sum() == 176 and data[17] == 17
np.testing.assert_allclose(total, band.member('fY'), rtol=0, atol=1e-13)
np.testing.assert_allclose(total, plot_source['h_tot_postFit'].values(), rtol=0, atol=1e-13)
yaml_total = {line.strip().replace('- ', '').split(':', 1)[0]: ast.literal_eval(line.split(':', 1)[1])
              for line in (P / f'{R}_prefit.yaml').read_text().split('Total:')[1].splitlines() if ': [' in line}
np.testing.assert_array_equal(band.member('fY'), yaml_total['Yield'])
np.testing.assert_array_equal(band.member('fEYhigh'), yaml_total['UncertaintyUp'])
np.testing.assert_array_equal(-band.member('fEYlow'), yaml_total['UncertaintyDown'])
exports = []
for folder, stem in [('modified', 'paper_style'), ('reconstructed', 'ROOT_reconstructed')]:
    path = A / folder / f'VRW_NonRes_MET_25GeV_{stem}_verification.root'
    out = uproot.open(path)
    for name, values in samples.items():
        np.testing.assert_allclose(out[name].values(), values, rtol=0, atol=1e-13)
    np.testing.assert_array_equal(out['Data'].values(), data)
    for field in ['fX', 'fY', 'fEXlow', 'fEXhigh', 'fEYlow', 'fEYhigh']:
        np.testing.assert_array_equal(out['plotted_uncertainty'].member(field), band.member(field))
    mask = data > 0
    np.testing.assert_array_equal(out['data_points'].member('fY'), data[mask])
    np.testing.assert_allclose(out['data_ratio'].member('fY'), data[mask]/total[mask], rtol=0, atol=1e-12)
    exports.append(str(path.relative_to(A)))
record = {
    'correction': 'Supersedes the previous erroneous *_orig reconstruction. Uses the nominal histograms and saved plotted uncertainty graph, without editing their bin contents.',
    'source_histogram_key': f'{R}/<sample>/nominal/{R}_<sample>',
    'uncertainty_source': f'{R}.root:Graph_from_{R}_Dijet',
    'source_files_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'fit_taunub_N_minus_1_histos.root', P/f'{R}.root', P/f'{R}_prefit.yaml']},
    'group_members': groups,
    'bin_edges_GeV': edges.tolist(), 'data': data.tolist(),
    'samples': {k: v.tolist() for k,v in samples.items()}, 'total_background': total.tolist(),
    'plotted_uncertainty_up': band.member('fEYhigh').tolist(),
    'plotted_uncertainty_down': band.member('fEYlow').tolist(),
    'checks': {'number_of_bins':40, 'data_sum': float(data.sum()), 'background_sum':float(total.sum()),
               'data_425_450':float(data[17]), 'background_425_450':float(total[17]),
               'uncertainty_425_450':float(band.member('fEYhigh')[17]),
               'last_bin_single_top':float(samples['SingleTop'][-1]), 'last_bin_total':float(total[-1]),
               'last_bin_uncertainty':float(band.member('fEYhigh')[-1]),
               'ROOT_and_YAML_agree_all_40_bins':True, 'exported_graph_coordinates_verified':True},
    'verified_exports': exports,
    'note': 'Dijet nominal contains the pre-existing TREx floor 1e-6/bin. Its legend is hidden but the values remain in the stack. No rebinning, smoothing or fit is performed.'
}
(A/'histogram_values_unchanged.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record['checks'],indent=2))
