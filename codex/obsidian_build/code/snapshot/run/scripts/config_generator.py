#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch-replace a target string in a config template and produce one new config
per MU*.root file found in a given folder.

Example:
python config_generator.py \
  /path/to/config_taunub_plot_sys_1l.config \
  /path/to/root_dir \
  M2500_gU2_5_23L1_0 \
  /path/to/output_dir

Arguments:
1) config      Path to the original config template file
2) input_dir   Folder containing .root files (we use those starting with "MU")
3) target      The exact substring to be replaced in the template
4) output_dir  Destination folder for generated config files (auto-created)
"""

import re
from pathlib import Path
import argparse
from typing import List

def collect_signal_names(root_dir: Path) -> List[str]:
    """
    Collect all filenames (without extension) that start with 'MU' and end with '.root'.

    Example:
      MU2500_gU0_5_23L1_4_NonRes.root → MU2500_gU0_5_23L1_4
    """
    # Keep it simple: no extra validation
    names = []
    for p in sorted(root_dir.iterdir()):
        # if p.is_file() and p.name.endswith("noWeights_combined_Res.root") and p.name.startswith("MU"):
        # if p.is_file() and p.name.endswith("noWeights_bsm_Res.root") and p.name.startswith("MU"):
        # if p.is_file() and p.name.endswith("alldecay_corrected_bsm_Res.root") and p.name.startswith("MU"):
        if p.is_file() and p.name.endswith("b33Rm1_0_alldecay_corrected_bsm_Res.root") and p.name.startswith("MU"):
            stem = p.stem
            # 去掉末尾的 _NonRes 或 _Res
            # new_name = re.sub(r'_(?:noWeights_combined_NonRes|noWeights_combined_Res)$', '', stem) # suffix removal for signal samples e.g. alldecay_corrected_NonRes
            # new_name = re.sub(r'_(?:noWeights_bsm_NonRes|noWeights_bsm_Res)$', '', stem) # suffix removal for signal samples e.g. alldecay_corrected_NonRes
            # new_name = re.sub(r'_(?:alldecay_corrected_bsm_NonRes|alldecay_corrected_bsm_Res)$', '', stem) # suffix removal for signal samples e.g. alldecay_corrected_NonRes
            new_name = re.sub(r'_(?:b33Rm1_0_alldecay_corrected_bsm_NonRes|b33Rm1_0_alldecay_corrected_bsm_Res)$', '', stem) # suffix removal for signal samples e.g. alldecay_corrected_NonRes
            names.append(new_name)
    return names


def generate_configs(
    template_path: Path,
    output_dir: Path,
    target: str,
    signal_name_list: List[str],
) -> None:
    """
    For each signal name, replace `target` in the template text and write a new config file:
      <template_stem>_<signal_name><template_suffix>
    """
    text = template_path.read_text(encoding="utf-8")

    output_dir.mkdir(parents=True, exist_ok=True)

    base = template_path.stem
    ext = template_path.suffix  # e.g., ".config"

    for signal_name in signal_name_list:
        # check if target is in the text
        if target not in text:
            print(f"[ERROR] Target {target} not found in the template {template_path}")
            continue
        new_text = text.replace(target, signal_name)
        out_path = output_dir / f"{base}_{signal_name}{ext}"
        out_path.write_text(new_text, encoding="utf-8")
        print(f"[OK] Wrote: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate configs by replacing a target string with each MU*.root basename."
    )
    parser.add_argument("--config", type=Path, help="Path to the config template file")
    parser.add_argument("--signals_dir", type=Path, help="Folder containing MU*.root files")
    parser.add_argument("--placeholder", type=str, help="Substring in the template to replace")
    parser.add_argument("--out_dir", type=Path, help="Folder to save generated configs")

    args = parser.parse_args()

    template_path: Path = args.config
    root_dir: Path = args.signals_dir
    output_dir: Path = args.out_dir
    target: str = args.placeholder

    # 2) Collect MU*.root basenames into the `signal_name` variable (a list of strings)
    signal_name: List[str] = collect_signal_names(root_dir)

    # 3) & 4) Replace and write out new config files with the signal name suffix
    generate_configs(template_path, output_dir, target, signal_name)


if __name__ == "__main__":
    main()