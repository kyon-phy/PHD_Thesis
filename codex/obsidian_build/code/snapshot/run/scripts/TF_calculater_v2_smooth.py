import ROOT
import math
from array import array

ROOT.gStyle.SetOptStat(0)

def get_hist_names(file_path, file_directory):
    # get the root file name and TDirectory name from file_directory
    root_file_name = list(file_directory.keys())[0]
    tdirectory_name = file_directory[root_file_name]
    # open the file
    f = ROOT.TFile.Open(file_path + '/' + root_file_name)
    # get the hist names
    hist_names = [key.GetName() for key in f.Get(tdirectory_name).GetListOfKeys()]
    # close the file
    f.Close()
    return hist_names

# User-defined input structure: mapping each system to a dict of filename -> TDirectory
file_directory = {
    'NOSYS': {
        # Top nominal
        # 'ttbar_nonallhad.root':      'NOSYS',
        # 'ttbar_dilep.root':      'NOSYS',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'NOSYS',

        # Top nominal
        # 'SingleTop.root': 'NOSYS',
        # 'ttbar.root': 'NOSYS',

        # Wjets nominal
        # 'Wtaunu_HF.root':  'NOSYS',
        # 'Wtaunu_METTAU.root':  'NOSYS',
        'Wlnu.root':       'NOSYS',

        # other BGs (not needed when estimating the theory uncertainties for Top and Wjets)
        # 'ttZ.root':  'NOSYS',
        # 'Ztautau.root':  'NOSYS',
        # 'Zll.root':  'NOSYS',
        # 'Zjet_EWK.root':  'NOSYS',
        # 'Znunu.root':  'NOSYS',
        # 'Diboson.root':  'NOSYS',
        # 'Diboson_semiLep.root':  'NOSYS',
    },
    'SYS': {
        # top nominal
        # 'ttbar_dilep.root':      'NOSYS',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'NOSYS',

        # Wjets nominal
        # 'Wtaunu_HF.root':  'NOSYS',
        # 'Wtaunu_METTAU.root':  'NOSYS',
        # 'Wlnu.root':       'NOSYS',


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
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_Hdamp.root': 'NOSYS',

        # Top recoil to top
        # 'ttbar_Recoil_to_Top.root': 'NOSYS',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
        # 'SingleTop_tW.root':  'NOSYS',

        # SingleTop Wt interference
        # 'ttbar_dilep.root':      'NOSYS',
        # 'SingleTop_sch.root':  'NOSYS',
        # 'SingleTop_tch.root':  'NOSYS',
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

        # Wjets muRmF up (ME+PS) for sch (SR)
        'Wlnu.root':       'GEN_MUR2_MUF1_PDF303200_PSMUR2_PSMUF1',
        # 'Wtaunu_HF.root':  'GEN_MUR2_MUF1_PDF303200_PSMUR2_PSMUF1',
        # 'Wtaunu_METTAU.root':  'GEN_MUR2_MUF1_PDF303200_PSMUR2_PSMUF1',

        # Wjets muRmF down (ME+PS) for sch (SR)
        # 'Wlnu.root':       'GEN_MUR05_MUF05_PDF303200_PSMUR05_PSMUF05',
        # 'Wtaunu_HF.root':  'GEN_MUR05_MUF05_PDF303200_PSMUR05_PSMUF05',
        # 'Wtaunu_METTAU.root':  'GEN_MUR05_MUF05_PDF303200_PSMUR05_PSMUF05',

        # Wjets muRmF up (ME+PS) for tch (SR)
        # 'Wlnu.root':       'GEN_MUR1_MUF2_PDF303200_PSMUR1_PSMUF2',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF2_PDF303200_PSMUR1_PSMUF2',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF2_PDF303200_PSMUR1_PSMUF2',

        # Wjets muRmF down (ME+PS) for tch (SR)
        # 'Wlnu.root':       'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',
        # 'Wtaunu_HF.root':  'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',
        # 'Wtaunu_METTAU.root':  'GEN_MUR05_MUF1_PDF303200_PSMUR05_PSMUF1',

        # Wjets EW correction (additive)
        # 'Wlnu.root':       'GEN_MUR1_MUF1_PDF303200_ASSEW',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF1_PDF303200_ASSEW',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF1_PDF303200_ASSEW',

        # Wjets EW correction (multiplicative)
        # 'Wlnu.root':       'GEN_MUR1_MUF1_PDF303200_MULTIASSEW',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF1_PDF303200_MULTIASSEW',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF1_PDF303200_MULTIASSEW',

        # Wjets EW correction (exponentiated)
        # 'Wlnu.root':       'GEN_MUR1_MUF1_PDF303200_EXPASSEW',
        # 'Wtaunu_HF.root':  'GEN_MUR1_MUF1_PDF303200_EXPASSEW',
        # 'Wtaunu_METTAU.root':  'GEN_MUR1_MUF1_PDF303200_EXPASSEW',

        # SingleTop JET uncertainties (UP)
        # 'SingleTop.root': 'JET_InSitu_NonClosure_PreRec__1up',
        # 'ttbar.root': 'JET_JESUnc_VertexingAlg_PreRec__1up',

        # SingleTop JET uncertainties (DOWN)
        # 'SingleTop.root': 'JET_InSitu_NonClosure_PreRec__1down',
        # 'ttbar.root': 'JET_JESUnc_VertexingAlg_PreRec__1down',

        # other BGs (not needed when estimating the theory uncertainties for Top and Wjets)
        # 'ttZ.root':  'NOSYS',
        # 'Ztautau.root':  'NOSYS',
        # 'Zll.root':  'NOSYS',
        # 'Zjet_EWK.root':  'NOSYS',
        # 'Znunu.root':  'NOSYS',
        # 'Diboson.root':  'NOSYS',
        # 'Diboson_semiLep.root':  'NOSYS',
    }
}

# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_INTNOTE"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_nom_1l_ttbarSYS"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNbjets"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNbjets_looseNjets"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNbjets_looseNjets_looseTopVR"
file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNjets_loosetaupt_loosemT_looseTopVR"
# file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04"

# set the TF calculation for Resonance/Non-resonance region
channel = 'sch'
# channel = 'tch'

# set region
# CR = "WCR"
CR = "topCR"

# set the smooth option
# smooth = True
smooth = False

# set the plot range
plot_full_range = True
# plot_full_range = False

# set the Signal region name
if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNbjets":
    SR_name = "SR_1tau0l"
elif file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNjets_loosetaupt_loosemT_looseTopVR":
    SR_name = "SR_1tau0l"
else:
    SR_name = "SR_1tau0l1b"
    

# SR_name = "SR_1tau0l1b"

# set region suffix for tch and sch separately
if channel == 'sch':
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        SR_prefix = "InvM"
    else:
        SR_prefix = "Mtaub"
    # SR_prefix = "mT"
    VR_prefix = "Mlb"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        WVR_prefix = "Mtaujet"
    else:
        WVR_prefix = "MtauJet"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        topVR_prefix = "Mtaub"
    else:
        topVR_prefix = "Mtaub0"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory":
        SR_suffix = "looseInvM"
    elif file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNbjets":
        SR_suffix = "looseInvM_looseNbjets"
    elif file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNjets_loosetaupt_loosemT_looseTopVR":
        # SR_suffix = "looseInvM_loosemT"
        SR_suffix = "looseInvM_looseNbjets"
        # SR_suffix = "looseInvM_loosemT" # invM and mT relaxed SR
    else:
        SR_suffix = "InvM_N_minus_1"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        VR_suffix = "InvM_N_minus_1"
    else:
        VR_suffix = "looseInvM"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        WVR_suffix = "InvM_N_minus_1"
    else:
        WVR_suffix = "looseInvM"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory":
        topVR_suffix = "looseInvM"
    elif file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNbjets":
        topVR_suffix = "looseInvM"
    elif file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory_SR_looseNjets_loosetaupt_loosemT_looseTopVR":
        topVR_suffix = "looseInvM_looseNbjets"
    elif file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        topVR_suffix = "InvM_N_minus_1"
