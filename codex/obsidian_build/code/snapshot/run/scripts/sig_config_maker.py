#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

REGIONS = [
    "SR_1tau0l1b_sch",
    "WCR_0tau1l0b_sch",
    "topCR_1tau1l_sch",
    "VR_0tau1l1b_sch",
    "WVR_1tau0l0b_sch",
    "topVR_1tau0l2b_sch",
]
SIM_TYPE = "fastsim"

# dsname list 解析
RE_DSID = re.compile(r"mc20_13TeV\.(\d+)\.")
RE_TAG  = re.compile(r"_(bsm|inf)_")
RE_MU   = re.compile(r"_M(\d+)")
RE_G_L  = re.compile(r"_g(\d+_\d+)_b23L(\d+_\d+)")
RE_B33  = re.compile(r"_b33Rm1_0(?:_|\.|$)")

DEFAULT_G = "1_0"
DEFAULT_23L = "0_2"

CAMPAIGN_ORDER = ["mc20a", "mc20d", "mc20e"]
VALID_CAMPAIGNS = set(CAMPAIGN_ORDER)

def read_available_campaigns(filelist_path: str):
    """
    读 filelist：每行形如
      570604  mc20d  fastsim  /path/to/file.root
    只用前两列 (dsid, campaign)，建立 dsid -> set(campaigns)
    """
    avail = {}
    with open(filelist_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                # 像你最后一行 "570609" 这种，直接忽略
                continue
            dsid, camp = parts[0], parts[1]
            if not dsid.isdigit():
                continue
            if camp not in VALID_CAMPAIGNS:
                # 如果有别的 campaign 名字，先忽略；需要的话可扩展
                continue
            avail.setdefault(dsid, set()).add(camp)
    return avail

def parse_dsname_line(s: str):
    s = s.strip()
    if not s or s.startswith("#"):
        return None

    m_dsid = RE_DSID.search(s)
    if not m_dsid:
        return None
    dsid = m_dsid.group(1)

    m_tag = RE_TAG.search(s)
    if not m_tag:
        raise ValueError(f"Cannot find inf/bsm tag in: {s}")
    tag = m_tag.group(1)

    m_mu = RE_MU.search(s)
    if not m_mu:
        raise ValueError(f"Cannot find MU (_MXXXX) in: {s}")
    mu = m_mu.group(1)

    m_gl = RE_G_L.search(s)
    if m_gl:
        g = m_gl.group(1)
        l = m_gl.group(2)
    else:
        g = DEFAULT_G
        l = DEFAULT_23L

    b33_part = "_b33Rm1_0" if RE_B33.search(s) else ""
    name = f"MU{mu}_gU{g}_23L{l}{b33_part}_noWeights_{tag}_Res"

    return {
        "dsid": dsid,
        "name": name,
        "raw": s,
    }

def emit_yaml_entry(name: str, dsid: str, campaigns: list[str]):
    regions_str = ", ".join(f"\"{r}\"" for r in REGIONS)
    campaigns_str = ", ".join(f"\"{c}\"" for c in campaigns)
    return "\n".join([
        f'  - name: "{name}"',
        f"    dsids: [{dsid}]",
        f"    campaigns: [{campaigns_str}]",
        f'    simulation_type: "{SIM_TYPE}"',
        f"    regions: [{regions_str}]",
        f"",
    ])

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <dsname_list.txt> <filelist.txt>", file=sys.stderr)
        sys.exit(1)

    dsname_list = sys.argv[1]
    filelist = sys.argv[2]

    avail = read_available_campaigns(filelist)

    # 按 dsid 聚合（同一个 dsid 可能出现多行）
    by_dsid = {}

    with open(dsname_list, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                item = parse_dsname_line(line)
                if item is None:
                    continue

                dsid = item["dsid"]
                if dsid not in by_dsid:
                    by_dsid[dsid] = {"name": item["name"]}
                else:
                    if by_dsid[dsid]["name"] != item["name"]:
                        print(f"[WARN] DSID {dsid} has inconsistent name:", file=sys.stderr)
                        print(f"       old: {by_dsid[dsid]['name']}", file=sys.stderr)
                        print(f"       new: {item['name']}", file=sys.stderr)

            except Exception as e:
                print(f"[ERROR] line {lineno}: {e}", file=sys.stderr)
                print(f"        content: {line}", file=sys.stderr)

    yaml_out = []
    incomplete_lines = []
    fastframe_out = ""
    incomlete_rm_out = ""
    for dsid in sorted(by_dsid.keys(), key=int):
        name = by_dsid[dsid]["name"]

        # 关键规则：只写入 filelist 里存在的 DSID+campaign
        camps = [c for c in CAMPAIGN_ORDER if c in avail.get(dsid, set())]
        print(f"DSID: {dsid}, campaigns: {camps}")

        # append only if all three campaigns are present
        if len(camps) == 3:
            yaml_out.append(emit_yaml_entry(name, dsid, camps))
            fastframe_out += f'{name},'

        # append to incomplete list
        if len(camps) < 3:
            incomplete_lines.append(emit_yaml_entry(name, dsid, camps))
            incomlete_rm_out += f'{name}.root '
            
    if yaml_out:
        print("******************   FF samples config ******************")
        print("\n".join(yaml_out))
        
        print("******************   FF production sample names ******************")
        print(fastframe_out)
    
    if incomplete_lines:
        print("******************   FF incomplete samples config ******************")
        print("\n".join(incomplete_lines))
        
        print("******************   FF incomplete samples to remove ******************")
        print(incomlete_rm_out)

if __name__ == "__main__":
    main()
