#! /bin/bash


# interference fraction plots
# 1b SR
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 1b --mass_point 1500 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 1b --mass_point 1800 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 1b --mass_point 2000 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 1b --mass_point 2500 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 1b --mass_point 3000 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root &
# 0b SR
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 0b --mass_point 1500 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 0b --mass_point 1800 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 0b --mass_point 2000 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 0b --mass_point 2500 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04/ --out_dir plots/signal_yield_plotter --SR_type 0b --mass_point 3000 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp/output_mu_contours.root &
# optimized 0b SR
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04_0bSR_Optimized/ --out_dir plots/signal_yield_plotter_optimized --SR_type 0b --mass_point 1500 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04_0bSR_Optimized/ --out_dir plots/signal_yield_plotter_optimized --SR_type 0b --mass_point 1800 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04_0bSR_Optimized/ --out_dir plots/signal_yield_plotter_optimized --SR_type 0b --mass_point 2000 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04_0bSR_Optimized/ --out_dir plots/signal_yield_plotter_optimized --SR_type 0b --mass_point 2500 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp/output_mu_contours.root &
python signal_yield_plotter.py --input_dir ../output_plots/taunub_sys_1l_allVR_with_beamspot_v04_0bSR_Optimized/ --out_dir plots/signal_yield_plotter_optimized --SR_type 0b --mass_point 3000 --mu_contour_file plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp/output_mu_contours.root &

rm MU1800_gU1_25_23L1_8_noWeights_combined_NonRes.root; hadd MU1800_gU1_25_23L1_8_noWeights_combined_NonRes.root MU1800_gU1_25_23L1_8_noWeights_bsm_NonRes.root MU1800_gU1_25_23L1_8_noWeights_inf_NonRes.root
rm MU2000_gU2_0_23L1_0_noWeights_combined_NonRes.root; hadd MU2000_gU2_0_23L1_0_noWeights_combined_NonRes.root MU2000_gU2_0_23L1_0_noWeights_bsm_NonRes.root MU2000_gU2_0_23L1_0_noWeights_inf_NonRes.root
rm MU1800_gU3_0_23L0_6_noWeights_combined_NonRes.root; hadd MU1800_gU3_0_23L0_6_noWeights_combined_NonRes.root MU1800_gU3_0_23L0_6_noWeights_bsm_NonRes.root MU1800_gU3_0_23L0_6_noWeights_inf_NonRes.root

# draw limits by significance
python draw_limits.py ../run_signal_scan/fit_results/combined

# generate config files for TREXFItter fit with all parameter sets
python3 config_generator.py \
  --config /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/TRXconfig/config_taunub_plot_sys_1l_w_beamspot_v04.config  \
  --signals_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04 \
  --placeholder MU1500_gU1_5_23L0_2 \
  --out_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs

# draw limits by mu
# python draw_limits_mu.py ../run_signal_scan/fit_results/TwoSided_HF0_2_HFSeperated plots/TwoSided_HF0_2_HFSeperated
# python draw_limits_mu.py ../run_signal_scan/fit_results/TwoSided_HF0_2 plots/TwoSided_HF0_2
# python draw_limits_mu.py ../run_signal_scan/fit_results/combined plots/combined
# python draw_limits_mu.py ../run_signal_scan/fit_results/TwoSided_HF0_2_StatOnly plots/TwoSided_HF0_2_StatOnly
# python draw_limits_mu.py ../run_signal_scan/fit_results/BSM_Inf plots/BSM_Inf
# python draw_limits_mu.py ../run_signal_scan/fit_results/TwoSided_HF0_2_lumi_450 plots/TwoSided_HF0_2_lumi_450
# python draw_limits_mu.py ../run_signal_scan/fit_results/TwoSided_0tau1bCR plots/TwoSided_0tau1bCR
# python draw_limits_mu.py ../run_signal_scan/fit_results/TwoSided_0tau1b0bCR plots/TwoSided_0tau1b0bCR