elif channel == 'tch':
    SR_prefix = "met"
    # SR_prefix = "mT"
    # SR_prefix = "tau_pt"
    VR_prefix = "met"
    WVR_prefix = "met"
    topVR_prefix = "mT"
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_theory":
        SR_suffix = "looseMET" # mET relaxed SR
    else:
        SR_suffix = "looseMET_looseNbjets" # Nbjets and invM relaxed SR
    # SR_suffix = "loosetaupt_looseNbjets" # Nbjets and invM relaxed SR
    # SR_suffix = "loosetaupt_loosemT" # Nbjets and invM relaxed SR
    VR_suffix = "looseMET"
    WVR_suffix = "looseMET"
    topVR_suffix = "loosemT"



# List of histogram names to process
hist_names = []
hist_names = get_hist_names(file_path, file_directory["NOSYS"])


# Function to retrieve sum of weights and its propagated error from a TH1D
def get_sum_and_error(filename, dir_name, hist_name):
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
sr_sys[SR_name + channel], sr_sys_err[SR_name + channel] = results['SYS'][SR_prefix + '_' + SR_name + '_' + channel + "_" + SR_suffix]
sr_nom[SR_name + channel], sr_nom_err[SR_name + channel] = results['NOSYS'][SR_prefix + '_' + SR_name + '_' + channel + "_" + SR_suffix]
# 0tau VR (tch)
sr_sys["VR_0tau1l1b_" + channel], sr_sys_err["VR_0tau1l1b_" + channel] = results['SYS'][VR_prefix + '_VR_0tau1l1b_' + channel + "_" + VR_suffix]
sr_nom["VR_0tau1l1b_" + channel], sr_nom_err["VR_0tau1l1b_" + channel] = results['NOSYS'][VR_prefix + '_VR_0tau1l1b_' + channel + "_" + VR_suffix]
# top VR (tch)
sr_sys["topVR_1tau0l2b_" + channel], sr_sys_err["topVR_1tau0l2b_" + channel] = results['SYS'][topVR_prefix + '_topVR_1tau0l2b_' + channel + "_" + topVR_suffix]
sr_nom["topVR_1tau0l2b_" + channel], sr_nom_err["topVR_1tau0l2b_" + channel] = results['NOSYS'][topVR_prefix + '_topVR_1tau0l2b_' + channel + "_" + topVR_suffix]
# WVR (tch)
sr_sys["WVR_1tau0l0b_" + channel], sr_sys_err["WVR_1tau0l0b_" + channel] = results['SYS'][WVR_prefix + '_WVR_1tau0l0b_' + channel + "_" + WVR_suffix]
sr_nom["WVR_1tau0l0b_" + channel], sr_nom_err["WVR_1tau0l0b_" + channel] = results['NOSYS'][WVR_prefix + '_WVR_1tau0l0b_' + channel + "_" + WVR_suffix]
# CR (tch)
if CR == "topCR":
    # cr_sys, cr_sys_err = results['SYS']['met_topCR_1tau1l_' + channel]
    # cr_nom, cr_nom_err = results['NOSYS']['met_topCR_1tau1l_' + channel]
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        cr_sys, cr_sys_err = results['SYS']["met_topCR_1tau1e_sch_met_N_minus_1"]
        cr_nom, cr_nom_err = results['NOSYS']["met_topCR_1tau1e_sch_met_N_minus_1"]
    else:
        cr_sys, cr_sys_err = results['SYS'][topVR_prefix + '_topCR_1tau1l_' + channel]
        cr_nom, cr_nom_err = results['NOSYS'][topVR_prefix + '_topCR_1tau1l_' + channel]
elif CR == "WCR":
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        cr_sys, cr_sys_err = results['SYS']["met_WCR_0tau1mu0b_sch_met_N_minus_1;1"]
        cr_nom, cr_nom_err = results['NOSYS']["met_WCR_0tau1mu0b_sch_met_N_minus_1;1"]
    else:
        cr_sys, cr_sys_err = results['SYS']['met_WCR_0tau1l0b_' + channel]
        cr_nom, cr_nom_err = results['NOSYS']['met_WCR_0tau1l0b_' + channel]

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

###### block2 : draw the double ratio ########
# --- 1) 计算全局 CR 比值和误差 ---
# 从 file_directory 拿对应的文件和目录
sys_files =  [(fname, dirn) for fname,dirn in file_directory['SYS'].items()]
nom_files =  [(fname, dirn) for fname,dirn in file_directory['NOSYS'].items()]

