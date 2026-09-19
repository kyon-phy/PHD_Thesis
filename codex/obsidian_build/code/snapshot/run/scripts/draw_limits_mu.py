#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from array import array
import numpy as np

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# ========== 1) Parse sample directory names ==========
# Expected directory name format example:
#   fit_taunub_sys_1l_allVR_SPLUSB_MU1500_gU1_5_23L0_2_alldecay_corrected
#   -> MU=1500, gU=1.5, beta=0.2
RE_NAME_noWeights = re.compile(
    r".*SPLUSB_MU(?P<MU>\d+).*?gU(?P<gUa>\d+)_(?P<gUb>\d+).*?23L(?P<betaA>\d+)_(?P<betaB>\d+)_noWeights",
    re.IGNORECASE,
)
RE_NAME_alldecay_corrected = re.compile(
    r".*SPLUSB_MU(?P<MU>\d+).*?gU(?P<gUa>\d+)_(?P<gUb>\d+).*?23L(?P<betaA>\d+)_(?P<betaB>\d+).*?alldecay_corrected",
    re.IGNORECASE,
)
# AcceptanceEff: 从文件名解析 (MU, gU, beta)，文件名例: MU1500_gU2_0_23L0_2_noWeights_bsm.root
RE_FILENAME_AcceptanceEff = re.compile(
    r"^MU(?P<MU>\d+)_gU(?P<gUa>\d+)_(?P<gUb>\d+)_23L(?P<betaA>\d+)_(?P<betaB>\d+)_noWeights_bsm\.root$",
    re.IGNORECASE,
)

# Dedicated betaR33=-1 all-decay Acceptance*Efficiency inputs. Keep this
# separate from the legacy noWeights parser above so the old plotting modes
# retain exactly their previous behaviour.
RE_FILENAME_ACCEPTANCE_B33RM1 = re.compile(
    r"^(?P<sample>MU(?P<MU>\d+)_gU(?P<gUa>\d+)_(?P<gUb>\d+)_"
    r"23L(?P<betaA>\d+)_(?P<betaB>\d+)_"
    r"(?P<b33>b33R(?:m)?\d+_\d+)_alldecay_corrected_"
    r"(?P<component>bsm|inf))\.root$",
    re.IGNORECASE,
)

B33RM1_ACCEPTANCE_MODES = {
    "AcceptanceEff_b33Rm1_Res_1b": ("met_SR_1tau0l1b_sch", "SR1b-Res"),
    "AcceptanceEff_b33Rm1_NonRes_1b": ("met_SR_1tau0l1b_tch", "SR1b-NonRes"),
    "AcceptanceEff_b33Rm1_Res_0b": ("met_WVR_1tau0l0b_sch", "SR0b-Res"),
    "AcceptanceEff_b33Rm1_NonRes_0b": ("met_WVR_1tau0l0b_tch", "SR0b-NonRes"),
}

# Default-weight v04 Acceptance*Efficiency inputs.  These samples must use the
# sample -> DSID mapping in the FastFrames YAML because several PMG dataset
# names do not encode the scan parameters.
RE_FILENAME_ACCEPTANCE_DEFAULT_WEIGHT = re.compile(
    r"^(?P<sample>MU(?P<MU>\d+)_gU(?P<gUa>\d+)_(?P<gUb>\d+)_"
    r"23L(?P<betaA>\d+)_(?P<betaB>\d+)"
    r"(?:_(?P<b33>b33Rm1_0))?_noWeights_"
    r"(?P<component>bsm|inf))\.root$",
    re.IGNORECASE,
)

DEFAULT_WEIGHT_ACCEPTANCE_MODES = {
    "AcceptanceEff_defaultWeight_Res_1b": ("met_SR_1tau0l1b_sch", "SR1b-Res"),
    "AcceptanceEff_defaultWeight_NonRes_1b": ("met_SR_1tau0l1b_tch", "SR1b-NonRes"),
    "AcceptanceEff_defaultWeight_Res_0b": ("met_WVR_1tau0l0b_sch", "SR0b-Res"),
    "AcceptanceEff_defaultWeight_NonRes_0b": ("met_WVR_1tau0l0b_tch", "SR0b-NonRes"),
}

DEFAULT_WEIGHT_SAMPLE_CONFIG = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "taunub",
        "config_taunub",
        "config_taunub_plot_sys_1l_sigs_noWeights_AccepEff_v04.yml",
    )
)

# The all-decay samples do not encode gU/betaL23 in the PMG dataset name, so
# resolve their Filter Efficiency through the generated DSID for each mass.
B33RM1_DSIDS = {
    ("bsm", 1500): 567628,
    ("bsm", 2000): 567629,
    ("bsm", 2500): 567630,
    ("bsm", 3000): 567631,
    ("bsm", 4000): 567632,
    ("bsm", 5000): 567633,
    ("inf", 1500): 567634,
}

def parse_params_from_dirname(dirname, sig="alldecay"):
    """Extract MU, gU, beta from directory name"""
    if sig == "alldecay":
        RE_NAME = RE_NAME_alldecay_corrected
    elif sig == "noWeights":
        RE_NAME = RE_NAME_noWeights
    else:
        raise ValueError(f"Invalid signal type: {sig}")
    m = RE_NAME.match(dirname)
    if not m:
        return None
    MU = int(m.group("MU"))
    gU = float(f"{int(m.group('gUa'))}.{int(m.group('gUb'))}")
    beta = float(f"{int(m.group('betaA'))}.{int(m.group('betaB'))}")
    return (MU, gU, beta)


def parse_params_from_filename(filename):
    """Extract MU, gU, beta from AcceptanceEff ROOT filename (e.g. MU1500_gU2_0_23L0_2_noWeights_bsm.root)."""
    m = RE_FILENAME_AcceptanceEff.match(filename)
    if not m:
        return None
    MU = int(m.group("MU"))
    gU = float(f"{int(m.group('gUa'))}.{int(m.group('gUb'))}")
    beta = float(f"{int(m.group('betaA'))}.{int(m.group('betaB'))}")
    return (MU, gU, beta)


def parse_params_from_XsecFile(signal_name):
    # get the mass point and gU from the signal name e.g."MGPy8EG_LQtaunuj_bsm_U1_M3000_g2_0_b23L1_4"
    RE_NAME = re.compile(
        r".*M(?P<mass>\d+)_g(?P<gUa>\d+)_(?P<gUb>\d+).*?b23L(?P<betaA>\d+)_(?P<betaB>\d)",
        re.IGNORECASE,
    )
    m = RE_NAME.match(signal_name)
    if not m:
        return None
    mass = float(f"{int(m.group('mass'))}")
    gU = float(f"{int(m.group('gUa'))}.{int(m.group('gUb'))}")
    beta = float(f"{int(m.group('betaA'))}.{int(m.group('betaB'))}")
    if "NET150" in signal_name:
        tag = "inf"
    else:
        tag = "bsm"
    # print(f"signal_name: {signal_name}, mass: {mass}, gU: {gU}, beta: {beta}, tag: {tag}")
    return (mass, gU, beta, tag) 

def read_FilterEff(xSecFile):
    FilterEffmap = {}
    with open(xSecFile, 'r') as f:
        # read the file line by line 
        for line in f:
            # skip the first line
            if line.startswith("dataset_number"):
                continue
            # get second and forth column as signal name and filter efficiency
            signal_name = line.split()[1]
            filter_efficiency = line.split()[3]
            params = parse_params_from_XsecFile(signal_name)
            if not params:
                continue
            (mass, gU, beta, tag) = params
            FilterEffmap[(mass, gU, beta, tag)] = filter_efficiency
            # print(f"mass={mass}, gU={gU}, beta={beta}, tag={tag} --> filter_efficiency={filter_efficiency}")
    return FilterEffmap

def read_acceptance_sumw(root_file_path, hist_name):
    """
    从 root 文件中读取 NOSYS/<hist_name> 的 SumOfWeights。
    hist_name: "met_SR_1tau0l1b_sch" (AcceptanceEff_Res_1b) 或 "met_SR_1tau0l1b_tch" (AcceptanceEff_NonRes_1b).
    成功返回 float，失败返回 None。
    """
    if not os.path.isfile(root_file_path):
        return None
    f = ROOT.TFile.Open(root_file_path, "READ")
    if not f or f.IsZombie():
        return None
    d = f.Get("NOSYS")
    if not d or not d.InheritsFrom("TDirectory"):
        f.Close()
        return None
    h = d.Get(hist_name)
    if not h or not h.InheritsFrom("TH1"):
        f.Close()
        return None
    sumw = h.GetSumOfWeights()
    f.Close()
    return float(sumw)

def parse_b33rm1_acceptance_filename(filename):
    """Parse one betaR33=-1 all-decay Acceptance*Efficiency ROOT filename."""
    match = RE_FILENAME_ACCEPTANCE_B33RM1.match(filename)
    if not match or match.group("b33").lower() != "b33rm1_0":
        return None
    return {
        "sample": match.group("sample"),
        "mass": int(match.group("MU")),
        "gU": float(f"{int(match.group('gUa'))}.{match.group('gUb')}"),
        "betaL23": float(f"{int(match.group('betaA'))}.{match.group('betaB')}"),
        "component": match.group("component").lower(),
    }


def read_sumw_corr_ratios(path):
    """Read sample -> corrected/nominal sumW from column four of the pipe table."""
    ratios = {}
    with open(path, "r") as ratio_file:
        for line_number, line in enumerate(ratio_file, start=1):
            if "|" not in line:
                continue
            columns = [column.strip() for column in line.split("|")]
            if len(columns) < 4 or not columns[0] or columns[0] == "sample":
                continue
            if set(columns[0]) == {"-"}:
                continue
            sample = columns[0]
            try:
                ratio = float(columns[3])
            except ValueError as exc:
                raise ValueError(
                    f"{path}:{line_number}: invalid sumW ratio in column four: {columns[3]!r}"
                ) from exc
            if not np.isfinite(ratio) or ratio == 0.0:
                raise ValueError(
                    f"{path}:{line_number}: sumW ratio must be finite and non-zero, got {ratio}"
                )
            if sample in ratios:
                raise ValueError(f"{path}:{line_number}: duplicate sample {sample}")
            ratios[sample] = ratio
    if not ratios:
        raise ValueError(f"No sumW ratios found in {path}")
    return ratios


def read_filter_eff_by_dsid(xsec_file, required_dsids=None):
    """Read generator Filter Efficiency (PMG column four), keyed by DSID."""
    filter_efficiencies = {}
    required_dsids = set(required_dsids) if required_dsids is not None else None
    with open(xsec_file, "r") as pmg_file:
        for line_number, line in enumerate(pmg_file, start=1):
            fields = line.split()
            if len(fields) < 4 or fields[0] == "dataset_number":
                continue
            try:
                dsid = int(fields[0])
                filter_efficiency = float(fields[3])
            except ValueError:
                continue
            if required_dsids is not None and dsid not in required_dsids:
                continue
            if not np.isfinite(filter_efficiency) or filter_efficiency <= 0.0:
                raise ValueError(
                    f"{xsec_file}:{line_number}: invalid Filter Efficiency for DSID {dsid}"
                )
            previous = filter_efficiencies.get(dsid)
            if previous is not None and not np.isclose(previous, filter_efficiency):
                raise ValueError(
                    f"{xsec_file}:{line_number}: inconsistent duplicate DSID {dsid}"
                )
            filter_efficiencies[dsid] = filter_efficiency
    return filter_efficiencies


def scan_input_dir_acceptance_b33rm1(input_dir, hist_name, ratios, filter_efficiencies):
    """
    Return separate BSM/interference maps for betaR33=-1.

    FastFrames normalises the corrected event weight with nominal sumW, so the
    requested inclusive efficiency is

        A*epsilon = histogram_yield / (sum_corrected/sum_nominal) * FilterEff.

    The ratio is already combined with the mc20a/d/e period fractions.
    """
    groups = {"bsm": {}, "inf": {}}
    selected_samples = set()
    skipped_other_b33 = 0

    for filename in sorted(os.listdir(input_dir)):
        full_path = os.path.join(input_dir, filename)
        if not os.path.isfile(full_path) or not filename.endswith(".root"):
            continue

        match = RE_FILENAME_ACCEPTANCE_B33RM1.match(filename)
        if not match:
            continue
        if match.group("b33").lower() != "b33rm1_0":
            skipped_other_b33 += 1
            continue

        params = parse_b33rm1_acceptance_filename(filename)
        sample = params["sample"]
        mass = params["mass"]
        gU = params["gU"]
        beta = params["betaL23"]
        component = params["component"]

        if sample not in ratios:
            raise KeyError(
                f"No fourth-column sumW ratio for betaR33=-1 sample: {sample}"
            )
        ratio = ratios[sample]

        dsid_key = (component, mass)
        if dsid_key not in B33RM1_DSIDS:
            raise KeyError(f"No PMG DSID mapping for component/mass {dsid_key}")
        dsid = B33RM1_DSIDS[dsid_key]
        if dsid not in filter_efficiencies:
            raise KeyError(f"DSID {dsid} is missing from the PMG xsec file")
        filter_efficiency = filter_efficiencies[dsid]

        raw_yield = read_acceptance_sumw(full_path, hist_name)
        if raw_yield is None:
            raise RuntimeError(f"NOSYS/{hist_name} is missing in {full_path}")

        acceptance_efficiency = raw_yield / ratio * filter_efficiency
        if not np.isfinite(acceptance_efficiency):
            raise ValueError(f"Non-finite Acceptance*Efficiency for {sample}")

        key = (mass, gU, beta)
        if key in groups[component]:
            raise ValueError(f"Duplicate {component} parameter point {key}")
        groups[component][key] = {
            "value": acceptance_efficiency,
            "raw_yield": raw_yield,
            "ratio": ratio,
            "filter_efficiency": filter_efficiency,
            "dsid": dsid,
            "sample": sample,
        }
        selected_samples.add(sample)

    target_ratio_samples = {
        sample
        for sample in ratios
        if parse_b33rm1_acceptance_filename(sample + ".root") is not None
    }
    missing_root_files = sorted(target_ratio_samples - selected_samples)
    if missing_root_files:
        preview = ", ".join(missing_root_files[:5])
        raise RuntimeError(
            f"{len(missing_root_files)} betaR33=-1 ratio entries have no ROOT file "
            f"in {input_dir}; first entries: {preview}"
        )

    print(
        f"[INFO] betaR33=-1 inputs: {len(groups['bsm'])} BSM + "
        f"{len(groups['inf'])} interference; skipped "
        f"{skipped_other_b33} other-betaR33 ROOT files"
    )
    return groups

def parse_default_weight_acceptance_filename(filename):
    """Parse a default-weight v04 signal ROOT filename."""
    match = RE_FILENAME_ACCEPTANCE_DEFAULT_WEIGHT.match(filename)
    if not match:
        return None
    beta_r = "b33Rm1_0" if match.group("b33") else "b33R0_0"
    return {
        "sample": match.group("sample"),
        "mass": int(match.group("MU")),
        "gU": float(f"{int(match.group('gUa'))}.{match.group('gUb')}"),
        "betaL23": float(f"{int(match.group('betaA'))}.{match.group('betaB')}"),
        "beta_r": beta_r,
        "component": match.group("component").lower(),
    }


def read_sample_dsids_from_config(config_path):
    """Read top-level FastFrames sample names and DSIDs without a YAML dependency."""
    sample_dsids = {}
    in_samples = False
    current_sample = None

    with open(config_path, "r") as config_file:
        for line_number, line in enumerate(config_file, start=1):
            stripped = line.strip()
            if line.startswith("samples:") and stripped == "samples:":
                in_samples = True
                current_sample = None
                continue
            if in_samples and stripped and not line[0].isspace() and not stripped.startswith("#"):
                break
            if not in_samples:
                continue

            if line.startswith("  - name:"):
                if current_sample is not None and sample_dsids[current_sample] is None:
                    raise ValueError(
                        f"{config_path}: no DSID list found for sample {current_sample}"
                    )
                raw_name = line.split(":", 1)[1].split("#", 1)[0].strip()
                if len(raw_name) >= 2 and raw_name[0] == raw_name[-1] and raw_name[0] in "\"'":
                    raw_name = raw_name[1:-1]
                if not raw_name:
                    raise ValueError(f"{config_path}:{line_number}: empty sample name")
                if raw_name in sample_dsids:
                    raise ValueError(
                        f"{config_path}:{line_number}: duplicate sample {raw_name}"
                    )
                sample_dsids[raw_name] = None
                current_sample = raw_name
                continue

            if current_sample is not None and line.startswith("    dsids:"):
                payload = line.split(":", 1)[1].split("#", 1)[0]
                dsids = tuple(int(token) for token in re.findall(r"\d+", payload))
                if not dsids:
                    raise ValueError(
                        f"{config_path}:{line_number}: empty DSID list for {current_sample}"
                    )
                sample_dsids[current_sample] = dsids

    if current_sample is not None and sample_dsids[current_sample] is None:
        raise ValueError(f"{config_path}: no DSID list found for sample {current_sample}")
    if not sample_dsids:
        raise ValueError(f"No top-level samples found in {config_path}")
    return sample_dsids


