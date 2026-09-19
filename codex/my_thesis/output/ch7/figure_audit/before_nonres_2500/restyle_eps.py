"""Restyle copied ROOT EPS plots, preserving the background and uncertainty.

SR1b signals use the explicitly requested noWeights_BSM ROOT values, prepared
by prepare_bsm_signals.py. Only that signal path is replaced. All other top-pad
geometry is protected by a token hash. Data and the ratio pad are removed;
the coordinate system and background/uncertainty paths are never scaled.
"""
from pathlib import Path
import re, hashlib, json, subprocess, math

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('/Users/zang/Desktop/fit_results/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots')
OUT = ROOT / 'Figs/CH7'
TEXT = re.compile(r'gsave\s+[^\n]*?\([^\n]*?\) show (?:gr )?NC gr')

def digest(s):
    return hashlib.sha256(s.encode()).hexdigest()

def drawing_signature(s):
    # Text is not histogram geometry. Ignore whitespace introduced by ROOT.
    return digest(' '.join(TEXT.sub('', s).split()))


def signal_path_span(body):
    """Return only the final dashed histogram path, not its drawing style."""
    # Full EPS files also contain a dashed signal swatch in the legend.
    body = body.split('\nblack[ ] 0 sd 3 lw\ngsave 0 259 t', 1)[0]
    signal = list(re.finditer(r'c\[\s+12 12\s*\] 0 sd', body))[-1]
    path = re.search(r'c\s+([\d.]+\s+[\d.]+\s+m[\d.\sXYm-]+)\s+s',
                     body[signal.end():])
    assert path
    return signal.end() + path.start(1), signal.end() + path.end(1)


def without_signal_path(body):
    start, end = signal_path_span(body)
    return body[:start] + 'SIGNAL_PATH' + body[end:]


def replace_signal_path(body, record):
    """Draw physical BSM bin contents on the existing logarithmic frame."""
    edges, values = record['edges'], record['values']['BSM']
    x = [238 + 1945 * (edge-edges[0]) / (edges[-1]-edges[0]) for edge in edges]
    # Only rendering is clipped at the existing y-axis limits. The manifest
    # retains the unmodified physical yield, including zero/sub-range bins.
    y = [456 + 366 * math.log10(min(100, max(.1, v))/.1) for v in values]
    commands = [f'{x[0]:.5f} {y[0]:.5f} m']
    for i in range(len(values)):
        commands.append(f'{x[i+1]-x[i]:.5f} X')
        if i+1 < len(values):
            commands.append(f'{y[i+1]-y[i]:.5f} Y')
    start, end = signal_path_span(body)
    return body[:start] + ' '.join(commands) + body[end:]