# 控制区直方图名字 (以 tch 为例)
if CR == "topCR":
    if channel == 'sch':
        if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
            cr_name = "met_topCR_1tau1mu_sch_met_N_minus_1"
        else:
            cr_name = f"Mtaub0_topCR_1tau1l_{channel}" # Top uncertainties
    elif channel == 'tch':
        if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
            cr_name = "met_topCR_1tau1mu_tch_met_N_minus_1"
        else:
            cr_name = f"mT_topCR_1tau1l_{channel}" # Top uncertainties
elif CR == "WCR": 
    if file_path == "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_JETsys_1l_allVR_with_beamspot_v04":
        cr_name = "met_WCR_0tau1mu0b_" + channel + "_met_N_minus_1"
    else:
        cr_name = f"met_WCR_0tau1l0b_{channel}" # W uncertainties
else:
   raise KeyError(f"no CR is defined!!!")

def get_crop_hist(h, x_low, x_high, hist_name):
    print(f"x_low: {x_low}, x_high: {x_high}")
    bin_low = h.GetXaxis().FindBin(x_low)
    nbins = h.GetNbinsX()
    nbins_new = nbins - bin_low + 1
    x_label = h.GetXaxis().GetTitle()
    h_crop = ROOT.TH1D(f"{hist_name}",f";{x_label};", nbins_new, x_low, x_high)
    for i in range(1, nbins_new+1):
        h_crop.SetBinContent(i, h.GetBinContent(bin_low + i - 1))
        h_crop.SetBinError(i, h.GetBinError(bin_low + i - 1))
    # also include the overflow bins
    h_crop.SetBinContent(nbins_new + 1, h.GetBinContent(nbins+1))
    h_crop.SetBinError(nbins_new + 1, h.GetBinError(nbins+1))
    h = h_crop
    return h

def get_combined_hist(files, hist_name, smooth=False):
    """把所有文件的同名 hist 加在一起"""
    hist_counter = 0
    for fname, dirn in files:
        # read the hists
        # print(f"fname: {fname}, dirn: {dirn}, hist_name: {hist_name}")
        f = ROOT.TFile.Open(f"{file_path}/{fname}")
        h_cloned = None
        h = f.Get(f"{dirn}/{hist_name}")

        # modify the hist before smoothing, rebin the hist
        # if "met" in hist_name:
        if "met" in hist_name and "CR" not in hist_name:
            h = get_crop_hist(h, 200, 2000, f"{hist_name}_crop")

        # rebin, smooth and crop the hists
        # h.Rebin(4)

        if not h:
            f.Close()
            raise KeyError(hist_name)
        h_cloned = h.Clone(f"tmp_{hist_name}")  # 每次clone一份出来
        # print("")
        if hist_counter == 0:
            h_tot = h_cloned.Clone(f"tot_{hist_name}")
            h_tot.SetDirectory(0)
        else:
            h_tot.Add(h_cloned)
        hist_counter += 1
    return h_tot

# rescale h_sys using the sys/nom smoothed ratio
def rescale_sys(h_sys, h_nom, smooth):
    hist_name = h_sys.GetName()
    print(f"hist_name: {hist_name}")
    if smooth:
        h_sys_ratio = h_sys.Clone(f"h_sys_ratio")
        # print(f"h_sys_ratio_name: {h_sys_ratio.GetName()}, h_sys_ratio_nbins: {h_sys_ratio.GetNbinsX()}, h_sys_yield: {h_sys.Integral()}")
        h_sys_ratio.Divide(h_nom)
        h_sys_ratio.Smooth(1)
        # turn back to original scale to the sys plot
        h_sys_new = h_nom.Clone(f"h_sys_new")
        h_sys_new.Multiply(h_sys_ratio)
        # print(f"h_sys_new_name: {h_sys_new.GetName()}, h_sys_new_nbins: {h_sys_new.GetNbinsX()}, h_sys_new_yield: {h_sys_new.Integral()}")
        # # modify the hist after smoothing
        return h_sys_new
    else:
        return h_sys
        
h_sys_cr = get_combined_hist(sys_files, cr_name, smooth)
h_nom_cr = get_combined_hist(nom_files, cr_name, smooth)
# h_sys_cr = rescale_sys(h_sys_cr, h_nom_cr, smooth)