def scan_input_dir_acceptance_default_weight(
    input_dir, hist_name, sample_dsids, filter_efficiencies
):
    """
    Read every physical default-weight signal sample in the v04 config.

    These histograms use the nominal/default MC weight, so no corrected/nominal
    sumW ratio is applied:

        signal efficiency = histogram_yield * FilterEff.
    """
    configured = {}
    configured_by_sample = {}
    diagnostic_aliases = []

    for sample, dsids in sample_dsids.items():
        params = parse_default_weight_acceptance_filename(sample + ".root")
        if params is None:
            if re.match(r"^MU.*_noWeights_(?:bsm|inf)_mc20[ade]$", sample):
                diagnostic_aliases.append({"sample": sample, "dsids": dsids})
            continue
        if len(dsids) != 1:
            raise ValueError(
                f"Default-weight signal {sample} must map to exactly one DSID, got {dsids}"
            )
        dsid = dsids[0]
        group_key = (params["beta_r"], params["component"])
        point_key = (params["mass"], params["gU"], params["betaL23"])
        if group_key not in configured:
            configured[group_key] = {}
        if point_key in configured[group_key]:
            other = configured[group_key][point_key]["sample"]
            raise ValueError(
                f"Duplicate configured parameter point {group_key} {point_key}: "
                f"{other} and {sample}"
            )
        info = dict(params)
        info.update({"dsid": dsid, "key": point_key})
        configured[group_key][point_key] = info
        configured_by_sample[sample] = info

    required_dsids = {row["dsid"] for group in configured.values() for row in group.values()}
    missing_filter_eff = sorted(required_dsids - set(filter_efficiencies))
    if missing_filter_eff:
        raise KeyError(
            f"PMG Filter Efficiency is missing for DSIDs: {missing_filter_eff}"
        )

    groups = {group_key: {} for group_key in configured}
    selected_samples = set()
    skipped_non_signal = 0

    for filename in sorted(os.listdir(input_dir)):
        full_path = os.path.join(input_dir, filename)
        if not os.path.isfile(full_path) or not filename.endswith(".root"):
            continue
        params = parse_default_weight_acceptance_filename(filename)
        if params is None:
            skipped_non_signal += 1
            continue
        sample = params["sample"]
        if sample not in configured_by_sample:
            raise KeyError(
                f"ROOT sample {sample} is absent from the top-level samples block in the config"
            )
        info = configured_by_sample[sample]
        dsid = info["dsid"]
        filter_efficiency = filter_efficiencies[dsid]
        raw_yield = read_acceptance_sumw(full_path, hist_name)
        if raw_yield is None:
            raise RuntimeError(f"NOSYS/{hist_name} is missing in {full_path}")
        signal_efficiency = raw_yield * filter_efficiency
        if not np.isfinite(signal_efficiency):
            raise ValueError(f"Non-finite signal efficiency for {sample}")

        group_key = (info["beta_r"], info["component"])
        point_key = info["key"]
        if point_key in groups[group_key]:
            raise ValueError(f"Duplicate ROOT parameter point {group_key} {point_key}")
        row = dict(info)
        row.update(
            {
                "value": signal_efficiency,
                "raw_yield": raw_yield,
                "filter_efficiency": filter_efficiency,
                "status": "OK",
            }
        )
        groups[group_key][point_key] = row
        selected_samples.add(sample)

    missing_by_group = {group_key: [] for group_key in configured}
    for group_key, configured_points in configured.items():
        for point_key, info in configured_points.items():
            if info["sample"] in selected_samples:
                continue
            row = dict(info)
            row.update(
                {
                    "filter_efficiency": filter_efficiencies[info["dsid"]],
                    "status": "MISSING_ROOT",
                }
            )
            missing_by_group[group_key].append(row)
        missing_by_group[group_key].sort(key=lambda row: (row["key"], row["sample"]))

    available_count = sum(len(group) for group in groups.values())
    missing_count = sum(len(rows) for rows in missing_by_group.values())
    print(
        f"[INFO] default-weight inputs: {available_count} signal ROOT files, "
        f"{missing_count} configured physical samples missing ROOT, "
        f"{len(diagnostic_aliases)} campaign diagnostic aliases, "
        f"{skipped_non_signal} non-signal ROOT files skipped"
    )
    return groups, missing_by_group, diagnostic_aliases


# get hist frame
def get_empty_frame(hist, x_range=None, y_range=None):
    """
    创建空 frame 用于建立坐标系。
    若提供 x_range/y_range，则创建一个只有 1 bin 的 TH2F，轴范围完全由参数决定，不受原 hist 的 binning 约束。
    否则克隆原 hist 并清空内容。
    """
    if x_range is not None or y_range is not None:
        xlo = x_range[0] if x_range else hist.GetXaxis().GetXmin()
        xhi = x_range[1] if x_range else hist.GetXaxis().GetXmax()
        ylo = y_range[0] if y_range else hist.GetYaxis().GetXmin()
        yhi = y_range[1] if y_range else hist.GetYaxis().GetXmax()
        frame = ROOT.TH2F("frame", hist.GetTitle(), 1, xlo, xhi, 1, ylo, yhi)
        frame.SetDirectory(0)
        frame.SetStats(0)
        frame.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
        frame.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
        frame.GetXaxis().SetLabelSize(hist.GetXaxis().GetLabelSize())
        frame.GetYaxis().SetLabelSize(hist.GetYaxis().GetLabelSize())
        frame.GetXaxis().SetTitleSize(hist.GetXaxis().GetTitleSize())
        frame.GetYaxis().SetTitleSize(hist.GetYaxis().GetTitleSize())
        frame.GetXaxis().SetTitleOffset(hist.GetXaxis().GetTitleOffset())
        frame.GetYaxis().SetTitleOffset(hist.GetYaxis().GetTitleOffset())
        return frame
    frame = hist.Clone("frame")
    frame.SetDirectory(0)
    frame.Reset("ICES")
    frame.SetStats(0)
    return frame

# ========== NEW: 读取 Limits 的期望 μ 及其 ±1σ/±2σ ==========
def read_limits_mu_Asymptotics(root_file_path, unblind=False):
    """
    从 Limits/Asymptotics/myLimit.root 读取 TTree 'stats' 的期望上限：
      exp_upperlimit, exp_upperlimit_plus1/plus2, exp_upperlimit_minus1/minus2
    返回 dict: {'exp': float, 'p1': float, 'p2': float, 'm1': float, 'm2': float}
    """
    if not os.path.isfile(root_file_path):
        return None

    f = ROOT.TFile.Open(root_file_path, "READ")
    if not f or f.IsZombie():
        return None

    t = f.Get("stats")
    if not t or not isinstance(t, ROOT.TTree) or t.GetEntries() <= 0:
        f.Close()
        return None

    # 分支缓冲
    buf = {
        'exp': array('f', [0.0]),
        'p1':  array('f', [0.0]),
        'p2':  array('f', [0.0]),
        'm1':  array('f', [0.0]),
        'm2':  array('f', [0.0]),
    }
    # 分支名映射
    if not unblind:
        branches = {
            'exp': "exp_upperlimit",
            'p1':  "exp_upperlimit_plus1",
            'p2':  "exp_upperlimit_plus2",
            'm1':  "exp_upperlimit_minus1",
            'm2':  "exp_upperlimit_minus2",
        }
    else:
        branches = {
            'exp': "obs_upperlimit",
            'p1':  "exp_upperlimit_plus1",
            'p2':  "exp_upperlimit_plus2",
            'm1':  "exp_upperlimit_minus1",
            'm2':  "exp_upperlimit_minus2",
        }
    # 检查并绑定
    for k, bname in branches.items():
        br = t.GetBranch(bname)
        if not br:
            print(f"[WARN] branch '{bname}' missing in: {root_file_path}")
            f.Close()
            return None
        t.SetBranchAddress(bname, buf[k])

    t.GetEntry(0)
    out = {k: float(v[0]) for k, v in buf.items()}
    f.Close()
    return out

def read_limits_mu_toy(root_file_path, unblind=False):
    """
    从 Limits/Asymptotics/myLimit.root 读取 TTree 'stats' 的期望上限：
      exp_upperlimit, exp_upperlimit_plus1/plus2, exp_upperlimit_minus1/minus2
    返回 dict: {'exp': float, 'p1': float, 'p2': float, 'm1': float, 'm2': float}
    """
    if not os.path.isfile(root_file_path):
        return None

    f = ROOT.TFile.Open(root_file_path, "READ")
    if not f or f.IsZombie():
        return None

    t = f.Get("stats")
    if not t or not isinstance(t, ROOT.TTree) or t.GetEntries() <= 0:
        f.Close()
        return None

    # 分支缓冲
    buf = {
        'exp': array('f', [0.0]),
        'p1':  array('f', [0.0]),
        'p2':  array('f', [0.0]),
        'm1':  array('f', [0.0]),
        'm2':  array('f', [0.0]),
    }
    # 分支名映射
    if not unblind:
        branches = {
            'exp': "expectedLimit",
            'p1':  "expectedLimit_plus1",
            'p2':  "expectedLimit_plus2",
            'm1':  "expectedLimit_minus1",
            'm2':  "expectedLimit_minus2",
        }
    else:
        branches = {
            'exp': "observedLimit",
            'p1':  "expectedLimit_plus1",
            'p2':  "expectedLimit_plus2",
            'm1':  "expectedLimit_minus1",
            'm2':  "expectedLimit_minus2",
        }
    # 检查并绑定
    for k, bname in branches.items():
        br = t.GetBranch(bname)
        if not br:
            print(f"[WARN] branch '{bname}' missing in: {root_file_path}")
            f.Close()
            return None
        t.SetBranchAddress(bname, buf[k])

    t.GetEntry(0)
    out = {k: float(v[0]) for k, v in buf.items()}
    f.Close()
    return out

# ========== 3) Collect significance map ==========
# ========== NEW: 收集 μ 地图 ==========
def scan_input_dir_limits(input_dir, FilterEffmap, unblind=False, sig="alldecay", use_toy=False):
    """
    遍历 input_dir 的子目录，解析 (MU,gU,beta)，
    从 Limits/Asymptotics/myLimit.root 读出期望 μ 及其 ±1σ/±2σ。
    返回 dict: {(MU,gU,beta): {'exp':..., 'p1':..., 'p2':..., 'm1':..., 'm2':...}}

    若 sig 为 AcceptanceEff_Res_1b / AcceptanceEff_NonRes_1b：不扫目录名，改为扫 input_dir 下
    匹配 MU*_gU*_23L*_noWeights_bsm.root 的文件名，从 ROOT 的 NOSYS 里读
    met_SR_1tau0l1b_sch (Res) 或 met_SR_1tau0l1b_tch (NonRes) 的 SumOfWeights。
    """
    mmap = {}
    hist_name = ""
    
    if "AcceptanceEff" in sig:
        if sig == "AcceptanceEff_Res_1b":
            hist_name = "met_SR_1tau0l1b_sch" 
        elif sig == "AcceptanceEff_NonRes_1b":
            hist_name = "met_SR_1tau0l1b_tch"
        elif sig == "AcceptanceEff_Res_0b":
            hist_name = "met_WVR_1tau0l0b_sch"
        elif sig == "AcceptanceEff_NonRes_0b":
            hist_name = "met_WVR_1tau0l0b_tch"
        for name in os.listdir(input_dir):
            full = os.path.join(input_dir, name)
            if not os.path.isfile(full) or not name.endswith(".root"):
                continue
            params = parse_params_from_filename(name)
            if not params:
                continue
            MU, gU, beta = params
            sumw = read_acceptance_sumw(full, hist_name)
            filter_efficiency = float(FilterEffmap.get((MU, gU, beta, "bsm"), 1.0))
            if sumw is None:
                print(f"[WARN] NOSYS/{hist_name} SumOfWeights missing for: {name}")
                continue
            sumw_corrected = sumw * filter_efficiency
            muvals = {"exp": sumw_corrected, "p1": sumw_corrected, "m1": sumw_corrected, "p2": sumw_corrected, "m2": sumw_corrected}
            mmap[(MU, gU, beta)] = muvals
            print(f"Signal_name={name:>4}, MU={MU:>4}, gU={gU:>4}, beta={beta:>4} --> SumOfWeights({hist_name})={sumw:.4g}, filter_efficiency={filter_efficiency:.4g}, SumOfWeights_corrected={sumw_corrected:.4g}")
        return mmap

    for name in os.listdir(input_dir):
        full = os.path.join(input_dir, name)
        if not os.path.isdir(full):
            continue
        params = parse_params_from_dirname(name, sig)
        if not params:
            continue

        (MU, gU, beta) = params
        if use_toy:
            root_path = os.path.join(full, "Limits", "Toys.root")
            muvals = read_limits_mu_toy(root_path, unblind)
        else:
            root_path = os.path.join(full, "Limits", "Asymptotics", "myLimit.root")
            muvals = read_limits_mu_Asymptotics(root_path, unblind)
        if muvals is None:
            print(f"[WARN] limits missing for: {name}")
            continue

        mmap[(MU, gU, beta)] = muvals
        print(f"MU={MU:>4}, gU={gU:>4}, beta={beta:>4} --> μ_exp={muvals['exp']:.3f} (+1σ={muvals['p1']:.3f}, -1σ={muvals['m1']:.3f}, +2σ={muvals['p2']:.3f}, -2σ={muvals['m2']:.3f})")
    return mmap

# ========== NEW: 提取指定水平的等值线（返回第一条） ==========
def get_first_contour_at_level(h2, level, extend_x_low=None, extend_x_high=None):
    """
    给定 TH2D h2，提取水平=level 的第一条等值线 TGraph（Clone 返回）。
    注意：如果有多条等值线，这里只取第一条；复杂拓扑时可自行扩展。

    参数:
      extend_x_low : float or None
        若不为 None，将等值线在 x 负方向按端点斜率外推到该 x 值。
      extend_x_high : float or None
        若不为 None，将等值线在 x 正方向按端点斜率外推到该 x 值。
    """
    # ROOT 的等值线机制：SetContour + Draw("cont list") + gROOT.specials["contours"]
    lvl = np.array([level], dtype='float64')
    h2.SetContour(1, lvl)

    ctmp = ROOT.TCanvas("", "", 800, 600)  # 临时画布
    h2.Draw("CONT LIST")
    ctmp.Update()

    contours_obj = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    if not contours_obj:
        print("[WARN] No contours object found.")
        return None
    contours_list = contours_obj.At(0)  # 水平=level 对应的列表
    if not contours_list or contours_list.GetSize() == 0:
        print("[WARN] No contour graphs at this level.")
        return None

    g = contours_list.At(0)
    if not g:
        return None
    g2 = g.Clone()
    ROOT.SetOwnership(g2, False)

    # 延长等值线（按端点斜率外推）
    # 斜率用“端点 + 第二点”：首端用 (idx0, idx0_2)，末端用 (idxN, idxN_2)
    max_n = g2.GetN()
    idx0, idx0_2 = 0, 1       # 首端：第 0 点与第 1 点
    idxN_2, idxN = -2, -1     # 末端：倒数第 2 点与最后一点（下面会转为 n+idx）
    from ctypes import c_double
    if (extend_x_low is not None or extend_x_high is not None) and g2.GetN() >= 2:
        n = g2.GetN()
        x0, y0 = c_double(), c_double()
        x1, y1 = c_double(), c_double()
        xN, yN = c_double(), c_double()
        xN1, yN1 = c_double(), c_double()
        g2.GetPoint(idx0, x0, y0)
        g2.GetPoint(idx0_2, x1, y1)
        g2.GetPoint(n + idxN_2, xN1, yN1)
        g2.GetPoint(n + idxN, xN, yN)

        # 判断哪端是 x_min、哪端是 x_max
        if x0.value <= xN.value:
            # 首点=x_min端，末点=x_max端
            low_x, low_y, low_x2, low_y2 = x0.value, y0.value, x1.value, y1.value
            high_x, high_y, high_x2, high_y2 = xN.value, yN.value, xN1.value, yN1.value
            low_is_front = True
        else:
            # 末点=x_min端，首点=x_max端
            low_x, low_y, low_x2, low_y2 = xN.value, yN.value, xN1.value, yN1.value
            high_x, high_y, high_x2, high_y2 = x0.value, y0.value, x1.value, y1.value
            low_is_front = False

        # x 负方向延长
        if extend_x_low is not None:
            dx = low_x - low_x2
            if abs(dx) > 1e-12:
                slope = (low_y - low_y2) / dx
                y_ext = low_y + slope * (extend_x_low - low_x)
            else:
                y_ext = low_y
            if low_is_front:
                _extend_graph_front(g2, extend_x_low, y_ext)
            else:
                g2.SetPoint(g2.GetN(), extend_x_low, y_ext)

        # x 正方向延长
        if extend_x_high is not None:
            dx = high_x - high_x2
            if abs(dx) > 1e-12:
                slope = (high_y - high_y2) / dx
                y_ext = high_y + slope * (extend_x_high - high_x)
            else:
                y_ext = high_y
            if low_is_front:
                # x_max端在末尾，直接 append
                g2.SetPoint(g2.GetN(), extend_x_high, y_ext)
            else:
                # x_max端在首部，插入到最前面
                _extend_graph_front(g2, extend_x_high, y_ext)

    return g2


