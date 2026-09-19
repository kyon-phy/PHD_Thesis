import numpy as np
import math

FIELDS = ("exp","p1","p2","m1","m2")

import numpy as np

def enforce_monotone_axes(arr, mus, gus, betas):
    """
    arr shape = (len(mus), len(gus), len(betas))
    要求:
      - MU   增大 => arr 单调增
      - gU   增大 => arr 单调减
      - beta 增大 => arr 单调减
    """

    mus = np.asarray(mus, dtype=float)
    gus = np.asarray(gus, dtype=float)
    betas = np.asarray(betas, dtype=float)

    # 最好保证输入网格本身是升序
    if not np.all(np.diff(mus) > 0):
        raise ValueError("mus 必须严格升序")
    if not np.all(np.diff(gus) > 0):
        raise ValueError("gus 必须严格升序")
    if not np.all(np.diff(betas) > 0):
        raise ValueError("betas 必须严格升序")

    out = np.array(arr, dtype=float, copy=True)

    # 1) 随 MU 单调增
    # out[i,j,k] >= out[i-1,j,k]
    out = np.maximum.accumulate(out, axis=0)

    # 2) 随 gU 单调减
    # out[i,j,k] <= out[i,j-1,k]
    out = np.minimum.accumulate(out, axis=1)

    # 3) 随 beta 单调减
    # out[i,j,k] <= out[i,j,k-1]
    out = np.minimum.accumulate(out, axis=2)

    return out

def build_full_grid_monotone(mmap, mus, gus, betas, clip_max=99.0):
    # 1) 收集散点
    pts = []
    vals = {f: [] for f in FIELDS}

    eps_beta = 1e-6  # 避免 beta=0 的 log
    for (mu, gu, be), d in mmap.items():
        # 清洗：+inf->clip_max, nan->0, -inf->0，其它裁剪到[0,clip_max]
        dd = {}
        for f in FIELDS:
            v = d.get(f, 0.0)

            if v is None:
                v = 0.0
            else:
                v = float(v)
                if math.isnan(v):
                    v = 0.0
                elif math.isinf(v):
                    v = clip_max if v > 0 else 0.0

            if not np.isfinite(v):
                v = 0.0

            v = max(0.0, min(float(v), clip_max))
            dd[f] = v

        x = math.log(float(gu))
        y = math.log(float(be) + eps_beta)
        z = -math.log(float(mu))
        pts.append((x, y, z))
        for f in FIELDS:
            vals[f].append(math.log(dd[f] + 1.0))  # log1p

    pts = np.array(pts, dtype=float)

    # 2) 目标网格坐标
    X = np.array([math.log(g) for g in gus], dtype=float)
    Y = np.array([math.log(b + eps_beta) for b in betas], dtype=float)
    Z = np.array([-math.log(m) for m in mus], dtype=float)

    # mesh: (len(mus), len(gus), len(betas)) 我们按 (mu,gu,beta) 输出
    Zg, Xg, Yg = np.meshgrid(Z, X, Y, indexing="ij")
    grid_pts = np.stack([Xg.ravel(), Yg.ravel(), Zg.ravel()], axis=1)

    # 3) 用 scipy 做 3D 线性插值（边界外用 nearest 补）
    from scipy.interpolate import griddata

    out = {}
    for f in FIELDS:
        v = np.array(vals[f], dtype=float)

        lin = griddata(pts, v, grid_pts, method="linear")
        nn  = griddata(pts, v, grid_pts, method="nearest")
        vfill = np.where(np.isfinite(lin), lin, nn)  # 线性插值为主，空的用最近邻补

        # 反变换回原值域：expm1，并裁剪到[0,clip_max]
        raw = np.expm1(vfill)
        raw = np.where(np.isfinite(raw), raw, 0.0)
        raw = np.clip(raw, 0.0, clip_max)

        # 写回字典
        raw = raw.reshape((len(mus), len(gus), len(betas)))
        
        # enforce monotonicity
        raw = enforce_monotone_axes(raw, mus, gus, betas)

        for i, mu in enumerate(mus):
            for j, gu in enumerate(gus):
                for k, be in enumerate(betas):
                    key = (mu, gu, be)
                    out.setdefault(key, {})
                    out[key][f] = float(raw[i, j, k])

    return out
