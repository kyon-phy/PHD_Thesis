#!/usr/bin/env python3
"""Expand the CH6 section inputs into a single editable LaTeX text file."""
from pathlib import Path
import re

directory = Path(__file__).resolve().parent
project = directory.parents[1]
master = directory / "CH6_draft.tex"
source = master.read_text(encoding="utf-8")

def expand(match):
    section = project / match.group(1)
    if section.suffix != ".tex":
        section = section.with_suffix(".tex")
    return section.read_text(encoding="utf-8").rstrip() + "\n"

combined = re.sub(r"\\input\{(output/ch6/sections/[^}]+)\}", expand, source)
target = directory / "CH6.txt"
target.write_text(combined, encoding="utf-8")
print(f"Combined chapter written to {target}")
