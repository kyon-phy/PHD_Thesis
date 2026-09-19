"""Archive the remote bitmap; edit only colours and annotations of a ROOT-derived EPS."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'tmp/pdfs/plb_reply_plot_search/python_packages'))
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from matplotlib.patches import Rectangle
from matplotlib import colors

ARCHIVE = PROJECT / 'output/plb_comments/VRW_NonRes_fine_MET_archive'
ORIGINAL = ARCHIVE / 'original_lxatut'
BASE = ARCHIVE / 'reconstructed'
MOD = ARCHIVE / 'modified'
for folder in (ORIGINAL, BASE, MOD):
    folder.mkdir(parents=True, exist_ok=True)

def sha(data):
    return hashlib.sha256(data).hexdigest()

verified = []
for line in (ORIGINAL / 'remote_sha256.txt').read_text().splitlines():
    expected, remote = line.split(maxsplit=1)
    local = ORIGINAL / Path(remote).name
    assert sha(local.read_bytes()) == expected, local
    verified.append({'remote': remote, 'local': str(local), 'sha256': expected})

# This deliberately stays a bitmap: it is a format conversion, not vectorisation.
png = ORIGINAL / 'VR_0tau1l1b_tch_met_N_minus_1_met.png'
with Image.open(png) as im:
    width, height = im.size
pdf = ORIGINAL / 'VR_0tau1l1b_tch_met_N_minus_1_met_png_wrapped.pdf'
c = canvas.Canvas(str(pdf), pagesize=(width, height))
c.setTitle('Unmodified lxatut PNG wrapped in PDF; original plot does not display data')
c.drawImage(ImageReader(str(png)), 0, 0, width=width, height=height)
c.showPage()
c.save()
wrapped_eps = pdf.with_suffix('.eps')
subprocess.run(['/usr/local/bin/gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=eps2write',
                '-sOutputFile=' + str(wrapped_eps), str(pdf)], check=True)

# Use the already validated 40-bin ROOT reconstruction as the editable source.
source_script = PROJECT / 'output/plb_comments/fine_met_recovery/restore_fine_met.py'
code = source_script.read_text().split("pdf = OUT / ")[0]
ns = {'__file__': str(source_script), '__name__': '__fine_met_export__'}
exec(compile(code, str(source_script), 'exec'), ns)
fig, ax = ns['fig'], ns['ax']
original_texts = list(ax.texts)
original_texts[2].set_text('fit_taunub_nom_1l_allVR_N_minus_1')
original_texts[2].set_position((.035, .795))
original_texts[3].set_text('0tau1l1b, Non-Resonance 0tauVR')
original_texts[3].set_position((.035, .725))
prefit = ax.text(.035, .655, 'Pre-fit', transform=ax.transAxes)
layout = original_texts[2:] + [prefit]
layout += [a for a in ax.patches if isinstance(a, Rectangle)]
layout += [a for a in ax.lines if a.get_transform() == ax.transAxes]

def tagged_draw(artist, tag):
    draw = artist.draw
    def wrapped(renderer):
        writer = getattr(renderer, '_pswriter', None)
        if writer:
            writer.write(f'\n%%BEGIN_EDITABLE_LAYOUT {tag}\n')
        draw(renderer)
        if writer:
            writer.write(f'\n%%END_EDITABLE_LAYOUT {tag}\n')
    artist.draw = wrapped

for i, artist in enumerate(layout):
    tagged_draw(artist, str(i))

base_eps = BASE / 'VRW_NonRes_MET_25GeV_ROOT_reconstructed.eps'
fig.savefig(base_eps, format='eps')
ns['plt'].close(fig)
raw = base_eps.read_text()
layout_re = re.compile(r'\n%%BEGIN_EDITABLE_LAYOUT (\d+)\n.*?\n%%END_EDITABLE_LAYOUT \1\n', re.S)
body, removed = layout_re.subn('', raw)
assert removed == len(layout), (removed, len(layout))

# Exact non-stroking RGB values extracted from arXiv:2606.02067v1, Figure 3.
paper_colours = {
    'W+jets': (1.0, .800781, 1.0),
    'Diboson': (1.0, .662109, .0549011),
    'ttbar': (.24707, .564453, .855469),
    'SingleTop': (.724609, .673828, .439209),
    'Z+jets': (.580078, .642578, .634766),
}
before_colours = body
colour_changes = {}
for name, new in paper_colours.items():
    old = colors.to_rgb(ns['colours'][name])
    old_command = ' '.join(f'{v:.3f}'.rstrip('0').rstrip('.') for v in old) + ' setrgbcolor'
    new_command = ' '.join(f'{v:.7f}' for v in new) + ' setrgbcolor'
    count = body.count(old_command)
    assert count > 0, (name, old_command)
    body = body.replace(old_command, new_command)
    colour_changes[name] = {'old': old, 'new': new, 'commands_changed': count}

colour_re = re.compile(r'(?:[-+.0-9]+\s+){3}setrgbcolor')
def protected_signature(content):
    return sha(' '.join(colour_re.sub('COLOUR', content).split()).encode())
assert protected_signature(before_colours) == protected_signature(body)

W, H = fig.get_size_inches() * 72
x0, y0, aw, ah = .13 * W, .31 * H, .84 * W, .65 * H
ps = ['%%BEGIN_NEW_LAYOUT', 'gsave', '0 setgray', '/Helvetica findfont 12 scalefont setfont']

def text(x, y, value, font='Helvetica', size=12):
    escaped = value.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    ps.append(f'/{font} findfont {size} scalefont setfont {x:.5f} {y:.5f} moveto ({escaped}) show')

text(x0 + .035 * aw, y0 + .795 * ah, 'VRW-NonRes')
text(x0 + .035 * aw, y0 + .725 * ah, 'Pre-fit')

# Two columns, reading order retained from the public-paper legend.
entries = [('Data', 'Data'), ('W+jets', 'W+jets'),
           ('Diboson', 'Diboson'), ('ttbar', 'ttbar'),
           ('SingleTop', 'single t'), ('Z+jets', 'Z+jets'),
           ('Uncertainty', 'Uncertainty')]
for i, (key, label) in enumerate(entries):
    col, row = i % 2, i // 2
    x = x0 + (.55 if col == 0 else .79) * aw
    y = y0 + (.94 - .076 * row) * ah
    ps += ['gsave', '0 setgray', '0.75 setlinewidth']
    if key == 'Data':
        ps += [f'newpath {x:.5f} {y:.5f} moveto {x+14:.5f} {y:.5f} lineto stroke',
               f'newpath {x+7:.5f} {y:.5f} 2.0 0 360 arc fill']
    elif key == 'Uncertainty':
        ps += [f'newpath {x:.5f} {y-4:.5f} moveto 14 0 rlineto 0 9 rlineto -14 0 rlineto closepath clip',
               '0.4078431 0.4078431 0.9568627 setrgbcolor', '0.45 setlinewidth']
        for delta in range(-12, 20, 4):
            ps.append(f'newpath {x+delta:.5f} {y-4:.5f} moveto 9 9 rlineto stroke')
    else:
        rgb = paper_colours[key]
        ps += [' '.join(f'{v:.7f}' for v in rgb) + ' setrgbcolor',
               f'newpath {x:.5f} {y-4:.5f} moveto 14 0 rlineto 0 9 rlineto -14 0 rlineto closepath fill',
               '0 setgray', '0.4 setlinewidth',
               f'newpath {x:.5f} {y-4:.5f} moveto 14 0 rlineto 0 9 rlineto -14 0 rlineto closepath stroke']
    ps += ['grestore', '0 setgray']
    tx, ty = x + 19, y - 3.8
    if key == 'ttbar':
        text(tx, ty, 'tt', 'Helvetica-Oblique', 11.5)
        ps.append(f'0.65 setlinewidth newpath {tx+3.4:.5f} {ty+9.1:.5f} moveto 4.2 0 rlineto stroke')
    elif key == 'SingleTop':
        text(tx, ty, 'single ', size=11.5)
        ps.append('/Helvetica-Oblique findfont 11.5 scalefont setfont (t) show')
    else:
        text(tx, ty, label, size=11.5)

# Paper-style red L arrow: VR requires MET > 400 GeV.
cut_x = x0 + aw * .4
arrow_y = y0 + ah * (4 / 6)  # 10^3 on the original logarithmic axis.
tip_x = cut_x + aw * .09
ps += ['1 0 0 setrgbcolor', '2.0 setlinewidth',
       f'newpath {cut_x:.5f} {y0:.5f} moveto {cut_x:.5f} {arrow_y:.5f} lineto {tip_x-7:.5f} {arrow_y:.5f} lineto stroke',
       f'newpath {tip_x:.5f} {arrow_y:.5f} moveto -9 4 rlineto 0 -8 rlineto closepath fill']
text(cut_x + 13, arrow_y + 8, 'VR', size=11.5)
ps += ['grestore', '%%END_NEW_LAYOUT']
overlay = '\n'.join(ps) + '\n'
tail = body.rfind('end\nshowpage')
assert tail > 0
modified = body[:tail] + overlay + body[tail:]
out_eps = MOD / 'VRW_NonRes_MET_25GeV_paper_style.eps'
out_eps.write_text(modified)

for eps in (base_eps, out_eps):
    subprocess.run(['/usr/local/bin/gs', '-q', '-dBATCH', '-dNOPAUSE', '-dEPSCrop',
                    '-sDEVICE=pdfwrite', '-sOutputFile=' + str(eps.with_suffix('.pdf')), str(eps)], check=True)
    subprocess.run(['/usr/local/bin/gs', '-q', '-dBATCH', '-dNOPAUSE', '-dEPSCrop',
                    '-sDEVICE=pngalpha', '-r300', '-sOutputFile=' + str(eps.with_suffix('.png')), str(eps)], check=True)

numbers = PROJECT / 'output/plb_comments/fine_met_recovery/restored_histograms.json'
shutil.copy2(numbers, ARCHIVE / 'histogram_values_unchanged.json')
shutil.copy2(PROJECT / 'Figs/CH8/VRW_NonRes_fine_met.pdf', ORIGINAL / 'INT_note_original_JPEG_wrapped.pdf')
manifest = {
    'original_downloads_verified': verified,
    'native_fine_binning_eps_found': False,
    'original_png_contains_data_points': False,
    'original_conversion': [str(png), str(pdf), str(wrapped_eps)],
    'original_conversion_note': 'PNG wrapped in PDF, then converted to EPS; remains raster.',
    'editable_baseline': str(base_eps),
    'editable_baseline_note': 'ROOT-derived vector reconstruction, not an original downloaded EPS.',
    'modified_eps': str(out_eps),
    'style_reference': 'https://arxiv.org/abs/2606.02067v1; Figure 3, page 13',
    'paper_rgb': paper_colours,
    'legend_reading_order': [v for _, v in entries],
    'legend_columns': 2,
    'changes': ['Remove fit_taunub label', 'Replace 0tau1l label with VRW-NonRes',
                'Retain Pre-fit', 'Add red VR selection arrow at MET=400 GeV pointing right',
                'Apply paper background RGB colours and names', 'Remove numerical legend yields',
                'Remove zero-yield Dijet legend entry; its zero-valued histogram is retained'],
    'bin_content_change': False,
    'histogram_data_file_sha256': sha(numbers.read_bytes()),
    'histogram_geometry_hash_before': protected_signature(before_colours),
    'histogram_geometry_hash_after': protected_signature(body),
    'all_histogram_and_data_geometry_identical': True,
    'original_stack_order_preserved': True,
    'colour_commands': colour_changes,
    'removed_layout_blocks': removed,
    'source_and_modified_eps_sha256': [sha(raw.encode()), sha(modified.encode())],
}
(ARCHIVE / 'archive_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'modified': str(out_eps), 'geometry_verified': True,
                  'hash': manifest['histogram_geometry_hash_after']}, indent=2))
