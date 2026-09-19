import numpy as np
import math

FIELDS = ("exp", "p1", "p2", "m1", "m2")
BAND_ORDER = ("m2", "m1", "exp", "p1", "p2")


def _clean_value(v, clip_max=99.0):
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

    return max(0.0, min(float(v), clip_max))


def _build_anchor_arrays(mmap, mus, gus, betas, field, clip_max=99.0):
    """
    把原始输入点中，正好落在目标规则网格上的点提取成 anchor。
    这些点在最终输出中保持不变。
    """
    mu_to_i = {float(mu): i for i, mu in enumerate(mus)}
    gu_to_j = {float(gu): j for j, gu in enumerate(gus)}
    be_to_k = {float(be): k for k, be in enumerate(betas)}

    shape = (len(mus), len(gus), len(betas))
    anchor_mask = np.zeros(shape, dtype=bool)
    anchor_vals = np.zeros(shape, dtype=float)

    for (mu, gu, be), d in mmap.items():
        mu = float(mu)
        gu = float(gu)
        be = float(be)

        if (mu not in mu_to_i) or (gu not in gu_to_j) or (be not in be_to_k):
            # 不在目标网格上的输入点，仍参与插值，但无法作为输出网格上的固定锚点
            continue

        v = _clean_value(d.get(field, 0.0), clip_max=clip_max)

        i = mu_to_i[mu]
        j = gu_to_j[gu]
        k = be_to_k[be]

        anchor_mask[i, j, k] = True
        anchor_vals[i, j, k] = v

    return anchor_mask, anchor_vals


def _check_anchor_consistency(anchor_mask, anchor_vals, mus, gus, betas,
                              field_name="unknown", tol=1e-12, max_report=20):
    """
    检查单个 field 的 anchor 是否与目标轴单调性冲突。

    目标单调性:
      - MU   增 -> 值增
      - gU   增 -> 值减
      - beta 增 -> 值减

    即若:
      i1 <= i2, j1 >= j2, k1 >= k2
    则必须:
      v1 <= v2
    """
    idx = np.argwhere(anchor_mask)
    vals = [anchor_vals[tuple(p)] for p in idx]

    conflicts = []
    n = len(idx)

    for a in range(n):
        i1, j1, k1 = idx[a]
        v1 = vals[a]
        for b in range(n):
            if a == b:
                continue
            i2, j2, k2 = idx[b]
            v2 = vals[b]

            if (i1 <= i2) and (j1 >= j2) and (k1 >= k2):
                if v1 > v2 + tol:
                    conflicts.append({
                        "field": field_name,
                        "p1_idx": (i1, j1, k1),
                        "p1_coord": (mus[i1], gus[j1], betas[k1]),
                        "p1_val": v1,
                        "p2_idx": (i2, j2, k2),
                        "p2_coord": (mus[i2], gus[j2], betas[k2]),
                        "p2_val": v2,
                    })
                    if len(conflicts) >= max_report:
                        break
        if len(conflicts) >= max_report:
            break

    if conflicts:
        lines = [
            f"[AXIS MONOTONIC CONFLICT] field = {field_name}, 共找到至少 {len(conflicts)} 个冲突(最多显示 {max_report} 个):"
        ]
        for c in conflicts:
            mu1, gu1, be1 = c["p1_coord"]
            mu2, gu2, be2 = c["p2_coord"]
            lines.append(
                f"  ({field_name}) "
                f"P1: mu={mu1}, gu={gu1}, beta={be1}, value={c['p1_val']}  "
                f"应 <=  "
                f"P2: mu={mu2}, gu={gu2}, beta={be2}, value={c['p2_val']}"
            )
        raise ValueError("\n".join(lines))