# draw unblinded limits
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_2_HFSeperated_Renamed_unblind_SPLUSB --out_dir plots/TwoSided_HF0_2_HFSeperated_Renamed_unblind_exp --unblind False --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_2_HFSeperated_Renamed_unblind_SPLUSB --out_dir plots/TwoSided_HF0_2_HFSeperated_Renamed_unblind_exp_test --unblind False --plot_option combined --limit_path plots/TwoSided_HF0_2_HFSeperated_Renamed_unblind_obs/output_mu_contours.root
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_2_HFSeperated_Renamed_unblind_SPLUSB --out_dir plots/TwoSided_HF0_2_HFSeperated_Renamed_unblind_obs --unblind True --plot_option single

# draw unblinded limits using noWeights signals. (bsm)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_obs/output_mu_contours.root # compare with obs limits
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_bsm_combined_exp --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_exp/output_mu_contours.root # compare with BSM+inf limits
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_asymptotic_exp --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_exp/output_mu_contours.root # compare with toy limits

# draw unblinded limits using noWeights signals and overlay with Res/NonRes-only limits.
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_exp_obs_Res_NonRes --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_obs/output_mu_contours.root --extra_path_1 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_Res_exp/output_mu_contours.root --extra_path_2 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_NonRes_exp/output_mu_contours.root


# draw unblinded limits using noWeights signals. (bsm+inf)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_comb --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_comb --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_obs --unblind True --sig noWeights --plot_option single

# draw acceptance efficiency maps # paper Figure 11 and 12
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_Res_1b --sig AcceptanceEff_Res_1b --plot_option single
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_NonRes_1b --sig AcceptanceEff_NonRes_1b --plot_option single
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_Res_0b --sig AcceptanceEff_Res_0b --plot_option single
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_NonRes_0b --sig AcceptanceEff_NonRes_0b --plot_option single

# draw all v04 default-weight signal efficiencies into separate v05 map directories
# No corrected-sumW/Xsec normalisation: signal efficiency = raw yield * FilterEff.
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_v05_noWeights_Res_1b --sig AcceptanceEff_defaultWeight_Res_1b --plot_option single --sample_config /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/config_taunub/config_taunub_plot_sys_1l_sigs_noWeights_AccepEff_v04.yml
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_v05_noWeights_NonRes_1b --sig AcceptanceEff_defaultWeight_NonRes_1b --plot_option single --sample_config /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/config_taunub/config_taunub_plot_sys_1l_sigs_noWeights_AccepEff_v04.yml
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_v05_noWeights_Res_0b --sig AcceptanceEff_defaultWeight_Res_0b --plot_option single --sample_config /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/config_taunub/config_taunub_plot_sys_1l_sigs_noWeights_AccepEff_v04.yml
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_sig_Acceptance_Eff --out_dir plots/acceptance_eff_v05_noWeights_NonRes_0b --sig AcceptanceEff_defaultWeight_NonRes_0b --plot_option single --sample_config /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/config_taunub/config_taunub_plot_sys_1l_sigs_noWeights_AccepEff_v04.yml

# draw betaR33=-1 all-decay Acceptance*Efficiency maps (BSM and interference)
# The fourth column of sumW_corr_ratios.txt includes the mc20a/d/e period fractions.
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v05_sig_Acceptance_Eff_b33Rm1_0_bsm_inf --out_dir plots/acceptance_eff_b33Rm1_Res_1b --sig AcceptanceEff_b33Rm1_Res_1b --plot_option single --sumw_ratio_file /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/script_codex/sumW_corr/sumW_corr_ratios.txt
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v05_sig_Acceptance_Eff_b33Rm1_0_bsm_inf --out_dir plots/acceptance_eff_b33Rm1_NonRes_1b --sig AcceptanceEff_b33Rm1_NonRes_1b --plot_option single --sumw_ratio_file /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/script_codex/sumW_corr/sumW_corr_ratios.txt
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v05_sig_Acceptance_Eff_b33Rm1_0_bsm_inf --out_dir plots/acceptance_eff_b33Rm1_Res_0b --sig AcceptanceEff_b33Rm1_Res_0b --plot_option single --sumw_ratio_file /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/script_codex/sumW_corr/sumW_corr_ratios.txt
python draw_limits_mu.py --input_dir /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v05_sig_Acceptance_Eff_b33Rm1_0_bsm_inf --out_dir plots/acceptance_eff_b33Rm1_NonRes_0b --sig AcceptanceEff_b33Rm1_NonRes_0b --plot_option single --sumw_ratio_file /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/script_codex/sumW_corr/sumW_corr_ratios.txt

