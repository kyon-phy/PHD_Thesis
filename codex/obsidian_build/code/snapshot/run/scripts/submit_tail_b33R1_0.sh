# b33R1_0 alldecay-corrected BSM — M4000 / M5000 (new mass points)
# One condor job per sample via --samples list (42 jobs per config).
# request_cpus 1 matches number_of_cpus: 1 in the v05_b33R1_0 configs.

CONFIG_DIR=/afs/cern.ch/work/z/zang/LQanalysis/taux_fastframes/taunub/config_taunub

# usage: build_samples <mass> <bsm|inf> <Res|NonRes> [gU values...]
build_samples () {
    local mass=$1 tag=$2 ch=$3
    shift 3
    local gus="$*"
    [ -z "$gus" ] && gus="0_5 1_0 1_5 2_0 2_5 3_0"
    local list="" gu lam
    for gu in $gus; do
        for lam in 0_0 0_2 0_6 1_0 1_4 1_8 2_2; do
            list="${list}MU${mass}_gU${gu}_23L${lam}_b33Rm1_0_alldecay_corrected_${tag}_${ch},"
        done
    done
    echo "${list%,}"
}

# M4000 (DSID 567632) + M5000 (DSID 567633) -> group_prod2
python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M4000_Res.yml \
  --samples $(build_samples 4000 bsm Res) \
  --queue group_prod2 --job 52 --request_cpus 1

python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M4000_NonRes.yml \
  --samples $(build_samples 4000 bsm NonRes) \
  --queue group_prod2 --job 53 --request_cpus 1

python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M5000_Res.yml \
  --samples $(build_samples 5000 bsm Res) \
  --queue group_prod2 --job 54 --request_cpus 1

python3 Plotter_submit_lxatut_FastFrame.py \
  --config_file ${CONFIG_DIR}/config_taunub_plot_sys_1l_sigs_alldecay_v05_b33R1_0_M5000_NonRes.yml \
  --samples $(build_samples 5000 bsm NonRes) \
  --queue group_prod2 --job 55 --request_cpus 1
