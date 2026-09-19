# b33R1_0 alldecay-corrected BSM — M4000 / M5000 resubmit failed samples
# 7 samples missing ROOT output (kerberos stale file handle -> Setup.sh/FastFrames failed):
#   531496.12  MU4000_gU1_0_23L1_8_b33Rm1_0_alldecay_corrected_bsm_Res
#   531496.20  MU4000_gU1_5_23L2_2_b33Rm1_0_alldecay_corrected_bsm_Res
#   531496.21  MU4000_gU2_0_23L0_0_b33Rm1_0_alldecay_corrected_bsm_Res
#   531496.26  MU4000_gU2_0_23L1_8_b33Rm1_0_alldecay_corrected_bsm_Res
#   531497.0   MU4000_gU0_5_23L0_0_b33Rm1_0_alldecay_corrected_bsm_NonRes
#   531498.26  MU5000_gU2_0_23L1_8_b33Rm1_0_alldecay_corrected_bsm_Res
#   531498.27  MU5000_gU2_0_23L2_2_b33Rm1_0_alldecay_corrected_bsm_Res

CONFIG_DIR=/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/config_taunub

python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M4000_Res.yml \
  --samples MU4000_gU1_0_23L1_8_b33Rm1_0_alldecay_corrected_bsm_Res,MU4000_gU1_5_23L2_2_b33Rm1_0_alldecay_corrected_bsm_Res,MU4000_gU2_0_23L0_0_b33Rm1_0_alldecay_corrected_bsm_Res,MU4000_gU2_0_23L1_8_b33Rm1_0_alldecay_corrected_bsm_Res \
  --queue group_prod2 --job 56 --request_cpus 1

python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M4000_NonRes.yml \
  --samples MU4000_gU0_5_23L0_0_b33Rm1_0_alldecay_corrected_bsm_NonRes \
  --queue group_prod2 --job 57 --request_cpus 1

python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M5000_Res.yml \
  --samples MU5000_gU2_0_23L1_8_b33Rm1_0_alldecay_corrected_bsm_Res,MU5000_gU2_0_23L2_2_b33Rm1_0_alldecay_corrected_bsm_Res \
  --queue group_prod2 --job 58 --request_cpus 1