def tgraph_interp_y(g, x_query):
    """
    对 TGraph g 在 x=x_query 处做线性插值求 y。若 x_query 在 g 的 x 范围外则返回 None。
    """
    from ctypes import c_double
    if not g or g.GetN() < 2:
        return None
    n = g.GetN()
    xs = [g.GetX()[i] for i in range(n)]
    ys = [g.GetY()[i] for i in range(n)]
    x_min, x_max = min(xs), max(xs)
    if x_query < x_min or x_query > x_max:
        return None
    for i in range(n - 1):
        xa, xb = xs[i], xs[i + 1]
        if (xa - x_query) * (xb - x_query) <= 0:
            if xb == xa:
                return ys[i]
            t = (x_query - xa) / (xb - xa)
            return ys[i] + t * (ys[i + 1] - ys[i])
    return None


def get_x_at_y(g, y_target):
    """
    给定 TGraph g，求曲线与水平线 y=y_target 的所有交点对应的 x 值（线段线性插值）。
    返回 list of float。
    """
    from ctypes import c_double
    if not g or g.GetN() < 2:
        return []
    out = []
    for i in range(g.GetN() - 1):
        xa, ya = c_double(), c_double()
        xb, yb = c_double(), c_double()
        g.GetPoint(i, xa, ya)
        g.GetPoint(i + 1, xb, yb)
        ya, yb = ya.value, yb.value
        xa, xb = xa.value, xb.value
        if ya == yb:
            if ya == y_target:
                out.extend([xa, xb])
            continue
        t = (y_target - ya) / (yb - ya)
        if 0 <= t <= 1:
            out.append(xa + t * (xb - xa))
    return out


def print_x_at_y_values(g, label, y_values=(0.2, 2.0)):
    """对 TGraph g 在给定的 y 值处求 x 并打印。label 用于标识（如 MU=1500 或 beta=1.2）。"""
    if not g:
        return
    for y in y_values:
        xs = get_x_at_y(g, y)
        xs_str = ", ".join(f"{x:.4g}" for x in xs) if xs else "—"
        print(f"  [{label}] y={y} -> x = {xs_str}")


def _extend_graph_front(g, x_new, y_new):
    """在 TGraph g 的最前面插入一个点 (x_new, y_new)。"""
    from ctypes import c_double
    n = g.GetN()
    # 先读出所有已有的点
    xs, ys = [], []
    for i in range(n):
        xi, yi = c_double(), c_double()
        g.GetPoint(i, xi, yi)
        xs.append(xi.value)
        ys.append(yi.value)
    # 重新写入：新点在最前面
    g.Set(n + 1)
    g.SetPoint(0, x_new, y_new)
    for i in range(n):
        g.SetPoint(i + 1, xs[i], ys[i])

# ========== NEW: 填充两条等值线之间的半透明阴影 ==========
def fill_between_contours(canvas, g_low, g_high, color=ROOT.kGreen+1, alpha=0.25, fill_style=1001):
    """
    用两条等值线 g_low / g_high 构造闭合多边形并填充阴影。
    注意：如果等值线有多个不连通片段，这里只处理第一条 g 对象。
    """
    if not (g_low and g_high):
        return None

    n_hi = g_high.GetN()
    n_lo = g_low.GetN()
    if n_hi < 3 or n_lo < 3:
        return None

    # 用 array('d',[0.0]) 作为 GetPoint 的缓冲
    def graph_to_lists(g):
        xs, ys = [], []
        xb = array('d', [0.0])
        yb = array('d', [0.0])
        for i in range(g.GetN()):
            g.GetPoint(i, xb, yb)
            xs.append(xb[0])
            ys.append(yb[0])
        return xs, ys

    xh_list, yh_list = graph_to_lists(g_high)
    xl_list, yl_list = graph_to_lists(g_low)

    # 构造闭合多边形：high 正向 + low 反向
    xs = array('d', xh_list + xl_list[::-1])
    ys = array('d', yh_list + yl_list[::-1])
    n  = len(xs)

    poly = ROOT.TGraph(n, xs, ys)
    ROOT.SetOwnership(poly, False)
    try:
        poly.SetFillColorAlpha(color, alpha)  # 新版 ROOT 支持透明度
    except Exception:
        poly.SetFillColor(color)
    poly.SetFillStyle(fill_style)
    poly.SetLineColor(0)

    canvas.cd()
    poly.Draw("F SAME")
    canvas.Update()
    return poly

def enforce_monotonic_limits(mmap, fields=('exp','p1','m1','p2','m2'), EPS=1e-9):
    """
    对 mmap 中的每个通道值执行单调性清洗：
      - 固定 (MU, gU)，beta↑ => d 非增
      - 固定 (MU, beta)，gU↑ => d 非增
      - 固定 (gU, beta)，MU↑ => d 非减
    当违反时，把两者中较小的那个点的 d 置为 99. （若两者都为 99. 则不动）
    返回一个新的 dict，不修改原 mmap。
    """
    # 复制一份可写字典
    cleaned = {k: dict(v) for k, v in mmap.items()}

    mus   = sorted({k[0] for k in cleaned})
    gus   = sorted({k[1] for k in cleaned})
    betas = sorted({k[2] for k in cleaned})
    maximum = 99.0

    def set_to_maximum(key, f, changed_flag):
        if key in cleaned and f in cleaned[key] and cleaned[key][f] != maximum:
            print(f"set {key} {f} to maximum: {cleaned[key][f]} -> {maximum}")
            cleaned[key][f] = maximum
            return True
        return changed_flag

    changed = True
    while changed:
        changed = False

        # # # 1) (MU, gU) 固定，beta 递增：非增
        # for mu in mus:
        #     for gu in gus:
        #         for i in range(len(betas)-1):
        #             b0, b1 = betas[i], betas[i+1]
        #             k0 = (mu, gu, b0); k1 = (mu, gu, b1)
        #             if k0 not in cleaned or k1 not in cleaned:
        #                 continue
        #             for f in fields:
        #                 v0 = cleaned[k0][f]; v1 = cleaned[k1][f]
        #                 if v0 == maximum and v1 == maximum:
        #                     continue
        #                 if (v1 is None) or (v0 is None):
        #                     continue
        #                 # 违反非增：v1 > v0
        #                 if v1 > v0 + EPS:
        #                     # 把较小者置 maximum
        #                     if v0 <= v1:
        #                         changed = set_to_maximum(k0, f, changed)
        #                     else:
        #                         changed = set_to_maximum(k1, f, changed)

        # 2) (MU, beta) 固定，gU 递增：非增
        for mu in mus:
            for be in betas:
                for i in range(len(gus)-1):
                    g0, g1 = gus[i], gus[i+1]
                    k0 = (mu, g0, be); k1 = (mu, g1, be)
                    if k0 not in cleaned or k1 not in cleaned:
                        continue
                    for f in fields:
                        v0 = cleaned[k0][f]; v1 = cleaned[k1][f]
                        if v0 == maximum and v1 == maximum:
                            continue
                        if (v1 is None) or (v0 is None):
                            continue
                        # 违反非增：v1 > v0
                        if v1 > v0 + EPS:
                            if v0 <= v1:
                                changed = set_to_maximum(k0, f, changed)
                            else:
                                changed = set_to_maximum(k1, f, changed)

        # # 3) (gU, beta) 固定，MU 递增：非减
        # for gu in gus:
        #     for be in betas:
        #         for i in range(len(mus)-1):
        #             m0, m1 = mus[i], mus[i+1]
        #             k0 = (m0, gu, be); k1 = (m1, gu, be)
        #             if k0 not in cleaned or k1 not in cleaned:
        #                 continue
        #             for f in fields:
        #                 v0 = cleaned[k0][f]; v1 = cleaned[k1][f]
        #                 if v0 == maximum and v1 == maximum:
        #                     continue
        #                 if (v1 is None) or (v0 is None):
        #                     continue
        #                 # 违反非减：v1 < v0
        #                 if v1 + EPS < v0:
        #                     # 把较小者置 maximum
        #                     if v1 <= v0:
        #                         changed = set_to_maximum(k1, f, changed)
        #                     else:
        #                         changed = set_to_maximum(k0, f, changed)

    return cleaned

# get the yield histogram from output_yield.root
def get_yields(root_file_path, tag):
    f = ROOT.TFile.Open(root_file_path, "READ")
    if not f or f.IsZombie():
        return None
    h_yield_tmp = f.Get(f"h_interference_fraction_{tag}_Inf")
    h_yield = h_yield_tmp.Clone()
    h_yield.SetDirectory(0)
    f.Close()
    return h_yield


def draw_hist2d_text(hist, scale=100.0, decimals=3):
    """
    绘制 TH2 的 TEXT，可选将数值乘以 scale（如 1000 表示 fb）并只保留 decimals 位小数。
    不修改原 hist，用克隆绘制。
    """
    if scale == 1.0 and decimals is None:
        hist.Draw("TEXT")
        return
    h = hist.Clone(hist.GetName() + "_text_display")
    h.SetDirectory(0)
    ROOT.SetOwnership(h, False)
    if scale != 1.0:
        h.Scale(scale)
    # if decimals is not None and hasattr(h, "SetPaintTextFormat"):
    #     h.SetPaintTextFormat("%%.%df" % decimals)
    # ROOT.gStyle.SetPaintTextFormat(".%df%%" % decimals)
    ROOT.gStyle.SetPaintTextFormat(".2f%%")
    h.SetMarkerSize(1.5)
    h.Draw("TEXT")


