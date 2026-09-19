#!/usr/bin/env python3
import sys
import re
from collections import Counter

EXPECTED = 3
# 匹配形如：mc20_13TeV.570862.MGPy...
pat = re.compile(r"\.(\d+)\.")

cnt = Counter()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    m = pat.search(line)
    if not m:
        # 像最后一行 "mc" 这种不完整的行会被忽略
        continue
    sample_id = m.group(1)
    cnt[sample_id] += 1

# 输出所有“不是3个”的 sample id
bad = [(sid, n) for sid, n in cnt.items() if n != EXPECTED]
for sid, n in sorted(bad, key=lambda x: int(x[0])):
    print(f"{sid}\t{n}")
