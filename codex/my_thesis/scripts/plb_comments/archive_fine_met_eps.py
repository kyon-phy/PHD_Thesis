"""Export nominal ROOT histograms in the original typography and validate every bin."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[2]
ARCHIVE = PROJECT / 'output/plb_comments/VRW_NonRes_fine_MET_archive'
ORIGINAL = ARCHIVE / 'original_lxatut'
REMOTE = '/tmp/zang_fine_met_style_20260919'
HOST = 'codex_lxatut'
MACRO = PROJECT / 'scripts/plb_comments/render_fine_met_root.C'
REGION = 'VR_0tau1l1b_tch_met_N_minus_1_met'

def run(*args):
    subprocess.run(list(map(str,args)),check=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

verified=[]
for line in (ORIGINAL/'remote_sha256.txt').read_text().splitlines():
    expected,remote=line.split(maxsplit=1)
    local=ORIGINAL/Path(remote).name
    assert sha(local)==expected,local
    verified.append({'remote':remote,'local':str(local),'sha256':expected})
region_sha='b2c59a84433e5f3122948899817da8556a20178874c95bea3778756258084a47'
assert sha(ORIGINAL/(REGION+'.root'))==region_sha
run('ssh','-o','BatchMode=yes',HOST,f'mkdir -p {REMOTE}')
run('scp',MACRO,ORIGINAL/'fit_taunub_N_minus_1_histos.root',ORIGINAL/(REGION+'.root'),HOST+':'+REMOTE+'/')
run('ssh','-o','BatchMode=yes',HOST,f'cd {REMOTE} && /usr/bin/root -l -b -q "render_fine_met_root.C(true)" && /usr/bin/root -l -b -q "render_fine_met_root.C(false)"')
for folder,stem in [('modified','paper_style'),('reconstructed','ROOT_reconstructed')]:
    dest=ARCHIVE/folder;dest.mkdir(exist_ok=True)
    stem='VRW_NonRes_MET_25GeV_'+stem
    run('scp',HOST+':'+REMOTE+'/'+stem+'*',dest)
    eps=dest/(stem+'.eps')
    run('/usr/local/bin/gs','-q','-dBATCH','-dNOPAUSE','-dEPSCrop','-sDEVICE=pdfwrite','-sOutputFile='+str(eps.with_suffix('.pdf')),eps)
    run('/usr/local/bin/gs','-q','-dBATCH','-dNOPAUSE','-dEPSCrop','-sDEVICE=pngalpha','-r300','-sOutputFile='+str(eps.with_suffix('.png')),eps)
run(sys.executable,PROJECT/'scripts/plb_comments/verify_fine_met.py')
record=json.loads((ARCHIVE/'histogram_values_unchanged.json').read_text())
manifest={
    'revision':'2026-09-19 nominal-histogram correction and original ROOT typography',
    'supersedes':'superseded_2026-09-19_raw_orig; the previous _orig reconstruction is withdrawn',
    'original_downloads_verified':verified,
    'additional_original_region_ROOT_sha256':region_sha,
    'native_fine_binning_eps_found':False,
    'original_conversion_note':'The archived PNG-to-PDF-to-EPS conversion is unchanged and remains a raster image.',
    'editable_baseline_note':'New vector reconstruction from nominal ROOT histograms and the saved uncertainty graph; not an original downloaded EPS.',
    'modified_eps':'modified/VRW_NonRes_MET_25GeV_paper_style.eps',
    'style_reference':'Original 1240x904 bitmap for typography and markers; arXiv:2606.02067v1 Figure 3 for process colours and names.',
    'style':{'reference_canvas_pixels':[1240,904],'text_font':43,'ATLAS_font':73,'text_and_legend_size_pixels':30,'marker_style':20,'marker_size':2.0,'error_line_width':2,'postscript_line_scale':2,'legend_columns':2},
    'paper_rgb':{'Wjets':[1,.800781,1],'Diboson':[1,.662109,.0549011],'ttbar':[.24707,.564453,.855469],'SingleTop':[.724609,.673828,.439209],'Zjets':[.580078,.642578,.634766]},
    'legend_reading_order':['Data','W+jets','Diboson','ttbar','single t','Z+jets','Uncertainty'],
    'source_bin_contents_modified':False,
    'source_correction_relative_to_previous_export':True,
    'checks':record['checks'],
    'numerical_validation_file':'histogram_values_unchanged.json',
    'generated_files_sha256':{str(p.relative_to(ARCHIVE)):sha(p) for folder in ['modified','reconstructed'] for p in (ARCHIVE/folder).glob('*') if p.is_file()}
}
(ARCHIVE/'archive_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Validated and exported corrected ROOT figures.')
