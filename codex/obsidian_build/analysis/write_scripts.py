from pathlib import Path
import json, datetime, zoneinfo
b=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/obsidian_build/code')
v=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/obsidian/LQ taunub search/80_Scripts');v.mkdir(exist_ok=True)
snapshot=json.loads((b/'remote_snapshot.json').read_text())
meta={Path(x['path']).name:x for x in snapshot['files'] if x.get('relative','').startswith('run/scripts/') and Path(x['path']).suffix in ('.py','.sh')}
groups={
 '脚本专题-样本清单配置生成与结果检查':['sig_config_maker.py','config_generator.py','toy_config_maker.py','check_failed_jobs.py','check_files.py','hadd_bsm_inf.py','copy_blank_grids.sh','run_script.sh'],
 '脚本专题-SF和signal权重验证':['SF_Comparison_el.py','SF_Comparison_jet.py','run_SF_Comparison.sh','validate_signal_reweight.py','validate_preselected.py','compare_sum_of_weights.py'],
 '脚本专题-transfer-factor与systematics检查':['TF_calculater.py','TF_calculater_v2.py','TF_calculater_v2_smooth.py','ratio_calculator.py'],
 '脚本专题-limit读取插值与acceptance':['draw_limits.py','draw_limits_mu.py','interpolate_function.py','interpolate_function_backup.py','draw_vis_Xsec.py'],
 '脚本专题-interference与cut优化':['signal_yield_plotter.py','compare_inf_b33R_shapes.py','compare_inf_b33R_ntuple_shapes.py','significance_scan.py'],
 '脚本专题-提交与失败重扫':['submit_tail_b33R1_0.sh','submit_tail_b33R1_0_M4000_M5000.sh','submit_tail_TREx_betaR33Rm1_0_1bSR.sh','submit_job_lxatut_TREx_betaR33Rm1_0_1bSR.sh','submit_job_lxatut_TREx_betaR33Rm1_0_1bSR_rescan.sh','update_betaR33Rm1_0_scan_ranges.py'],
 '脚本专题-检查图与paper图整理':['pdf_generator.py','pdf_generator_mc20d.py','eps_modifier.py','copy_figs.py']}
assert set(sum(groups.values(),[]))==set(meta),(set(meta)-set(sum(groups.values(),[])))
def link(n,line=None):
 return f'[{n}]({b}/snapshot/run/scripts/{n}'+(f':{line}' if line else '')+')'
def sources(group):
 return '\n\n## 源码与版本\n\n'+'\n'.join('- '+link(n)+f'；远程 `{meta[n]["path"]}`。' for n in groups[group])+f'\n\n本页来自 2026-09-07 只读源码审阅；没有运行分析、提交 jobs、重算 limits 或修改远程 scripts。每个文件的时间和 SHA-256 前缀见 [[Scripts脚本目录与时间索引]]；完整哈希来自 [remote_snapshot.json]({b}/remote_snapshot.json)。真实创建时间不能由 mtime / ctime 代替。\n'
def write(n,t):
 (v/(n+'.md')).write_text(f'---\ntype: script-reference\nupdated: 2026-09-07\nstatus: 已按当前源码归类\ntags: [ATLAS, taunub, scripts, FastFrames, TRExFitter]\n---\n\n# {n}\n\n'+t+(sources(n) if n in groups else ''))