def _build_lower_envelope(shape, anchor_mask, anchor_vals):
    """
    构造每个格点允许的最小值 L，使其满足：
      - 轴单调
      - anchor 固定
    """
    I, J, K = shape
    L = np.full(shape, -np.inf, dtype=float)
    L[anchor_mask] = anchor_vals[anchor_mask]

    for i in range(I):
        for j in range(J - 1, -1, -1):
            for k in range(K - 1, -1, -1):
                lb = L[i, j, k]
                if i > 0:
                    lb = max(lb, L[i - 1, j, k])
                if j + 1 < J:
                    lb = max(lb, L[i, j + 1, k])
                if k + 1 < K:
                    lb = max(lb, L[i, j, k + 1])

                if anchor_mask[i, j, k]:
                    if lb > anchor_vals[i, j, k] + 1e-12:
                        raise ValueError(
                            f"anchor[{i},{j},{k}]={anchor_vals[i,j,k]} "
                            f"小于其必须满足的单调下界 {lb}，无解"
                        )
                    L[i, j, k] = anchor_vals[i, j, k]
                else:
                    L[i, j, k] = lb

    L[np.isneginf(L)] = 0.0
    return L


def _build_upper_envelope(shape, anchor_mask, anchor_vals, clip_max=99.0):
    """
    构造每个格点允许的最大值 U，使其满足：
      - 轴单调
      - anchor 固定
    """
    I, J, K = shape
    U = np.full(shape, np.inf, dtype=float)
    U[anchor_mask] = anchor_vals[anchor_mask]

    for i in range(I - 1, -1, -1):
        for j in range(J):
            for k in range(K):
                ub = U[i, j, k]
                if i + 1 < I:
                    ub = min(ub, U[i + 1, j, k])
                if j - 1 >= 0:
                    ub = min(ub, U[i, j - 1, k])
                if k - 1 >= 0:
                    ub = min(ub, U[i, j, k - 1])

                if anchor_mask[i, j, k]:
                    if ub < anchor_vals[i, j, k] - 1e-12:
                        raise ValueError(
                            f"anchor[{i},{j},{k}]={anchor_vals[i,j,k]} "
                            f"大于其必须满足的单调上界 {ub}，无解"
                        )
                    U[i, j, k] = anchor_vals[i, j, k]
                else:
                    U[i, j, k] = ub

    U[np.isposinf(U)] = clip_max
    return U


def _project_monotone_keep_anchors(arr, anchor_mask, anchor_vals,
                                   mus, gus, betas,
                                   field_name="unknown",
                                   clip_max=99.0, max_iter=200, tol=1e-10):
    """
    把单个 field 的 3D 数组投影到:
      1) 满足轴单调
      2) anchor 保持不变
    的可行集合中。
    """
    arr = np.asarray(arr, dtype=float)
    shape = arr.shape
    I, J, K = shape

    _check_anchor_consistency(
        anchor_mask,
        anchor_vals,
        mus=mus,
        gus=gus,
        betas=betas,
        field_name=field_name,
        tol=1e-12,
        max_report=20,
    )

    L = _build_lower_envelope(shape, anchor_mask, anchor_vals)
    U = _build_upper_envelope(shape, anchor_mask, anchor_vals, clip_max=clip_max)

    if np.any(L > U + tol):
        raise ValueError(
            f"[NO FEASIBLE SOLUTION] field={field_name}: "
            f"不存在同时满足轴单调且保持输入点不变的解"
        )

    out = np.clip(arr, L, U)
    out[anchor_mask] = anchor_vals[anchor_mask]

    for _ in range(max_iter):
        old = out.copy()

        # forward pass
        for i in range(I):
            for j in range(J - 1, -1, -1):
                for k in range(K - 1, -1, -1):
                    if anchor_mask[i, j, k]:
                        continue

                    lb = L[i, j, k]
                    if i > 0:
                        lb = max(lb, out[i - 1, j, k])
                    if j + 1 < J:
                        lb = max(lb, out[i, j + 1, k])
                    if k + 1 < K:
                        lb = max(lb, out[i, j, k + 1])

                    if out[i, j, k] < lb:
                        out[i, j, k] = lb

        # backward pass
        for i in range(I - 1, -1, -1):
            for j in range(J):
                for k in range(K):
                    if anchor_mask[i, j, k]:
                        continue

                    ub = U[i, j, k]
                    if i + 1 < I:
                        ub = min(ub, out[i + 1, j, k])
                    if j - 1 >= 0:
                        ub = min(ub, out[i, j - 1, k])
                    if k - 1 >= 0:
                        ub = min(ub, out[i, j, k - 1])

                    if out[i, j, k] > ub:
                        out[i, j, k] = ub

        out = np.clip(out, L, U)
        out[anchor_mask] = anchor_vals[anchor_mask]

        if np.max(np.abs(out - old)) < tol:
            break

    return out


