"""Restyle copied ROOT EPS plots without regenerating any histogram.

The original top-pad drawing through the last signal path is protected by a
token hash. Only its y-axis title is changed where necessary. Data paths and
the ratio pad are removed, and the original x labels are translated to the
top-pad baseline. The plot coordinate system and bin paths are never scaled.
"""
from pathlib import Path
import re, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('/Users/zang/Desktop/fit_results/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots')
OUT = ROOT / 'Figs/CH7'
TEXT = re.compile(r'gsave\s+[^\n]*?\([^\n]*?\) show (?:gr )?NC gr')

def digest(s):
    return hashlib.sha256(s.encode()).hexdigest()

def drawing_signature(s):
    # Text is not histogram geometry. Ignore whitespace introduced by ROOT.
    return digest(' '.join(TEXT.sub('', s).split()))

def restyle(name, target, region, dimensionless=False):
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
        body = body.replace('(Events / 100 GeV)', '(Events)')
    assert drawing_signature(body) == drawing_signature(protected)

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
    assert 'm20' not in result[result.index('%%EndSetup'):]
    assert not any(x in result for x in ['(ATLAS)', '(Data)', 'Data /', '(Preliminary)', '(Internal)'])
    OUT.mkdir(exist_ok=True)
    dest = OUT / (target + '.eps')
    dest.write_text(result)
    subprocess.run(['/usr/local/bin/gs','-q','-dBATCH','-dNOPAUSE','-dEPSCrop',
                    '-sDEVICE=pdfwrite','-dCompatibilityLevel=1.5',
                    '-sOutputFile='+str(dest.with_suffix('.pdf')), str(dest)], check=True)
    yaml_source=source.with_name(source.stem+'_prefit.yaml')
    yaml_text=yaml_source.read_text()
    bin_edges=json.loads(re.search(r'BinEdges: (\[.*\])',yaml_text)[1])
    total=json.loads(re.search(r'Total:\s+- Yield: (\[.*\])',yaml_text)[1])
    return dict(source=str(source), target=str(dest), source_sha256=digest(original),
                edited_sha256=digest(result), protected_drawing_sha256=drawing_signature(protected),
                preserved_top_pad=True, removed_data=True, removed_ratio_panel=True,
                x_label_translation=259, plot_scaling_change=1,
                numerical_source=str(yaml_source), bin_edges=bin_edges,
                original_background_bin_yields=total,
                region=region, y_axis=('Events' if dimensionless else 'Events / 100 GeV'))

if __name__ == '__main__':
    manifest=[]
    suffixes={'InvM':'InvM','met':'met','mT':'mT','tau_pT':'tau_pT','nlightjets':'nLightJets','dphi':'dphi_taumet'}
    for cat in ['Res','NonRes']:
        for var,suffix in suffixes.items():
            manifest.append(restyle(f'SR_1tau0l1b_loose_{cat}_{var}_N_minus_1_{suffix}.eps',
                                    f'SR1b_{cat}_{var}',f'Loose SR1b-{cat}',
                                    var in ['nlightjets','dphi']))
    for cat,var,suffix in [('Res','InvM','Mtaujet'),('NonRes','mT','mT_tau_met')]:
        manifest.append(restyle(f'SR_1tau0l0b_{cat}_{var}_N_minus_1_{suffix}.eps',
                                f'SR0b_{cat}_{var}',f'SR0b-{cat}'))
    (ROOT/'output/ch7/figure_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(f'Created {len(manifest)} EPS/PDF pairs; all protected drawing hashes match.')