h_sys_cr.SetName(f"h_sys_{cr_name}")
h_nom_cr.SetName(f"h_nom_{cr_name}")
print(f"h_sys_cr: {h_sys_cr.GetName()}, h_sys_cr: {h_sys_cr.GetNbinsX()}, h_sys_yield: {h_sys_cr.Integral()}")
print(f"h_nom_cr: {h_nom_cr.GetName()}, h_nom_cr: {h_nom_cr.GetNbinsX()}, h_nom_yield: {h_nom_cr.Integral()}")


# cr_ratio = h_sys_cr.Integral() / h_nom_cr.Integral()
nbins = h_nom_cr.GetNbinsX()
err_arr_sys = array('d', [0.0])
err_arr_nom = array('d', [0.0])
cr_sys = h_sys_cr.IntegralAndError(0, nbins +1, err_arr_sys)
cr_nom = h_nom_cr.IntegralAndError(0, nbins +1, err_arr_nom)

cr_ratio = cr_sys / cr_nom
cr_ratio_err = cr_ratio * ((err_arr_sys[0]/cr_sys) ** 2 + (err_arr_nom[0]/cr_nom) ** 2) ** 0.5
print(f"cr_sys: {cr_sys}, cr_nom: {cr_nom}, cr_ratio: {cr_ratio}, cr_ratio_err: {cr_ratio_err}")
# print(f"debug2")

# 用 IntegralAndError 来算误差也可以，但示例中直接从你的结果里取：
# cr_ratio_err2 = cr_sys_err/cr_nom if cr_nom>0 else 0  # 或直接用你已有的值
# bin by bin ratio plot
h_ratio_cr = h_sys_cr.Clone(f"cr_ratio_{cr_name}")
h_ratio_cr.SetDirectory(0)
h_ratio_cr.Divide(h_nom_cr)
h_ratio_cr.SetName(f"cr_ratio_{cr_name}")
h_ratio_cr.SetTitle(f"cr_ratio_{cr_name}")

# 打开一个新的 ROOT 文件，用于保存所有 double‑ratio hist
out_file = ROOT.TFile.Open("doubleRatio.root", "RECREATE")
h_ratio_cr.Write()
h_sys_cr.Write()
h_nom_cr.Write()


