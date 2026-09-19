import ROOT
from array import array

# User-defined input structure: mapping each system to a dict of filename -> TDirectory
file_directory = {
    'NOSYS': {
        'ttbar_dilep.root':      'NOSYS',
        # 'ttbar_nonallhad.root':      'NOSYS',
        'Wlnu.root':       'NOSYS',
        'SingleTop_sch.root':  'NOSYS',
        'SingleTop_tch.root':  'NOSYS',
        'SingleTop_tW.root':  'NOSYS',
        'Ztautau.root':  'NOSYS',
        'Zll.root':  'NOSYS',
        'Zjet_EWK.root':  'NOSYS',
        'Wtaunu_HF.root':  'NOSYS',
        'Wtaunu_METTAU.root':  'NOSYS',
        'ttZ.root':  'NOSYS',
        'Znunu.root':  'NOSYS',
        'Diboson.root':  'NOSYS',
        'Diboson_semiLep.root':  'NOSYS',
    },
    'SYS': {
        # top nominal
        'ttbar_dilep.root':      'NOSYS',
        'SingleTop_sch.root':  'NOSYS',
        'SingleTop_tch.root':  'NOSYS',
        'SingleTop_tW.root':  'NOSYS',

        # Wjets nominal
        # 'Wlnu.root':       'NOSYS',
        # 'Wtaunu_HF.root':  'NOSYS',
        # 'Wtaunu_METTAU.root':  'NOSYS',


        # top ISR up
        # 'ttbar_dilep.root':      'GEN_Var3cUp',
        # 'SingleTop_sch.root':  'GEN_Var3cUp',
        # 'SingleTop_tch.root':  'GEN_Var3cUp',
        # 'SingleTop_tW.root':  'GEN_Var3cUp',

        # top ISR down
        # 'ttbar_dilep.root':      'GEN_Var3cDown',
        # 'SingleTop_sch.root':  'GEN_Var3cDown',
        # 'SingleTop_tch.root':  'GEN_Var3cDown',
        # 'SingleTop_tW.root':  'GEN_Var3cDown',
       
        # Top FSR up
        # 'ttbar_dilep.root':      'GEN_isrmuRfac10_fsrmuRfac20',
        # 'SingleTop_sch.root':  'GEN_isrmuRfac10_fsrmuRfac20',
        # 'SingleTop_tch.root':  'GEN_isrmuRfac10_fsrmuRfac20',
        # 'SingleTop_tW.root':  'GEN_isrmuRfac10_fsrmuRfac20',
 
        # Top FSR down
        # 'ttbar_dilep.root':      'GEN_isrmuRfac10_fsrmuRfac05',
        # 'SingleTop_sch.root':  'GEN_isrmuRfac10_fsrmuRfac05',
        # 'SingleTop_tch.root':  'GEN_isrmuRfac10_fsrmuRfac05',
        # 'SingleTop_tW.root':  'GEN_isrmuRfac10_fsrmuRfac05',

        # Top muF up
        # 'ttbar_dilep.root':      'GEN_muR_10_muF_05',
        # 'SingleTop_sch.root':  'GEN_muR_100_muF_050',
        # 'SingleTop_tch.root':  'GEN_muR_100_muF_050',
        # 'SingleTop_tW.root':  'GEN_MUR1_MUF05_PDF260000',

        # Top muF down
        # 'ttbar_dilep.root':      'GEN_muR_10_muF_20',
        # 'SingleTop_sch.root':  'GEN_muR_100_muF_200',
        # 'SingleTop_tch.root':  'GEN_muR_100_muF_200',
        # 'SingleTop_tW.root':  'GEN_MUR1_MUF2_PDF260000',

        # Top muR up
        # 'ttbar_dilep.root':      'GEN_muR_20_muF_10',
        # 'SingleTop_sch.root':  'GEN_muR_200_muF_100',
        # 'SingleTop_tch.root':  'GEN_muR_200_muF_100',
        # 'SingleTop_tW.root':  'GEN_MUR2_MUF1_PDF260000',

        # Top muR down
        # 'ttbar_dilep.root':      'GEN_muR_05_muF_10',
        # 'SingleTop_sch.root':  'GEN_muR_050_muF_100',
        # 'SingleTop_tch.root':  'GEN_muR_050_muF_100',
        # 'SingleTop_tW.root':  'GEN_MUR05_MUF1_PDF260000',

        # Top ME
        # 'ttbar_ME.root': 'NOSYS',
        # 'SingleTop_ME.root': 'NOSYS',

        # Top PS
        # 'ttbar_PS.root': 'NOSYS',
        # 'SingleTop_PS.root': 'NOSYS',

        # Top hdamp
        # 'ttbar_Hdamp.root': 'NOSYS',
        # 'SingleTop_Hdamp.root': 'NOSYS',

        # Top recoil to top
        # 'ttbar_Recoil_to_Top.root': 'NOSYS',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'NOSYS',

        # SingleTop Wt interference
        # 'ttbar_dilep.root':      'NOSYS',
        # 'Wt_Interference.root': 'NOSYS',

        # Top PDF alphaS up    
        # 'ttbar_dilep.root':      'GEN_PDF_266000',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'GEN_MUR1_MUF1_PDF266000',

         # Top PDF alphaS down    
        # 'ttbar_dilep.root':      'GEN_PDF_265000',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'GEN_MUR1_MUF1_PDF265000',

        # ttbar NNLO 3D (nonallhad)
        # 'ttbar_nonallhad_NNLO_3D.root': 'NOSYS',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'NOSYS',
      
        # Wjets alphaS up
        # 'Wlnu.root':       'GEN_MUR1_MUF1_PDF270000',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF1_PDF270000',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF1_PDF270000',

        # Wjets alphaS down
        # 'Wlnu.root':       'GEN_MUR1_MUF1_PDF269000',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF1_PDF269000',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF1_PDF269000',

        # Wjets muRmF up (ME+PS) for sch
        'Wlnu.root':       'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',
        'Wtaunu_HF.root':  'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',
        'Wtaunu_METTAU.root':  'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',

        # Wjets muRmF down (ME+PS) for sch
        # 'Wlnu.root':       'GEN_MUR05_MUF05_PDF303200_PSMUR05_PSMUF05',
        # 'Wtaunu_HF.root':  'GEN_MUR05_MUF05_PDF303200_PSMUR05_PSMUF05',
        # 'Wtaunu_METTAU.root':  'GEN_MUR05_MUF05_PDF303200_PSMUR05_PSMUF05',

        # Wjets muRmF up (ME+PS) for tch
        # 'Wlnu.root':       'GEN_MUR1_MUF2_PDF303200_PSMUR1_PSMUF2',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF2_PDF303200_PSMUR1_PSMUF2',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF2_PDF303200_PSMUR1_PSMUF2',

        # Wjets muRmF down (ME+PS) for sch
        # 'Wlnu.root':       'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',
        # 'Wtaunu_HF.root':  'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',
        # 'Wtaunu_METTAU.root':  'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',

        # other BGs
        'Ztautau.root':  'NOSYS',
        'Zll.root':  'NOSYS',
        'Zjet_EWK.root':  'NOSYS',
        'ttZ.root':  'NOSYS',
        'Znunu.root':  'NOSYS',
        'Diboson.root':  'NOSYS',
        'Diboson_semiLep.root':  'NOSYS',
    }
}

