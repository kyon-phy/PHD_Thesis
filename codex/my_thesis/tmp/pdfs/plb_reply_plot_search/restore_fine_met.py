"""Re-export the recovered 25 GeV ROOT histograms, without digitising the JPEG."""
from pathlib import Path
import hashlib
import json
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter
import numpy as np
from scipy.stats import chi2
import uproot

WORK = Path(__file__).resolve().parents[3]
ROOT = Path(__file__).resolve().parent
OUT = WORK / 'output/pdf'
AUDIT = WORK / 'output/plb_comments/fine_met_recovery'
OUT.mkdir(parents=True, exist_ok=True)
AUDIT.mkdir(parents=True, exist_ok=True)
source = ROOT / 'remote_fine/fit_taunub_N_minus_1_histos.root'
if not source.exists():
    source = ROOT / 'fit_taunub_N_minus_1_histos.root'
assert source.exists()
f = uproot.open(source)
region = 'VR_0tau1l1b_tch_met_N_minus_1_met'
groups = {
    'ttbar': ['ttbar_dilep', 'ttZ'],
    'SingleTop': ['SingleTop_tch', 'SingleTop_sch', 'SingleTop_tW'],
    'Z+jets': ['Zll', 'Znunu', 'Ztautau', 'Zjet_EWK'],
    'W+jets': ['Wlnu', 'Wtaunu_METTAU', 'Wtaunu_HF'],
    'Diboson': ['Diboson', 'Diboson_semiLep'],
    'Dijet': ['Dijet'],
}

def read(name):
    h = f[f'{region}/{name}/nominal/{region}_{name}_orig']
    return h.values().copy(), h.variances().copy(), h.axis().edges().copy()

data, _, edges = read('Data')
assert np.array_equal(edges, np.arange(0, 1001, 25))
assert data.sum() == 176 and data[17] == 17
samples = {}
variance = np.zeros_like(data)
for name, members in groups.items():
    values = np.zeros_like(data)
    sample_variance = np.zeros_like(data)
    for member in members:
        v, var, e = read(member)
        assert np.array_equal(e, edges)
        values += v
        sample_variance += var
    samples[name] = values
    variance += sample_variance

total = np.sum(list(samples.values()), axis=0)
mc_error = np.sqrt(variance)
assert abs(total.sum() - 146.61439801472824) < 1e-9
# ROOT's kPoisson convention: central 68.268949% Garwood interval.
alpha = 1 - 0.6826894921370859
lower = np.zeros_like(data)
positive = data > 0
lower[positive] = chi2.ppf(alpha / 2, 2 * data[positive]) / 2
upper = chi2.ppf(1 - alpha / 2, 2 * (data + 1)) / 2
data_errors = np.vstack((data - lower, upper - data))
centres = (edges[1:] + edges[:-1]) / 2

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 12, 'axes.labelsize': 14, 'xtick.labelsize': 12,
    'ytick.labelsize': 12, 'mathtext.fontset': 'stixsans',
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.linewidth': 1.0,
    'hatch.linewidth': 0.45,
})
fig = plt.figure(figsize=(8.4, 6.5))
ax = fig.add_axes([0.13, 0.31, 0.84, 0.65])
ratio_ax = fig.add_axes([0.13, 0.115, 0.84, 0.195], sharex=ax)
colours = {'ttbar': '#4393e2', 'SingleTop': '#c52200',
           'Z+jets': '#812bb9', 'W+jets': '#747783',
           'Diboson': '#ffad00', 'Dijet': '#b3a86b'}
# Match the old figure's stack order; preserve signed MC contents.
bottom = np.zeros_like(data)
for name in reversed(list(groups)):
    ax.stairs(bottom + samples[name], edges, baseline=bottom,
              fill=True, facecolor=colours[name], linewidth=0)
    bottom += samples[name]
assert np.allclose(bottom, total, rtol=0, atol=1e-12)
band_colour = '#6868f4'
ax.stairs(total + mc_error, edges, baseline=np.maximum(total - mc_error, 1e-8),
          fill=True, facecolor='none', edgecolor=band_colour,
          hatch='////', linewidth=0)
# As in the original plot, do not draw empty observed bins as upper limits.
ax.errorbar(centres[positive], data[positive], yerr=data_errors[:, positive],
            fmt='o', markersize=4.8, color='black', capsize=0,
            elinewidth=1.1, zorder=5)
ax.set_yscale('log')
ax.set_xlim(0, 1000)
ax.set_ylim(0.1, 1e5)
ax.set_ylabel('Events', loc='top', labelpad=9)
ax.yaxis.set_major_locator(LogLocator(base=10, numticks=7))
ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * .1, numticks=100))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.tick_params(axis='x', labelbottom=False)
ax.text(0.035, .94, r'$\bf{\it{ATLAS}}$ Internal', transform=ax.transAxes, fontsize=14)
ax.text(0.035, .865, r'$\sqrt{s}=13$ TeV, $140\ \mathrm{fb}^{-1}$', transform=ax.transAxes)
ax.text(0.035, .795, r'VRW-NonRes, $0\tau\,1\ell\,1b$', transform=ax.transAxes)
ax.text(0.035, .725, 'Pre-fit', transform=ax.transAxes)

# Keep the original yields visible, with clean alignment.
legend_names = [('Data', 'Data', int(data.sum())),
                ('ttbar', r'$t\bar{t}$', samples['ttbar'].sum()),
                ('SingleTop', 'Single top', samples['SingleTop'].sum()),
                ('Z+jets', r'$Z$+jets', samples['Z+jets'].sum()),
                ('W+jets', r'$W$+jets', samples['W+jets'].sum()),
                ('Diboson', 'Diboson', samples['Diboson'].sum()),
                ('Dijet', 'Dijet', samples['Dijet'].sum()),
                ('Total', 'Total', total.sum()),
                ('Uncertainty', 'Uncertainty', None)]
