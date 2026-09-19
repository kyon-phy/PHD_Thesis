import numpy as np
def ratio_with_error(B, B_err, S, S_err):
    """
    计算 r = b/a 及其误差传递 dr
    a, b 为测量值，da, db 为各自标准差
    """
    r = S / B
    dr = r * ((S_err / S)**2 + (B_err / B)**2)**0.5
    return r, dr

MC = 475.12258103
MC_theory_err = 0.0 * MC
MC_stat_err = 35.556922
MC_err = np.sqrt(MC_stat_err**2+MC_theory_err**2)
Data = 474
Data_err = np.sqrt(Data)

r1, dr1 = ratio_with_error(MC, MC_err, Data, Data_err)
print(f"MC/Data = {r1:.6f} ± {dr1:.6f}")