# cp the new figures
cp /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots/acceptance_eff_Res_1b/*pdf /afs/cern.ch/work/z/zang/LQanalysis/ANA-EXOT-2025-06-PAPER/figures/Aux/Accep_Eff_Res_1b/
cp /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots/acceptance_eff_Res_0b/*pdf /afs/cern.ch/work/z/zang/LQanalysis/ANA-EXOT-2025-06-PAPER/figures/Aux/Accep_Eff_Res_0b/
cp /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots/acceptance_eff_NonRes_1b/*pdf /afs/cern.ch/work/z/zang/LQanalysis/ANA-EXOT-2025-06-PAPER/figures/Aux/Accep_Eff_NonRes_1b/
cp /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/scripts/plots/acceptance_eff_NonRes_0b/*pdf /afs/cern.ch/work/z/zang/LQanalysis/ANA-EXOT-2025-06-PAPER/figures/Aux/Accep_Eff_NonRes_0b/
rm Accep_Eff*/mu1_contours_beta*
rm Accep_Eff*/mu1_contours_mu4000*
rm Accep_Eff*/mu1_contours_mu5000*

# draw unblinded limits using noWeights signals. (bsm, Res-only, Nosys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_Res_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_Res_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_Res_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_Res_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_Res_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_Res_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_Res_obs/output_mu_contours.root

# draw unblinded limits using noWeights signals. (bsm, NonRes-only, Nosys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_NonRes_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_NonRes_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_NonRes_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_NonRes_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_NonRes_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_NonRes_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_Res_exp/output_mu_contours.root


# draw toy limits with noweights signals. (bsm only)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_TOY --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_exp --unblind False --sig noWeights --plot_option single --use_toy
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_TOY --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_obs --unblind True --sig noWeights --plot_option single --use_toy
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_TOY --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_exp_obs --unblind False --sig noWeights --plot_option combined --use_toy --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_obs/output_mu_contours.root

# generate signal config files for FastFrame yaml file and Condor tasks
python3 sig_config_maker.py filelist_DAOD_v3.txt /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/input/filelist_sigs_noWeights.txt

# check failed jobs
python3 check_failed_jobs.py /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig_TOY /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_sig_TOY \
  -o /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_sig_TOY_miss \
  -t missing_list.txt

# generate toy configs based on Asymptotic limits (BSM only)
python3 toy_config_maker.py /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_sig /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_sig_TOY/
# generate toy configs based on Asymptotic limits (BSM + interference)
python3 toy_config_maker.py /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_sig_comb /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_sig /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_sig_comb_TOY --combined
# generate toy configs based on Asymptotic limits with addtional 0b1bSR SR (BSM + interference)
python3 toy_config_maker.py /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/run_signal_scan/configs/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy --combined


# draw limits using 1tau0l0b + 1tau0l1b as SR. (combined, NoSys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_obs/output_mu_contours.root
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_1bSR_NoSys_exp --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_NoSys_exp/output_mu_contours.root # comparison with 0b1bSR limits
# draw limits using 1tau0l1b as SR. (combined, NoSys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_NoSys_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_NoSys_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_1bSR_NoSys --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_NoSys_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_NoSys_obs/output_mu_contours.root

# draw limits using optimized 1tau0l0b + 1tau0l1b as SR. (combined, NoSys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys_Optimized --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys_Optimized --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys_Optimized --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_Optimized_obs/output_mu_contours.root
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NoSys_Optimized --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_1bSR_NoSys_Optimized_exp --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_exp/output_mu_contours.root # comparison with origin 0b+1bSR 

# draw Aysmptotic limits using 1tau0l0b + 1tau0l1b as SR. (combined, full-sys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_obs/output_mu_contours.root

# draw Aysmptotic limits using 1tau0l0b + 1tau0l1b as SR. (combined, nosys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NOSYS --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NOSYS_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NOSYS --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NOSYS_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NOSYS --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NOSYS_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NOSYS_obs/output_mu_contours.root