def _check_band_anchor_consistency(anchor_masks, anchor_vals, mus, gus, betas,
                                   tol=1e-12, max_report=20):
    """
    检查 anchor 在同一个格点上是否已违反 band 顺序:
      m2 <= m1 <= exp <= p1 <= p2

    只有当两个字段都被 anchor 固定时，才要求它们必须满足顺序。
    """
    shape = anchor_vals[BAND_ORDER[0]].shape
    I, J, K = shape

    conflicts = []

    for i in range(I):
        for j in range(J):
            for k in range(K):
                for a in range(len(BAND_ORDER) - 1):
                    f1 = BAND_ORDER[a]
                    f2 = BAND_ORDER[a + 1]

                    if anchor_masks[f1][i, j, k] and anchor_masks[f2][i, j, k]:
                        v1 = anchor_vals[f1][i, j, k]
                        v2 = anchor_vals[f2][i, j, k]

                        if v1 > v2 + tol:
                            conflicts.append({
                                "grid_idx": (i, j, k),
                                "coord": (mus[i], gus[j], betas[k]),
                                "f1": f1,
                                "v1": v1,
                                "f2": f2,
                                "v2": v2,
                            })
                            if len(conflicts) >= max_report:
                                break
                if len(conflicts) >= max_report:
                    break
            if len(conflicts) >= max_report:
                break
        if len(conflicts) >= max_report:
            break

    if conflicts:
        lines = [
            f"[BAND ORDER CONFLICT] 共找到至少 {len(conflicts)} 个冲突(最多显示 {max_report} 个):"
        ]
        for c in conflicts:
            mu, gu, be = c["coord"]
            lines.append(
                f"  at mu={mu}, gu={gu}, beta={be}: "
                f"{c['f1']}={c['v1']} > {c['f2']}={c['v2']}"
            )
        raise ValueError("\n".join(lines))


def _project_band_point_keep_anchors(y, fixed_mask, fixed_vals,
                                     clip_max=99.0, max_iter=100, tol=1e-12):
    """
    对单个格点上的 5 维向量做 band 顺序修正，保持 fixed 项不变。
    顺序要求:
      m2 <= m1 <= exp <= p1 <= p2
    """
    y = np.asarray(y, dtype=float)
    fixed_mask = np.asarray(fixed_mask, dtype=bool)
    fixed_vals = np.asarray(fixed_vals, dtype=float)

    n = len(y)
    if n != 5:
        raise ValueError(f"band 向量长度必须为 5，当前为 {n}")

    lower = np.zeros(n, dtype=float)
    upper = np.full(n, clip_max, dtype=float)

    lower[fixed_mask] = fixed_vals[fixed_mask]
    upper[fixed_mask] = fixed_vals[fixed_mask]

    running = 0.0
    for t in range(n):
        if fixed_mask[t]:
            running = max(running, fixed_vals[t])
        lower[t] = max(lower[t], running)

    running = clip_max
    for t in range(n - 1, -1, -1):
        if fixed_mask[t]:
            running = min(running, fixed_vals[t])
        upper[t] = min(upper[t], running)

    if np.any(lower > upper + tol):
        raise ValueError(
            f"band anchor 冲突，无解: lower={lower}, upper={upper}, fixed_vals={fixed_vals}"
        )

    x = np.clip(y, lower, upper)
    x[fixed_mask] = fixed_vals[fixed_mask]

    for _ in range(max_iter):
        old = x.copy()

        x = np.maximum.accumulate(x)
        x = np.minimum.accumulate(x[::-1])[::-1]

        x = np.clip(x, lower, upper)
        x[fixed_mask] = fixed_vals[fixed_mask]

        if np.max(np.abs(x - old)) < tol:
            break

    return x