# 2) 对每个 SR/VR，做 bin-by-bin double ratio 并写入 out_file
for region in [SR_name, 'VR_0tau1l1b', 'topVR_1tau0l2b', 'WVR_1tau0l0b']:
    if region == SR_name:
        name = f"{SR_prefix}_{region}_{channel}_{SR_suffix}"
        if channel == 'sch':
            if SR_prefix == "Mtaub" or SR_prefix == "InvM":
                cut_low = 800 # InvM
            elif SR_prefix == "mT":
                cut_low = 200 # mT
            else:
                raise KeyError(f"no SR_prefix is defined correctly!!!")
        elif channel == 'tch':
            if SR_prefix == "met":
                cut_low = 400 # MET
            elif SR_prefix == "mT":
                cut_low = 600 # mT
            elif SR_prefix == "tau_pt":
                cut_low = 200 # tau_pt
            else:
                raise KeyError(f"no SR_prefix is defined correctly!!!")
    elif region == 'VR_0tau1l1b':
        name = f"{VR_prefix}_{region}_{channel}_{VR_suffix}"
        if channel == 'sch':
            cut_low = 800 # InvM
        elif channel == 'tch':
            cut_low = 400 # MET
    elif region == 'topVR_1tau0l2b':
        name = f"{topVR_prefix}_{region}_{channel}_{topVR_suffix}"
        if channel == 'sch':
            cut_low = 400 # InvM
        elif channel == 'tch':
            cut_low = 200 # mT
    elif region == 'WVR_1tau0l0b':
        name = f"{WVR_prefix}_{region}_{channel}_{WVR_suffix}"
        if channel == 'sch':
            cut_low = 800 # InvM
        elif channel == 'tch':
            cut_low = 400 # MET
    else:
        raise KeyError(f"no region is defined!!!")
    h_sys = get_combined_hist(sys_files, name, smooth)
    h_nom = get_combined_hist(nom_files, name, smooth)
    # smooth the sys hist
    h_sys = rescale_sys(h_sys, h_nom, smooth)
    # crop the hists after smoothing
    if not plot_full_range:
        if channel == 'sch':
            cut_high = 2000
        elif channel == 'tch':
            cut_high = 2000
        h_sys = get_crop_hist(h_sys, cut_low, cut_high, f"{name}_sys_crop")
        h_nom = get_crop_hist(h_nom, cut_low, cut_high, f"{name}_nom_crop") 
    
    h_sys.SetName(f"h_sys_{name}")
    h_nom.SetName(f"h_nom_{name}")

    print(f"h_sys_sr: {h_sys.GetName()}, h_sys_sr: {h_sys.GetNbinsX()}, h_sys_sr_yield: {h_sys.Integral()}")
    print(f"h_nom_sr: {h_nom.GetName()}, h_nom_sr: {h_nom.GetNbinsX()}, h_nom_sr_yield: {h_nom.Integral()}")

    # calcualte SR/VR sys/nom ratio and error
    err_arr_sys_sr = array('d', [0.0])
    err_arr_nom_sr = array('d', [0.0])
    sr_sys = h_sys.IntegralAndError(0, nbins +1, err_arr_sys_sr)
    sr_nom = h_nom.IntegralAndError(0, nbins +1, err_arr_nom_sr)
    
    sr_ratio = sr_sys / sr_nom
    sr_ratio_err = sr_ratio * ((err_arr_sys_sr[0]/sr_sys) ** 2 + (err_arr_nom_sr[0]/sr_nom) ** 2) ** 0.5
    print(f"sr_sys: {sr_sys}, sr_nom: {sr_nom}, sr_ratio: {sr_ratio}, sr_ratio_err: {sr_ratio_err}")


    # 复制一份 sys，之后在上面做运算
    h_ratio_sr = h_sys.Clone(f"sr_ratio_{name}")
    h_ratio_sr.SetDirectory(0)
    h_ratio_sr.Divide(h_nom)         # r_sr_bin

    # 把 CR 的误差项加到每个 bin 上
    nb = h_ratio_sr.GetNbinsX()
    for ib in range(1, nb+1):
        dr   = h_ratio_sr.GetBinContent(ib)
        err0 = h_ratio_sr.GetBinError(ib)
        sigma_cr = abs((dr) * (cr_ratio_err / cr_ratio))
        total_err = math.hypot(err0, sigma_cr)
        h_ratio_sr.SetBinError(ib, total_err)

    

    # calcualte double ratio and error
    dr_ratio = sr_ratio / cr_ratio
    dr_ratio_err = dr_ratio * ((sr_ratio_err/sr_ratio) ** 2 + (cr_ratio_err/cr_ratio) ** 2) ** 0.5
    print(f"sr_ratio: {sr_ratio}, sr_ratio_err: {sr_ratio_err}, cr_ratio: {cr_ratio}, cr_ratio_err: {cr_ratio_err}, dr_ratio-1: {dr_ratio-1}, dr_ratio_err: {dr_ratio_err}")

    # # draw double ratio with CR ratio
    # h_DR = h_ratio_sr.Clone(f"dr_ratio_{name}")
    # h_DR.Divide(h_ratio_cr)
    # for i in range(1, h_DR.GetNbinsX()+1):
    #     if h_DR.GetBinContent(i) != 0:
    #        h_DR.SetBinContent(i, h_DR.GetBinContent(i) - 1)
    #     #    if h_DR.GetBinContent(i) == 0:
    #     #       h_DR.SetBinError(i, 0.1) h_sys
    # h_DR.SetName(f"dr_ratio_{name}")
    # DR_name = "double_ratio_" + name + ";E_{T}^{miss} [GeV];#DeltaTF/TF"
    # h_DR.SetTitle(DR_name)
        

    # 写入 output ROOT 文件
    out_file.cd()
    h_ratio_sr.Write()
    # h_DR.Write()
    h_sys.Write()
    h_nom.Write()
    # h_DR.SaveAs(f"dr_ratio_{name}.png")
    # c1.Write()

# 3) 关闭并保存
out_file.Close()
print("Saved all double-ratio histograms into doubleRatio.root")