def two_column_legend(s):
    """Translate the original text and swatches, retaining ROOT's typography."""
    blocks = list(TEXT.finditer(s))
    starts = [0]
    for label in ['(W+jets)', '(Diboson)']:
        starts.append(next(m.start() for m in blocks if label in m.group()))
    dib = starts[-1]
    starts.append(next(m.start() for m in blocks
                       if m.start() > dib and '(t) show' in m.group()))
    starts.append(next(m.start() for m in blocks
                       if '(single )' in m.group()) )
    # ROOT emits the italic t before the word 'single'. Include both blocks.
    starts[-1] = max(m.start() for m in blocks if m.start() < starts[-1])
    for label in ['(Z+jets)', '(Uncertainty)']:
        starts.append(next(m.start() for m in blocks if label in m.group()))
    axes = re.search(r'black 1 1 1 c black 3 lw 238 456 m', s)
    assert axes
    starts.append(axes.start())
    # Row-major order: U1/W, diboson/ttbar, single t/Z, uncertainty.
    old_x = [1410.2, 1874.57, 1079.73, 1410.2, 1874.57, 1079.73, 1410.2]
    old_y = [1447.24, 1447.24, 1370.32, 1370.32, 1370.32, 1293.4, 1293.4]
    result = []
    for i in range(7):
        x = 1150 if i % 2 == 0 else 1750
        y = 1447.24 - 76.92 * (i // 2)
        result.append(f'gsave {x-old_x[i]:.5f} {y-old_y[i]:.5f} t black[ ] 0 sd 3 lw\n'
                      + s[starts[i]:starts[i+1]] + '\ngrestore\n')
    return ''.join(result) + s[axes.start():]


def selection_arrow(edges, cut, direction):
    """Copy the paper's L-shaped cut marker, mirrored for an upper bound.

    Geometry measured from figures/Aux/post_fit_plots/SR1b_Res_InvM.pdf:
    2.5 pt stroke; vertical stem from the axis; 40 pt horizontal reach;
    filled head 12.5 pt long and 11 pt high. EPS units are quarter points.
    """
    x = 238 + 1945 * (cut - edges[0]) / (edges[-1] - edges[0])
    y = 1185
    tip = x + direction * 160
    return (f'\n% CH7 final selection: {cut}, direction {direction}\n'
            '% Paper L-shaped cut marker; original histogram geometry untouched\n'
            'gsave 1 0 0 c[ ] 0 sd 10 lw\n'
            f'{x:.5f} 449 m 0 741 d s\n'
            f'{x-direction*3:.5f} {y} m {direction*123} 0 d s\n'
            f'{tip:.5f} {y} m {-direction*50} 22 d 0 -44 d closepath f\n'
            'grestore\n')


def restyle(name, target, region, dimensionless=False, cut=None, direction=1,
            bsm_record=None):
    source = SOURCE / name
    original = source.read_text()
    s = original
    top = re.search(r'1 1 1 c 1945 1098\s+238 456 bf', s)
    assert top, name
    # The data graph follows the final (dashed) signal histogram.
    atlas = s.index('(ATLAS)')
    labelstart = s.rfind('gsave', 0, atlas)
    top_part = s[top.start():labelstart]
    signal = list(re.finditer(r'c\[\s+12 12\s*\] 0 sd', top_part))[-1]
    data = re.search(r's black\[\s*\] 0 sd', top_part[signal.end():])
    assert data, name
    stop = signal.end() + data.start() + 1
    protected = top_part[:stop]
    removed_data = top_part[stop:]
    assert 'm20' in removed_data, name
    body = protected
    if dimensionless:
        # ROOT right-aligns its original rotated title at y=1554. Shortening
        # the title without moving its origin incorrectly centres 'Events'.
        body = body.replace('92.502 1105.37 t 90 r /Helvetica findfont 62 sf 0 0 m (Events / 100 GeV)',
                            '92.502 1554 t 90 r /Helvetica findfont 62 sf (Events) stringwidth pop neg 0 m (Events)')
    assert drawing_signature(body) == drawing_signature(protected)
    if bsm_record is not None:
        body = replace_signal_path(body, bsm_record)
        assert drawing_signature(without_signal_path(body)) == drawing_signature(without_signal_path(protected))

    # Only the original bottom x labels (numbers and title), before the top
    # border of the ratio frame, are retained. Shift by exactly 456 - 197.
    xt = []
    for m in TEXT.finditer(s[:top.start()]):
        if '2268 456 0 0 C' not in m.group():
            continue
        pos = re.search(r'C ([\d.]+) ([\d.]+) t', m.group())
        if pos and float(pos[2]) < 160:
            xt.append(m.group().replace('2268 456 0 0 C', '2268 1630 0 0 C'))
    assert xt, name
    if target.startswith('SR1b_') and any(target.endswith('_'+v)
                                        for v in ['tau_pT','nlightjets','dphi']):
        # The paper's main mathematical axis font is 95 EPS units (23.75 pt).
        # These three source titles retained ROOT's smaller default. Transform
        # text blocks alone, about the right edge, leaving all ticks untouched.
        factor=95/57.0348
        for i, block in enumerate(xt):
            pos=re.search(r'C ([\d.]+) ([\d.]+) t', block)
            if float(pos[2]) >= 130:
                continue
            x=2183+(float(pos[1])-2183)*factor
            y=57.4311+(float(pos[2])-48.4311)*factor
            block=block[:pos.start()]+f'C {x:.5f} {y:.5f} t'+block[pos.end():]
            block=re.sub(r'findfont ([\d.]+) sf',
                         lambda m:f'findfont {float(m[1])*factor:.5f} sf',block)
            xt[i]=block
    xlabels = 'gsave 0 259 t\n' + '\n'.join(xt) + '\ngrestore\n'
    xlabels = xlabels.replace('(F) show', '(f) show')

    labels = s[labelstart:]
    labelblocks = list(TEXT.finditer(labels))
    a = next(m for m in labelblocks if '(ATLAS)' in m.group())
    b = next(m for m in labelblocks if '( = 13 TeV, 140 fb)' in m.group())
    ay = float(re.search(r'C [\d.]+ ([\d.]+) t', a.group())[1])
    by = float(re.search(r'C [\d.]+ ([\d.]+) t', b.group())[1])
    delta = ay-by
    sqrtstart = next(m.start() for m in labelblocks if '(\\2551)' in m.group())
    fitstart = next(m.start() for m in labelblocks if '(Background' in m.group())
    sqrtblock = labels[sqrtstart:fitstart]
    oldregion = next(m for m in labelblocks if 'Loose ' in m.group() or '(SR0b' in m.group())
    oldy = float(re.search(r'C [\d.]+ ([\d.]+) t', oldregion.group())[1])
    regionblock = re.sub(r'\([^\n]*\) show', '(' + region + ') show', oldregion.group())
    siglegend = next(m.start() for m in labelblocks if ' TeV\\)' in m.group())
    legend_and_axes = labels[siglegend:]
    if target.startswith('SR1b_'):
        legend_and_axes = two_column_legend(legend_and_axes)
    labels = ('black[ ] 0 sd 3 lw\n'
              + f'gsave 0 {delta:.5f} t\n' + sqrtblock + '\ngrestore\n'
              + f'gsave 0 {by-oldy:.5f} t\n' + regionblock + '\ngrestore\n'
              + legend_and_axes)
    header = s[:s.index('newpath  gsave')]
    # Crop whitespace below the relocated x title. This changes page extent,
    # not the scale of the remaining plot (all coordinates stay unchanged).
    header = re.sub(r'%%BoundingBox:.*', '%%BoundingBox: 0 65 567 407', header)
    result = header + 'newpath gsave .25 .25 scale gsave 0 0 t black[ ] 0 sd 3 lw\n'
    result += body + '\nblack[ ] 0 sd 3 lw\n' + xlabels + labels
    yaml_source=source.with_name(source.stem+'_prefit.yaml')
    yaml_text=yaml_source.read_text()
    bin_edges=json.loads(re.search(r'BinEdges: (\[.*\])',yaml_text)[1])
    if cut is not None:
        arrow = selection_arrow(bin_edges, cut, direction)
        # Insert within the scaled plot context, before ROOT closes the page.
        close = re.search(r'gr\s+gr\s+showpage', result)
        assert close, target
        end = close.start()
        result = result[:end] + arrow + result[end:]
    assert 'm20' not in result[result.index('%%EndSetup'):]
    assert not any(x in result for x in ['(ATLAS)', '(Data)', 'Data /', '(Preliminary)', '(Internal)'])
    OUT.mkdir(exist_ok=True)
    dest = OUT / (target + '.eps')
    dest.write_text(result)
    subprocess.run(['/usr/local/bin/gs','-q','-dBATCH','-dNOPAUSE','-dEPSCrop',
                    '-sDEVICE=pdfwrite','-dCompatibilityLevel=1.5',
                    '-sOutputFile='+str(dest.with_suffix('.pdf')), str(dest)], check=True)
    total=json.loads(re.search(r'Total:\s+- Yield: (\[.*\])',yaml_text)[1])
    return dict(source=str(source), target=str(dest), source_sha256=digest(original),
                edited_sha256=digest(result), protected_drawing_sha256=drawing_signature(protected),
                preserved_top_pad=bsm_record is None,
                preserved_background_and_uncertainty=True,
                background_drawing_sha256=drawing_signature(without_signal_path(body)),
                signal_replaced=bsm_record is not None,
                signal_source=bsm_record,
                removed_data=True, removed_ratio_panel=True,
                x_label_translation=259, plot_scaling_change=1,
                numerical_source=str(yaml_source), bin_edges=bin_edges,
                original_background_bin_yields=total,
                region=region, y_axis=('Events' if dimensionless else 'Events / 100 GeV'),
                legend_columns=2 if target.startswith('SR1b_') else 3,
                final_cut_arrow=cut, arrow_direction=direction if cut is not None else None,
                arrow_style='paper L-shaped marker' if cut is not None else None)

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--sr1b-only', action='store_true')
    args=parser.parse_args()
    manifest=[]
    signal_records={r['target']:r for r in json.loads(
        (ROOT/'output/ch7/figure_audit/bsm_signal_bins.json').read_text())}
    # Fail rather than drawing a stale cache after the source ROOT changes.
    for record in signal_records.values():
        source=record['source']
        assert hashlib.sha256(Path(source['local_path']).read_bytes()).hexdigest()==source['sha256']
    suffixes={'InvM':'InvM','met':'met','mT':'mT','tau_pT':'tau_pT','nlightjets':'nLightJets','dphi':'dphi_taumet'}
    for cat in ['Res','NonRes']:
        for var,suffix in suffixes.items():
            # Integer jet counts fill bins [n,n+1): the boundaries are 4 and 2.
            cuts={'Res':{'InvM':800,'met':200,'mT':200,'tau_pT':200,'nlightjets':4},
                  'NonRes':{'met':400,'mT':600,'tau_pT':200,'nlightjets':2,'dphi':1.2}}
            manifest.append(restyle(f'SR_1tau0l1b_loose_{cat}_{var}_N_minus_1_{suffix}.eps',
                                    f'SR1b_{cat}_{var}',f'Loose SR1b-{cat}',
                                    var in ['nlightjets','dphi'], cuts[cat].get(var),
                                    -1 if var=='nlightjets' else 1,
                                    signal_records[f'SR1b_{cat}_{var}']))
    sr0b=[] if args.sr1b_only else [('Res','InvM','Mtaujet'),('NonRes','mT','mT_tau_met')]
    for cat,var,suffix in sr0b:
        manifest.append(restyle(f'SR_1tau0l0b_{cat}_{var}_N_minus_1_{suffix}.eps',
                                f'SR0b_{cat}_{var}',f'SR0b-{cat}'))
    manifest_path=ROOT/'output/ch7/figure_manifest.json'
    if args.sr1b_only and manifest_path.exists():
        manifest.extend(x for x in json.loads(manifest_path.read_text())
                        if Path(x['target']).name.startswith('SR0b_'))
    manifest_path.write_text(json.dumps(manifest,indent=2))
    print(f'Created {12 if args.sr1b_only else len(manifest)} EPS/PDF pairs; SR1b signals use noWeights_BSM; background/uncertainty drawing hashes match.')
