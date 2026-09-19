#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys
from pathlib import Path
from collections import defaultdict


def find_tag_position(tokens):
    """
    在文件名（去掉扩展名后按 '_' 分割）中寻找唯一的 'inf' 或 'bsm' token。
    返回 (位置, 标签)；如果没有或不唯一，返回 (None, None)
    """
    positions = [(i, t) for i, t in enumerate(tokens) if t in ("inf", "bsm")]
    if len(positions) != 1:
        return None, None
    return positions[0]


def group_root_files(folder: Path, key_word: str):
    """
    把文件按“除了 inf/bsm 外其余部分都相同”的规则分组。
    key: 把 inf/bsm 替换成特殊占位符后的 token tuple
    value: {"inf": Path(...), "bsm": Path(...)}
    """
    groups = defaultdict(dict)

    for file_path in folder.glob("*.root"):
        # skip specific samples
        if key_word not in file_path.name:
            continue
        
        stem = file_path.stem  # 去掉 .root
        tokens = stem.split("_")

        pos, tag = find_tag_position(tokens)
        if pos is None:
            continue

        key_tokens = tokens.copy()
        key_tokens[pos] = "{tag}"
        key = tuple(key_tokens)

        groups[key][tag] = file_path

    return groups


def build_output_name(key_tokens):
    """
    根据 key_tokens 生成输出文件名，把占位符替换成 combined
    """
    tokens = list(key_tokens)
    tokens = ["combined" if t == "{tag}" else t for t in tokens]
    return "_".join(tokens) + ".root"


def run_hadd(input_inf: Path, input_bsm: Path, output_file: Path, force=False):
    cmd = ["hadd"]
    if force:
        cmd.append("-f")
    cmd.extend([str(output_file), str(input_inf), str(input_bsm)])

    print("Running:", " ".join(cmd))
    # try run test
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"[ERROR] hadd failed for:\n  {input_inf.name}\n  {input_bsm.name}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False

    print(f"[OK] Created: {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Find matching inf/bsm ROOT files in a folder and hadd them into combined ROOT files."
    )
    parser.add_argument("folder", help="Path to the folder containing .root files")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists (passes -f to hadd)"
    )
    parser.add_argument("--key_word", help="Key word to filter files, e.g. MU1500, MU3000, etc.", default="MU1500")

    args = parser.parse_args()
    folder = Path(args.folder).resolve()
    key_word = args.key_word if args.key_word else "MU1500"

    if not folder.is_dir():
        print(f"[ERROR] Not a valid folder: {folder}", file=sys.stderr)
        sys.exit(1)

    groups = group_root_files(folder, key_word)

    found_any_pair = False

    for key, files in groups.items():
        if "inf" in files and "bsm" in files:
            found_any_pair = True
            output_name = build_output_name(key)
            output_path = folder / output_name

            if output_path.exists() and not args.force:
                print(f"[SKIP] Output already exists: {output_path}")
                print("       Use --force to overwrite.")
                continue

            run_hadd(files["inf"], files["bsm"], output_path, force=args.force)

    if not found_any_pair:
        print("[INFO] No matching inf/bsm pairs found.")


if __name__ == "__main__":
    main()