# ========== NEW: 2D (固定 MU) 的 μ=1 等值线与 1σ/2σ 阴影 ==========
def draw_mu_slice_limits(mmap, outdir, output_file, base_hist="mu", limit_path=None, mu_exp=1, text_fb_3decimals=False, sigs=None, extra_path_1=None, extra_path_2=None):
    print("*********** draw mu slice (μ limits) ***********")
    mus    = sorted({k[0] for k in mmap})
    gus    = sorted({k[1] for k in mmap})
    betas  = sorted({k[2] for k in mmap})
    print("mus: ", mus)
    print("gus: ", gus)
    print("betas: ", betas)
    gu_edges   = get_bin_edges(gus,   n_steps=3)
    beta_edges = get_bin_edges(betas, n_steps=2)

    os.makedirs(outdir, exist_ok=True)

    for MU in mus:
        
        # extend canvas
        if sigs.startswith("AcceptanceEff"):
            set_appended_new_betas = {
                1500: [2.4, 2.6, 3.0],
                1800: [2.4, 2.6, 3.0],
                2000: [2.4, 2.6, 3.0],
                2500: [2.4, 2.6, 3.0],
                3000: [2.4, 2.6, 3.0],
                4000: [2.4, 2.6, 3.0],
                5000: [2.4, 2.6, 3.0],
            }
            added_betas = set_appended_new_betas[MU]
            betas_new = betas + added_betas
            beta_edges_new = get_bin_edges(betas_new, n_steps=2)
        else:
            beta_edges_new = beta_edges
        # 为五个集合各建一个 TH2D（内容=期望 μ）
        h_exp = ROOT.TH2D(f"h2_mu{MU}_exp", f";#it{{g_{{U}}}};#it{{#beta}}_{{#it{{L}}}}^{{23}};#mu (exp) (MU={MU} GeV)",
                          len(gu_edges)-1, gu_edges, len(beta_edges_new)-1, beta_edges_new)
        h_p1  = ROOT.TH2D(f"h2_mu{MU}_p1",  ";#it{g}_{U};#beta_{L}^{23};#mu (+1#kern[0.25]{#sigma})", len(gu_edges)-1, gu_edges, len(beta_edges_new)-1, beta_edges_new)
        h_m1  = ROOT.TH2D(f"h2_mu{MU}_m1",  ";#it{g}_{U};#beta_{L}^{23};#mu (-1#kern[0.25]{#sigma})", len(gu_edges)-1, gu_edges, len(beta_edges_new)-1, beta_edges_new)
        h_p2  = ROOT.TH2D(f"h2_mu{MU}_p2",  ";#it{g}_{U};#beta_{L}^{23};#mu (+2#sigma)", len(gu_edges)-1, gu_edges, len(beta_edges_new)-1, beta_edges_new)
        h_m2  = ROOT.TH2D(f"h2_mu{MU}_m2",  ";#it{g}_{U};#beta_{L}^{23};#mu (-2#sigma)", len(gu_edges)-1, gu_edges, len(beta_edges_new)-1, beta_edges_new)

        

        for (mu, gu, be), d in mmap.items():
            if mu != MU: 
                continue
            h_exp.Fill(gu, be, pow(d['exp'], mu_exp))
            h_p1.Fill(gu, be, pow(d['p1'], mu_exp)); h_m1.Fill(gu, be, pow(d['m1'], mu_exp))
            h_p2.Fill(gu, be, pow(d['p2'], mu_exp)); h_m2.Fill(gu, be, pow(d['m2'], mu_exp))

        # 提取 μ=1 的等值线
        g_exp = get_first_contour_at_level(h_exp, 1.0, extend_x_low=0, extend_x_high=3.2)
        g_p1  = get_first_contour_at_level(h_p1,  1.0, extend_x_low=0, extend_x_high=3.2)
        g_m1  = get_first_contour_at_level(h_m1,  1.0, extend_x_low=0, extend_x_high=3.2)
        g_p2  = get_first_contour_at_level(h_p2,  1.0, extend_x_low=0, extend_x_high=3.2)
        g_m2  = get_first_contour_at_level(h_m2,  1.0, extend_x_low=0, extend_x_high=3.2)
        print_x_at_y_values(g_exp, f"MU={MU}, x: gU, y: betaL23", y_values=(0.2, 1.4, 2.2)) # x: gU, y: betaL23

        # Print g_exp points
        # if g_exp is not None:
        #     n_points = g_exp.GetN()
        #     print(f"g_exp has {n_points} points for MU={MU}:")
        #     for i in range(n_points):
        #         x = g_exp.GetX()[i]
        #         y = g_exp.GetY()[i]
        #         print(f"  Point {i}: x={x}, y={y}")
        # else:
        #     print(f"g_exp is None for MU={MU}")

        # 画底图（用 text 帮助定位，或可换成 COLZ）
        c2 = ROOT.TCanvas(f"c_mu_limits_{MU}", "", 900, 750)
        
        # set grid and Ndiv
        # c2.SetGrid(True)
        # Ndivisions = 1050
        # h_exp.GetXaxis().SetNdivisions(Ndivisions)
        # h_exp.GetXaxis().SetTickLength(2)
        # set label size
        h_exp.GetXaxis().SetLabelSize(0.044)
        h_exp.GetYaxis().SetLabelSize(0.042)
        # set title size
        h_exp.GetXaxis().SetTitleSize(0.045)
        h_exp.GetYaxis().SetTitleSize(0.042)
        # set title offset
        h_exp.GetXaxis().SetTitleOffset(1.0)
        h_exp.GetYaxis().SetTitleOffset(1.13)
        
        # Adjust the x and y axis range for different mass points MU
        # You can define the ranges for each MU as needed
        # Example: set_ranges = {1000: ((0.0, 3.0), (0.0, 2.2)), 1500: ((0.2, 2.1), (0.1, 2.0)), ...}
        if sigs.startswith("AcceptanceEff"):
            set_ranges = {
                1500: ((0.5, 3.0), (0.1, 5.0)),
                1800: ((0.5, 3.0), (0.1, 5.0)),
                2000: ((0.5, 3.0), (0.1, 5.0)),
                2500: ((0.5, 3.0), (0.1, 5.0)),
                3000: ((0.5, 3.0), (0.1, 5.0)),
                4000: ((0.5, 3.0), (0.1, 5.0)),
                5000: ((0.5, 3.0), (0.1, 5.0)),
            }
        else:
            set_ranges = {
                # 1500: ((0.4, 3.0), (0, 2.2)), # nominal
                1500: ((0.4, 3.0), (0, 2.6)), # for 0b/1b SR overlap plots
                1800: ((0.4, 3.0), (0, 2.2)),
                2000: ((0.7, 3.0), (0, 2.2)),
                2500: ((0.8, 3.0), (0.4, 2.2)),
                3000: ((1.2, 3.0), (0.7, 2.2)),
                4000: ((1.2, 3.0), (0.7, 2.2)),
                5000: ((1.2, 3.0), (0.7, 2.2)),
            }
        set_legends_pos = {
             1500: (0.53,0.34,0.92,0.66),
             1800: (0.58,0.44,0.92,0.66),
             2000: (0.59,0.43,0.92,0.66),
             2500: (0.61,0.44,0.92,0.66),
             3000: (0.61,0.44,0.92,0.66),
             4000: (0.57,0.50,0.92,0.66),
             5000: (0.57,0.50,0.92,0.66),
        }
        set_legends_size = {
            1500: 0.035,
            1800: 0.03,
            2000: 0.03,
            2500: 0.03,
            3000: 0.03,
            5000: 0.03,
            4000: 0.03,
        }
        legends_pos = set_legends_pos[MU]
        x_range, y_range = set_ranges.get(MU, (None, None))
        
        # draw the yield histogram from output_yield.root
        if base_hist == "interference":
            root_file_path = "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots/output_yields.root"
            h_yield = get_yields(root_file_path, "tch")
            h_yield.Draw("TEXT")
            del h_yield
        elif base_hist == "mu":
            frame = get_empty_frame(h_exp, x_range=x_range, y_range=y_range)
            frame.Draw()
            if text_fb_3decimals:
                draw_hist2d_text(h_exp, scale=100.0, decimals=2)
            else:
                h_exp.Draw("TEXT")
        elif base_hist == "limit_read":
            frame = get_empty_frame(h_exp, x_range=x_range, y_range=y_range)
            frame.Draw()
            f = ROOT.TFile.Open(limit_path, "READ")
            g_exp_read = f.Get(f"g_exp_mu_{MU}")
            del f
        else:
            print(f"Invalid base option: {base_hist} or root file path: {root_file_path}")
            return

        # rename g_exp 
        if g_exp:
            g_exp.SetName(f"g_exp_mu_{MU}")
        if base_hist == "limit_read":
            g_exp_read.SetName(f"g_obs_mu_{MU}")
        if g_m1:
            g_m1.SetName(f"g_m1_mu_{MU}")
        if g_p1:
            g_p1.SetName(f"g_p1_mu_{MU}")
        if g_m2:
            g_m2.SetName(f"g_m2_mu_{MU}")
        if g_p2:
            g_p2.SetName(f"g_p2_mu_{MU}")

        
        # Draw a line at betaL23=0.2 and betaL23 = 2.0
        # line111 = ROOT.TLine(gu_edges[0], 0.2, gu_edges[-1], 0.2)
        # line111.SetLineColor(ROOT.kBlack); line111.SetLineStyle(1); line111.SetLineWidth(1); line111.Draw("L SAME")
        # line222 = ROOT.TLine(gu_edges[0], 2.0, gu_edges[-1], 2.0)
        # line222.SetLineColor(ROOT.kBlack); line222.SetLineStyle(1); line222.SetLineWidth(1); line222.Draw("L SAME")
        
        # 读取额外的两张图（格式与 limit_path 相同）
        g_extra_1, g_extra_2 = None, None
        graph_key = f"g_exp_mu_{MU}"
        if extra_path_1:
            f1 = ROOT.TFile.Open(extra_path_1, "READ")
            if f1 and not f1.IsZombie():
                g_extra_1 = f1.Get(graph_key)
                if g_extra_1:
                    g_extra_1 = g_extra_1.Clone(f"g_extra1_mu_{MU}")
                    ROOT.SetOwnership(g_extra_1, False)
                f1.Close()
        if extra_path_2:
            f2 = ROOT.TFile.Open(extra_path_2, "READ")
            if f2 and not f2.IsZombie():
                g_extra_2 = f2.Get(graph_key)
                if g_extra_2:
                    g_extra_2 = g_extra_2.Clone(f"g_extra2_mu_{MU}")
                    ROOT.SetOwnership(g_extra_2, False)
                f2.Close()


        
        # 先填 2σ 带，再填 1σ 带
        poly_2sigma = fill_between_contours(c2, g_m2, g_p2, color=ROOT.kYellow, alpha=0.85)  # 2σ 浅色
        poly_1sigma = fill_between_contours(c2, g_m1, g_p1, color=ROOT.kGreen, alpha=1) # 1σ 深一点

        # Draw expected limit
        if base_hist == "limit_read" and g_exp_read:
            g_exp_read.SetLineColor(ROOT.kRed); g_exp_read.SetLineStyle(1); g_exp_read.SetLineWidth(3);
            g_exp_read.Draw("L SAME")

        # set line styles
        if g_exp: g_exp.SetLineColor(ROOT.kBlack);  g_exp.SetLineStyle(2); g_exp.SetLineWidth(2); g_exp.Draw("L SAME")

        # Draw extra graphs (g_extra_1 and g_extra_2)
        if g_extra_1:
            g_extra_1.SetLineColor(ROOT.kBlue); g_extra_1.SetLineStyle(7); g_extra_1.SetLineWidth(2)
            g_extra_1.Draw("L SAME")
        if g_extra_2:
            g_extra_2.SetLineColor(ROOT.kMagenta); g_extra_2.SetLineStyle(9); g_extra_2.SetLineWidth(2)
            g_extra_2.Draw("L SAME")

        # 注释
        mu_teV = float(MU) * 1e-3
        lat = ROOT.TLatex(); lat.SetNDC(True); lat.SetTextSize(0.045)
        lat2 = ROOT.TLatex(); lat2.SetNDC(True); lat2.SetTextSize(0.04)
        lat3 = ROOT.TLatex(); lat3.SetNDC(True); lat3.SetTextSize(0.04)
        lat4 = ROOT.TLatex(); lat4.SetNDC(True); lat4.SetTextSize(0.04)
        lat_pos_x = 0.15
        lat_pos_y = 0.83
        lat_pos_y_step = 0.05
        if sigs == "AcceptanceEff_Res_1b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat2.DrawLatex(lat_pos_x, lat_pos_y - lat_pos_y_step, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, "#bf{Signal Acceptance*Efficiency}")
            lat4.DrawLatex(lat_pos_x, lat_pos_y - 3*lat_pos_y_step, "#bf{#it{m}_{#it{U}}_{1} = %.1f TeV, SR1b-Res}" % mu_teV)
        elif sigs == "AcceptanceEff_NonRes_1b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat2.DrawLatex(lat_pos_x, lat_pos_y - lat_pos_y_step, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, "#bf{Signal Acceptance*Efficiency}")
            lat4.DrawLatex(lat_pos_x, lat_pos_y - 3*lat_pos_y_step, "#bf{#it{m}_{#it{U}}_{1} = %.1f TeV, SR1b-NonRes}" % mu_teV)
        elif sigs == "AcceptanceEff_Res_0b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat2.DrawLatex(lat_pos_x, lat_pos_y - lat_pos_y_step, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, "#bf{Signal Acceptance*Efficiency}")
            lat4.DrawLatex(lat_pos_x, lat_pos_y - 3*lat_pos_y_step, "#bf{#it{m}_{#it{U}}_{1} = %.1f TeV, SR0b-Res}" % mu_teV)
        elif sigs == "AcceptanceEff_NonRes_0b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat2.DrawLatex(lat_pos_x, lat_pos_y - lat_pos_y_step, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, "#bf{Signal Acceptance*Efficiency}")
            lat4.DrawLatex(lat_pos_x, lat_pos_y - 3*lat_pos_y_step, "#bf{#it{m}_{#it{U}}_{1} = %.1f TeV, SR0b-NonRes}" % mu_teV)
        else:
            if g_extra_1:
                lat.DrawLatex(0.5, lat_pos_y, f"#it{{ATLAS}}")
            else:
                lat.DrawLatex(0.5, lat_pos_y, f"#it{{ATLAS}}")
            lat2.DrawLatex(0.5, lat_pos_y - lat_pos_y_step, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
            lat3.DrawLatex(0.5, lat_pos_y - 2*lat_pos_y_step, "#bf{#it{m}_{#it{U}}_{1} = %.1f TeV}" % mu_teV)
            lat4.DrawLatex(0.5, lat_pos_y - 3*lat_pos_y_step, "#bf{95% CL upper limit}")
        leg = ROOT.TLegend(legends_pos[0],legends_pos[1],legends_pos[2],legends_pos[3])
        leg.SetTextSize(set_legends_size[MU])
        leg.SetMargin(0.15)
        if g_exp:
            leg.AddEntry(g_exp, "Exp.", "l")
        if poly_1sigma:
            leg.AddEntry(poly_1sigma, "Exp. #pm1#kern[0.25]{#sigma}","f")
        if poly_2sigma:
            leg.AddEntry(poly_2sigma, "Exp. #pm2#sigma","f")
        if base_hist == "limit_read" and g_exp_read:
            leg.AddEntry(g_exp_read, "Obs.","l")
            # leg.AddEntry(g_exp_read, "BSM+Interference Exp.","l")
            # leg.AddEntry(g_exp_read, "TOY Exp.","l")
        if g_extra_1:
            leg.AddEntry(g_extra_1, "Exp. (SR0b)", "l")
            # leg.AddEntry(g_extra_1, "Exp. (SR1b-Res + SR0b-Res)", "l")
        if g_extra_2:
            leg.AddEntry(g_extra_2, "Exp. (SR1b)", "l")
            # leg.AddEntry(g_extra_2, "Exp. (SR1b-NonRes + SR0b-NonRes)", "l")


        # 叠加 b 异常阴影（可选，沿用你已有的工具）
        # Draw limit without cLL fit values
        # gU_beta_limit_high, gU_beta_limit_low = get_b_anomalies_production_limit(MU * 1e-3) 
        # fill_between_curves(c2, MU, gU_beta_limit_low, gU_beta_limit_high, gu_edges[0], gu_edges[-1], n_points=200, fill_color=ROOT.kGray+2, fill_style=3004)

        # Draw shaded b anomalies region with cLL fit values
        if sigs.startswith("AcceptanceEff"):
            pass
        else:
            fill_between_curves(c2, leg, MU, gu_edges[0], gu_edges[-1], n_points=200, fill_color=ROOT.kGray+1, fill_style=3004, Alpha=1, sigma=2)
            fill_between_curves(c2, leg, MU, gu_edges[0], gu_edges[-1], n_points=200, fill_color=ROOT.kGray+2, fill_style=3005, Alpha=1, sigma=1)
            # draw the legend
            leg.SetTextAlign(13);
            leg.SetFillStyle(0);
            leg.SetBorderSize(0); leg.Draw()

        # draw ticks on the right and top of the canvas
        ROOT.gPad.SetTicks(1,1)
        ROOT.gPad.RedrawAxis()

        # 输出
        output_file.cd()
        # c2.Write()
        if g_exp:
            g_exp.Write()
        if base_hist == "limit_read" and g_exp_read:
            g_exp_read.Write()
        if g_extra_1:
            g_extra_1.Write()
        if g_extra_2:
            g_extra_2.Write()
        if g_m1:
            g_m1.Write()
        if g_p1:
            g_p1.Write()
        if g_m2:
            g_m2.Write()
        if g_p2:
            g_p2.Write()
        if base_hist == "mu":
            h_exp.Write()
        c2.SaveAs(os.path.join(outdir, f"mu1_contours_mu{MU}.pdf"))

        c2.Close()
        del h_exp, h_p1, h_m1, h_p2, h_m2

# ========== NEW: 2D (固定 beta) 的 μ=1 等值线与 1σ/2σ 阴影 ==========
def draw_beta_slice_limits(mmap, outdir, output_file, base_hist="mu", limit_path=None, extra_path_1=None, extra_path_2=None, mu_exp=1, text_fb_3decimals=False, sigs=None):
    print("*********** draw beta slice (μ limits) ***********")
    mus    = sorted({k[0] for k in mmap})
    gus    = sorted({k[1] for k in mmap})
    betas  = sorted({k[2] for k in mmap})
    
    mu_edges  = get_bin_edges(mus,  n_steps=2)
    gu_edges  = get_bin_edges(gus,  n_steps=2)

    os.makedirs(outdir, exist_ok=True)

    for beta in betas:
        
        # extend canvas gus range
        set_appended_new_gus = {
            0.0: [3.2, 3.5, 4.0],
            0.2: [3.2, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
            0.4: [3.2, 3.5, 4.0, 4.5, 5.0],
            0.6: [3.2, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0],
            0.8: [3.2, 3.5, 4.0, 4.5],
            1.0: [3.2, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0],
            1.2: [3.2, 3.5, 4.0],
            1.4: [3.2],
            1.6: [3.2],
            1.8: [3.2],
            2.0: [3.2],
            2.2: [3.2],
        }
        added_gus = set_appended_new_gus[beta]
        gus_new = gus + added_gus
        gu_edges_new = get_bin_edges(gus_new,  n_steps=2)

        h_exp = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_exp", f";#it{{m}}_{{#it{{U}}_{{1}}}} [GeV];#it{{g_{{U}}}};#mu (exp) (beta={beta})", len(mu_edges)-1, mu_edges, len(gu_edges)-1, gu_edges)
        h_p1  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_p1",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (+1#kern[0.25]{#sigma})", len(mu_edges)-1, mu_edges, len(gu_edges)-1, gu_edges)
        h_m1  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_m1",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (-1#kern[0.25]{#sigma})", len(mu_edges)-1, mu_edges, len(gu_edges)-1, gu_edges)
        h_p2  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_p2",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (+2#sigma)", len(mu_edges)-1, mu_edges, len(gu_edges)-1, gu_edges)
        h_m2  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_m2",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (-2#sigma)", len(mu_edges)-1, mu_edges, len(gu_edges)-1, gu_edges)

        h_exp_new = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_exp_new", f";#it{{m}}_{{#it{{U}}_{{1}}}} [GeV];#it{{g_{{U}}}};#mu (exp) (beta={beta})", len(mu_edges)-1, mu_edges, len(gu_edges_new)-1, gu_edges_new)
        h_p1_new  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_p1_new",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (+1#kern[0.25]{#sigma})", len(mu_edges)-1, mu_edges, len(gu_edges_new)-1, gu_edges_new)
        h_m1_new  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_m1_new",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (-1#kern[0.25]{#sigma})", len(mu_edges)-1, mu_edges, len(gu_edges_new)-1, gu_edges_new)
        h_p2_new  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_p2_new",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (+2#sigma)", len(mu_edges)-1, mu_edges, len(gu_edges_new)-1, gu_edges_new)
        h_m2_new  = ROOT.TH2D(f"h2_beta{str(beta).replace('.','_')}_m2_new",  ";#it{{m}}_{#it{{U}}_{{1}}} [GeV];g_{#it{{U}}};#mu (-2#sigma)", len(mu_edges)-1, mu_edges, len(gu_edges_new)-1, gu_edges_new)

        for (mu, gu, be), d in mmap.items():
            if be != beta:
                continue
            h_exp.Fill(mu, gu, pow(d['exp'], mu_exp))
            h_p1.Fill(mu, gu, pow(d['p1'], mu_exp)); h_m1.Fill(mu, gu, pow(d['m1'], mu_exp))
            h_p2.Fill(mu, gu, pow(d['p2'], mu_exp)); h_m2.Fill(mu, gu, pow(d['m2'], mu_exp))

        g_exp = get_first_contour_at_level(h_exp, 1.0, extend_x_low=1300, extend_x_high=3000)
        g_p1  = get_first_contour_at_level(h_p1,  1.0, extend_x_low=1300, extend_x_high=3000)
        g_m1  = get_first_contour_at_level(h_m1,  1.0, extend_x_low=1300, extend_x_high=3000)
        print(f"Start drawing g_p2")
        g_p2  = get_first_contour_at_level(h_p2,  1.0, extend_x_low=1300, extend_x_high=3000)
        print(f"Start drawing g_m2")
        g_m2  = get_first_contour_at_level(h_m2,  1.0, extend_x_low=1300, extend_x_high=3000)
        print_x_at_y_values(g_exp, f"beta={beta}, x:MU, y: gU", y_values=(3.3, 3.35, 3.36, 3.37, 3.38, 3.39, 3.4, 3.45)) # x:MU, y: gU
        
        # Check if the contours exist and can be drawn
        contours = {
            "Expected Limit μ=1": g_exp,
            "+1σ (μ=1)": g_p1,
            "-1σ (μ=1)": g_m1,
            "+2σ (μ=1)": g_p2,
            "-2σ (μ=1)": g_m2,
        }
        for label, g in contours.items():
            if g is None or not hasattr(g, "Draw"):
                print(f"Warning: {label} contour is not valid for beta = {beta} (g is None or not drawable)")
            # 当目标是g_p2且不存在时，用 g_m2 关于 g_exp 对称得到：在两根线共同 x 范围内插值取点，y_p2 = 2*y_exp - y_m2
            if label == "+2σ (μ=1)" and (g is None or not hasattr(g, "Draw")):
                g_ref = g_exp
                g_other = g_m2
                if g_ref is not None and g_ref.GetN() >= 2 and g_other is not None and g_other.GetN() >= 2:
                    # 收集两根线都存在的 x：取两图 x 的并集，且在两者共同范围内的 x
                    x_ref = [g_ref.GetX()[i] for i in range(g_ref.GetN())]
                    x_other = [g_other.GetX()[i] for i in range(g_other.GetN())]
                    x_min = max(min(x_ref), min(x_other))
                    x_max = min(max(x_ref), max(x_other))
                    x_common = sorted(set(x_ref + x_other))
                    x_common = [x for x in x_common if x_min <= x <= x_max]
                    if not x_common:
                        print(f"Cannot create symmetric +2σ for beta = {beta}: no overlapping x range")
                    else:
                        from array import array
                        x_p2 = array('d')
                        y_p2 = array('d')
                        for x in x_common:
                            y_exp = tgraph_interp_y(g_ref, x)
                            y_m2 = tgraph_interp_y(g_other, x)
                            if y_exp is not None and y_m2 is not None:
                                x_p2.append(x)
                                y_p2.append(2.0 * y_exp - y_m2)
                        if len(x_p2) >= 2:
                            g_p2_sym = ROOT.TGraph(len(x_p2), x_p2, y_p2)
                            g_p2_sym.SetLineStyle(2)
                            g_p2_sym.SetLineColor(4)
                            print(f"Created symmetric '+2σ (μ=1)' contour from '-2σ (μ=1)' and 'Expected Limit μ=1' for beta = {beta} ({len(x_p2)} points)")
                            contours[label] = g_p2_sym
                            g_p2 = g_p2_sym
                        else:
                            print(f"Cannot create symmetric +2σ for beta = {beta}: got only {len(x_p2)} points after interpolation")
                else:
                    print(f"Cannot create symmetric +2σ for beta = {beta}: reference graph missing or invalid")
            else:
                print(f"{label} contour is valid and drawable for beta = {beta}")

        c2 = ROOT.TCanvas(f"c_beta_limits_{str(beta).replace('.','_')}", "", 900, 750)
        
        # set label size
        h_exp_new.GetXaxis().SetLabelSize(0.044)
        h_exp_new.GetYaxis().SetLabelSize(0.042)
        # set title size
        h_exp_new.GetXaxis().SetTitleSize(0.044)
        h_exp_new.GetYaxis().SetTitleSize(0.042)
        # set title offset
        h_exp_new.GetXaxis().SetTitleOffset(1.0)
        h_exp_new.GetYaxis().SetTitleOffset(1.05)
        
        # Adjust the x and y axis range for different beta points
        # You can define the ranges for each beta as needed
        # Example: set_ranges = {1000: ((0.0, 3.0), (0.0, 2.2)), 1500: ((0.2, 2.1), (0.1, 2.0)), ...}
        set_ranges = {
            0.0: ((1500, 2000), (0, 5.)),
            0.2: ((1500, 2000), (0.01, 5.5)),
            0.4: ((1500, 3000), (0, 6.5)),
            0.6: ((1500, 3000), (0, 6.8)),
            0.8: ((1500, 3000), (0, 5.5)),
            1.0: ((1500, 3000), (0, 5.5)),
            1.2: ((1500, 3000), (0, 4.)),
            1.4: ((1500, 3000), (0, 3.5)),
            1.6: ((1500, 3000), (0, 3.2)),
            1.8: ((1500, 3000), (0, 3.)),
            2.0: ((1500, 3000), (0, 2.7)),
            2.2: ((1500, 3000), (0, 2.5)),
        }
        set_legends_pos = {
            0.0: (0.5,0.73,0.84,0.86),
            0.2: (0.46,0.59,0.84,0.86),
            0.4: (0.46,0.61,0.84,0.86),
            0.6: (0.46,0.61,0.84,0.86),
            0.8: (0.46,0.61,0.84,0.86),
            # 1.0: (0.46,0.54,0.88,0.86), # nominal
            1.0: (0.44,0.50,0.88,0.86), # for Res/NonRes overlap plots
            1.2: (0.46,0.61,0.84,0.86),
            1.4: (0.46,0.61,0.84,0.86),
            1.6: (0.46,0.59,0.84,0.86),
            1.8: (0.46,0.58,0.84,0.86),
            2.0: (0.46,0.60,0.84,0.86),
            2.2: (0.46,0.60,0.84,0.86),
        }
        set_legends_size = {
            0.0: 0.031,
            0.2: 0.031,
            0.4: 0.031,
            0.6: 0.031,
            0.8: 0.031,
            # 1.0: 0.031, # nominal
            1.0: 0.029, # for Res/NonRes overlap plots
            1.2: 0.031,
            1.4: 0.031,
            1.6: 0.031,
            1.8: 0.031,
            2.0: 0.031,
            2.2: 0.031,
        }
        legends_pos = set_legends_pos[beta]
        x_range, y_range = set_ranges.get(beta, (None, None))
        print(f"x_range: {x_range}, y_range: {y_range}, beta: {beta}")

        # 用自由范围的 frame 建立坐标系（不受 histogram binning 约束）
        frame = get_empty_frame(h_exp_new, x_range=x_range, y_range=y_range)
        # set N divisions for ticks
        if beta == 0.2:
            frame.GetXaxis().SetNdivisions(505) # ticks = N1 + 100*N2 + 10000*N3
        frame.Draw()
        if base_hist == "mu":
            if text_fb_3decimals:
                draw_hist2d_text(h_exp_new, scale=100, decimals=2)
            else:
                h_exp_new.Draw("TEXT SAME")
        elif base_hist == "limit_read":
            f = ROOT.TFile.Open(limit_path, "READ")
            g_exp_read = f.Get(f"g_exp_beta_{str(beta).replace('.','_')}")
            del f

        # 读取额外的两张图（格式与 limit_path 相同）
        g_extra_1, g_extra_2 = None, None
        graph_key = f"g_exp_beta_{str(beta).replace('.','_')}"
        if extra_path_1:
            f1 = ROOT.TFile.Open(extra_path_1, "READ")
            if f1 and not f1.IsZombie():
                g_extra_1 = f1.Get(graph_key)
                if g_extra_1:
                    g_extra_1 = g_extra_1.Clone(f"g_extra1_beta_{str(beta).replace('.','_')}")
                    ROOT.SetOwnership(g_extra_1, False)
                f1.Close()
        if extra_path_2:
            f2 = ROOT.TFile.Open(extra_path_2, "READ")
            if f2 and not f2.IsZombie():
                g_extra_2 = f2.Get(graph_key)
                if g_extra_2:
                    g_extra_2 = g_extra_2.Clone(f"g_extra2_beta_{str(beta).replace('.','_')}")
                    ROOT.SetOwnership(g_extra_2, False)
                f2.Close()


        poly_2sigma = fill_between_contours(c2, g_m2, g_p2, color=ROOT.kYellow, alpha=0.85)
        poly_1sigma = fill_between_contours(c2, g_m1, g_p1, color=ROOT.kGreen, alpha=1)

        # draw read limits
        if base_hist == "limit_read" and g_exp_read:
            g_exp_read.SetLineColor(ROOT.kRed); g_exp_read.SetLineStyle(1); g_exp_read.SetLineWidth(3);
            g_exp_read.Draw("L SAME")

        # draw expected limits
        if g_exp: g_exp.SetLineColor(ROOT.kBlack);  g_exp.SetLineStyle(2); g_exp.SetLineWidth(2); g_exp.Draw("L SAME")

        # rename g_exp 
        if g_exp:
            g_exp.SetName(f"g_exp_beta_{str(beta).replace('.','_')}")
        if base_hist == "limit_read" and g_exp_read:
            g_exp_read.SetName(f"g_obs_beta_{str(beta).replace('.','_')}")
        if g_m1:
            g_m1.SetName(f"g_m1_beta_{str(beta).replace('.','_')}")
        if g_p1:
            g_p1.SetName(f"g_p1_beta_{str(beta).replace('.','_')}")
        if g_m2:
            g_m2.SetName(f"g_m2_beta_{str(beta).replace('.','_')}")
        if g_p2:
            g_p2.SetName(f"g_p2_beta_{str(beta).replace('.','_')}") 


        # 画额外的两条线
        if g_extra_1:
            g_extra_1.SetLineColor(ROOT.kBlue); g_extra_1.SetLineStyle(7); g_extra_1.SetLineWidth(2)
            g_extra_1.Draw("L SAME")
        if g_extra_2:
            g_extra_2.SetLineColor(ROOT.kMagenta); g_extra_2.SetLineStyle(9); g_extra_2.SetLineWidth(2)
            g_extra_2.Draw("L SAME")

        # draw the legend and latex
        lat_pos_x = 0.15
        lat_pos_y = 0.82
        lat_pos_y_step = 0.05
        lat = ROOT.TLatex(); lat.SetNDC(True); lat.SetTextSize(0.045)
        lat2 = ROOT.TLatex(); lat2.SetNDC(True); lat2.SetTextSize(0.04)
        lat2.DrawLatex(lat_pos_x, lat_pos_y - lat_pos_y_step, f"#bf{{#sqrt{{s}} = 13 TeV, 140 fb^{{-1}}}}")
        lat3 = ROOT.TLatex(); lat3.SetNDC(True); lat3.SetTextSize(0.04)
        if sigs == "AcceptanceEff_Res_1b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, f"#bf{{#it{{#beta}}_{{#it{{L}}}}^{{23}} = {beta}, SR1b-Res}}")
        elif sigs == "AcceptanceEff_NonRes_1b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, f"#bf{{#it{{#beta}}_{{#it{{L}}}}^{{23}} = {beta}, SR1b-NonRes}}")
        elif sigs == "AcceptanceEff_Res_0b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, f"#bf{{#it{{#beta}}_{{#it{{L}}}}^{{23}} = {beta}, SR0b-Res}}")
        elif sigs == "AcceptanceEff_NonRes_0b":
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}} #bf{{Simulation}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, f"#bf{{#it{{#beta}}_{{#it{{L}}}}^{{23}} = {beta}, SR0b-NonRes}}")
        else:
            lat.DrawLatex(lat_pos_x, lat_pos_y, f"#it{{ATLAS}}")
            lat3.DrawLatex(lat_pos_x, lat_pos_y - 2*lat_pos_y_step, f"#bf{{#it{{#beta}}_{{#it{{L}}}}^{{23}} = {beta}}}")
        lat4 = ROOT.TLatex(); lat4.SetNDC(True); lat4.SetTextSize(0.04)
        lat4.DrawLatex(lat_pos_x, lat_pos_y - 3*lat_pos_y_step, "#bf{95% CL upper limit}")
        leg2 = ROOT.TLegend(legends_pos[0],legends_pos[1],legends_pos[2],legends_pos[3])
        leg2.SetTextSize(set_legends_size[beta])
        leg2.SetMargin(0.15)
        if g_exp:
            leg2.AddEntry(g_exp, "Exp.", "l")
        if poly_1sigma:
            leg2.AddEntry(poly_1sigma, "Exp. #pm1#kern[0.25]{#sigma}","f")
        if poly_2sigma:
            leg2.AddEntry(poly_2sigma, "Exp. #pm2#sigma","f")
        if base_hist == "limit_read" and g_exp_read:
            leg2.AddEntry(g_exp_read, "Obs.", "l")
            # leg2.AddEntry(g_exp_read, "BSM+Interference Exp.", "l")
        if g_extra_1:
            # leg2.AddEntry(g_extra_1, "Exp. (SR0b)", "l")
            leg2.AddEntry(g_extra_1, "Exp. (SR1b-Res + SR0b-Res)", "l")
        if g_extra_2:
            # leg2.AddEntry(g_extra_2, "Exp. (SR1b)", "l")
            leg2.AddEntry(g_extra_2, "Exp. (SR1b-NonRes + SR0b-NonRes)", "l")
        leg2.SetTextAlign(13);
        leg2.SetFillStyle(0)
        leg2.SetBorderSize(0); leg2.Draw()

        # 叠加 b 异常质量-耦合阴影（沿用你已有函数）
        x_range = [mu_edges[0], mu_edges[-1]]
        print(f"x_range for b anomalies region: {x_range}")
        # draw_b_anomalies_mass_region(c2, x_range, beta)
        draw_gU_beta_limit_from_cLL(c2, leg2, x_range, beta, fill_color=ROOT.kGray+1, fill_style=3004, Alpha=1, n_points=2, sigma=2)
        draw_gU_beta_limit_from_cLL(c2, leg2, x_range, beta, fill_color=ROOT.kGray+2, fill_style=3005, Alpha=1, n_points=2, sigma=1)

        # draw ticks on the right and top of the canvas
        ROOT.gPad.SetTicks(1,1)
        ROOT.gPad.RedrawAxis()

        output_file.cd()
        # c2.Write()
        if g_exp:
            g_exp.Write()
        if base_hist == "limit_read" and g_exp_read:
            g_exp_read.Write()
        if g_extra_1:
            g_extra_1.Write()
        if g_extra_2:
            g_extra_2.Write()
        if g_m1:
            g_m1.Write()
        if g_p1:
            g_p1.Write()
        if g_m2:
            g_m2.Write()
        if g_p2:
            g_p2.Write()
        c2.SaveAs(os.path.join(outdir, f"mu1_contours_beta{str(beta).replace('.','_')}.pdf"))

        c2.Close()
        del h_exp, h_p1, h_m1, h_p2, h_m2

