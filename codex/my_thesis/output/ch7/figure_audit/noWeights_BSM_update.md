# Fig. 7.3 / 7.4: noWeights_BSM signal

**最新更新：NonRes 已改为与 cutflow 相同的 `(2.5 TeV, 2.5, 1.0)`，文件为 `MU2500_gU2_5_23L1_0_noWeights_BSM.root`。Res 保持 `(1.5 TeV, 1.5, 0.6)`。两者统一用 BSM：完整 SR yield 比较中，BSM 在两个 region 都比 combined 更接近旧 cutflow，详见 `bsm_vs_combined_cutflow.json`。六张 NonRes 图、legend 和 caption 已更新并编译。下面保留首次改用 BSM 时的历史说明，其中 NonRes 的 3.0 TeV 数字已被替换；当前逐 bin 数值以 `bsm_signal_bins.json` 为准。**

2026-09-20：按用户要求，用 `noWeights_BSM` 替换 12 张 loose SR1b N−1 图中的 signal。保留两个 benchmark 和全部 background / uncertainty 数值。

## Signal 文件及读取方式

- SR1b-Res：`MU1500_gU1_5_23L0_6_noWeights_BSM.root`，参数 `(MU, gU, betaL23) = (1.5 TeV, 1.5, 0.6)`。
- SR1b-NonRes：`MU3000_gU2_5_23L1_0_noWeights_BSM.root`，参数 `(MU, gU, betaL23) = (3.0 TeV, 2.5, 1.0)`。

实际文件名中的 `BSM` 是大写。CERN 源目录：

```text
/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_N_minus_1_v3/
```

通过现有 SSH alias `codex_lxatut` 读取。本地副本：

```text
/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/my_thesis/data/ch7/signal_noWeights_v3/
```

对应的 `_noWeights_inf.root` 和 `_noWeights_comb.root` 也已保存用于数值验证。六个文件的 SHA256 与远端完全一致，记录为该目录的 `source_manifest.json`。

读取对象为：

```text
NOSYS/<suffix>_SR_1tau0l1b_loose_<Res|NonRes>_<variable>_N_minus_1
```

`variable → suffix`：`InvM → InvM`、`met → met`、`mT → mT`、`tau_pT → tau_pT`、`nlightjets → nLightJets`、`dphi → dphi_taumet`。

沿用原图的 bin edges，以及 TRExFitter 配置 `MergeUnderOverFlow: True` 的处理：将范围外和 under/overflow 的内容合入首末 bin。不加 signal scale，不对齐或归一化到旧曲线。先用此处理复现全部原 `comb` 曲线，再对 BSM 采用同一处理。12 张图的 raw `comb = BSM + inf` 已逐 bin 验证；comb 的 variance 也等于两者 variance 之和。

## 图中 signal 总和

以下为显示 bins 的总和（含合入的 overflow），**不是 final SR yield**。旧 `comb → BSM`，单位 events：

- Res InvM：6.437935520 → 7.183792654。
- Res MET：4.789457592 → 4.937685944。
- Res mT：4.810661271 → 4.959056336。
- Res tau pT：4.804699080 → 4.952927432。
- Res light jets：5.202734458 → 5.565828024。
- Res delta phi：5.098146746 → 5.460362063。
- NonRes InvM：5.799853973 → 7.105476603。
- NonRes MET：7.208040288 → 8.830096847。
- NonRes mT：6.219955898 → 7.792273302。
- NonRes tau pT：5.799853973 → 7.105476603。
- NonRes light jets：14.880638693 → 19.339637187。
- NonRes delta phi：10.829517503 → 14.140195674。

完整 bin 内容、variance、ROOT key、路径、checksum 及原 comb 比较保存在 `bsm_signal_bins.json`。新结果仍不能直接等同于 INT note：旧 signal 的生成/权重流程、部分 benchmark 和 binning 与此版本不同，详情见上一轮审计。

## 验证及版式

`verified_bins_and_provenance.json` 已更新：新 signal 逐 bin 对照上述 BSM ROOT；五组背景和总背景仍对照原 nominal ROOT/YAML；误差带仍对照原 TGraphAsymmErrors/YAML。实际 EPS signal 路径的每个 bin 高度也已检查。

除 signal 折线的坐标外，12 个 EPS 的其余内容与更换前逐字节一致。因此图例、轴、两种 signal 的颜色/虚线、所有 stack、error band 和 paper L 形箭头均保留。原图、脚本、manifest、audit 及 TeX 备份于 `before_bsm_signal/`。

本轮未修改 LaTeX 格式或正文。绘图程序只替换 EPS 中 signal 路径的 `m`（起点）、`X`（相对水平线段）、`Y`（相对竖直线段）坐标，使用原有对数纵轴映射；原颜色、dash、line width 和坐标系不变。低于绘图下界 0.1 的 bin 在画面下界裁切，JSON 保留真实数值。

CH7 已重新编译，共 22 页；Fig. 7.3 / 7.4 位于第 7 / 10 页。逐一核对 latexmk 输入 MD5，确认新 12 个 PDF 已进入最终编译。保留已有 class、bibliography、fancyhdr、hyperref、TikZ-Feynman warnings；无 LaTeX error、overfull box 或未定义引用。

## 复现

从 thesis 根目录运行：

```sh
PYTHONPATH=tmp/ch7_plot_deps:tmp/skill_validation_deps /usr/local/bin/python3 scripts/ch7/prepare_bsm_signals.py
/usr/local/bin/python3 scripts/ch7/restyle_eps.py --sr1b-only
PYTHONPATH=tmp/ch7_plot_deps:tmp/skill_validation_deps /usr/local/bin/python3 scripts/ch7/audit_sr_figures.py
```

本次范围为 Fig. 7.3 / 7.4 的 12 张 SR1b 分布。SR0b、optimisation scan 和 cutflow/yield tables 沿用各自原来源。
