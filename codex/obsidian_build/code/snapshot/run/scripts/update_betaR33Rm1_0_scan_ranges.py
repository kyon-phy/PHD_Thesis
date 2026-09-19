#!/usr/bin/env python3
"""Update sqrt_mu scan Max and write TREx resubmit script for betaR33Rm1_0 configs."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

MED_RE = re.compile(r"Expected limit \(median\):\s*([0-9.eE+\-infINF]+)")
P2_RE = re.compile(r"Expected limit \(\s*2 sig\):\s*([0-9.eE+\-infINF]+)")
CFG_RE = re.compile(r"(MU\d+_gU[\d_]+_23L[\d_]+)")
SQRT_MU_BLOCK_RE = re.compile(
    r'(NormFactor: "sqrt_mu"\n(?:\t[^\n]+\n)*?\tMax: )([0-9.eE+\-]+)',
    re.MULTILINE,
)
READ_MAX_RE = re.compile(
    r'NormFactor: "sqrt_mu"\n(?:\t[^\n]+\n)*?\tMax: ([0-9.eE+\-]+)',
    re.MULTILINE,
)

LOG_GLOBS = [
    "53273*.out",
    "53274*.out",
    "53319*.out",
    "53320*.out",
]


def parse_val(raw: str) -> float:
    s = raw.strip()
    if s.lower() == "inf":
        return float("inf")
    if s.lower() == "-inf":
        return float("-inf")
    return float(s)


def usable_positive(val: float | None) -> bool:
    return val is not None and val not in (float("inf"), float("-inf")) and val > 0


def format_max(val: float) -> str:
    if val < 1:
        return f"{val:.6f}".rstrip("0").rstrip(".")
    if val < 10:
        return f"{val:.4f}".rstrip("0").rstrip(".")
    return f"{val:.3f}".rstrip("0").rstrip(".")


def parse_logs(logdir: Path) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    outs: list[Path] = []
    for pattern in LOG_GLOBS:
        outs.extend(logdir.glob(pattern))
    outs = sorted(set(outs), key=lambda p: (p.name,))
    for path in outs:
        text = path.read_text(errors="ignore")
        if "betaR33Rm1_0" not in text[:80000]:
            continue
        m_cfg = CFG_RE.search(text)
        m_med = MED_RE.search(text)
        if not m_cfg or not m_med:
            continue
        cfg = m_cfg.group(1)
        med = parse_val(m_med.group(1))
        p2 = parse_val(p2m.group(1)) if (p2m := P2_RE.search(text)) else None
        rows[cfg] = {"median": med, "p2": p2}
    return rows


def read_current_max(path: Path) -> float:
    m = READ_MAX_RE.search(path.read_text(encoding="utf-8"))
    if not m:
        raise RuntimeError(f"sqrt_mu Max not found in {path}")
    return float(m.group(1))


def config_path(config_dir: Path, cfg: str) -> Path:
    return config_dir / (
        "config_taunub_plot_sys_1l_w_beamspot_v04_unblind_noWeights_comb_1bSR_"
        f"b33Rm1_0_alldecay_{cfg}.config"
    )


def update_config(path: Path, new_max: float) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, n = SQRT_MU_BLOCK_RE.subn(rf"\g<1>{format_max(new_max)}", text, count=1)
    if n != 1:
        raise RuntimeError(f"failed to update sqrt_mu Max in {path}")
    path.write_text(new_text, encoding="utf-8")


def fit_output_dir(output_dir: Path, cfg: str) -> str:
    return f"fit_taunub_sys_1l_allVR_SPLUSB_{cfg}_b33Rm1_0_alldecay_bsm_unblind"


def choose_updates(
    config_dir: Path,
    rows: dict[str, dict[str, float]],
) -> list[dict]:
    updates = []
    negative_skip = []

    for path in sorted(config_dir.glob("*.config")):
        cfg_m = re.search(r"alldecay_(MU\d+_gU[\d_]+_23L[\d_]+)", path.name)
        if not cfg_m:
            continue
        cfg = cfg_m.group(1)
        old_max = read_current_max(path)
        log = rows.get(cfg)
        median = log["median"] if log else None
        p2 = log["p2"] if log else None

        if median is not None and median < 0:
            negative_skip.append(cfg)
            continue

        reason = None
        new_max = None

        if old_max < 1:
            new_max = 2.0
            reason = "max_lt_1"
        elif median is not None and median > 100 and usable_positive(p2) and p2 > old_max:
            new_max = p2 * 1.5
            reason = "high_p2_gt_max"

        if new_max is None or abs(new_max - old_max) < 1e-9:
            continue

        updates.append(
            {
                "cfg": cfg,
                "median": median,
                "p2": p2,
                "old_max": old_max,
                "new_max": new_max,
                "reason": reason,
            }
        )

    print(f"skipped negative-limit configs: {len(negative_skip)}")
    for cfg in negative_skip:
        print(f"  skip {cfg} (median={rows[cfg]['median']:.6g})")
    return updates


def write_submit_script(
    submit_path: Path,
    config_dir: Path,
    output_dir: Path,
    updates: list[dict],
    job_start: int = 198,
) -> None:
    by_mass: dict[str, list[str]] = defaultdict(list)
    for item in updates:
        mass = re.search(r"MU(\d+)", item["cfg"]).group(1)
        by_mass[mass].append(str(config_path(config_dir, item["cfg"])))

    lines = [
        "#!/bin/sh",
        "",
        "# Resubmit betaR33Rm1_0 configs after sqrt_mu Max fixes.",
        "# - Max < 1 -> 2",
        "# - median > 100 and +2sigma > Max -> Max = +2sigma * 1.5",
        "# - negative-limit configs skipped",
        f"# configs to resubmit: {len(updates)}",
        "",
        f"OUTPUT={output_dir}",
        "mkdir -p ${OUTPUT}",
        "",
        "# clear previous condor logs",
        "rm -f /data/data3/zp/zang/condor_log/*",
        "",
        "# remove previous fit outputs so TRExFitter can rewrite results",
    ]
    for item in updates:
        cfg = item["cfg"]
        lines.append(f"rm -rf ${{OUTPUT}}/{fit_output_dir(output_dir, cfg)}")
    lines.append("")

    job = job_start
    prod2_masses = ["1500", "2000", "2500"]
    prod3_masses = ["3000", "4000", "5000"]
    for masses, queue in ((prod2_masses, "group_prod2"), (prod3_masses, "group_prod3")):
        for mass in masses:
            cfgs = by_mass.get(mass, [])
            if not cfgs:
                continue
            lines.append("python3 Plotter_submit_lxatut_TREx.py \\")
            lines.append(f"  --config_file {' '.join(cfgs)} \\")
            lines.append(f"  --output ${{OUTPUT}} --queue {queue} --job {job}")
            lines.append("")
            job += 1

    submit_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logdir", type=Path, default=Path("/data/data3/zp/zang/condor_log"))
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path(
            "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/"
            "configs/TwoSided_HF0_3_HFSeperated_Renamed_unblinded_noWeights_comb_1bSR_betaR33Rm1_0"
        ),
    )
    parser.add_argument(
        "--submit-script",
        type=Path,
        default=Path(
            "/data/data3/zp/zang/lxatut_submit/"
            "submit_job_lxatut_TREx_betaR33Rm1_0_1bSR_rescan.sh"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/"
            "fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_1bSR_betaR33Rm1_0"
        ),
    )
    parser.add_argument("--job-start", type=int, default=198)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = parse_logs(args.logdir)
    updates = choose_updates(args.config_dir, rows)
    print(f"parsed logs: {len(rows)}")
    print(f"configs to update/resubmit: {len(updates)}")

    for item in updates:
        print(
            f"[{item['reason']}] {item['cfg']}: median={item['median']} "
            f"+2sig={item['p2']} Max {item['old_max']} -> {format_max(item['new_max'])}"
        )
        if not args.dry_run:
            update_config(config_path(args.config_dir, item["cfg"]), item["new_max"])

    if not args.dry_run:
        write_submit_script(
            args.submit_script,
            args.config_dir,
            args.output_dir,
            updates,
            job_start=args.job_start,
        )
        print(f"wrote submit script: {args.submit_script}")


if __name__ == "__main__":
    main()