# ========== 4) Draw significance vs gU-beta for fixed MU ==========
# functions to generate the bin edges for limit plot
def generate_edges_with_E0(bin_center, E0):
    # calcualte the bin edges based on the center value of bin and the first bin edge E0
    N = len(bin_center)
    # set the first bin edge
    edges = [round(E0, 4)]
    # set the middle bin edges
    for i in range(N):
        Ei = edges[i]
        E_next = 2 * bin_center[i] - Ei
        # 精确到三位有效数字
        edges.append(round(E_next, 4))
    return array('d', edges)

def is_strictly_increasing(lst):
    """判断列表 lst 的值是否严格单调递增"""
    return all(x < y for x, y in zip(lst, lst[1:]))

def get_bin_edges(centers, n_steps=10):
    """
    在区间 (2*c0-c1, c0) 内迭代搜索一个合适的 E0，
    使得生成的边界序列严格单调递增。
    
    参数:
      centers : list
         按升序排列的 bin 中心值数组
      n_steps : int
         网格搜索的步数
    返回:
      (E0, edges) : 成功找到的 E0 与对应的边界数组
    """
    c0, c1 = centers[0], centers[1]
    # E0_low = 2*c0 - c1  # 下界
    E0_low = 2*c0 - c1  # 下界
    E0_high = c0       # 上界
    for i in range(n_steps + 1):
        # candidate_E0 = E0_low + i * (E0_high - E0_low) / n_steps
        candidate_E0 = E0_low + i * (E0_high - E0_low) / n_steps
        edges = generate_edges_with_E0(centers, candidate_E0)
        if is_strictly_increasing(edges) and candidate_E0 > -0.5:
            print("Center: ", centers, " find the feasible E0 with step size: ", n_steps, " -> E0: ", candidate_E0, " edges: ", edges)
            return edges
    raise ValueError(f"cannot find the feasible E0 with step size: {n_steps} and centers: {centers}")

# get shaded region for b anomalies
# legacy function to get the gU limit for b anomalies
def get_gU_limit_for_b_anomalies(MLQ):
    # limit for line gU^2/MU^2*beta23*beta33, gU normalized while beta33=1, beta23=0.2
    # gU_high = 1.4 * MLQ + 0.1
    # gU_low = 0.55 * MLQ + 0.05
    gU_high = MLQ / 0.69 # 0.973 \pm 0.303 (TeV-1) is the 1 sigma error of the best fit beta23
    gU_low = MLQ / 1.71 # 0.973 \pm 0.303 (TeV-1) is the 1 sigma error of the best fit beta23
    return gU_high, gU_low