for i, (key, label, value) in enumerate(legend_names):
    y = .94 - i * .068
    if key == 'Data':
        ax.plot([.61, .65], [y + .004, y + .004], transform=ax.transAxes, color='black', lw=1)
        ax.plot(.63, y + .004, 'o', transform=ax.transAxes, color='black', markersize=4.8)
    elif key in colours:
        ax.add_patch(plt.Rectangle((.605, y - .019), .047, .043,
                     transform=ax.transAxes, facecolor=colours[key], edgecolor='none'))
    elif key == 'Uncertainty':
        ax.add_patch(plt.Rectangle((.605, y - .019), .047, .043,
                     transform=ax.transAxes, facecolor='none', edgecolor=band_colour,
                     hatch='////', linewidth=0))
    ax.text(.675, y, label, transform=ax.transAxes, va='center', fontsize=11.5)
    if value is not None:
        ax.text(.965, y, f'{value:.1f}', transform=ax.transAxes, va='center', ha='right', fontsize=11.5)

valid = total > 0
relative = np.divide(mc_error, total, out=np.zeros_like(total), where=valid)
ratio_ax.stairs(1 + relative, edges, baseline=1 - relative,
                fill=True, facecolor='none', edgecolor=band_colour, hatch='////', linewidth=0)
ratio_ax.axhline(1, color='black', linestyle=':', linewidth=1.3)
ratios = np.divide(data, total, out=np.zeros_like(data), where=valid)
errors_ratio = np.divide(data_errors, total[None, :], out=np.zeros_like(data_errors), where=valid[None, :])
shown = positive & valid & (ratios <= 2)
ratio_ax.errorbar(centres[shown], ratios[shown], yerr=errors_ratio[:, shown],
                  fmt='o', color='black', markersize=4.8, capsize=0, elinewidth=1.1, zorder=5)
offscale = positive & valid & (ratios > 2)
for x, r, err in zip(centres[offscale], ratios[offscale], errors_ratio[0, offscale]):
    if r - err < 2:
        ratio_ax.vlines(x, max(0, r - err), 1.97, color='black', linewidth=1.1, zorder=5)
    ratio_ax.plot(x, 1.88, '^', markersize=6, markerfacecolor='white',
                   markeredgecolor=band_colour, markeredgewidth=1.1, zorder=6)
ratio_ax.set_ylim(0, 2)
ratio_ax.set_yticks([0, .5, 1, 1.5])
ratio_ax.yaxis.set_minor_locator(MultipleLocator(.1))
ratio_ax.set_ylabel('Data / Bkg.', labelpad=9)
ratio_ax.set_xlabel(r'$E_{\mathrm{T}}^{\mathrm{miss}}$ [GeV]', loc='right', labelpad=9)
ratio_ax.xaxis.set_major_locator(MultipleLocator(100))
ratio_ax.xaxis.set_minor_locator(MultipleLocator(25))
for a in (ax, ratio_ax):
    a.tick_params(which='both', direction='in', top=True, right=True)
    a.tick_params(which='major', length=6)
    a.tick_params(which='minor', length=3)

pdf = OUT / 'VRW_NonRes_fine_met_restored.pdf'
png = OUT / 'VRW_NonRes_fine_met_restored.png'
fig.savefig(pdf, metadata={'Title': 'VRW-NonRes MET: recovered original 25 GeV histograms',
                          'Subject': 'Pre-fit; ROOT histogram contents and Sumw2 preserved'})
fig.savefig(png, dpi=450)
plt.close(fig)
record = {
    'source_host': 'codex_lxatut / lxatut3.cern.ch',
    'source_path': '/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_N_minus_1/Histograms/fit_taunub_N_minus_1_histos.root',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'histogram_region': region,
    'histogram_suffix': '_orig',
    'group_members': groups,
    'bin_edges_GeV': edges.tolist(),
    'data': data.tolist(),
    'samples': {k: v.tolist() for k, v in samples.items()},
    'total_background': total.tolist(),
    'mc_statistical_error': mc_error.tolist(),
    'data_error_low': data_errors[0].tolist(),
    'data_error_high': data_errors[1].tolist(),
    'data_interval': 'central Garwood 68.26894921370859 percent',
    'checks': {'data_sum': float(data.sum()), 'background_sum': float(total.sum()),
               'data_425_450': float(data[17]), 'background_425_450': float(total[17]),
               'background_stat_error_425_450': float(mc_error[17])},
    'rendering': 'Original 0-1000 GeV bin edges; all values unchanged; no smoothing or interpolation. Signed MC bins retained. Data bins with zero counts are not drawn, matching the original plot. Ratios above the original upper limit of 2 are indicated with upward triangles. No JPEG content was used to infer bin values.',
    'scope': 'Restoration of the historical diagnostic plot; not a new final-model fit.',
}
(AUDIT / 'restored_histograms.json').write_text(json.dumps(record, indent=2) + '\n')
if source.resolve() != (AUDIT / source.name).resolve():
    shutil.copy2(source, AUDIT / source.name)
if Path(__file__).resolve() != (AUDIT / 'restore_fine_met.py').resolve():
    shutil.copy2(__file__, AUDIT / 'restore_fine_met.py')
print(json.dumps({'pdf': str(pdf), 'png': str(png), 'checks': record['checks']}, indent=2))