# set the TF calculation for Resonance/Non-resonance region
# channel = 'sch'
channel = 'tch'

# List of histogram names to process
hist_names = ['met_WCR_0tau1l0b_sch', 'met_topCR_1tau1l_sch', 'met_SR_1tau0l1b_sch', 'met_VR_VR_0tau1l1b_sch', 'met_WVR_1tau0l0b_sch', 'met_topVR_1tau0l2b_sch', 'met_WCR_0tau1l0b_tch', 'met_topCR_1tau1l_tch', 'met_SR_1tau0l1b_tch', 'met_VR_VR_0tau1l1b_tch', 'met_WVR_1tau0l0b_tch', 'met_topVR_1tau0l2b_tch']

# Function to retrieve sum of weights and its propagated error from a TH1D
def get_sum_and_error(filename, dir_name, hist_name):
    # file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_INTNOTE"
    file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR"
    full_filename = file_path + '/' + filename
    f = ROOT.TFile.Open(full_filename)
    hist = f.Get(dir_name + '/' + hist_name)
    if not hist:
        raise KeyError(f"Histogram {hist_name} not found in {dir_name} of {full_filename}")
    # Ensure sumw2 is active for correct error calculation
    # hist.Sumw2() # already activated in the root file
    # Use ROOT's IntegralAndError to compute sum and its error
    nbins = hist.GetNbinsX()
    err_arr = array('d', [0.0])
    total = hist.IntegralAndError(0, nbins+1, err_arr)
    f.Close()
    return float(total), float(err_arr[0])