# define the constants for B anomalies region calculation
cLL_high_1sigma = 0.09 # 1 sigma
cLL_low_1sigma = 0.038 # 1 sigma
cLL_high_2sigma = 0.11 # 2 sigma
cLL_low_2sigma = 0.018 # 2 sigma
# cLL_low = max(0, 0.051 - 0.027*1.96)
v = 246 # GeV
Vcs=0.97349
Vcb=0.04182

def get_beta_limit_from_cLL(MLQ, gU, sigma=1):
    # get the gU limit from the cLL best fit value 0.051 \pm 0.027
    # C_LL^c = v^2*g_U^2 / (4*M_U^2) * ( 1+ V_cs/V_cb*beta23)
    if sigma == 1:
        cLL_high = cLL_high_1sigma
        cLL_low = cLL_low_1sigma
    elif sigma == 2:
        cLL_high = cLL_high_2sigma
        cLL_low = cLL_low_2sigma
    else:
        raise ValueError(f"sigma must be 1 or 2, but got {sigma}")
    beta23_high = (cLL_high * 4 * MLQ**2 / (gU**2 * v**2) - 1) / (Vcs/Vcb)
    beta23_low = (cLL_low * 4 * MLQ**2 / (gU**2 * v**2) - 1) / (Vcs/Vcb)
    return beta23_low, beta23_high

def get_gU_limit_from_cLL(MLQ, beta, sigma=1):
    # get the gU limit from the cLL best fit value 0.051 \pm 0.027
    # C_LL^c = v^2*g_U^2 / (4*M_U^2) * ( 1+ V_cs/V_cb*beta23)
    if sigma == 1:
        cLL_high = cLL_high_1sigma
        cLL_low = cLL_low_1sigma
    elif sigma == 2:
        cLL_high = cLL_high_2sigma
        cLL_low = cLL_low_2sigma
    else:
        raise ValueError(f"sigma must be 1 or 2, but got {sigma}")
    gU_high = np.sqrt(cLL_high * 4 * MLQ**2 / (v**2 * (1+Vcs/Vcb*beta)))
    gU_low = np.sqrt(cLL_low * 4 * MLQ**2 / (v**2 * (1+Vcs/Vcb*beta)))
    return gU_high, gU_low

# legacy function to get the b anomalies flavoured region
def get_b_anomalies_production_limit(MLQ, enable_cU=False):
    # limit for line gU^2*v^2/(4*MU^2)*(1+Vcs/Vcb*beta23), gU normalized while beta33=1, beta23=0.20, (MU is merged in the constant computation though.)
    gU_high, gU_low = get_gU_limit_for_b_anomalies(MLQ)
    Vcs=0.97349
    Vcb=0.04182
    best_fit_beta23 = 0.15631
    v = 0.246 # TeV
    
    if not enable_cU:
        gU_beta_limit_high = gU_high**2 * (1+Vcs/Vcb*best_fit_beta23)
        gU_beta_limit_low = gU_low**2 * (1+Vcs/Vcb*best_fit_beta23)
        cLL_high = gU_high**2 * v**2 / (4 * MLQ**2) * (1+Vcs/Vcb*best_fit_beta23)
        cLL_low = gU_low**2 * v**2 / (4 * MLQ**2) * (1+Vcs/Vcb*best_fit_beta23)
        print(f"MLQ: {MLQ}, gU_high: {gU_high}, gU_low: {gU_low}, gU_beta_limit_high: {gU_beta_limit_high}, gU_beta_limit_low: {gU_beta_limit_low}, Vcs/Vcb: {Vcs/Vcb}, beta23: {best_fit_beta23}, cLL_high: {cLL_high}, cLL_low: {cLL_low}")
        return gU_beta_limit_high, gU_beta_limit_low
    else:
        cU_high = get_cU(gU_high, MLQ * 1e3) # MLQ in GeV unit
        cU_low = get_cU(gU_low, MLQ * 1e3) # MLQ in GeV unit
        cU_beta_limit_high = cU_high**2 * (1+Vcs/Vcb*best_fit_beta23)
        cU_beta_limit_low = cU_low**2 * (1+Vcs/Vcb*best_fit_beta23)
        # print(f"cU_beta_limit_high: {cU_beta_limit_high}, cU_beta_limit_low: {cU_beta_limit_low}, gU_high: {gU_high}, gU_low: {gU_low}, cU_high: {cU_high}, cU_low: {cU_low}, MLQ: {MLQ}")
        return cU_beta_limit_high, cU_beta_limit_low

# fill the shaded region for b anomalies
# def fill_between_curves(canvas, MU, c, d, x_min, x_max, n_points=100, fill_color=ROOT.kGray+1, fill_style=3004):
def fill_between_curves(canvas, leg, MU, x_min, x_max, n_points=100, fill_color=ROOT.kGray+1, fill_style=3004, Alpha=1, sigma=2):
    """
    在给定的canvas上填充由两条曲线 x^2*(1+Vcs/Vcb*y)=c 和 x^2*(1+Vcs/Vcb*y)=d 所限定的区域。
    要求 x 在 [x_min, x_max] 内，且 x ≠ 0（因此建议 x_min > 0）。
    
    参数：
      canvas    : 目标 ROOT.TCanvas
      MU        : 质量 MU
      c         : 曲线下界对应的常数
      d         : 曲线上界对应的常数
      x_min     : x 轴下限（建议大于 0）
      x_max     : x 轴上限
      n_points  : 用于生成曲线的采样点数，默认 100
      fill_color: 填充颜色，默认为 ROOT.kGray+2
      fill_style: 填充样式，默认为 3004（斜线填充）
      
    返回：
      填充区域的 TGraph 对象。
    """
    # 在 x 方向生成采样点
    xs = np.linspace(x_min, x_max, n_points)
    
    # 根据公式计算两条曲线的 y 值
    # Vcs=0.97349
    # Vcb=0.04182
    # y_lower = [(c / x**2 - 1) / (Vcs/Vcb) for x in xs]  # 下界： y = (c/(x^2)-1)/(Vcs/Vcb)
    # y_upper = [(d / x**2 - 1) / (Vcs/Vcb) for x in xs]  # 上界： y = (d/(x^2)-1)/(Vcs/Vcb)
    
    # get y values from the cLL
    y_lower, y_upper = get_beta_limit_from_cLL(MU, xs, sigma)
    
    # 构造闭合多边形的顶点：
    # 先沿上界曲线正向采样，再沿下界曲线反向采样
    poly_x = list(xs) + list(xs[::-1])
    poly_y = list(y_upper) + list(y_lower[::-1])
    
    n_poly = len(poly_x)
    
    # 转换为 TGraph 需要的数组类型
    x_vals = array('d', poly_x)
    y_vals = array('d', poly_y)
    
    # 构造 TGraph 对象
    polygon = ROOT.TGraph(n_poly, x_vals, y_vals)
    ROOT.SetOwnership(polygon, False)
    polygon.SetFillColorAlpha(fill_color, Alpha)
    polygon.SetLineColor(fill_color)
    polygon.SetFillStyle(fill_style)
    
    # add the legend
    if sigma == 1:
        leg.AddEntry(polygon, f"#splitline{{B anomalies favoured}}{{region within 1#kern[0.25]{{#sigma}}}}", "f")
    else: 
        leg.AddEntry(polygon, f"#splitline{{B anomalies favoured}}{{region within {sigma}#sigma}}", "f")
    # add the blank entry to avoid the overlapping with the other entries
    leg.AddEntry(0, "", "")
    
    # 在给定的 canvas 上绘制填充阴影区域
    canvas.cd()
    polygon.Draw("F same")  # "F" 表示填充，"same" 保证叠加到已有图形上
    canvas.Update()
    
    return polygon

def draw_gU_1D(zmap, outdir, outputfile):
    print("*********** draw gU slice ***********")
    mus = sorted({k[0] for k in zmap})
    gus = sorted({k[1] for k in zmap})
    betas = sorted({k[2] for k in zmap})
    first_canvas = True
    gu_max = 4
    gu_min = 0.15

    for MU in mus:
        for beta in betas:
            # creat and fill TGraph
            # 创建两个TGraph对象
            g1 = ROOT.TGraph()
            g1.SetName(f"g1_mu_{MU}_beta_{str(beta).replace('.','_')}")
            g1.SetTitle(f"MU={MU} GeV, beta={beta};g_{{U}};#mu_{{exp}}")

            g1_square = ROOT.TGraph()
            g1_square.SetName(f"g1_square_mu_{MU}_beta_{str(beta).replace('.','_')}")
            g1_square.SetTitle(f"MU={MU} GeV, beta={beta};g_{{U}}; sqrt(#mu_{{exp}})")

            # 填充数据点
            point_index = 0
            for (mu, gu, be), d in zmap.items():
                if mu != MU or be != beta or gu == 5:
                    continue
                g1.SetPoint(point_index, gu, d['exp'])
                g1_square.SetPoint(point_index, gu, np.sqrt(d['exp']))
                point_index += 1

            # 绘图
            c = ROOT.TCanvas(f"c_mu_{MU}_beta_{str(beta).replace('.','_')}", "", 900, 750)
            g1.SetMarkerStyle(20)
            g1.SetLineColor(ROOT.kBlue)
            g1.Draw("ALP")   # A:坐标轴, L:连线, P:点
            # draw a line where mu=1.0
            line = ROOT.TLine(gu_min, 1, gu_max, 1)
            line.SetLineColor(ROOT.kRed)
            line.SetLineStyle(2)
            line.Draw("L SAME")
            # draw the legend
            leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
            leg.AddEntry(g1, f"#mu_{{exp}} (MU={MU} GeV, beta={beta})", "l")
            leg.AddEntry(line, f"#mu_{{exp}}=1.0", "l")
            leg.Draw()

            c.Update()

            c2 = ROOT.TCanvas(f"c_mu2_{MU}_beta_{str(beta).replace('.','_')}", "", 900, 750)
            g1_square.SetMarkerStyle(21)
            g1_square.SetLineColor(ROOT.kRed)
            g1_square.Draw("ALP")
            # draw a line where mu=1.0
            line2 = ROOT.TLine(gu_min, 1, gu_max, 1)
            line2.SetLineColor(ROOT.kRed)
            line2.SetLineStyle(2)
            line2.Draw("L SAME")
            # draw the legend
            leg2 = ROOT.TLegend(0.6,0.70,0.88,0.88)
            leg2.AddEntry(g1_square, f"sqrt(#mu_{{exp}}) (MU={MU} GeV, beta={beta})", "l")
            leg2.AddEntry(line2, f"#mu_{{exp}}=1.0", "l")
            leg2.Draw()
            c2.Update()

            # save as PDF
            if first_canvas:
                c.Print(f"{outdir}/gU_1D_plots.pdf(")
                c2.Print(f"{outdir}/gU_1D_plots.pdf")
                first_canvas = False
            else:
                c.Print(f"{outdir}/gU_1D_plots.pdf")
                c2.Print(f"{outdir}/gU_1D_plots.pdf")
            # 写入输出文件
            outputfile.cd()
            # c.Write()
            # c2.Write()

            # 清理
            del g1, g1_square, c, c2, line, line2, leg, leg2
    # close the pdf
    final_canvas = ROOT.TCanvas("c_end", "", 1, 1)
    final_canvas.Print(f"{outdir}/gU_1D_plots.pdf)")  # 关闭 PDF 文件


def draw_beta_1D(zmap, outdir, outputfile):
    print("*********** draw gU slice ***********")
    mus = sorted({k[0] for k in zmap})
    gus = sorted({k[1] for k in zmap})
    betas = sorted({k[2] for k in zmap})
    first_canvas = True
    beta_max = max(betas)
    
    for MU in mus:
        for GU in gus:
            # creat and fill TGraph
            # 创建两个TGraph对象
            g1 = ROOT.TGraph()
            g1.SetName(f"g1_mu_{MU}_gu_{str(GU).replace('.','_')}")
            g1.SetTitle(f"MU={MU} GeV, gU={GU};#beta_{{L}}^{{23}};#mu_{{exp}}")

            g1_square = ROOT.TGraph()
            g1_square.SetName(f"g1_square_mu_{MU}_beta_{str(GU).replace('.','_')}")
            g1_square.SetTitle(f"MU={MU} GeV, gu={GU};#beta_{{L}}^{{23}}; sqrt(#mu_{{exp}})")



            # 填充数据点
            point_index = 0
            for (mu, gu, be), d in zmap.items():
                if mu != MU or gu != GU:
                    continue
                g1.SetPoint(point_index, be, d['exp'])
                g1_square.SetPoint(point_index, be, np.sqrt(d['exp']))
                point_index += 1

            # 绘图
            c = ROOT.TCanvas(f"c_mu_{MU}_beta_{str(GU).replace('.','_')}", "", 900, 750)
            g1.SetMarkerStyle(20)
            g1.SetLineColor(ROOT.kBlue)
            g1.Draw("ALP")   # A:坐标轴, L:连线, P:点
            # draw a line where mu=1.0
            line = ROOT.TLine(0, 1, beta_max, 1)
            line.SetLineColor(ROOT.kRed)
            line.SetLineStyle(2)
            line.Draw("L SAME")
            # draw the legend
            leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
            leg.AddEntry(g1, f"#mu_{{exp}} (MU={MU} GeV, gU={GU})", "l")
            leg.AddEntry(line, f"#mu_{{exp}}=1.0", "l")
            leg.Draw()
            c.Update()

            c2 = ROOT.TCanvas(f"c_mu2_{MU}_beta_{str(GU).replace('.','_')}", "", 900, 750)
            g1_square.SetMarkerStyle(21)
            g1_square.SetLineColor(ROOT.kRed)
            g1_square.Draw("ALP")
            # draw a line where mu=1.0
            line2 = ROOT.TLine(0, 1, beta_max, 1)
            line2.SetLineColor(ROOT.kRed)
            line2.SetLineStyle(2)
            line2.Draw("L SAME")
            # draw the legend
            leg2 = ROOT.TLegend(0.6,0.70,0.88,0.88)
            leg2.AddEntry(g1_square, f"sqrt(#mu_{{exp}}) (MU={MU} GeV, gU={GU})", "l")
            leg2.AddEntry(line2, f"#mu_{{exp}}=1.0", "l")
            leg2.Draw()
            c2.Update()

            # save as PDF
            if first_canvas:
                c.Print(f"{outdir}/beta_1D_plots.pdf(")
                c2.Print(f"{outdir}/beta_1D_plots.pdf")
                first_canvas = False
            else:
                c.Print(f"{outdir}/beta_1D_plots.pdf")
                c2.Print(f"{outdir}/beta_1D_plots.pdf")
            # 写入输出文件
            outputfile.cd()
            # c.Write()
            # c2.Write()

            # 清理
            del g1, g1_square, c, c2, line, line2, leg, leg2
    # close the pdf
    final_canvas = ROOT.TCanvas("c_end", "", 1, 1)
    final_canvas.Print(f"{outdir}/beta_1D_plots.pdf)")  # 关闭 PDF 文件

# ========== 5) Draw significance vs MU-gU for fixed beta ==========
# legacy function to draw the b anomalies region
# add shading to canvas
def draw_b_anomalies_mass_region(canvas, x_range, beta23, fill_color=ROOT.kGray+1):
    # factors to convert beta23=0 to beta23=1.0 or 0.2
    Vcs=0.97349
    Vcb=0.04182
    best_fit_beta23 = 0.2
    gU_sf = np.sqrt((1+best_fit_beta23*Vcs/Vcb)/(1+beta23*Vcs/Vcb)) # v^2*gU^2/(4MU^2)*(1+Vcs/Vcb*beta23)=0.051 \pm 0.027
    print(f"beta23: {beta23}, gU_sf: {gU_sf}, x_range: {x_range}")
    # get gU limit for b anomalies favoured region for x axis mass range
    gU_high_0, gU_low_0 = get_gU_limit_for_b_anomalies(x_range[0] * 1e-3)
    gU_high_1, gU_low_1 = get_gU_limit_for_b_anomalies(x_range[1] * 1e-3)
    line1 = [(x_range[0], gU_high_0 * gU_sf), (x_range[1], gU_high_1 * gU_sf)]
    line2 = [(x_range[0], gU_low_0 * gU_sf), (x_range[1], gU_low_1 * gU_sf)]

    points = []
    for pt in line1:
        points.append(pt)
    for pt in reversed(line2):
        points.append(pt)
    
    npoints = len(points)
    x_vals = array('d', [pt[0] for pt in points])
    y_vals = array('d', [pt[1] for pt in points])
    
    # construct closed polygon
    poly = ROOT.TGraph(npoints, x_vals, y_vals)
    print("npoints: ", npoints, " x_vals: ", x_vals, " y_vals: ", y_vals)
    ROOT.SetOwnership(poly, False)
    poly.SetFillColor(fill_color)
    poly.SetLineColor(fill_color)
    poly.SetFillStyle(3004)  # modify fill style, 3004 for dashed fill
    
    # draw shading on the canvas
    canvas.cd()
    poly.Draw("f same")
    canvas.Update()