def _project_band_keep_anchors(field_arrays, anchor_masks, anchor_vals,
                               clip_max=99.0, max_iter=100, tol=1e-10):
    """
    对整个 3D 网格逐点施加 band 顺序，保持 anchor 不变。
    """
    _check_band_anchor_consistency(
        anchor_masks,
        anchor_vals,
        mus=_project_band_keep_anchors._mus,
        gus=_project_band_keep_anchors._gus,
        betas=_project_band_keep_anchors._betas,
        tol=1e-12,
        max_report=20,
    )

    out = {f: np.array(field_arrays[f], dtype=float, copy=True) for f in FIELDS}
    shape = out[BAND_ORDER[0]].shape
    I, J, K = shape

    for i in range(I):
        for j in range(J):
            for k in range(K):
                y = np.array([out[f][i, j, k] for f in BAND_ORDER], dtype=float)
                fixed_mask = np.array([anchor_masks[f][i, j, k] for f in BAND_ORDER], dtype=bool)
                fixed_vals = np.array([anchor_vals[f][i, j, k] for f in BAND_ORDER], dtype=float)

                x = _project_band_point_keep_anchors(
                    y,
                    fixed_mask=fixed_mask,
                    fixed_vals=fixed_vals,
                    clip_max=clip_max,
                    max_iter=max_iter,
                    tol=tol,
                )

                for idx, f in enumerate(BAND_ORDER):
                    out[f][i, j, k] = x[idx]

    return out


def _assert_final_constraints(field_arrays, anchor_masks, anchor_vals, tol=1e-8):
    for f in FIELDS:
        arr = field_arrays[f]
        mask = anchor_masks[f]
        vals = anchor_vals[f]
        if np.any(np.abs(arr[mask] - vals[mask]) > tol):
            raise ValueError(f"{f}: 最终结果没有保持 anchor 不变")

    for f in FIELDS:
        arr = field_arrays[f]

        if arr.shape[0] > 1:
            if np.any(np.diff(arr, axis=0) < -tol):
                raise ValueError(f"{f}: MU 方向不单调")
        if arr.shape[1] > 1:
            if np.any(np.diff(arr, axis=1) > tol):
                raise ValueError(f"{f}: gU 方向不单调")
        if arr.shape[2] > 1:
            if np.any(np.diff(arr, axis=2) > tol):
                raise ValueError(f"{f}: beta 方向不单调")

    m2 = field_arrays["m2"]
    m1 = field_arrays["m1"]
    exp = field_arrays["exp"]
    p1 = field_arrays["p1"]
    p2 = field_arrays["p2"]

    if np.any(m2 > m1 + tol):
        raise ValueError("最终结果违反 band 顺序: m2 > m1")
    if np.any(m1 > exp + tol):
        raise ValueError("最终结果违反 band 顺序: m1 > exp")
    if np.any(exp > p1 + tol):
        raise ValueError("最终结果违反 band 顺序: exp > p1")
    if np.any(p1 > p2 + tol):
        raise ValueError("最终结果违反 band 顺序: p1 > p2")