# Aggregate results: results[systematic][hist_name] = (sum, error): results[systematic][hist_name] = (sum, error)
results = {sys: {} for sys in file_directory}
for sys, mapping in file_directory.items():
    for hname in hist_names:
        total_sum = 0.0
        total_err2 = 0.0
        for fname, dir_name in mapping.items():
            s, e = get_sum_and_error(fname, dir_name, hname)
            total_sum += s
            total_err2 += e ** 2
        results[sys][hname] = (total_sum, total_err2 ** 0.5)

# Error propagation for a ratio A/B
def propagate_ratio_sr(a, err_a, b, err_b):
    r = {}
    err = {}
    for region in a.keys():
        r[region] = a[region] / b[region]
        rel_err = ((err_a[region] / a[region]) ** 2 + (err_b[region] / b[region]) ** 2) ** 0.5
        err[region] = r[region] * rel_err
    return r, err

def propagate_ratio_cr(a, err_a, b, err_b):
    r = a / b
    rel_err = ((err_a / a) ** 2 + (err_b / b) ** 2) ** 0.5
    return r, r * rel_err


# Calculate double ratio: (SYS_SR/NOSYS_SR) / (SYS_CR/NOSYS_CR) - 1
sr_sys = {}
sr_nom = {}
sr_sys_err = {}
sr_nom_err = {}

# SR (tch)
sr_sys["SR_1tau0l1b_" + channel], sr_sys_err["SR_1tau0l1b_" + channel] = results['SYS']['met_SR_1tau0l1b_' + channel]
sr_nom["SR_1tau0l1b_" + channel], sr_nom_err["SR_1tau0l1b_" + channel] = results['NOSYS']['met_SR_1tau0l1b_' + channel]
# 0tau VR (tch)
sr_sys["VR_0tau1l1b_" + channel], sr_sys_err["VR_0tau1l1b_" + channel] = results['SYS']['met_VR_VR_0tau1l1b_' + channel]
sr_nom["VR_0tau1l1b_" + channel], sr_nom_err["VR_0tau1l1b_" + channel] = results['NOSYS']['met_VR_VR_0tau1l1b_' + channel]
# top VR (tch)
sr_sys["topVR_1tau0l2b_" + channel], sr_sys_err["topVR_1tau0l2b_" + channel] = results['SYS']['met_topVR_1tau0l2b_' + channel]
sr_nom["topVR_1tau0l2b_" + channel], sr_nom_err["topVR_1tau0l2b_" + channel] = results['NOSYS']['met_topVR_1tau0l2b_' + channel]
# WVR (tch)
sr_sys["WVR_1tau0l0b_" + channel], sr_sys_err["WVR_1tau0l0b_" + channel] = results['SYS']['met_WVR_1tau0l0b_' + channel]
sr_nom["WVR_1tau0l0b_" + channel], sr_nom_err["WVR_1tau0l0b_" + channel] = results['NOSYS']['met_WVR_1tau0l0b_' + channel]
# CR (tch)
cr_sys, cr_sys_err = results['SYS']['met_topCR_1tau1l_' + channel]
cr_nom, cr_nom_err = results['NOSYS']['met_topCR_1tau1l_' + channel]

# print(f"sr_sys: {sr_sys}, sr_sys_err: {sr_sys_err}, sr_nom: {sr_nom}, sr_nom_err: {sr_nom_err}")
# print(f"cr_sys: {cr_sys}, cr_sys_err: {cr_sys_err}, cr_nom: {cr_nom}, cr_nom_err: {cr_nom_err}")

r_sr, r_sr_err = propagate_ratio_sr(sr_sys, sr_sys_err, sr_nom, sr_nom_err)
# print(f"r_sr: {r_sr}, r_sr_err: {r_sr_err}")
r_cr, r_cr_err = propagate_ratio_cr(cr_sys, cr_sys_err, cr_nom, cr_nom_err)
# print(f"r_cr: {r_cr}, r_cr_err: {r_cr_err}")

double_ratio = {}
double_ratio_err = {}
for region in r_sr.keys():
    double_ratio[region] = r_sr[region] / r_cr - 1
    double_rel_err = ((r_sr_err[region] / r_sr[region]) ** 2 + (r_cr_err / r_cr) ** 2) ** 0.5
    # Propagate error for double ratio
    double_ratio_err[region] = r_sr[region] / r_cr * double_rel_err

for region in double_ratio.keys():
    print(f"Region: {region}, (double_ratio - 1) = {double_ratio[region]:.6f} ± {double_ratio_err[region]:.6f}")