def draw_gU_beta_limit_from_cLL(canvas, leg, x_range, beta, fill_color=ROOT.kGray+1, fill_style=3004, Alpha=1, n_points=2, sigma=2):
    # generate sample points for x axis
    xs = np.linspace(x_range[0], x_range[1], n_points)
    # get y values from the cLL
    y_upper, y_lower = get_gU_limit_from_cLL(xs, beta, sigma)
    # 构造闭合多边形的顶点：
    # 先沿上界曲线正向采样，再沿下界曲线反向采样
    poly_x = list(xs) + list(xs[::-1])
    poly_y = list(y_upper) + list(y_lower[::-1])
    
    n_poly = len(poly_x)
    
    # 转换为 TGraph 需要的数组类型
    x_vals = array('d', poly_x)
    y_vals = array('d', poly_y)
    
    # 构造 TGraph 对象
    polygon = ROOT.TGraph(n_poly, x_vals, y_vals)
    ROOT.SetOwnership(polygon, False)
    polygon.SetFillColorAlpha(fill_color, Alpha)
    polygon.SetLineColor(fill_color)
    polygon.SetFillStyle(fill_style)
    # add to legend
    if sigma == 1:
        leg.AddEntry(polygon, f"#splitline{{B anomalies favoured}}{{region within {sigma}#kern[0.25]{{#sigma}}}}", "f")
    else:
        leg.AddEntry(polygon, f"#splitline{{B anomalies favoured}}{{region within {sigma}#sigma}}", "f")
    # add the blank entry to avoid the overlapping with the other entries
    leg.AddEntry(0, "", "")
    
    # 在给定的 canvas 上绘制填充阴影区域
    canvas.cd()
    polygon.Draw("F same")  # "F" 表示填充，"same" 保证叠加到已有图形上
    canvas.Update()


def make_edges_from_centers(centers, singleton_half_width):
    """Build midpoint bin edges, including a well-defined single-bin case."""
    values = sorted(set(float(value) for value in centers))
    if not values:
        raise ValueError("Cannot build histogram edges from an empty coordinate list")
    if len(values) == 1:
        center = values[0]
        return array("d", [center - singleton_half_width, center + singleton_half_width])

    edges = [values[0] - 0.5 * (values[1] - values[0])]
    edges.extend(0.5 * (left + right) for left, right in zip(values[:-1], values[1:]))
    edges.append(values[-1] + 0.5 * (values[-1] - values[-2]))
    return array("d", edges)


def format_parameter_token(value):
    return f"{float(value):.1f}".replace(".", "_")


def set_axis_parameter_labels(axis, values):
    """Label each discrete grid bin with the exact generated parameter value."""
    for bin_number, value in enumerate(values, start=1):
        axis.SetBinLabel(bin_number, f"{value:g}")


def write_acceptance_grid_text(handle, title, column_name, columns, row_name, rows, value_at):
    """Write one human-readable aligned 2D table in percent."""
    row_label = f"{row_name} \\ {column_name}"
    cell_width = max(14, len(row_label) + 1)
    handle.write(f"\n{title}\n")
    handle.write("Values: Acceptance * Efficiency [%]\n")
    handle.write(f"{row_label:<{cell_width}}")
    for column in columns:
        handle.write(f"{column:>{cell_width}.6g}")
    handle.write("\n")
    handle.write("-" * (cell_width * (len(columns) + 1)) + "\n")
    for row in rows:
        handle.write(f"{row:<{cell_width}.6g}")
        for column in columns:
            value = value_at(row, column)
            if value is None:
                rendered = "--"
            elif isinstance(value, str):
                rendered = value
            else:
                rendered = f"{100.0 * value:.7g}"
            handle.write(f"{rendered:>{cell_width}}")
        handle.write("\n")


def draw_one_acceptance_grid(
    hist,
    outdir,
    basename,
    title,
    output_file,
    manifest,
    layout,
    fixed_value,
    expected_cells,
    status_hist=None,
):
    """Persist a fraction-valued TH2 and render a percentage text grid."""
    hist.SetDirectory(0)
    hist.SetStats(0)
    output_file.cd()
    hist.Write()

    display_hist = hist.Clone(hist.GetName() + "_percent_display")
    display_hist.SetDirectory(0)
    display_hist.Scale(100.0)
    display_hist.SetTitle(title)
    display_hist.GetZaxis().SetTitle("Acceptance #times Efficiency [%]")
    display_hist.GetXaxis().SetTitleSize(0.045)
    display_hist.GetYaxis().SetTitleSize(0.045)
    display_hist.GetZaxis().SetTitleSize(0.042)
    display_hist.GetXaxis().CenterTitle()
    display_hist.GetYaxis().CenterTitle()
    display_hist.GetZaxis().CenterTitle()
    display_hist.GetXaxis().SetTitleOffset(1.10)
    display_hist.GetYaxis().SetTitleOffset(1.10)
    display_hist.GetZaxis().SetTitleOffset(1.25)
    display_hist.GetXaxis().SetLabelSize(0.040)
    display_hist.GetYaxis().SetLabelSize(0.040)
    display_hist.GetZaxis().SetLabelSize(0.035)
    # The displayed histogram is already scaled from a fraction to percent.
    # Use a larger marker size so the two-decimal cell labels remain readable.
    display_hist.SetMarkerSize(1.70)

    canvas = ROOT.TCanvas("c_" + hist.GetName(), "", 1050, 800)
    canvas.SetLeftMargin(0.12)
    canvas.SetRightMargin(0.16)
    canvas.SetBottomMargin(0.12)
    canvas.SetTopMargin(0.10)
    ROOT.gStyle.SetPaintTextFormat(".2f")
    display_hist.Draw("COLZ TEXT")

    # The default-weight v04 scan is sparse.  Label absent combinations and
    # configured samples without a ROOT output explicitly so neither is
    # mistaken for a physical zero-efficiency bin in PDF/PNG output.
    sparse_labels = []
    if status_hist is not None:
        for xbin in range(1, status_hist.GetNbinsX() + 1):
            for ybin in range(1, status_hist.GetNbinsY() + 1):
                status = status_hist.GetBinContent(xbin, ybin)
                if status > 0.5:
                    continue
                label = ROOT.TLatex()
                label.SetTextAlign(22)
                label.SetTextFont(42)
                label.SetTextSize(0.030)
                label.SetTextColor(
                    ROOT.kRed + 1 if status < -0.5 else ROOT.kGray + 2
                )
                text = "MISS" if status < -0.5 else "--"
                label.DrawLatex(
                    display_hist.GetXaxis().GetBinCenter(xbin),
                    display_hist.GetYaxis().GetBinCenter(ybin),
                    text,
                )
                sparse_labels.append(label)
    ROOT.gPad.SetTicks(1, 1)
    ROOT.gPad.RedrawAxis()

    pdf_path = os.path.join(outdir, basename + ".pdf")
    png_path = os.path.join(outdir, basename + ".png")
    canvas.SaveAs(pdf_path)
    canvas.SaveAs(png_path)
    canvas.Close()

    manifest.write(
        f"{layout:<12} {str(fixed_value):<10} {expected_cells:>5} "
        f"{hist.GetNbinsX():>6} {hist.GetNbinsY():>6} "
        f"{os.path.basename(pdf_path)}\n"
    )


def beta_r_display_value(beta_r_label):
    values = {"b33R0_0": "0", "b33Rm1_0": "-1"}
    if beta_r_label not in values:
        raise ValueError(f"Unsupported betaR33 label: {beta_r_label}")
    return values[beta_r_label]


def draw_acceptance_text_grids(
    point_map,
    outdir,
    output_file,
    component,
    region_label,
    hist_name,
    beta_r_label="b33Rm1_0",
    normalization="corrected_sumw",
    allow_sparse=False,
    missing_rows=None,
):
    """Draw exact MC Acceptance*Efficiency grids, with explicit sparse cells."""
    os.makedirs(outdir, exist_ok=True)
    missing_rows = list(missing_rows or [])
    missing_keys = {row["key"] for row in missing_rows}
    duplicate_status_keys = missing_keys & set(point_map)
    if duplicate_status_keys:
        raise ValueError(
            f"Points marked both available and missing: {sorted(duplicate_status_keys)}"
        )
    configured_keys = set(point_map) | missing_keys
    if not configured_keys:
        raise RuntimeError(f"No configured points for {beta_r_label} {component}")

    masses = sorted({key[0] for key in configured_keys})
    gus = sorted({key[1] for key in configured_keys})
    betas = sorted({key[2] for key in configured_keys})
    expected_points = {
        (mass, gU, beta)
        for mass in masses
        for gU in gus
        for beta in betas
    }
    absent_points = sorted(expected_points - configured_keys)
    extra_points = sorted(configured_keys - expected_points)
    if not allow_sparse and (absent_points or extra_points):
        raise RuntimeError(
            f"Incomplete {component} grid: {len(absent_points)} missing and "
            f"{len(extra_points)} unexpected points"
        )

    mass_edges = make_edges_from_centers(masses, 250.0)
    gu_edges = make_edges_from_centers(gus, 0.25)
    beta_edges = make_edges_from_centers(betas, 0.10)
    component_label = "BSM" if component == "bsm" else "interference component"
    beta_r_value = beta_r_display_value(beta_r_label)
    safe_region = re.sub(r"[^A-Za-z0-9]+", "_", region_label).strip("_")
    all_rows = [point_map[key] for key in sorted(point_map)] + missing_rows
    sample_width = max(len("sample"), max(len(row["sample"]) for row in all_rows))

    points_path = os.path.join(outdir, "acceptance_eff_points.txt")
    with open(points_path, "w") as points_file:
        points_file.write(f"# betaR33 = {beta_r_value}\n")
        points_file.write(f"# component = {component}\n")
        points_file.write(f"# region = {region_label}\n")
        points_file.write(f"# histogram = NOSYS/{hist_name}\n")
        if normalization == "corrected_sumw":
            points_file.write(
                "# Acceptance*Efficiency = raw_yield / sumW_ratio * FilterEff; "
                "sumW_ratio is column four and already includes period fractions.\n"
            )
            points_file.write(
                f"{'sample':<{sample_width}}  {'DSID':>6}  {'raw_yield':>15}  "
                f"{'sumW_ratio':>15}  {'FilterEff':>11}  {'A_times_eff':>15}  "
                f"{'percent':>13}\n"
            )
            points_file.write("-" * (sample_width + 99) + "\n")
            for key in sorted(point_map):
                row = point_map[key]
                points_file.write(
                    f"{row['sample']:<{sample_width}}  {row['dsid']:>6d}  "
                    f"{row['raw_yield']:>15.9g}  {row['ratio']:>15.9g}  "
                    f"{row['filter_efficiency']:>11.7g}  {row['value']:>15.9g}  "
                    f"{100.0 * row['value']:>13.7g}\n"
                )
        elif normalization == "default_weight":
            points_file.write(
                "# Signal efficiency = raw_yield * FilterEff; default MC weight, "
                "no corrected-sumW/Xsec normalization.\n"
            )
            points_file.write(
                f"{'sample':<{sample_width}}  {'DSID':>6}  {'status':>12}  "
                f"{'raw_yield':>15}  {'FilterEff':>11}  {'signal_eff':>15}  "
                f"{'percent':>13}\n"
            )
            points_file.write("-" * (sample_width + 98) + "\n")
            rows_by_key = {row["key"]: row for row in missing_rows}
            rows_by_key.update({key: point_map[key] for key in point_map})
            for key in sorted(rows_by_key):
                row = rows_by_key[key]
                if row["status"] == "OK":
                    raw_text = f"{row['raw_yield']:.9g}"
                    eff_text = f"{row['value']:.9g}"
                    percent_text = f"{100.0 * row['value']:.7g}"
                else:
                    raw_text = eff_text = percent_text = "NA"
                points_file.write(
                    f"{row['sample']:<{sample_width}}  {row['dsid']:>6d}  "
                    f"{row['status']:>12}  {raw_text:>15}  "
                    f"{row['filter_efficiency']:>11.7g}  {eff_text:>15}  "
                    f"{percent_text:>13}\n"
                )
        else:
            raise ValueError(f"Unknown acceptance normalization mode: {normalization}")

    def grid_value(key):
        if key in point_map:
            return point_map[key]["value"]
        if key in missing_keys:
            return "MISSING"
        return None

    grids_path = os.path.join(outdir, "acceptance_eff_grids.txt")
    manifest_path = os.path.join(outdir, "grid_manifest.txt")
    with open(grids_path, "w") as grids_file, open(manifest_path, "w") as manifest:
        grids_file.write(f"# betaR33 = {beta_r_value}\n")
        grids_file.write(f"# component = {component}\n")
        grids_file.write(f"# region = {region_label}\n")
        grids_file.write("# Exact configured MC points; no interpolation.\n")
        if allow_sparse:
            grids_file.write(
                "# -- = no configured sample; MISSING = configured sample has no ROOT file.\n"
            )
        if component == "inf":
            grids_file.write(
                "# Interference values are signed-template relative selection "
                "efficiencies, not probabilities.\n"
            )

        manifest.write(
            f"{'layout':<12} {'fixed':<10} {'cells':>5} "
            f"{'x_bins':>6} {'y_bins':>6} file\n"
        )
        manifest.write("-" * 92 + "\n")

        for mass in masses:
            hist = ROOT.TH2D(
                f"h2_aeff_{component}_{safe_region}_fixedM_{mass}",
                "",
                len(gu_edges) - 1,
                gu_edges,
                len(beta_edges) - 1,
                beta_edges,
            )
            status_hist = hist.Clone(hist.GetName() + "_status")
            status_hist.Reset()
            status_hist.SetTitle("cell status: 1=available, -1=missing ROOT, 0=no sample")
            status_hist.SetDirectory(0)
            hist.GetXaxis().SetTitle("#it{g}_{U}")
            hist.GetYaxis().SetTitle("#it{#beta}_{L}^{23}")
            hist.GetZaxis().SetTitle("Acceptance #times Efficiency")
            set_axis_parameter_labels(hist.GetXaxis(), gus)
            set_axis_parameter_labels(hist.GetYaxis(), betas)
            set_axis_parameter_labels(status_hist.GetXaxis(), gus)
            set_axis_parameter_labels(status_hist.GetYaxis(), betas)
            for gU in gus:
                for beta in betas:
                    key = (mass, gU, beta)
                    xbin = hist.GetXaxis().FindBin(gU)
                    ybin = hist.GetYaxis().FindBin(beta)
                    if key in point_map:
                        hist.SetBinContent(xbin, ybin, point_map[key]["value"])
                        status_hist.SetBinContent(xbin, ybin, 1.0)
                    elif key in missing_keys:
                        status_hist.SetBinContent(xbin, ybin, -1.0)

            output_file.cd()
            status_hist.Write()
            basename = f"acceptance_eff_fixed_mass_M{mass}"
            title = (
                f"#beta_{{R}}^{{33}}={beta_r_value}, {component_label}, {region_label}, "
                f"m_{{U_{{1}}}}={mass / 1000.0:g} TeV;"
                "#it{g}_{U};#it{#beta}_{L}^{23};"
                "Acceptance #times Efficiency [%]"
            )
            configured_cells = sum(key[0] == mass for key in configured_keys)
            draw_one_acceptance_grid(
                hist,
                outdir,
                basename,
                title,
                output_file,
                manifest,
                "fixed_mass",
                mass,
                configured_cells,
                status_hist=status_hist if allow_sparse else None,
            )
            write_acceptance_grid_text(
                grids_file,
                f"fixed mass = {mass} GeV",
                "gU",
                gus,
                "betaL23",
                betas,
                lambda beta, gU, fixed_mass=mass: grid_value(
                    (fixed_mass, gU, beta)
                ),
            )

        if len(masses) > 1:
            for beta in betas:
                hist = ROOT.TH2D(
                    f"h2_aeff_{component}_{safe_region}_fixedBeta_"
                    f"{format_parameter_token(beta)}",
                    "",
                    len(mass_edges) - 1,
                    mass_edges,
                    len(gu_edges) - 1,
                    gu_edges,
                )
                status_hist = hist.Clone(hist.GetName() + "_status")
                status_hist.Reset()
                status_hist.SetTitle("cell status: 1=available, -1=missing ROOT, 0=no sample")
                status_hist.SetDirectory(0)
                hist.GetXaxis().SetTitle("#it{m}_{U_{1}} [GeV]")
                hist.GetYaxis().SetTitle("#it{g}_{U}")
                hist.GetZaxis().SetTitle("Acceptance #times Efficiency")
                set_axis_parameter_labels(hist.GetXaxis(), masses)
                set_axis_parameter_labels(hist.GetYaxis(), gus)
                set_axis_parameter_labels(status_hist.GetXaxis(), masses)
                set_axis_parameter_labels(status_hist.GetYaxis(), gus)
                for mass in masses:
                    for gU in gus:
                        key = (mass, gU, beta)
                        xbin = hist.GetXaxis().FindBin(mass)
                        ybin = hist.GetYaxis().FindBin(gU)
                        if key in point_map:
                            hist.SetBinContent(xbin, ybin, point_map[key]["value"])
                            status_hist.SetBinContent(xbin, ybin, 1.0)
                        elif key in missing_keys:
                            status_hist.SetBinContent(xbin, ybin, -1.0)

                output_file.cd()
                status_hist.Write()
                beta_token = format_parameter_token(beta)
                basename = f"acceptance_eff_fixed_betaL23_{beta_token}"
                title = (
                    f"#beta_{{R}}^{{33}}={beta_r_value}, {component_label}, {region_label}, "
                    f"#beta_{{L}}^{{23}}={beta:g};"
                    "#it{m}_{U_{1}} [GeV];#it{g}_{U};"
                    "Acceptance #times Efficiency [%]"
                )
                configured_cells = sum(key[2] == beta for key in configured_keys)
                draw_one_acceptance_grid(
                    hist,
                    outdir,
                    basename,
                    title,
                    output_file,
                    manifest,
                    "fixed_beta",
                    beta,
                    configured_cells,
                    status_hist=status_hist if allow_sparse else None,
                )
                write_acceptance_grid_text(
                    grids_file,
                    f"fixed betaL23 = {beta:g}",
                    "mass_GeV",
                    masses,
                    "gU",
                    gus,
                    lambda gU, mass, fixed_beta=beta: grid_value(
                        (mass, gU, fixed_beta)
                    ),
                )
        else:
            message = (
                "fixed_beta grids skipped: this component has only "
                f"one configured mass ({masses[0]} GeV)"
            )
            grids_file.write("\n# " + message + "\n")
            manifest.write(
                f"{'fixed_beta':<12} {'SKIPPED':<10} {'-':>5} "
                f"{'-':>6} {'-':>6} {message}\n"
            )
            print(f"[INFO] {beta_r_label} {component}: {message}")

    print(
        f"[DONE] {region_label} {beta_r_label} {component}: "
        f"{len(point_map)} available, {len(missing_rows)} missing ROOT, "
        f"text grids in {outdir}"
    )


