#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import shutil
from pathlib import Path


# A 子文件夹名中提取 x：SPLUSB_{x}_noWeights...
# 例如：fit_..._SPLUSB_MU1500_gU1_0_23L0_2_noWeights_unblind_test
RE_X = re.compile(r"SPLUSB_(?P<x>.+?)_noWeights")

# B 配置文件名中提取 y：unblind_noWeights_{y}(可能还有后缀)_?.config
# 例如：config_..._unblind_noWeights_MU2500_gU1_0_23L0_2_b33Rm1_0.config
# 或：..._unblind_noWeights_MU2000_gU3_0_23L1_0.config
RE_Y = re.compile(r"unblind_noWeights_(?P<y>.+?)\.config$")
# RE_Y = re.compile(r"unblind_noWeights_comb_(?P<y>.+?)\.config$")


def validate_dir(p: str) -> Path:
    path = Path(p).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"路径不存在: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"不是文件夹: {path}")
    return path


def extract_x_from_subdir_name(name: str) -> str | None:
    m = RE_X.search(name)
    return m.group("x") if m else None


def extract_y_from_config_name(name: str) -> str | None:
    m = RE_Y.search(name)
    return m.group("y") if m else None


def collect_x_set(folder_a: Path) -> tuple[set[str], list[str]]:
    x_set: set[str] = set()
    bad: list[str] = []
    for p in folder_a.iterdir():
        if not p.is_dir():
            continue
        x = extract_x_from_subdir_name(p.name)
        if x is None:
            bad.append(p.name)
            continue
        x_set.add(x)
    return x_set, bad


def collect_y_map(folder_b: Path) -> tuple[dict[str, list[Path]], list[str]]:
    """
    返回:
      y_to_files: key=y, value=匹配该 y 的 config 文件路径列表（通常 1 个，但也可能多个）
      bad: 无法解析 y 的文件名列表
    """
    y_to_files: dict[str, list[Path]] = {}
    bad: list[str] = []
    for p in folder_b.iterdir():
        if not p.is_file():
            continue
        if p.suffix != ".config":
            continue
        y = extract_y_from_config_name(p.name)
        if y is None:
            bad.append(p.name)
            continue
        y_to_files.setdefault(y, []).append(p)
    return y_to_files, bad


def safe_copy(src: Path, dst_dir: Path, overwrite: bool = False) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists() and not overwrite:
        # 避免覆盖：加序号
        stem = src.stem
        suffix = src.suffix
        i = 1
        while True:
            candidate = dst_dir / f"{stem}__dup{i}{suffix}"
            if not candidate.exists():
                dst = candidate
                break
            i += 1
    shutil.copy2(src, dst)
    return dst


def main():
    ap = argparse.ArgumentParser(
        description="对比 A 子文件夹中 SPLUSB_{x}_noWeights 与 B 配置中 unblind_noWeights_{y}.config，输出缺失的 y 并复制对应配置。"
    )
    ap.add_argument("folderA", help="文件夹A路径（里面全是子文件夹）")
    ap.add_argument("folderB", help="文件夹B路径（里面是 .config 配置文件）")
    ap.add_argument("-o", "--out-dir", default="missing_configs_out", help="输出目录（默认: missing_configs_out）")
    ap.add_argument("-t", "--out-txt", default="missing_configs.txt", help="输出txt文件名（默认: missing_configs.txt）")
    ap.add_argument("--overwrite", action="store_true", help="复制时允许覆盖同名文件（默认不覆盖，会自动改名）")
    ap.add_argument("--dry-run", action="store_true", help="只打印结果，不写txt也不复制文件")
    args = ap.parse_args()

    folder_a = validate_dir(args.folderA)
    folder_b = validate_dir(args.folderB)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_txt = Path(args.out_txt).expanduser().resolve()

    x_set, bad_a = collect_x_set(folder_a)
    y_to_files, bad_b = collect_y_map(folder_b)
    y_set = set(y_to_files.keys())

    missing_y = sorted(y_set - x_set)

    # 子集检查：理论上 x 应该是 y 的子集（即 x ⊆ y）
    if not x_set.issubset(y_set):
        extra_x = sorted(x_set - y_set)
        print("[WARN] 发现 A 中存在但 B 中不存在的 x（x 不是 y 的子集）:")
        for k in extra_x[:50]:
            print("   ", k)
        if len(extra_x) > 50:
            print(f"   ... 还有 {len(extra_x) - 50} 个未显示")

    print(f"[INFO] A 解析到 x 数量: {len(x_set)}")
    print(f"[INFO] B 解析到 y 数量: {len(y_set)}")
    if bad_a:
        print(f"[WARN] A 中有 {len(bad_a)} 个子文件夹名无法解析出 x（前 20 个）:")
        for n in bad_a[:20]:
            print("   ", n)
    if bad_b:
        print(f"[WARN] B 中有 {len(bad_b)} 个 .config 文件名无法解析出 y（前 20 个）:")
        for n in bad_b[:20]:
            print("   ", n)

    print(f"[RESULT] 缺失的 y 数量（只在 B 中出现、A 中没有对应 x）: {len(missing_y)}")

    if args.dry_run:
        for y in missing_y:
            files = y_to_files.get(y, [])
            for f in files:
                print(f"[DRY] {f.name}")
        return

    # 写 txt：每行一个配置文件名（若同一 y 对应多个文件，则都写）
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    copied = 0
    with out_txt.open("w", encoding="utf-8") as w:
        for y in missing_y:
            files = sorted(y_to_files.get(y, []), key=lambda p: p.name)
            for f in files:
                w.write(f.name + "\n")
                safe_copy(f, out_dir, overwrite=args.overwrite)
                copied += 1

    print(f"[OK] 已写入: {out_txt}")
    print(f"[OK] 已复制 {copied} 个配置文件到: {out_dir}")


if __name__ == "__main__":
    main()