def build_full_grid_monotone(mmap, mus, gus, betas, clip_max=99.0,
                             outer_iter=50, tol=1e-8):
    """
    在 (mus, gus, betas) 规则网格上做 3D 插值，并对最终结果施加:
      1) MU   增大 -> 值单调不减
      2) gU   增大 -> 值单调不增
      3) beta 增大 -> 值单调不增
      4) anchor 不变
      5) band 顺序: m2 <= m1 <= exp <= p1 <= p2

    如果 anchor 存在冲突，报错信息里会直接显示冲突对应的
      mu, gu, beta, field, value
    """
    from scipy.interpolate import griddata

    mus = list(mus)
    gus = list(gus)
    betas = list(betas)

    # 给 band 投影函数挂上网格坐标，便于 debug 输出
    _project_band_keep_anchors._mus = mus
    _project_band_keep_anchors._gus = gus
    _project_band_keep_anchors._betas = betas

    pts = []
    vals = {f: [] for f in FIELDS}

    eps_beta = 1e-6
    for (mu, gu, be), d in mmap.items():
        mu = float(mu)
        gu = float(gu)
        be = float(be)

        dd = {}
        for f in FIELDS:
            dd[f] = _clean_value(d.get(f, 0.0), clip_max=clip_max)

        x = math.log(gu)
        y = math.log(be + eps_beta)
        z = -math.log(mu)

        pts.append((x, y, z))

        for f in FIELDS:
            vals[f].append(math.log(dd[f] + 1.0))

    pts = np.array(pts, dtype=float)

    X = np.array([math.log(float(g)) for g in gus], dtype=float)
    Y = np.array([math.log(float(b) + eps_beta) for b in betas], dtype=float)
    Z = np.array([-math.log(float(m)) for m in mus], dtype=float)

    Zg, Xg, Yg = np.meshgrid(Z, X, Y, indexing="ij")
    grid_pts = np.stack([Xg.ravel(), Yg.ravel(), Zg.ravel()], axis=1)

    shape = (len(mus), len(gus), len(betas))

    field_arrays = {}
    anchor_masks = {}
    anchor_vals = {}

    for f in FIELDS:
        v = np.array(vals[f], dtype=float)

        lin = griddata(pts, v, grid_pts, method="linear")
        nn = griddata(pts, v, grid_pts, method="nearest")
        vfill = np.where(np.isfinite(lin), lin, nn)

        raw = np.expm1(vfill)
        raw = np.where(np.isfinite(raw), raw, 0.0)
        raw = np.clip(raw, 0.0, clip_max)
        raw = raw.reshape(shape)

        field_arrays[f] = raw
        anchor_masks[f], anchor_vals[f] = _build_anchor_arrays(
            mmap, mus, gus, betas, f, clip_max=clip_max
        )

    for f in FIELDS:
        _check_anchor_consistency(
            anchor_masks[f],
            anchor_vals[f],
            mus=mus,
            gus=gus,
            betas=betas,
            field_name=f,
            tol=1e-12,
            max_report=20,
        )

    _check_band_anchor_consistency(
        anchor_masks,
        anchor_vals,
        mus=mus,
        gus=gus,
        betas=betas,
        tol=1e-12,
        max_report=20,
    )

    for _ in range(outer_iter):
        old = {f: field_arrays[f].copy() for f in FIELDS}

        for f in FIELDS:
            field_arrays[f] = _project_monotone_keep_anchors(
                field_arrays[f],
                anchor_mask=anchor_masks[f],
                anchor_vals=anchor_vals[f],
                mus=mus,
                gus=gus,
                betas=betas,
                field_name=f,
                clip_max=clip_max,
                max_iter=100,
                tol=1e-10,
            )

        field_arrays = _project_band_keep_anchors(
            field_arrays,
            anchor_masks=anchor_masks,
            anchor_vals=anchor_vals,
            clip_max=clip_max,
            max_iter=100,
            tol=1e-10,
        )

        diff = max(np.max(np.abs(field_arrays[f] - old[f])) for f in FIELDS)
        if diff < tol:
            break

    for f in FIELDS:
        field_arrays[f] = _project_monotone_keep_anchors(
            field_arrays[f],
            anchor_mask=anchor_masks[f],
            anchor_vals=anchor_vals[f],
            mus=mus,
            gus=gus,
            betas=betas,
            field_name=f,
            clip_max=clip_max,
            max_iter=100,
            tol=1e-10,
        )

    field_arrays = _project_band_keep_anchors(
        field_arrays,
        anchor_masks=anchor_masks,
        anchor_vals=anchor_vals,
        clip_max=clip_max,
        max_iter=100,
        tol=1e-10,
    )

    _assert_final_constraints(field_arrays, anchor_masks, anchor_vals, tol=1e-7)

    out = {}
    for i, mu in enumerate(mus):
        for j, gu in enumerate(gus):
            for k, be in enumerate(betas):
                key = (mu, gu, be)
                out[key] = {
                    "exp": float(field_arrays["exp"][i, j, k]),
                    "p1": float(field_arrays["p1"][i, j, k]),
                    "p2": float(field_arrays["p2"][i, j, k]),
                    "m1": float(field_arrays["m1"][i, j, k]),
                    "m2": float(field_arrays["m2"][i, j, k]),
                }

    return out