# draw TOY limits using 1tau0l0b + 1tau0l1b as SR. (combined, full-sys) # paper Figure 3 and 4
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Toy --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_exp --unblind False --sig noWeights --plot_option single --use_toy
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Toy --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_obs --unblind True --sig noWeights --plot_option single --use_toy
# paper Figure 3 and 4
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Toy --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_exp_obs --unblind False --sig noWeights --plot_option combined --use_toy --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_obs/output_mu_contours.root  
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Toy --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_Asymptotic_exp --unblind False --sig noWeights --plot_option combined --use_toy --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NoSys_exp/output_mu_contours.root # comparison with Simplified Asymptotic 0b+1bSR 
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Toy --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_1bSR_Toy_exp --unblind False --sig noWeights --plot_option combined --use_toy --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_toy_exp/output_mu_contours.root # comparison with origin 1bSR 


# draw Res and NonRes limits
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Res --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Res --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_NonRes --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NonRes --unblind False --sig noWeights --plot_option single
# draw Res and NonRes limits overlay with Res+NonRes Asymptotic limits # paper Figure 13
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp_obs_Res_NonRes --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_obs/output_mu_contours.root --extra_path_1 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Res/output_mu_contours.root --extra_path_2 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_NonRes/output_mu_contours.root

# draw 0b and 1b SR-only limits
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0bSR_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0bSR_1bSR_exp --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root
# draw 0b and 1b SR-only limit overlay with 0b+1b toy limits
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_Toy --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_exp_0bSR_1bSR --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_Toy_obs/output_mu_contours.root --use_toy --extra_path_1 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0bSR_exp/output_mu_contours.root --extra_path_2 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root
# draw 0b and 1b SR-only limit overlay with 0b+1b Asymptotic limits # paper Figure 14
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_exp_0bSR_1bSR --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_obs/output_mu_contours.root --extra_path_1 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0bSR_exp/output_mu_contours.root --extra_path_2 plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_1bSR_exp/output_mu_contours.root

# get significance scan from N-1 plots
  --signal /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_nom_1l_allVR_with_beamspot_v04_N_minus_1_sigs_noWeights/MU1500_gU1_5_23L0_6_noWeights_combined.root \
  --signal /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_nom_1l_allVR_with_beamspot_v04_N_minus_1_sigs_noWeights/MU3000_gU2_0_23L1_8_noWeights_combined.root \
python3 significance_scan.py \
  --signal /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_nom_1l_allVR_with_beamspot_v04_N_minus_1_sigs_noWeights/MU1500_gU0_5_23L1_8_noWeights_combined.root \
  --background /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_nom_1l_allVR_with_beamspot_v04_N_minus_1_metTrig_Eff/allBG_merged.root \
  --sys-error 0.2\
  --output significance_scan.pdf

# draw Aysmptotic limits using 1tau0l0b + 1tau0l1b as SR. scaled with btautau contamination (combined, full-sys)
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_btautau --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_btautau_exp --unblind False --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_btautau --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_btautau_obs --unblind True --sig noWeights --plot_option single
python draw_limits_mu.py --input_dir ../run_signal_scan/fit_results/TwoSided_HF0_3_HFSeperated_Renamed_unblind_SPLUSB_noWeights_comb_0b1bSR_btautau --out_dir plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_btautau_exp_obs --unblind False --sig noWeights --plot_option combined --limit_path plots/TwoSided_HF0_3_HFSeperated_Renamed_unblind_noWeights_comb_0b1bSR_btautau_obs/output_mu_contours.root



# run hadd script for bsm and inf combined samples
python3 hadd_bsm_inf.py /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/output_plots/taunub_sys_1l_allVR_with_beamspot_v04_0bSR_Optimized --key_word MU1

# modify eps files
python3 eps_modifier.py /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots_paper_test; cp /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots_paper/*.eps /afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/run/fit_taunub_sys_1l_allVR_BONLY_MU3000_gU2_5_23L1_0_noWeights_N_minus_1_fullRegion_v3_modified/Plots_paper_test/

# read nutple event numbers
python3 read_eventNumbers.py