def run_acceptance_b33rm1(args):
    """Entry point for the isolated betaR33=-1 Acceptance*Efficiency mode."""
    hist_name, region_label = B33RM1_ACCEPTANCE_MODES[args.sig]
    ratios = read_sumw_corr_ratios(args.sumw_ratio_file)
    required_dsids = sorted(set(B33RM1_DSIDS.values()))
    filter_efficiencies = read_filter_eff_by_dsid(args.xSecFile, required_dsids)

    for dsid in required_dsids:
        if dsid not in filter_efficiencies:
            raise KeyError(f"Required DSID {dsid} is absent from {args.xSecFile}")
    print(
        "[INFO] PMG Filter Efficiency: "
        + ", ".join(
            f"{dsid}={filter_efficiencies[dsid]:g}" for dsid in required_dsids
        )
    )

    groups = scan_input_dir_acceptance_b33rm1(
        args.input_dir, hist_name, ratios, filter_efficiencies
    )
    os.makedirs(args.out_dir, exist_ok=True)
    for component in ("bsm", "inf"):
        point_map = groups[component]
        if not point_map:
            raise RuntimeError(f"No betaR33=-1 {component} samples were found")
        component_outdir = os.path.join(args.out_dir, component)
        os.makedirs(component_outdir, exist_ok=True)
        output_path = os.path.join(
            component_outdir, "output_acceptance_eff_grids.root"
        )
        output_file = ROOT.TFile(output_path, "RECREATE")
        if not output_file or output_file.IsZombie():
            raise OSError(f"Cannot create ROOT output file {output_path}")
        draw_acceptance_text_grids(
            point_map,
            component_outdir,
            output_file,
            component,
            region_label,
            hist_name,
            beta_r_label="b33Rm1_0",
            normalization="corrected_sumw",
        )
        output_file.Close()

    print(f"[DONE] betaR33=-1 Acceptance*Efficiency saved to {args.out_dir}")



def write_default_weight_signal_summary(
    outdir, groups, missing_by_group, diagnostic_aliases, region_label, hist_name
):
    """Write one aligned all-sample table for a default-weight region."""
    os.makedirs(outdir, exist_ok=True)
    available_rows = [
        row for point_map in groups.values() for row in point_map.values()
    ]
    missing_rows = [row for rows in missing_by_group.values() for row in rows]
    all_rows = available_rows + missing_rows
    sample_width = max(len("sample"), max(len(row["sample"]) for row in all_rows))
    output_path = os.path.join(outdir, "signal_efficiency_points.txt")
    with open(output_path, "w") as output:
        output.write("# All physical default-weight signal samples from the v04 config.\n")
        output.write(f"# region = {region_label}\n")
        output.write(f"# histogram = NOSYS/{hist_name}\n")
        output.write(
            "# signal_efficiency = raw_yield * FilterEff; no corrected-sumW/Xsec normalization.\n"
        )
        output.write(
            f"# available={len(available_rows)}, missing_ROOT={len(missing_rows)}, "
            f"campaign_diagnostic_aliases={len(diagnostic_aliases)}\n"
        )
        output.write(
            f"{'sample':<{sample_width}}  {'betaR33':>8}  {'component':>9}  "
            f"{'DSID':>6}  {'status':>12}  {'raw_yield':>15}  "
            f"{'FilterEff':>11}  {'signal_eff':>15}  {'percent':>13}\n"
        )
        output.write("-" * (sample_width + 126) + "\n")
        rows = sorted(
            all_rows,
            key=lambda row: (
                row["beta_r"],
                row["component"],
                row["key"],
                row["sample"],
            ),
        )
        for row in rows:
            beta_r_value = beta_r_display_value(row["beta_r"])
            if row["status"] == "OK":
                raw_text = f"{row['raw_yield']:.9g}"
                eff_text = f"{row['value']:.9g}"
                percent_text = f"{100.0 * row['value']:.7g}"
            else:
                raw_text = eff_text = percent_text = "NA"
            output.write(
                f"{row['sample']:<{sample_width}}  {beta_r_value:>8}  "
                f"{row['component']:>9}  {row['dsid']:>6d}  "
                f"{row['status']:>12}  {raw_text:>15}  "
                f"{row['filter_efficiency']:>11.7g}  {eff_text:>15}  "
                f"{percent_text:>13}\n"
            )

        if diagnostic_aliases:
            output.write("\n# Campaign-specific diagnostic aliases (not independent merged grid points):\n")
            for row in sorted(diagnostic_aliases, key=lambda item: item["sample"]):
                dsids = ",".join(str(dsid) for dsid in row["dsids"])
                output.write(
                    f"# {row['sample']}  DSID={dsids}  "
                    "status=DIAGNOSTIC_ALIAS_NO_ROOT\n"
                )
    return output_path


def run_acceptance_default_weight(args):
    """Entry point for all v04 default-weight signal efficiency samples."""
    hist_name, region_label = DEFAULT_WEIGHT_ACCEPTANCE_MODES[args.sig]
    sample_dsids = read_sample_dsids_from_config(args.sample_config)
    physical_dsids = {
        dsids[0]
        for sample, dsids in sample_dsids.items()
        if parse_default_weight_acceptance_filename(sample + ".root") is not None
        and len(dsids) == 1
    }
    filter_efficiencies = read_filter_eff_by_dsid(args.xSecFile, physical_dsids)
    missing_dsids = sorted(physical_dsids - set(filter_efficiencies))
    if missing_dsids:
        raise KeyError(
            f"Required signal DSIDs are absent from {args.xSecFile}: {missing_dsids}"
        )

    groups, missing_by_group, diagnostic_aliases = (
        scan_input_dir_acceptance_default_weight(
            args.input_dir,
            hist_name,
            sample_dsids,
            filter_efficiencies,
        )
    )
    os.makedirs(args.out_dir, exist_ok=True)
    summary_path = write_default_weight_signal_summary(
        args.out_dir,
        groups,
        missing_by_group,
        diagnostic_aliases,
        region_label,
        hist_name,
    )

    for beta_r_label in ("b33R0_0", "b33Rm1_0"):
        for component in ("bsm", "inf"):
            group_key = (beta_r_label, component)
            point_map = groups.get(group_key, {})
            missing_rows = missing_by_group.get(group_key, [])
            if not point_map and not missing_rows:
                continue
            component_outdir = os.path.join(
                args.out_dir, beta_r_label, component
            )
            os.makedirs(component_outdir, exist_ok=True)
            output_path = os.path.join(
                component_outdir, "output_acceptance_eff_grids.root"
            )
            output_file = ROOT.TFile(output_path, "RECREATE")
            if not output_file or output_file.IsZombie():
                raise OSError(f"Cannot create ROOT output file {output_path}")
            draw_acceptance_text_grids(
                point_map,
                component_outdir,
                output_file,
                component,
                region_label,
                hist_name,
                beta_r_label=beta_r_label,
                normalization="default_weight",
                allow_sparse=True,
                missing_rows=missing_rows,
            )
            output_file.Close()

    available_count = sum(len(point_map) for point_map in groups.values())
    missing_count = sum(len(rows) for rows in missing_by_group.values())
    print(
        f"[DONE] default-weight signal efficiency saved to {args.out_dir}: "
        f"{available_count} available + {missing_count} missing ROOT; "
        f"all-sample table: {summary_path}"
    )


# ========== main ==========
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Draw mu limits plots. Usage: %(prog)s --input_dir <input_dir> [--out_dir plots] [--unblind True/False] [--sig alldecay/noWeights] [--plot_option single/combined]"
    )
    parser.add_argument("--input_dir", required=True, help="Directory with limit results for input signals.")
    parser.add_argument("--out_dir", default="plots", help="Directory for output plots (default: plots)")
    parser.add_argument("--unblind", default="False", help="Whether to unblind results (True/False, default: False)")
    parser.add_argument("--sig", default="alldecay", help="Signal type (default: alldecay)")
    parser.add_argument("--plot_option", default="single", help="Plot option: single or combined (default: single)")
    parser.add_argument("--limit_path", default="plots/TwoSided_HF0_2_HFSeperated_Renamed_unblind_obs/output_mu_contours.root", help="Path to limit ROOT file for combined plotting (used when --plot_option=combined)")
    parser.add_argument("--extra_path_1", default=None, help="Path to extra ROOT file 1 (same format as limit_path)")
    parser.add_argument("--extra_path_2", default=None, help="Path to extra ROOT file 2 (same format as limit_path)")
    parser.add_argument("--xSecFile", type=str, default="/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/PMGxsecDB_mc16.txt")
    parser.add_argument(
        "--sumw_ratio_file",
        default=os.path.normpath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "script_codex",
                "sumW_corr",
                "sumW_corr_ratios.txt",
            )
        ),
        help=(
            "Pipe-delimited sumW table; betaR33=-1 AcceptanceEff modes use "
            "column four (corrected/nominal, including period fractions)."
        ),
    )
    parser.add_argument(
        "--sample_config",
        default=DEFAULT_WEIGHT_SAMPLE_CONFIG,
        help=(
            "FastFrames YAML providing sample -> DSID mapping for the "
            "default-weight AcceptanceEff modes."
        ),
    )
    parser.add_argument(
        "--use_toy",
        action="store_true",
        default=False,
        help="Read toy limits from myLimit.root instead of asymptotic limits"
    )


    args = parser.parse_args()

    input_dir = args.input_dir
    out_dir = args.out_dir
    unblind = args.unblind
    sig = args.sig
    plot_option = args.plot_option
    limit_path = args.limit_path
    extra_path_1 = args.extra_path_1
    extra_path_2 = args.extra_path_2
    xSecFile = args.xSecFile
    use_toy = args.use_toy
    
    if unblind == "True":
        unblind = True
    else:
        unblind = False

    # The new all-decay mode is intentionally isolated from the legacy
    # noWeights AcceptanceEff/limit machinery below.
    if sig in B33RM1_ACCEPTANCE_MODES:
        if plot_option != "single":
            print(
                f"[WARN] --plot_option={plot_option} is ignored by the "
                "betaR33=-1 AcceptanceEff mode"
            )
        run_acceptance_b33rm1(args)
        return

    if sig in DEFAULT_WEIGHT_ACCEPTANCE_MODES:
        if plot_option != "single":
            print(
                f"[WARN] --plot_option={plot_option} is ignored by the "
                "default-weight AcceptanceEff mode"
            )
        run_acceptance_default_weight(args)
        return

    # read filter efficiency and xSec for each dataset
    FilterEffmap = read_FilterEff(xSecFile)
    # for k, v in FilterEffmap.items():
        # print(f"mass={k[0]}, gU={k[1]}, beta={k[2]}, tag={k[3]} --> filter_efficiency={v}")

    # read limit or efficiency map
    mmap = scan_input_dir_limits(input_dir, FilterEffmap, unblind, sig, use_toy)
    if not mmap:
        print("[ERROR] No valid samples found. Check folder names and files.")
        sys.exit(2)
        
    # cleanup the mu limit in case couping is too weak
    if "AcceptanceEff" in sig:
        pass
    else:  
        mmap = enforce_monotonic_limits(mmap)
        print(f"[INFO] Collected {len(mmap)} points")

    # refill the map to make sure the grid is complete
    mus = sorted({k[0] for k in mmap})
    gus = sorted({k[1] for k in mmap})
    betas = sorted({k[2] for k in mmap})
    if "AcceptanceEff" in sig:
        mmap_adjusted = mmap
    else:  
        import interpolate_function as ifunc    
        mmap_adjusted = ifunc.build_full_grid_monotone(mmap, mus, gus, betas, clip_max=99.0)
        # mmap_adjusted = mmap

    print(f"[INFO] Collected {len(mmap_adjusted)} points after adjustment")

    for k, d in sorted(mmap_adjusted.items()):
        # choose interested points
        # if (k[2] != 0.2): continue
        # print keys that in mmap
        if k in mmap:
            print(f"Point (original): MU={k[0]:>4}, gU={k[1]:>4}, beta={k[2]:>4}  --> mu_exp={d['exp']:.3f} (+1σ={d['p1']:.3f}/-1σ={d['m1']:.3f}, +2σ={d['p2']:.3f}/-2σ={d['m2']:.3f})")
        # print keys that not in mmap
        if k not in mmap:
            print(f"Point (added): MU={k[0]:>4}, gU={k[1]:>4}, beta={k[2]:>4}  --> mu_exp={d['exp']:.3f} (+1σ={d['p1']:.3f}/-1σ={d['m1']:.3f}, +2σ={d['p2']:.3f}/-2σ={d['m2']:.3f})")


    # 输出 ROOT 文件
    os.makedirs(out_dir, exist_ok=True)
    output_file = ROOT.TFile(os.path.join(out_dir, "output_mu_contours.root"), "RECREATE")

    # Draw 2D limits
    text_fb_3decimals = sig.startswith("AcceptanceEff")
    if plot_option == 'single':
        draw_mu_slice_limits(mmap_adjusted, out_dir, output_file, mu_exp=1, text_fb_3decimals=text_fb_3decimals, sigs=sig, extra_path_1=extra_path_1, extra_path_2=extra_path_2)
        draw_beta_slice_limits(mmap_adjusted, out_dir, output_file, mu_exp=1, text_fb_3decimals=text_fb_3decimals, sigs=sig, extra_path_1=extra_path_1, extra_path_2=extra_path_2)
    elif plot_option == 'combined':
        draw_mu_slice_limits(mmap_adjusted, out_dir, output_file, base_hist="limit_read", limit_path=limit_path, mu_exp=1, text_fb_3decimals=text_fb_3decimals, sigs=sig, extra_path_1=extra_path_1, extra_path_2=extra_path_2)
        draw_beta_slice_limits(mmap_adjusted, out_dir, output_file, base_hist="limit_read", limit_path=limit_path, mu_exp=1, text_fb_3decimals=text_fb_3decimals, sigs=sig, extra_path_1=extra_path_1, extra_path_2=extra_path_2)
    
    # draw 1D gU and beta
    # draw_gU_1D(mmap, out_dir, output_file)
    # draw_beta_1D(mmap, out_dir, output_file)

    output_file.Close()
    print(f"[DONE] Plots saved to: {out_dir}/")

if __name__ == "__main__":
    main()