write('脚本专题-样本清单配置生成与结果检查',r'''## 样本清单 → YAML：sig_config_maker.py

输入两个文本：dataset names 和 FastFrames filelist（每行 `DSID campaign simtype path`）。按 DSID / coupling / bsm-inf tag 解析 sample name，只把 filelist 中 **mc20a、mc20d、mc20e 三个 campaigns 都存在** 的点放入完整样本输出，同时列出不完整样本、候选清理文件名。[源码 L30–103、L104–176]

```bash
python3 sig_config_maker.py dsname_list.txt filelist.txt > sample_report.txt
```

输出包含说明文字、完整 YAML、incomplete YAML、comma-separated sample names，不是一个可直接传给 FastFrames 的纯 YAML。当前 `REGIONS` 只列 `_sch` 六区，`SIM_TYPE=fastsim`；生成 NonRes 配置需要核对并调整相应 regions。缺失 coupling tokens 时有 `gU=1_0 / beta23=0_2` defaults；不得把推断出的 defaults 当源 dataset 已明确记录的参数。

## 模板 → 多个 TREx configs：config_generator.py

实际 CLI 使用 **named options**，不是文件头过时的 positional example：

```bash
python3 config_generator.py --config template.config \
  --signals_dir /path/to/ROOT_histograms \
  --placeholder MU1500_gU1_5_23L0_2 --out_dir configs_out
```

当前 active filter **只接受** `MU*_b33Rm1_0_alldecay_corrected_bsm_Res.root`，并剥去后缀取得参数名。不是所有 `MU*.root` 都会生成 config。随后对模板作字符串整体 `replace()`，输出 `<template_stem>_<signal>.config`。这是当前右手 all-decay 扫描工具状态，不能直接把旧 LH noWeights 命令拿来使用。[L27–47、L68–86]

## Asymptotic 输出 → toy configs：toy_config_maker.py

按参数点匹配 config 与 fit output directory，读取 `Limits/Asymptotics/myLimit.root` 中 `stats` 的 `exp_upperlimit`、±1σ、±2σ。默认输出范围：

$$\mathrm{ScanMin}=0,\qquad \mathrm{ScanMax}=L_{+2\sigma}+|L_{+2\sigma}-L_{+1\sigma}|,$$

并要求 max 至少 1.1；读到 NaN / Inf 时 fallback max=50。生成 `LimitType: TOYS`、`SplusBToys:10000`、`BonlyToys:10000`、`ScanSteps:15`、seed 默认 1234。[L86–103、L319–358]

```bash
python3 toy_config_maker.py configs_in fit_results configs_toy \
  --combined --seed 1234 --dry-run
```

去掉 `--dry-run` 才写 output configs。默认 ROOT 相对路径可用 `--root-relpath` 改。命名必须符合脚本 `noWeights_comb...` 与 `allVR_SPLUSB...` 正则；匹配不到就跳过。

**源码实际行为与注释的差别**：生成的 `LimitBlind: False`，不是 L90 注释的 TRUE；Limit block 的 POI 恒为 `sqrt_mu`。`--combined` 更新 `sqrt_mu` 和 `Norm_BSM=(sqrt_mu^2-sqrt_mu)`；不加 combined 只更新 `mu`，却仍写 `POI:sqrt_mu`。所以非 combined 模式需要先检查输出结构，不能直接用于 nominal production。这里的 square-root 参数应对照 [[统计分析与结果解释]] 与正式 fit config。

## 检查 missing results：check_failed_jobs.py

```bash
python3 check_failed_jobs.py fit_results configs \
  --out-dir missing_configs_out --out-txt missing_configs.txt --dry-run
```

比较文件夹 A 的结果子目录与文件夹 B 的 `.config` 参数点名称；缺少匹配结果目录的 configs 被报告并在非 dry-run 模式复制。`--overwrite` 控制复制重名行为。**只检查目录名存在性，不打开 ROOT / 验证 fit convergence**；存在空目录或失败结果仍可能漏检。[L21–75、L93–161]

## 检查 dataset count：check_files.py

```bash
python3 check_files.py < dataset_names.txt
```

从每行首个 `.数字.` 提取 DSID，列出出现次数不是 3 的 DSID。[L6–26] 它只数行数：三行不自动证明三个不同 campaigns 都齐全，也不能检验 ROOT 可读性。更完整的 campaign 对照用 sig_config_maker。

## BSM + interference 文件合并：hadd_bsm_inf.py

```bash
python3 hadd_bsm_inf.py /path/to/hists --key_word MU1500
```

按文件名唯一的 `_bsm_` / `_inf_` token 分组，相同参数 / suffix 配成一对，以 ROOT `hadd` 写 `_combined_` 文件。`--force` 允许覆盖输出；默认关键字是 `MU1500`，若想处理别的 masses 必须显式传入相应过滤词。[L11–121]

此相加得到 $S+I$ 的 histogram；正式 fit 若使用 $x(S+I)+(x^2-x)S$，才与 $x^2S+xI$ 一致。合并文件不是对任意 $\mu$ 都可统一乘 $\mu$ 的 signal。

## 旧操作片段：copy_blank_grids.sh / run_script.sh

- `copy_blank_grids.sh` 是把一个现有 fit-result directory 复制到其他参数点名称下。其 loop 使用 `target_grid_list`，而定义的是 `target_grid_list_M1500`，当前 loop 名称不匹配；底部仍有一个 active `cp -r`。**复制来的 fit result 不是真实独立参数点的结果**，不得用来宣称新增 MC / fit evidence。[L3–28]
- `run_script.sh` 是历史命令笔记，混有 plotting、config generation、acceptance、toy、interference、EPS 和 `rm` / `hadd` 等 active commands，也有不完整的 `--signal` 命令和缺失脚本 `read_eventNumbers.py`。它不是可靠的一键 pipeline；查所需单条 command，并对照对应 Python 当前 CLI。目录里的新版 `.py` 与本文件旧命令不保证同步。
''')
write('脚本专题-SF和signal权重验证',r'''## 两套 ntuples 的 electron / jet SF 对比

`SF_Comparison_el.py` 与 `SF_Comparison_jet.py` 递归寻找两目录的 ROOT files，建 `reco` TChain，按 **(eventNumber, randomRunNumber)** 匹配事件，比较对象 kinematics 与 SF。默认相对容差：$p_T$ 5%、$\sqrt{\eta^2+\phi^2}$ 5%；这不是标准 $\Delta R$ matching。[el L46–137；jet L61–160]

```bash
python3 SF_Comparison_el.py --filepath1 ntuples_a --filepath2 ntuples_b \
  --tree reco --out el_sf_ratio.root --png_dir el_sf_plots
python3 SF_Comparison_jet.py --filepath1 ntuples_a --filepath2 ntuples_b \
  --tree reco --out jet_sf_ratio.root --png_dir jet_sf_plots
```

- electron 默认比较 `el_id_effSF_TightLH_Loose_VarRad_NOSYS`、reco、iso 三个 vector SF，可用 `--sfs` 替换 comma-separated branch list。
- jet 默认比较 `weight_ftag_effSF_GN2v01_Continuous_NOSYS`；检查匹配 jets 的 85% selection，并要求至少一只匹配 b-jet 后比较 event SF。
- 可调 `--bins`、`--xmin`、`--xmax`、`--pt_tol`、`--etaphisq_tol`；输出 ROOT + 可选 per-SF PNG。
- 匹配按对象 index 和宽松 kinematic agreement，不是进行任意 permutation 最优匹配。重复 event keys 在 dictionary 中可能覆盖，因此不等同于通用 event integrity 检查。

`run_SF_Comparison.sh` 是这两个程序的固定路径批次 wrapper。使用前读清 input/output 和当前目录；它记录某次 production 对照，而不是自动查找“最新两版”。

## 检查 corrected signal weights：validate_signal_reweight.py

```bash
python3 validate_signal_reweight.py --filelist-a filelist_a.txt \
  --filelist-b filelist_b.txt --rtol 1e-5 --threads 8
```

逐 DSID + campaign，读取 `reco`，按 eventNumber 比较 `weight_mc_corrected_GEN_gU*` branches。默认假设：**567621–567627 应相同，567628–567634 应不同**，用于验证某次 LH / RH reweight 更新是否生效。可用 `--dsids` 限定。[L31–120]

该 expectation 是脚本中对这两批 production 的约定，不是所有 signal 生成的恒等式。报告共同事件数、每 branch 不一致数及最大相对差；不能把不匹配事件自动认为权重错误，也要查是否 input samples / skim 不同。

## 检查 skim 是 full sample 子集：validate_preselected.py

```bash
python3 validate_preselected.py --dir-full full_ntuple_dir \
  --dir-presel preselected_ntuple_dir --rtol 1e-5 --threads 8
```

按 DSID + campaign 匹配 events，检查 preselected 每个 event 是否存在于 full，并逐项比较 corrected coupling weights。可用 `--dsids` 限定。[L34–144] 这个检查的预期是 **所有 DSID 的匹配事件 weights 保持一致**，与上一程序“RH 更新后应不同”是两个不同问题。

## 检查 sum of weights：compare_sum_of_weights.py

```bash
python3 compare_sum_of_weights.py --file-a sumw_a.txt --file-b sumw_b.txt \
  --rtol 1e-5
```

输入行格式 `DSID campaign simtype variation value`，只比较 `GEN_gU*` variation sums；默认 DSID 分组同 signal-reweight 验证。可 `--dsids` 覆盖。[L25–106]

event-level weights 与 total sumW 都需看：event weight 更新而 normalization denominator 未同步，会改 histogram 的 overall yield。此程序不检查 x-section / filter-efficiency metadata；那一层需另外核对。

## 依赖和可复现限制

这些检查需要与生产相容的 PyROOT / ROOT，signal validators 还调用 RDataFrame / NumPy。资料库只保存其逻辑和使用方式，没有为验证而读取全部 DAOD / ntuple，故这里没有给出“两个 production 已通过”的结论。脚本创建时间和最后修改时间见 [[Scripts脚本目录与时间索引]]。
''')
write('脚本专题-transfer-factor与systematics检查',r'''## 三个 TF_calculater 版本共同在算什么

从 nominal / varied MC histogram yield 比較某 target region 与 control region 的 transfer factor：

$$\frac{\Delta T}{T}=\frac{N_{r}^{\rm var}/N_{r}^{\rm nom}}{N_{\rm CR}^{\rm var}/N_{\rm CR}^{\rm nom}}-1.$$

这剔除了可被 CR normalization 吸收的共同变化，着重检查 **CR→SR / VR extrapolation**，不是把每个 region 独立的 raw variation 都当新的总归一化误差。样本组成、`NOSYS` / systematic TDirectory、Res (`sch`) / NonRes (`tch`)、input path 都通过 **文件顶部变量和 active dict entries** 指定，三者没有 argparse CLI。

运行形式是 `python3 TF_calculater.py` 或相应版本，但先在工作副本设置 `file_directory`、`file_path`、`channel`、CR / target hist names。不能只把 filenames 换成“v2”就假设是在同一 inputs 上比较。

## TF_calculater.py：积分 double ratio

读取指定 sample / directory 的同名 histogram，合并 yield / error，计算目标 SR、旧 VR0tau、旧 WVR1tau、TopVR1tau 相对于 CR 的 double ratio，并在 stdout 打印。当前底部 CR 用 `met_topCR_1tau1l_...`；切换到 W systematic 应同步检查 CR choice。[L173–257]

误差按 numerator / denominator 相互独立的近似传播，未使用 nominal 和 systematic 同一 MC events 所产生的 covariance；double ratio error 是工具诊断值，不是自动得到最终 nuisance prior。

## TF_calculater_v2.py：增加 bin-by-bin distributions

保留积分检查，再合并 histogram、写 nominal / variation、SR ratio 与 double-ratio histogram 到 **`doubleRatio.root`**。[L294–450] 可查看 extrapolation distortion 随变量的变化。

- 输出用 `RECREATE`，同名文件会重写；不同 variations 应使用隔离输出目录。
- 当前 source 的 `SYS` active sample dict 与基础版不同，不能按名字断定 v2 是同一输入的严格替代版。
- 运行后的 histogram 名称和 axis title 要结合 `channel` / hist variable 检查，避免 generic MET title 残留。

## TF_calculater_v2_smooth.py：ratio smoothing 与 CR-rate 校正

该版自动列 nominal directory 的 hist names，并按 region / channel / input-directory 名选变量和 loosened selection suffix。对于非 CR 的 MET histogram，会 crop 到 **200–2000 GeV**。`smooth` 开启时，先算 varied/nominal ratio，做 `Smooth(1)`，再乘回 nominal；当前代码有些 rebin 行被注释，不能写成总会 rebin。[L245–316、L445–508]

CR 使用含 under/overflow 的积分计算 $r_{\rm CR}$；target 的 ratio 再除该 CR rate，CR uncertainty 以 quadrature 加入各 bin errors。输出当前只写校正后的 `h_ratio_sr`、nominal / varied 等，旧 `h_DR.Write()` 被注释。[L510–545、L600–663]

这份工具用于 modelling cross-check。`file_path` 的精确字符串参与分支选择，换路径时可能走不同 suffix；crop 的新 histogram 使用均匀边界，原 histogram 非均匀 binning 时须先确认是否保持物理 bin 对应。它不是不依赖输入格式的通用 smoother，也不能仅因 filename 含 `smooth` 就认定正式 fit 已使用相同 smoothing。

## ratio_calculator.py：简单 ratio error

函数 `ratio_with_error(B,B_err,S,S_err)` 实際返回 $S/B$ 与独立误差传播。底部 hard-coded example 传入 MC 作为 B、Data 作为 S，因此输出 **Data/MC**；print label 却写 `MC/Data`。[L2–19]

使用时可以 import 函数，但 module 也会执行底部 example。若手工改变 numbers，记录 ratio 的真实分子 / 分母；不能直接复制错标签进 note。遇到零分母 / 零分子时现有实现未特别处理。
''')
write('脚本专题-limit读取插值与acceptance',r'''## draw_limits.py 是旧 significance 作图入口

从包含 `SPLUSB_MU...alldecay_corrected` 的结果目录提取参数，读取 `stats` 的 `exp_significance`，画 significance 随 coupling 的 slices。名字含 limits，但它不是读取 `myLimit.root` 的最终 CLs plotting 程序。[L19–92、L512–539]

```bash
python3 draw_limits.py /path/to/old_significance_results plots_significance
```

当前 `main()` 只 active 调用 `draw_gU_1D`、`draw_beta_1D`；二维函数调用被注释，ROOT output 却 hard-coded 为 `plots/output_TH2D.root`，不完全遵循传入 out_dir。不要拿它替代最终 toy limit reader。

## draw_limits_mu.py：当前多模式主入口

```bash
python3 draw_limits_mu.py --input_dir /path/to/toy_fit_results \
  --out_dir plots_toy --sig noWeights --unblind False --use_toy
```

主要接口：`--input_dir` 必需；`--out_dir`；`--sig`；`--unblind True/False`（源码只把精确字符串 `True` 当 True）；`--plot_option single/combined`；combined 时 `--limit_path`、`--extra_path_1`、`--extra_path_2` 读已有 contours 作 overlay。[L2780–2863]

**两个 ROOT output 结构**：

- asymptotic：`Limits/Asymptotics/myLimit.root` 的 `stats`，branch 为 `exp_upperlimit`、`exp_upperlimit_plus1/plus2/minus1/minus2`，observed 用 `obs_upperlimit`。
- toy：实际 reader 用 `expectedLimit`、`expectedLimit_plus1/plus2/minus1/minus2`，observed 用 `observedLimit`。函数 docstring 还留有 asymptotic branch names，以 code 为准。[L560–672、L676–739]

流程包括读取参数网格 → `enforce_monotonic_limits()` 清理 → `interpolate_function.build_full_grid_monotone()` 填网格 → 取 level=1 contour → 作 expected / observed / uncertainty-band 图。保存 `output_mu_contours.root` 供 overlay 使用。**必须保留原始 fit output**，否则无法区分真实 grid points、被清理的点和 interpolation。

### Interpolation 不是新 fit

`draw_limits_mu.py` 的 preliminary monotonic cleanup 会把不符合假设的点值标为 **99**。`interpolate_function.py` 再以 $(\log g_U,\log(\beta_L^{23}+10^{-6}),-\log m)$ 为坐标，对 `log(value+1)` 做 SciPy `griddata` linear interpolation，缺值用 nearest 补；随后施加质量方向不减、couplings 方向不增，以及 $-2σ\le-1σ\le\mathrm{exp}\le+1σ\le+2σ$ 顺序。[draw L958–1053、L2876–2906；interpolate L464–632]

当前版保护 surviving input anchors，遇到 anchor 内部冲突会报错；`interpolate_function_backup.py` 是较短旧版，轴方向 monotonic enforcement 没有同等 anchor-preserving machinery。两者是 import modules，不是通过 CLI 输入任意 ROOT 的 standalone 工具。

取 contour 的 `get_first_contour_at_level()` 只取 **第一条连通 contour**，有可选 endpoint extrapolation；复杂 topology 的其他 segments 可能没有保留。[draw L741–833] 单调性是 plotting algorithm 的假设，不是所有 finite-width / interference 物理的定理；不能把被清理点的存在隐藏成“原始结果天然平滑”。

B-anomaly favoured region 的公式、常数与相位约定在独立专题记录；本页只覆盖程序入口 / 数据流，避免将 low-energy favoured band 与 collider expected band 混淆。

## Acceptance × efficiency 模式

`draw_limits_mu.py` 还提供独立 acceptance modes，不能仅看文件名认定所有调用都在画 limit。[L181–527、L2184–2778]

- **betaR33=-1 corrected-weight modes**：读取 BSM / interference samples 分开，使用 corrected/nominal sumW ratio（含 campaign fractions），计算
  $$A\epsilon=\frac{\text{histogram yield}}{\mathrm{sumW_{corr}/sumW_{nom}}}\times\mathrm{FilterEff}.$$
  ratio table 用 `--sumw_ratio_file`；默认在 `run/script_codex/sumW_corr/sumW_corr_ratios.txt`。
- **default-weight v04 modes**：通过 `--sample_config` 得 sample→DSID，计算 `raw histogram yield × FilterEff`，不再除 corrected sumW ratio。
- 精确 grids 以离散生成点作 text tables / ROOT plots；没有生成的点保留 sparse cells，不能由 contour interpolation 冒充实际 MC acceptance。
- `--xSecFile` 默认指 PMGxsecDB；FilterEff、单位、histogram 先前是否已被 luminosity/xsection scaling 必须与产生此 acceptance input 的 config 一致。

可用的精确 `--sig` token 从文件头 `B33RM1_ACCEPTANCE_MODES` / `DEFAULT_WEIGHT_ACCEPTANCE_MODES` 及 `run_script.sh` 的对应示例查找；这些 mode 的 `--plot_option combined` 会被忽略，不与 limit overlay 混用。

## draw_vis_Xsec.py：手填 numbers 的 visible-cross-section 图

没有 CLI / ROOT 输入。脚本头部硬编码 masses **1.5、2、2.5、4 TeV** 和两组 pb values，转 fb、画 $|\beta_R^{33}|=0/1$ comparison 及其 ratio；输出 `visible_xsec_SR1b_SR0b.pdf`。[L12–25、L223–228]

这是某次 right-handed study 的展示脚本，不会自行执行 fit 或从最新 ROOT 提取结果。改变 masses / values / region labels 后才能用于其他版本；它不等同于公开 paper 的 LH coupling exclusion。
''')
write('脚本专题-interference与cut优化',r'''## signal_yield_plotter.py：每个 coupling 点的 I/S

扫描 `MU<mass>_gU..._23L..._noWeights_<tag>.root`，读取 `NOSYS` 下相应 SR 的 `met` histogram。`--SR_type 1b` 用 `met_SR_1tau0l1b_sch/tch`；`0b` 用仍叫 WVR 的 `met_WVR_1tau0l0b_sch/tch`。读取 bsm / inf yield 与 error，作 interference fraction grid，并叠加已有 exclusion contour。[L22–100、L168–352]

```bash
python3 signal_yield_plotter.py --input_dir /path/to/signal_histograms \
  --out_dir plots_inf --SR_type 0b --mass_point 1500 \
  --mu_contour_file /path/to/output_mu_contours.root
```

默认积分包含 underflow + overflow；`--include_under_overflow` 被定义为 `store_true, default=True`，所以当前 CLI **没有关闭它的选项**。input_dir 默认 None，实际上运行时应明确传入。比例对应该 parameter / region，不适合作为固定常数应用到其他 coupling；negative I 可以物理地出现。

## compare_inf_b33R_shapes.py：已生成 histograms 的 RH/LH interference 比较

对 DSID **567627 ($\beta_R^{33}=0$)** 与 **567634 ($\beta_R^{33}=-1$)** 比较已有 FastFrames outputs；这些 histograms 已含 xsection/sumW normalization。`OUT` 与 file suffix、parameter-grid parsing 在源码头部 / `list_common()` 中指定；没有 argparse。[L1–80]

比较总 signed yield ratio，另以各自 signed integral 归一化比较 shape，报告 TV / bin difference / KS distance 等，再画 PDF。ROOT KS 采用 **absolute-bin-content** 的归一化 clones，因为 standard KS 要求非负分布。[L80–143]

这些形状指标是诊断量：对带正负 MC weights 的 interference 不可把 KS output 直接当严格的物理 hypothesis-test p-value。只能支持“当前 sample / selection 的 shapes 多接近”，不能单凭一质量点复制全部 RH interference 到其他 masses。

## compare_inf_b33R_ntuple_shapes.py：直接从 reco 构建检查

读取 hard-coded `input/filelist_v05.txt` 与 `sum_of_weights_v05.txt`，按 $\sigma/\mathrm{sumW}$ 权重构建 MET 和 leading tau-$p_T$，再比较相同两个 DSID。头部 `XSEC` 是固定数值，`WEIGHTS` 列 NOSYS 与三个 coupling variations；nominal sumW 使用 `GEN_MUR10_MUF10_PDF260800`。[L19–42、L45–109]

运行 `python3 compare_inf_b33R_ntuple_shapes.py` 前需核对 filelist、sumW、XSEC、输出目录；它读取 ntuple 而不是 hist outputs，计算与上一程序相近的 signed yield / normalized-shape diagnostics。[L110–242] 这可区分差异来自 generator/reweight 还是后续 region selection，但本次资料整理没有执行完整数据检查。

## significance_scan.py：N−1 histogram 上扫描 MET cut

```bash
python3 significance_scan.py --signal signal.root --background allBG.root \
  --sys-error 0.2 --output significance_scan.pdf
```

可用 `--yield-output` 指定 yield plot，`--ymax` 控制纵轴。当前 histogram paths 在源码头部选 **0b MET N−1**；切换 1b 或 $m_T$ 需要手改 names，并确保 signal/background 物理 bin edges 一致。[L12–29、L34–64]

从每个 bin index 积分到上界（含 overflow）取得 S、B 及 MC-stat error，合并背景相对 systematics：

$$\sigma_B=\sqrt{(\delta_{\rm sys} B)^2+\sigma^2_{B,\rm MCstat}}.$$

使用带背景不确定度的 counting Asimov-significance formula；当 $\sigma_B=0$ 时退回 $\sqrt{2[(S+B)\ln(1+S/B)-S]}$。Res / NonRes 组合用 $\sqrt{Z_{\rm Res}^2+Z_{\rm NonRes}^2}$。[L78–125、L167–183]

这不是完整 CR-constrained profile-likelihood scan，也没有自动处理 Res / NonRes covariance 或 overlap。代码取四个 histograms 的 **最小 bin count**，未检查 bin edges；x 轴用 `(index−1) × first-bin-width`，并非读取真实 low edge。[L159–187] 因而不同 histogram binning 不能靠 min(nbins) 自动兼容。源码明确记录旧 1b hist bins 不一致，需要重做合适 input。

分析中 SR0b-Res MET 600 GeV 的 optimisation 最终未纳入 nominal，见 [[分析区域与选择变量]]；不要把本程序某次 best cut 当成公开 paper selection。
''')
write('脚本专题-提交与失败重扫',r'''这些文件记录 **2026 年右手 $\beta_R^{33}=-1$ 扩展研究** 的任务提交，不能与公开 paper 的纯 LH nominal result 自动等同。命名有 `b33R1_0`，实际 sample token 是 `b33Rm1_0`，应以 dataset / config 内容确认符号。

## FastFrames 生产 / 补交

- `submit_tail_b33R1_0.sh`：通过外部 `Plotter_submit_lxatut_FastFrame.py` 提交 **M4000 / M5000、BSM、Res / NonRes** 四个配置；每个 sample 单独 job。默认扫描 $g_U=0.5,1,1.5,2,2.5,3$ 与 $\beta_L^{23}=0,0.2,0.6,1,1.4,1.8,2.2$，每 config 42 samples；`group_prod2`、1 CPU。[L1–41]
- `submit_tail_b33R1_0_M4000_M5000.sh`：仅补交源码注释列出的 **7 个缺失 ROOT outputs**，3 次 helper 调用；不是重跑两个质量的所有 points。注释把失败归因为 stale Kerberos / file handles，这只是当时诊断记录。[L1–26]

两者 hard-code AFS YAML path、queue / job IDs，需要在有相应 `Plotter_submit_lxatut_FastFrame.py` 的运行目录调用 `bash script.sh`；资料库没有执行提交。重用前要检查 job IDs、input names 和 output destinations。

## TREx 1b-only scan

`submit_tail_TREx_betaR33Rm1_0_1bSR.sh` 调用外部 `Plotter_submit_lxatut_TREx.py`，按 1.5、2、2.5、3、4、5 TeV 六个质量提交，总注释为 252 configs = 6×42；queues group_prod2/3，job IDs 186–191。[L1–10]

**实际副作用**：脚本先 `mkdir -p`，随后 `rm -rf` 清空指定 fit-results 目录，再提交。它不是只追加 jobs 的 wrapper，不应把整份作为无条件可重跑命令。复现需要先保存 / 换出 output directory 并核查目标，这里只记录现有作用。

## 两个 submit_job_lxatut 文件只是跳转提示

- `submit_job_lxatut_TREx_betaR33Rm1_0_1bSR.sh`
- `submit_job_lxatut_TREx_betaR33Rm1_0_1bSR_rescan.sh`

当前 `run/scripts` 版本只打印“到 lxatut3 的 `/data/data3/zp/zang/lxatut_submit/` 运行同名脚本”，然后 `exit 1`。**本地副本不提交任何 job**。rescan 注释说 11 configs / `sqrt_mu Max=20000`，这是指向外部脚本的描述，不是本文件的执行代码。

## 根据 log 更新范围：update_betaR33Rm1_0_scan_ranges.py

```bash
python3 update_betaR33Rm1_0_scan_ranges.py \
  --logdir /path/to/condor_logs --config-dir /path/to/configs \
  --submit-script /path/to/resubmit.sh --output-dir /path/to/fit_results \
  --job-start 198 --dry-run
```

- 只解析匹配 betaR33Rm1_0 的 logs / config naming。
- 若旧 `sqrt_mu Max<1`，改为 2。
- 若 median >100，且可用 +2σ limit 超过旧 max，则新 max = **1.5 × +2σ**。
- negative median 的点跳过；这份 current algorithm 并不保证自动修复每个 Inf / failed fit。[L52–147]
- 去掉 dry-run 后会 **原地修改 config**、写 resubmit shell。程序自身不执行 generated submission script。[L201–257]

重新运行前需要核对 logs 的 fit identity 和 square-root POI convention。文件名的“最新”不能代替新 range 已产生正确 ROOT / convergence 的证据；验证应另查 outputs。
''')
write('脚本专题-检查图与paper图整理',r'''## pdf_generator.py：systematic / nominal 对照 PDF

```bash
python3 pdf_generator.py --input sample.root --output sample_systematics.pdf
```

要求 ROOT 顶层包含 `TDirectoryFile` 类型的 `NOSYS` 和 systematic directories，处理 `TH1D`。按 up/down 名称分组，与 NOSYS 一起画；当前 `filter_rules` 对不同 NP family 只选指定 topCR-1e observables，不是无筛选导出所有 histograms。[L15–59、L223–230]

用于人工诊断 variation 的 shape / rate。对象 / region names 被硬编码；换 muon 或 SR 输入时应同步改 rules。`MUON_*`、`MET_*` 旁的 crash 注释保留，实际能否访问依赖输入中的 hist existence，不能当成已验证通用 PDF exporter。

## pdf_generator_mc20d.py：更早的逐图导出

没有 CLI。底部固定读取 `output_taunub_sys_mc20d/ttbar.root`，写 `histograms_combined_ttbar_sys_mc20d.pdf`。以第一个 TDirectory 的 TH1D names 为列表，遍历每个 directory，逐页 log-y 作图。[L3–66]

它不按 NOSYS / up/down 做同一套 grouping，较适合旧输出逐页检查；需要修改脚本末尾的输入/输出路径。不应仅因名字含 mc20d 就以为会自动找到当前 mc20d files。

## eps_modifier.py：特定 paper EPS 的排版后处理

```bash
python3 eps_modifier.py /path/to/copied_eps_directory
```

也接受单一 `.eps` 文件。程序根据 filename patterns 和 hard-coded PostScript coordinates 调整轴标题 / label / line widths / signal legend、去掉 `Preliminary` 文本，并加入指定 cut arrows，随后调用 **`ps2pdf -dEPSCrop`** 产生同名 PDF。[L4–22、L202–227]

该脚本会 **原地改 EPS**，是针对某版 TREx paper plots 的专用补丁，不是从 physics histograms 重新绘图。对新 plot geometry 不保证命中正确位置；保留原 EPS、只在复制目录跑，输出视觉核对后才能用于论文。这里没有运行它，也未改变任何已有 publication label。

## copy_figs.py：按映射复制到 paper tree

读取脚本同目录的 `paper_figs_map.txt`（每行 `source_name destination_relative_path`），把 `source_dir` 内图复制到 `ANA-EXOT-2025-06-PAPER/figures` 的对应位置，自动建目录，源不存在则 warn；同名目标会被覆盖。[L4–30]

没有 CLI，三个 paths 都在文件头。当前 37 脚本缓存没有提供 `paper_figs_map.txt`，因此单靠这份脚本不能重建 publication figure mapping；需补读外部 map。程序只搬运图，不验证 Figure number / caption / contents 对应。

## 跨图复现顺序

先由 [[脚本专题-limit读取插值与acceptance]] 或 TRExFitter 正确生成物理图，再单独做视觉修正，最后按 mapping 复制。`run_script.sh` 中的旧 paths / command order 可能未同步；不要用“文件复制成功”替代结果身份和 plot provenance 检查。
''')
owner={n:g for g,ns in groups.items() for n in ns}
t='''本目录覆盖远程 `taux_fastframes/run/scripts` 本次快照中的 **37 个 Python / shell scripts**，按功能归类，逐项说明输入、输出、使用方法和当前限制。特别关注 B-anomaly favoured region 的公式 / 实现，另见该专题笔记。\n\n## 按任务选入口\n\n'''
for g,ns in groups.items():t+=f'- [[{g}]]：'+', '.join('`'+n+'`' for n in ns)+'。\n'
t+='''\n## 创建时间与“新旧”的证据\n\n本次 AFS 文件系统未返回 birth time（`stat_birth` 为 `-` / `birthtime=null`）；37 个 scripts 在仓库状态中都是 untracked，没有可用 first/last git commit。因此 **真实创建时间全部未知**。下表列的是远程 filesystem **最后修改时间 mtime，Asia/Tokyo (UTC+9)**，仅用于大致判断最近改过哪些文件，不能改称创建时间。ctime 也不是创建时间；本地下载/cache 时间不能代表源文件年龄。\n\n如果之后提供早期版本、备份或首次 commit，可以补充“最早可验证存在时间”，与 mtime 分列。当前新文件也可能仍含旧 docstrings / defaults，优先按执行语句判断功能。\n\n## 文件时间索引（最近修改在前）\n\n| Script / 源码快照 | 真实创建时间 | 远程最后修改时间 JST | SHA-256 前12位 | 功能笔记 |\n|---|---|---|---|---|\n'''
for n,x in sorted(meta.items(),key=lambda a:a[1]['mtime'],reverse=True):
 dt=datetime.datetime.fromtimestamp(x['mtime'],zoneinfo.ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')
 t+=f'| {link(n)} | 未知 | {dt} | `{x["sha256"][:12]}` | [[{owner[n]}]] |\n'
t+=f'''\n## 审阅范围和复现入口\n\n- 远程根目录：`/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts`。\n- [内容与完整 SHA-256 / mtime 快照]({b}/remote_snapshot.json)，采集 UTC `{snapshot['collected_utc']}`。\n- [git 与 birth-time 检查]({b}/details.json)。\n- [函数 / CLI 行号索引]({b}/script_outline.json)。\n\n这里做了静态源码审阅，没有运行 ROOT 分析或提交 batch jobs。Usage 示例中 `/path/to` 是待填路径；有 no-CLI hard-coded paths、覆盖输出或删除目录的脚本均已逐项说明。`Plotter_submit_lxatut_*`、`paper_figs_map.txt`、`script_codex` 等外部依赖不属于这 37 个文件，资料库不把尚未读取的依赖描述为已验证。\n'''
write('Scripts脚本目录与时间索引',t)
print('Wrote',len(list(v.glob('*.md'))),'script notes for',len(meta),'scripts.')
